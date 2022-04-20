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
        print("Board enters actions\n"+state.board.to_string())
        print("missing numbers:\n",state.board.missing_numbers)
        actions_list = []
        #for each missing number, get +1 and -1 on the board 
        for missing_num in state.board.missing_numbers:
            """ time.sleep(1) """
            print("\n\n\nmissing_num gerau:\n\n\n",missing_num)
            intersection = False
            if missing_num - 1 not in state.board.missing_numbers and missing_num -1 != 0 and missing_num + 1 not in state.board.missing_numbers and missing_num + 1 <= state.board.size**2:
                intersection = True
            if missing_num - 1 not in state.board.missing_numbers and missing_num -1 != 0:
                #TODO meter isto numa funcao - FIX
                #dicionario board_positions keys in string
                temp_actions = []
                if str(missing_num-1) in state.board.board_positions.keys():
                    pos = state.board.board_positions[str(missing_num-1)]
                    hor = state.board.adjacent_horizontal_numbers(pos[0],pos[1])
                    vert = state.board.adjacent_vertical_numbers(pos[0],pos[1])
                    adj_list = hor + vert
                    #adicionar o numero as posicoes adjacentes
                    if adj_list[0] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 0, -1)
                    if adj_list[1] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 1, -1)
                    if adj_list[2] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 2, -1)
                    if adj_list[3] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 3, -1)

                if intersection:
                    print("\n\nSo ha -1 no board intersetcion\n\n",temp_actions)
                    actions_list.append(temp_actions)
                    temp_actions = []
                else:
                    print("\n\nSo ha -1 no board\n\n",temp_actions)
                    return temp_actions
            #if missing_num is the last one, doesnt do nothing
            if missing_num + 1 not in state.board.missing_numbers and missing_num + 1 <= state.board.size**2:
                #TODO meter isto numa funcao - FIX
                temp_actions = []
                if str(missing_num + 1) in state.board.board_positions.keys():
                    pos = state.board.board_positions[str(missing_num+1)]
                    hor = state.board.adjacent_horizontal_numbers(pos[0],pos[1])
                    vert = state.board.adjacent_vertical_numbers(pos[0],pos[1])
                    adj_list = hor + vert
                    #adicionar o numero as posicoes adjacentes
                    if adj_list[0] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 0, 1)
                    if adj_list[1] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 1, 1)
                    if adj_list[2] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 2, 1)
                    if adj_list[3] == 0:
                        temp_actions+=self.get_action(state, missing_num, pos, 3, 1)
                    
                if intersection:
                    print("\n\nSo ha +1 no board intersection\n\n",temp_actions)
                    actions_list.append(temp_actions)
                    temp_actions = []
                else:
                    print("\n\nSo ha +1 no board\n\n",temp_actions)
                    return temp_actions
            #if the neighbours are both on the board, return the intersection of their possible actions    
            print("actions_list total:",actions_list)
            if intersection:
                for action in actions_list[0]:
                    if action not in actions_list[1]:
                        actions_list[0].remove(action)
                print("\n\nHa -1 e +1 no board\n\n",actions_list[0])
                return actions_list[0]


    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        #create board copy
        new_board = deepcopy(state.board)
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
    
    def two_consecutive_nums(self, adj_list):
        for i in adj_list:
            for j in adj_list:
                if i != None and j != None and i!= 0 and j!=0:
                    if i==j+2:
                        return j+1
                    if i==j-2:
                        return i+1
        return 0
    
    #checks if action is compatible with manhattan distance and returns it
    def get_action(self, state, missing_num, pos, adj_pos, case):
        action = []
        print("board que entra no get:\n"+state.board.to_string())
        print("posicao do missing_num",pos)
        print("adj_pos:",adj_pos)
        used_num = 0
        if case == -1:
            #when missing_num-1 is on the board, if a adjacent number is zero, check the distance between that position and the next greater number on the board if compatible return action
            for used_num_str in sorted(state.board.board_positions.keys()):
                if int(used_num_str) > missing_num:
                    used_num = int(used_num_str)
                    break
        elif case == 1:
            #when missing_num+1 is on the board, if a adjacent number is zero, check the distance between that position and the next smaller number on the board if compatible return action
            for used_num_str in sorted(state.board.board_positions.keys()):
                if int(used_num_str) > missing_num:
                    break
                else:
                    used_num = int(used_num_str)

        print("used_num in dict",used_num_str)
        print("missing_num",missing_num)
        if(adj_pos == 0):
            """ print("posicao p manhattan:",pos[0],pos[1]-1)
            print("diff numeros:",abs(used_num-missing_num),"manhattan distance:",self.manhattan_distance(state.board.board_positions[used_num_str],(pos[0],pos[1]-1))) """
            if(abs(used_num-missing_num) >= self.manhattan_distance(state.board.board_positions[used_num_str],(pos[0],pos[1]-1))):
                action.append((pos[0],pos[1]-1,missing_num))
        elif(adj_pos == 1):
            if(abs(used_num-missing_num) >= self.manhattan_distance(state.board.board_positions[used_num_str],(pos[0],pos[1]+1))):
                action.append((pos[0],pos[1]+1,missing_num))
        elif(adj_pos == 2):
            if(abs(used_num-missing_num) >= self.manhattan_distance(state.board.board_positions[used_num_str],(pos[0]+1,pos[1]))):
                action.append((pos[0]+1,pos[1],missing_num))
        elif(adj_pos == 3):
            """ print("posicao p manhattan:",pos[0],pos[1]-1)
            print("diff numeros:",abs(used_num-missing_num),"manhattan distance:",self.manhattan_distance(state.board.board_positions[used_num_str],(pos[0]-1,pos[1]))) """
            if(abs(used_num-missing_num) >= self.manhattan_distance(state.board.board_positions[used_num_str],(pos[0]-1,pos[1]))):
                action.append((pos[0]-1,pos[1],missing_num))
        return action
    
    def manhattan_distance(self, pos1, pos2):
        return sum(abs(a-b) for a, b in zip(pos1,pos2))

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    filepath = sys.argv[1]
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance(filepath)
    # Criar uma instância de Numbrix:
    problem = Numbrix(board)
    # Obter o nó solução usando a procura:
    goal_node = depth_first_tree_search(problem)

    # Verificar se foi atingida a solução
    print("Solution:\n", goal_node.state.board.to_string(), sep="")