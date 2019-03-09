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

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        # if turns_left == 100:
        #     # Pre-game calculations.
        #     self.pre_game_calc(game_map, your_units)
        moves = []
        workers = your_units.get_all_unit_of_type('worker')
        melees = your_units.get_all_unit_of_type('melee')
        locations = game_map.find_all_resources()

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
                    s_path = game_map.bfs(melees[i].position(), target_node)
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
                s_path = game_map.bfs(workers[i].position(), target_node)
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
                    s_path = game_map.bfs(worker.position(), closest_node)
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
                    s_path = game_map.bfs(melee.position(), closest_node)
                    if s_path:
                        moves.append(melee.move_towards(s_path[1]))

        return moves