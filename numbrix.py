# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 052:
# 95622 Luis Afonso
# 95575 Francisco Goncalves

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search
from copy import deepcopy
import time
from math import sqrt
import collections

class NumbrixState:
    state_id = 0
    
    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """
    def __init__(self):
        self.matrix = []
        self.size = 0
        self.missing_numbers = set()
        self.board_positions = {}
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.matrix[row][col]
    
    def set_number(self, row: int, col: int, number: int):
        """ Coloca o valor na respetiva posição do tabuleiro. """
        self.matrix[row][col] = number
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        vert = []
        global size
        if(row+1 > self.size-1):
            vert.append(None)
        else:
            vert.append(self.matrix[row+1][col])

        if(row-1 < 0):
            vert.append(None)
        else:
            vert.append(self.matrix[row-1][col])
        
        return vert 
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        hor = []
        if(col-1 < 0):
            hor.append(None)
        else:
            hor.append(self.matrix[row][col-1])

        if(col+1 > self.size-1):
            hor.append(None)
        else:
            hor.append(self.matrix[row][col+1])
        
        return hor
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        board = Board()
        f = open(filename,"r")

        with open(filename) as f:
            lines = f.readlines()
        board.size = int(lines[0])

        for i in range (1, board.size**2+1):
            board.missing_numbers.add(i)
        #remove used numbers from missing numbers and save used numbers positions to a dictionary; example -> 6:(x,y)
        row = []
        for i in range(1, board.size + 1):
            row = lines[i].split()
            new_row = []
            for j in range(len(row)):
                new_row.append(int(row[j]))
                if int(row[j]) > 0:
                    board.missing_numbers.remove(int(row[j]))
                    board.board_positions[row[j]] = (i-1,j)
            board.matrix.append(new_row)

        return board

    def get_actions(self):
        all_missing_num_actions_list = []

        actions_list = []
        """ print("missing_numbers:\n",self.missing_numbers) """
        #for each missing number, get +1 and -1 on the board, if they exist.
        #fill their adjacent positions with the missing number if:
        # - the manhattan distance between the position and the next greater/smaller number is smaller than the diff between numbers
        # - if the action is valid based on the numbrix restrictions (is_valid_action)
        #Add the valid actions of each missing number to the action_list
        #When an action is not valid, the whole board is useless
        for missing_num in self.missing_numbers:
            """ time.sleep(1) """
            """ print("missing num:",missing_num) """
            intersection = False
            if missing_num - 1 not in self.missing_numbers and missing_num -1 != 0 and missing_num + 1 not in self.missing_numbers and missing_num + 1 <= self.size**2:
                intersection = True
            if missing_num - 1 not in self.missing_numbers and missing_num -1 != 0:
                #TODO meter isto numa funcao - FIX
                #dictionary board_positions keys in string
                temp_actions = []
                if str(missing_num-1) in self.board_positions.keys():
                    pos = self.board_positions[str(missing_num-1)]
                    hor = self.adjacent_horizontal_numbers(pos[0],pos[1])
                    vert = self.adjacent_vertical_numbers(pos[0],pos[1])
                    adj_list = hor + vert
                    #adicionar o numero as posicoes adjacentes se for valido
                    if adj_list[0] == 0:
                        if missing_num != self.size**2:
                            action = self.get_action_distance_ok(missing_num, pos, 0, -1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0],pos[1]-1,self.size**2)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    if adj_list[1] == 0:
                        if missing_num != self.size**2:
                            action = self.get_action_distance_ok(missing_num, pos, 1, -1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0],pos[1]+1,self.size**2)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    if adj_list[2] == 0:
                        if missing_num != self.size**2:
                            action = self.get_action_distance_ok(missing_num, pos, 2, -1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0]+1,pos[1],self.size**2)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    if adj_list[3] == 0:
                        if missing_num != self.size**2:
                            action = self.get_action_distance_ok(missing_num, pos, 3, -1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0]-1,pos[1],self.size**2)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action

                if intersection:
                    actions_list.append(temp_actions)
                    temp_actions = []
                else:
                    if temp_actions != []:
                        all_missing_num_actions_list.append(temp_actions)
            #if missing_num is the last one, doesnt do nothing
            if missing_num + 1 not in self.missing_numbers and missing_num + 1 <= self.size**2:
                #TODO meter isto numa funcao - FIX
                temp_actions = []
                if str(missing_num + 1) in self.board_positions.keys():
                    pos = self.board_positions[str(missing_num+1)]
                    hor = self.adjacent_horizontal_numbers(pos[0],pos[1])
                    vert = self.adjacent_vertical_numbers(pos[0],pos[1])
                    adj_list = hor + vert
                    #adicionar o numero as posicoes adjacentes
                    if adj_list[0] == 0:
                        #if missing num is 1, there isnt a lower number to compare distances with
                        if missing_num != 1:
                            action = self.get_action_distance_ok(missing_num, pos, 0, 1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0],pos[1]-1,1)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    if adj_list[1] == 0:
                        if missing_num != 1:
                            action = self.get_action_distance_ok(missing_num, pos, 1, 1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0],pos[1]+1,1)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    if adj_list[2] == 0:
                        if missing_num != 1:
                            action = self.get_action_distance_ok(missing_num, pos, 2, 1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0]+1,pos[1],1)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    if adj_list[3] == 0:
                        if missing_num != 1:
                            action = self.get_action_distance_ok(missing_num, pos, 3, 1)
                            if action != []:
                                if self.is_valid_action(action[0]):
                                    temp_actions+=action
                        else:
                            action = [(pos[0]-1,pos[1],1)]
                            if self.is_valid_action(action[0]):
                                temp_actions+=action
                    
                if intersection:
                    actions_list.append(temp_actions)
                    temp_actions = []
                else:
                    if temp_actions != []:
                        all_missing_num_actions_list.append(temp_actions)
            #if the neighbours are both on the board, return the intersection of their possible actions    
            if intersection:
                for action in actions_list[0]:
                    if action not in actions_list[1]:
                        actions_list[0].remove(action)
                if actions_list[0] != []:
                    all_missing_num_actions_list.append(actions_list[0])

        """ print(self.to_string()) """
        #if no actions available return []
        if all_missing_num_actions_list == []:
            """ print(all_missing_num_actions_list) """
            """ input() """
            return []
        #return the action list with smaller length
        else:
            min_len = -1
            min_len_index = -1
            for i in range(len(all_missing_num_actions_list)):
                #if theres a action list with lenght 1, returns it
                if all_missing_num_actions_list[i] == 1:
                    return all_missing_num_actions_list[i]
                elif min_len == -1:
                    min_len = len(all_missing_num_actions_list[i])
                    min_len_index = i
                elif len(all_missing_num_actions_list[i]) < min_len:
                    min_len = len(all_missing_num_actions_list[i])
                    min_len_index = i
            """ print(all_missing_num_actions_list[min_len_index]) """
            """ input() """
            return all_missing_num_actions_list[min_len_index]
    
    #checks if action is compatible with manhattan distance and returns it
    def get_action_distance_ok(self, missing_num, pos, adj_pos, case):
        action = []
        used_num = 0
        temp = 0
        if case == -1:
            #when missing_num-1 is on the board, if a adjacent number is zero, check the distance between that position and the next greater number on the board if compatible return action
            for used_num_str in self.board_positions.keys():
                if int(used_num_str) > missing_num:
                    if temp == 0:
                        temp = int(used_num_str)
                    elif int(used_num_str) < temp:
                        temp = int(used_num_str)
            used_num = temp
                    
        elif case == 1:
            #when missing_num+1 is on the board, if a adjacent number is zero, check the distance between that position and the next smaller number on the board if compatible return action
            for used_num_str in self.board_positions.keys():
                if int(used_num_str) < missing_num:
                    if temp == 0:
                        temp = int(used_num_str)
                    elif int(used_num_str) > temp:
                        temp = int(used_num_str)
            used_num = temp
        
        """ print("missing_num:",missing_num)
        print("caso:",case)
        print("numero mais proximo:",used_num)
        print("pos_adj:",adj_pos) """

        #if used_num == 0, there is no next greater/smaller number, so justs add action
        
        if(adj_pos == 0):
            if used_num != 0:
                if(abs(used_num-missing_num) >= self.manhattan_distance(self.board_positions[str(used_num)],(pos[0],pos[1]-1))):
                    action.append((pos[0],pos[1]-1,missing_num))
            else:
                action.append((pos[0],pos[1]-1,missing_num))
        elif(adj_pos == 1):
            if used_num != 0:
                if(abs(used_num-missing_num) >= self.manhattan_distance(self.board_positions[str(used_num)],(pos[0],pos[1]+1))):
                    action.append((pos[0],pos[1]+1,missing_num))
            else:
                action.append((pos[0],pos[1]+1,missing_num))
        elif(adj_pos == 2):
            if used_num != 0:
                if(abs(used_num-missing_num) >= self.manhattan_distance(self.board_positions[str(used_num)],(pos[0]+1,pos[1]))):
                    action.append((pos[0]+1,pos[1],missing_num))
            else:
                action.append((pos[0]+1,pos[1],missing_num))
        elif(adj_pos == 3):
            if used_num != 0:
                if(abs(used_num-missing_num) >= self.manhattan_distance(self.board_positions[str(used_num)],(pos[0]-1,pos[1]))):
                    action.append((pos[0]-1,pos[1],missing_num))
            else:
                action.append((pos[0]-1,pos[1],missing_num))

        """ print("action devolvida distance:",action) """
        return action
    
    def manhattan_distance(self, pos1, pos2):
        return sum(abs(a-b) for a, b in zip(pos1,pos2))
    
    def is_valid_action(self, action):
        """ return True """
        row = action[0]
        col = action[1]
        num = action[2]

        hor = self.adjacent_horizontal_numbers(row,col)
        vert = self.adjacent_vertical_numbers(row,col)
        adj_list = hor + vert

        zeros_in_adj = adj_list.count(0)
        valid_in_adj = 0
        for adj in adj_list:
            if adj != None and adj != 0 and abs(adj-num) == 1:
                valid_in_adj+=1
        
        if num == 1 or num == self.size**2:
            if valid_in_adj == 1 or zeros_in_adj == 1:
                return True
        elif valid_in_adj == 2 or zeros_in_adj > 1:
            return True
        elif valid_in_adj == 1 and zeros_in_adj > 0:
            return True

        return False

    
    def to_string(self):
        output = ""
        counter = 1
        for l in self.matrix:
            for i in l:
                if counter == self.size:
                    output += str(i) + "\n"
                else:
                    output += str(i) + "\t"
                counter +=1
            counter = 1
        return output
        

class Numbrix(Problem):
    
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)
    
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        #all actions of each missing_number gets added to this list, return the action list with the least actions
        return state.board.get_actions()
                

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        #create board copy
        new_board = Board()
        new_matrix = []
        for row in state.board.matrix:
            new_matrix.append(row.copy())
        new_board.matrix = new_matrix
        new_board.size = state.board.size
        missing_numbers = set()
        for missing_num in state.board.missing_numbers:
            missing_numbers.add(missing_num)
        new_board.missing_numbers = missing_numbers
        new_board_positions = {}
        for k,v in state.board.board_positions.items():
            new_board_positions[k] = v
        new_board.board_positions = new_board_positions

        #if number is being replaced, add number to missing numbers
        old_num = new_board.get_number(action[0],action[1])
        if old_num != 0:
            new_board.missing_numbers.add(old_num)
        #set new number on board
        new_board.set_number(action[0],action[1],action[2])
        #remove new number from missing numbers
        new_board.missing_numbers.remove(action[2])
        #update number position
        new_board.board_positions[str(action[2])] = (action[0],action[1])

        return NumbrixState(new_board)
    
    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        pos = ()
        for i in range (state.board.size):
            for j in range (state.board.size):
                if state.board.get_number(i,j) == 1:
                    pos = (i,j)
                    while (state.board.get_number(pos[0],pos[1]) != state.board.size**2):
                        hor = state.board.adjacent_horizontal_numbers(pos[0],pos[1])
                        vert = state.board.adjacent_vertical_numbers(pos[0],pos[1])
                        adj = hor+vert
                        new_pos = pos
                        for adj_index in range(len(adj)):
                            if adj[adj_index] == state.board.get_number(i,j) + 1:
                                if adj_index == 0:
                                    j-=1
                                elif adj_index == 1:
                                    j+=1
                                elif adj_index == 2:
                                    i+=1
                                elif adj_index == 3:
                                    i-=1
                                new_pos = (i,j)
                                break
                        if new_pos == pos:
                            return False
                        pos = new_pos
                    return True
        return False
                        
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    start = time.time()
    filepath = sys.argv[1]
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance(filepath)
    # Criar uma instância de Numbrix:
    problem = Numbrix(board)
    # Obter o nó solução usando a procura:
    goal_node = depth_first_tree_search(problem)
    end = time.time()
    print(end-start)
    # Verificar se foi atingida a solução
    print("Solution:\n", goal_node.state.board.to_string(), sep="")