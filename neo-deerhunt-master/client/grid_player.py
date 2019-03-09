import operator

class GridPlayer:

    def __init__(self):
        self.foo = True
        # self.safe_turns = 0

    # def set_safety(self, safe):
    #     self.safe_turns = safe

    # def pre_game_calc(self, game_map, your_units):
    #     workers = your_units.get_all_unit_of_type('worker')
    #     melees = your_units.get_all_unit_of_type('melee')
    #     resource_nodes = game_map.find_all_resources()
    #     column = len(game_map.grid[0])
    #     row = len(game_map.grid)
    #     print("MAP SIZE: {0} x {1}".format(column, row))

    #     enemy_distance = []
    #     for m in melees:
    #         enemy_coord = (abs(column - m.x), abs(row - m.y))
    #         enemy_distance.append(len(game_map.bfs(enemy_coord, resource_nodes[0])) - 1)
    #     self.set_safety(min(enemy_distance))

    def bfs2(self, map, workers,  en_w, en_m, melees, start: (int, int), dest: (int, int)) -> [(int, int)]:
        """(Map, (int, int), (int, int)) -> [(int, int)]
        Finds the shortest path from <start> to <dest>.
        Returns a path with a list of coordinates starting with
        <start> to <dest>.
        """
        graph = map.grid
        width = len(graph[0])
        height = len(graph)
        queue = [[start]]
        vis = set(start)
        if start == dest or graph[start[1]][start[0]] == 'X' or \
                not (0 < start[0] < len(graph[0])-1 \
                     and 0 < start[1] < len(graph)-1):
            return None

        while queue:
            path = queue.pop(0)
            node = path[-1]
            r = node[1]
            c = node[0]

            if node == dest:
                return path
            for adj in ((c+1, r), (c-1, r), (c, r+1), (c, r-1)):
                if (self.is_occupied(workers, melees, en_w, en_m, adj, width, height) == False or graph[adj[1]][adj[0]] == 'R') and (adj not in vis):
                    queue.append(path + [adj])
                    vis.add(adj)
                # elif self.is_occupied(workers, melees, adj, width, height) == False and graph[adj[1]][adj[0]] == 'R' and adj not in vis:
                #     queue.append(path + [adj])
                #     vis.add(adj)
                


    def is_occupied(self, workers, melees, en_w, en_m,  node, width, height):
        if node[0] == 0 or node[1] == 0 or node[0] == width-1 or node[1] == height-1:
            return True
        for w in workers:
            if w.position == node:
                return True
        for m in melees:
            if m.position == node:
                return True
        for w in en_w:
            if w.position == node:
                return True
        for m in en_m:
            if m.position == node:
                return True
        return False


    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        # if turns_left == 100:
        #     # Pre-game calculations.
        #     self.pre_game_calc(game_map, your_units)
        moves = []
        workers = your_units.get_all_unit_of_type('worker')
        melees = your_units.get_all_unit_of_type('melee')
        locations = game_map.find_all_resources()

        en_w = enemy_units.get_all_unit_of_type('worker')
        en_m = enemy_units.get_all_unit_of_type('melee')

        # resource_nodes = game_map.find_all_resources()
        # asymmetrical_node = resource_nodes[(len(resource_nodes) // 2)]
        # my_nodes = []
        # print(self.safe_turns)
        # print(resource_nodes, asymmetrical_node)
        # count = 0

        # If there are any melees then assign the first melee to look for enemies
        if len(melees) > 0:
            enemy_list = melees[0].nearby_enemies_by_distance(enemy_units)
            closest_node = game_map.closest_resources(melees[0])
            
            if enemy_list:
                attack_list = melees[0].can_attack(enemy_units)
                if attack_list:
                    moves.append(melees[0].attack(attack_list[0][1]))
                else:
                    s_path = game_map.bfs(melees[0].position(), closest_node)
                    if s_path:
                        moves.append(melees[0].move_towards(s_path[1]))
            else: pass

        for i in range(1, len(melees)):
            enemy_list = melees[i].nearby_enemies_by_distance(enemy_units)
            target_node = locations[i]
            
            if enemy_list:
                attack_list = melees[i].can_attack(enemy_units)
                if attack_list:
                    moves.append(melees[i].attack(attack_list[0][1]))
                else:
                    s_path = self.bfs2(game_map, workers, melees, en_w, en_m, unit.position(), closest_node)
                    if s_path:
                        moves.append(melees[i].move_towards(s_path[1]))
            else: pass # something else should go here, need to make them more aggressive?
            # else:
            #     closest_node = game_map.closest_resources(unit)
            #     test_node = tuple(map(operator.add, closest_node, (-1, 0)))
            #     s_path = game_map.bfs(unit.position(), test_node)
            #     if s_path:
            #         moves.append(unit.move_towards(s_path[1]))             

        # If there are any workers, then assign the first worker to the closest node  
        if len(workers) > 0:
            if workers[0].can_mine(game_map):
                moves.append(workers[0].mine())
            else:
                closest_node = game_map.closest_resources(workers[0])
                s_path = game_map.bfs(workers[0].position(), closest_node)
                if s_path:
                    moves.append(workers[0].move_towards(s_path[1]))

        for i in range(1, len(workers)):
            target_node = locations[i]
            if workers[i].can_mine(game_map):
                moves.append(workers[i].mine())
            else:
                closest_node = game_map.closest_resources(unit)
                s_path = self.bfs2(game_map, workers, melees, en_w, en_m,  unit.position(), closest_node)
                if s_path:
                    moves.append(workers[i].move_towards(s_path[1]))

        #melees dead
        if melees == []:
            for worker in workers:
                enemy_melees = enemy_units.get_all_unit_of_type('melee')
            
                if enemy_melees:
                    en_pos = enemy_melees[0].position
                    work_pos = worker.position
                    if en_pos[0] == work_pos[0] and en_pos[1] > work_pos[1]:
                        moves.append(worker.move('UP'))
                    elif en_pos[0] == work_pos[0] and en_pos[1] < work_pos[1]:
                        moves.append(worker.move('DOWN'))
                    elif en_pos[0] < work_pos[0] and en_pos[1] == work_pos[1]:
                        moves.append(worker.move('RIGHT'))
                    else:
                        moves.append(worker.move('LEFT'))
                else:
                    closest_node = game_map.closest_resources(worker)
                    s_path = self.bfs2(game_map, workers, melees, en_w, en_m,  unit.position(), closest_node)
                    if s_path:
                        moves.append(worker.move_towards(s_path[1]))

        # If workers are dead:
        if workers == []:
            for melee in melees:
                enemy_workers = enemy_units.get_all_unit_of_type('worker')
                enemy_melees = enemy_units.get_all_unit_of_type('melee')
                if enemy_workers: # if there are enemy workers to kill, kill them first
                    attack_list = melee.can_attack(enemy_workers)
                    if attack_list:
                        moves.append(melee.attack(attack_list[0][1]))
                    else: 
                        closest = enemy_units.units[enemy_workers[0][0]]
                        moves.append(melee.move_towards((closest.x, closest.y)))
                elif enemy_melees: # only attack enemy melees if they are in immediate vicinity
                    attack_list = melee.can_attack(enemy_melees)
                    if attack_list:
                        moves.append(melee.attack(attack_list[0][1]))
                    else:
                        pass
                else: # move to the closest resource in order to try and find enemies to kill
                    closest_node = game_map.closest_resources(melee)
                    s_path = self.bfs2(game_map, workers, melees,  en_w, en_m, unit.position(), closest_node)
                    if s_path:
                        moves.append(melee.move_towards(s_path[1]))

        return moves