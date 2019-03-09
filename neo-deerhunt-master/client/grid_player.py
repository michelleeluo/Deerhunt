class GridPlayer:

    def __init__(self):
        self.foo = True

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        #print("turns left!!! {}\n", turns_left)
        melees = your_units.get_all_unit_of_type('melee')
        #melees = []
        workers = your_units.get_all_unit_of_type('worker')
        moves = []

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


        #moves.append(melees[0].move_towards((3,8)))
        #moves.append((melees[0]).move('LEFT'))
        #print("my move")
        return moves