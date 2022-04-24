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
        self.board_positions = []
    
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

    def get_pos(self, num: int):
        return self.board_positions[num-1]

    def all_adjacent_numbers(self, row: int, col:int):
        hor = self.adjacent_horizontal_numbers(row,col)
        vert = self.adjacent_vertical_numbers(row,col)
        return hor+vert

    def adjacent_zero_positions(self, num: int):
        positions = []
        num_pos = self.get_pos(num)
        row, col = num_pos
        adj_list = self.all_adjacent_numbers(row,col)
        if adj_list[0] == 0:
            positions.append((row,col-1))
        if adj_list[1] == 0:
            positions.append((row,col+1))
        if adj_list[2] == 0:
            positions.append((row+1,col))
        if adj_list[3] == 0:
            positions.append((row-1,col)) 
        return positions

    def get_neighbours_in_board(self, num: int):
        neighbours = []
        if num - 1 not in self.missing_numbers and num - 1 != 0:
            neighbours.append(num-1)
        if num + 1 not in self.missing_numbers and num + 1 != self.size**2:
            neighbours.append(num+1)
        return neighbours

    def get_neighbours_not_in_board(self, num: int):
        neighbours = []
        if num - 1 in self.missing_numbers and num - 1 != 0:
            neighbours.append(num-1)
        if num + 1 in self.missing_numbers and num + 1 != self.size**2:
            neighbours.append(num+1)
        return neighbours
    
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
            board.board_positions.append(None)
        #remove used numbers from missing numbers and save used numbers positions to a dictionary; example -> 6:(x,y)
        row = []
        for i in range(1, board.size + 1):
            row = lines[i].split()
            new_row = []
            for j in range(len(row)):
                new_row.append(int(row[j]))
                if int(row[j]) > 0:
                    board.missing_numbers.remove(int(row[j]))
                    board.board_positions[int(row[j])-1] = (i-1,j)
            board.matrix.append(new_row)

        return board

    def get_actions(self):
        min_len_action_set = []
        min_len = -1
        for missing_num in self.missing_numbers:
            local_actions = []
            neighbours = self.get_neighbours_in_board(missing_num)
            
            if len(neighbours) == 0:
                continue
            elif len(neighbours) == 2:
                pass
            else:
                #vai à posicao de cada um neighbour
                for pos in self.adjacent_zero_positions(neighbours[0]):
                    r,c = pos
                    if self.is_valid_action(r,c,missing_num):
                        local_actions.append((r,c,missing_num))
                    else:
                        continue
            
            if len(local_actions) == 1:
                return local_actions

            if local_actions != []:
                if min_len == -1:
                    min_len_action_set = local_actions
                    min_len = len(local_actions)
                elif len(local_actions) < min_len:
                    min_len_action_set = local_actions

        return min_len_action_set

    def is_valid_action(self, r, c, num):
        return self.is_distance_ok(r, c, num) and not self.interferes_with_board(r, c, num)

    def interferes_with_board(self, r, c, num):
        for adj_r,adj_c in self.adjacent_zero_positions(num):
            if self.inteferes_with_adjacent(num,adj_r,adj_c):
                return False
        return True

    def interferes_with_adjacent(self, num, r, c):
        value = self.matrix[row][col]
        #se true, ta mal
        #se valor que ele quer por é neighbour do adjacente, não pode pôr se o numero de adjacentes livres  do adjacente for menor que o numero de neighbours que ainda faltam colocar
        if num in (value-1,value+1):
            return len(self.adjacent_zero_positions(value)) < len(self.get_neighbours_not_in_board(value))
            
        return len(self.adjacent_zero_positions(value)) - 1 < len(self.get_neighbours_not_in_board(value))

    def is_distance_ok(self, r, c, num):
        for pos in self.get_previous_next_number_pos_board(num):
            if pos != ():
                pnr,pnc = pos
                if (self.manhattan_distance(pos, (r,c)) > abs(num-self.get_number(pnr, pnc))):
                    return False
        return True

    def get_previous_next_number_pos_board(self, num):
        prev = ()
        nxt = ()

        index = num - 1 
        while(index > 0):
            if self.board_positions[index-1] != None:
                prev = self.board_positions[index-1]
                break
            index-=1
        
        index = num + 1
        while(index <= self.size):
            if self.board_positions[index-1] != None:
                prev = self.board_positions[index-1]
                break
            index+=1
        
        return (prev,nxt)

    
    def manhattan_distance(self, pos1, pos2):
        return sum(abs(a-b) for a, b in zip(pos1,pos2))
    
    def to_string(self):
        output = ""
        counterx = 1
        countery = 1
        for l in self.matrix:
            for i in l:
                if counterx == self.size and countery != self.size:
                    output += str(i) + "\n"
                elif counterx == self.size and countery == self.size:
                    output += str(i)
                else:
                    output += str(i) + "\t"
                counterx +=1
            countery += 1
            counterx = 1
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
        new_board_positions = []
        for i in range(state.board.board_positions):
            new_board_positions[i].append(state.board.board_positions[i].copy())
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
        new_board.board_positions[action[2]-1] = (action[0],action[1])

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
        if node.action == None:
            return 10
        heur = 0
        x,y,n = node.action
        lists = board.adjacent_horizontal_numbers(x,y) + board.adjacent_vertical_numbers(x,y)
        for num in lists:
            if num == 0:
                heur += 1
        
        return heur
    

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
    print(goal_node.state.board.to_string(),sep="")