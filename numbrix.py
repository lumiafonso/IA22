# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 052:
# 95622 Luis Afonso
# 95575 Francisco Goncalves

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


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
        self.used_numbers = []
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return board.matrix[row][col]

    def set_number(self, row: int, col: int, number: int):
        """ Coloca o valor na respetiva posição do tabuleiro. """
        board.matrix[row][col] = number
        
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        vert = []
        global size
        if(row+1 > board.size-1):
            vert.append(None)
        else:
            vert.append(board.matrix[row+1][col])

        if(row-1 < 0):
            vert.append(None)
        else:
            vert.append(board.matrix[row-1][col])
        
        return vert 
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        hor = []
        if(col-1 < 0):
            hor.append(None)
        else:
            hor.append(board.matrix[row][col-1])

        if(col+1 > board.size-1):
            hor.append(None)
        else:
            hor.append(board.matrix[row][col+1])
        
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

        row = []
        for i in range(1, board.size + 1):
            row = lines[i].split()
            new_row = []
            for n in row:
                new_row.append(int(n))
                if int(n) > 0:
                    board.used_numbers.append(int(n))
            board.matrix.append(new_row)

        return board

    def to_string(self):
        output = ""
        counter = 1
        for l in self.matrix:
            for i in l:
                output += str(i) + "\t"
            if counter != self.size:
                output += "\n"
            counter +=1
        return output


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions_list = []
        for i in range (state.board.size):
            for j in range (state.board.size):
                if state.board.get_number(i,j) == 0:
                    hor = state.board.adjacent_horizontal_numbers(i,j)
                    vert = state.board.adjacent_vertical_numbers(i,j)
                    adj_list = hor+vert
                    #se ha dois numeros consecutivos ja sabe qual valor meter
                    value = self.two_consecutive_nums(adj_list) 

                    print("pos: ",i,",",j)

                    if (value != 0):
                        print("numeros consecutivos")
                        """ self.update_actions(actions_list, value) """
                        actions_list.append((i,j,value))
                    #se nao ha vizinhos 0, para chegar aqui quer dizer que vai ser ou 1 ou size**2
                    #falta apagar os da actions list caso se faca um append antes do else
                    elif (0 not in adj_list):
                        print("nao tem zeros ao lado")
                        if 2 in adj_list:
                            """ self.update_actions(actions_list,1) """
                            actions_list.append((i,j,1))
                        elif state.board.size**2-1 in adj_list:
                            """ self.update_actions(actions_list,state.board.size**2) """
                            actions_list.append((i,j,state.board.size**2))
                    elif (all(v == 0 or v == None for v in adj_list)):
                        for x in range(1,state.board.size**2+1):
                            if x not in state.board.used_numbers:
                                actions_list.append((i,j,x))
                    else:
                        print("normal")
                        print(state.board.used_numbers)
                        for adj in adj_list:
                            if adj != None and adj != 0:
                                if (adj-1 != 0) and (adj-1 not in state.board.used_numbers):
                                    actions_list.append((i,j,adj-1))
                                if (adj+1 <= state.board.size ** 2) and (adj+1 not in state.board.used_numbers):
                                    actions_list.append((i,j,adj+1))
                    print(actions_list)

                    return actions_list

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        new_board = state.board
        old_num = new_board.get_number(action[0],action[1])
        if old_num != 0:
            new_board.used_numbers.remove(old_num)
        new_board.set_number(action[0],action[1],action[2])
        new_board.used_numbers.append(action[2])
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

    def update_actions(self, actions_list, value):
        for action in actions_list:
            if action[2] == value:
                actions_list.remove(action)


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
    state = NumbrixState(board)
    print(state.board.to_string())
    # Obter o nó solução usando a procura:
    """ goal_node = breadth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.to_string(), sep="") """