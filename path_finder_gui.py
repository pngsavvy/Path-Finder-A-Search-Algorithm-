import pygame
from math import sqrt

class Gui:
    pygame.init()

    board_scale = 15   # the bigger the number the bigger each node will be
    number_of_columns, number_of_rows = 30, 20
    width = int(number_of_columns * board_scale)
    height = int(number_of_rows * board_scale)

    all_nodes = []        # will be a multidimentional array that will hold data for all nodes
    connected_nodes = []  # will store all nodes that are connected to each individual node
    shorest_path = []     

    current_path_index = 0

    # all_nodes([f_cost = 0, left = 1, right = 2, top = 3, bottom = 4, is_wall = 5, is_closed = 6, is_open = 7, node_number = 8])
    # each of the values for the indexes that will be stored in the multidimentional array
    f_cost_i, h_cost_i, g_cost_i, left_i, right_i, top_i, bottom_i, is_wall_i, is_closed_i, is_open_i, already_set_cost_i, is_shortest_path_i, node_number_i = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    
    # indexes for connected array
    C_left_i, C_right_i, C_top_i, C_bottom_i, C_top_left_i, C_top_right_i, C_bottom_left_i, C_bottom_right_i, node_number_index = 0, 1, 2, 3, 4, 5, 6, 7, 8
    closer_path = 10  # if node is adjacent to current node
    farther_path = 14 # if node is diagonal from current node 

    found_path = False      # find_node will run until the path is found
    start_node = number_of_columns + 1      # this will be the starting node
    current_node = start_node


    last_node = start_node
    end_node =  number_of_columns * number_of_rows - number_of_columns - 2

    # initialize colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (96, 96, 96)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (153, 153, 0)
    dark_green = (16, 82, 0)
    brown = ((115,53,7))
    gold = (233, 197, 16)

    gameDisplay = pygame.display.set_mode((1, 1))
    pygame.display.set_caption('Path Finder')
    font = pygame.font.SysFont("Calibri", 13)
    larger_font = pygame.font.SysFont("Calibri", 20)
    pygame.event.get()

    def __init__(self):
        gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.create_nodes()
        
    def create_nodes(self):
        self.set_connected_nodes()

        node_number = 0

        # will use to increment to the next node and set new boundaries
        increment = self.height / self.number_of_rows
        
        right = 0
        bottom = 0

        # ofset top so will start at 0 when increment is added
        top = -self.width / self.number_of_columns
        for column in range(self.number_of_rows):

            # reset values for next row
            left = -self.width / self.number_of_columns
            right = 0
            top += increment
            bottom += increment

            for row in range(self.number_of_columns):
                # boundaries for each node
                left += increment
                right += increment
                
                # start with -1 as f_cost until calulate
                # all_nodes([f_cost = 0, h_cost = 1, g_cost = 2 left = 3, right = 4, top = 5, bottom = 6, is_wall = 7, is_closed = 8, is_open = 9, already_set_cost = 10 , is_shortest_path = 11, node_number = 12])
                self.all_nodes.append([0, 0, 0, left, right, top, bottom, False, False, False, False, False, node_number]) 
                node_number += 1
        
    def set_connected_nodes(self):
        left, right, top, bottom, top_left, top_right, bottom_left, bottom_right, node_index = -1, -1, -1, -1, -1, -1, -1, -1, -1

        max_index = self.number_of_rows * self.number_of_columns - 1

        for node_index in range(max_index):

            left = node_index - 1
            top_left = node_index - self.number_of_columns - 1
            bottom_left = node_index + self.number_of_columns - 1
            right = node_index + 1
            top_right = node_index - self.number_of_columns + 1
            bottom_right = node_index + self.number_of_columns + 1
            top = node_index - self.number_of_columns
            bottom = node_index + self.number_of_columns

            if node_index % self.number_of_columns == 0:
                left = -1
                top_left = -1
                bottom_left = -1
            elif node_index % self.number_of_columns == self.number_of_columns - 1:
                right = -1
                top_right = -1
                bottom_right = -1
                
                           
            # left, right, top, bottom, top_left, top_right, bottom_left, bottom_right, node_index
            self.connected_nodes.append([left, right, top, bottom, top_left, top_right, bottom_left, bottom_right, node_index])        

    def select_walls(self, mx, my):
        for node in self.all_nodes:
            if node[self.left_i] <= mx <= node[self.right_i]:
                if node[self.top_i] <= my <= node[self.bottom_i]:
                    node[self.is_wall_i] = True

    def draw_lines(self):
        next_line = self.width / self.number_of_columns
        for line in range(self.number_of_columns):
            # draw columns
            pygame.draw.line(self.gameDisplay, self.black, [next_line, 0], [next_line, self.height])
            next_line += self.width / self.number_of_columns

        next_line = self.height / self.number_of_rows
        # draw rows
        for line in range(self.number_of_rows):
            pygame.draw.line(self.gameDisplay, self.black, [0, next_line], [self.width, next_line])
            next_line += self.height / self.number_of_rows

    def fill_blocks(self):
        for node in self.all_nodes:
            if node[self.is_wall_i] == True:
                # all_nodes([f_cost = 0, left = 1, right = 2, top = 3, bottom = 4, is_wall = 5, is_closed = 6, is_open = 7, node_number = 8])
                #                                               left               top               width                                   height
                pygame.draw.rect(self.gameDisplay, self.black ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))
            
            # if node is open
            if node[self.is_open_i] == True:
                pygame.draw.rect(self.gameDisplay, self.green ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))
                
            # if node is closed
            if node[self.is_closed_i]:
                pygame.draw.rect(self.gameDisplay, self.gray ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))

            # color current node
            if node[self.node_number_i] == self.current_node:
                pygame.draw.rect(self.gameDisplay, self.dark_green ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))
            
            # render path
            if self.found_path:
                # dont change end node color
                if node[self.node_number_i] != self.end_node:
                    if node[self.is_shortest_path_i]:
                        pygame.draw.rect(self.gameDisplay, self.white ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))

            # color start node
            if node[self.node_number_i] == self.start_node:
                pygame.draw.rect(self.gameDisplay, self.brown ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))

            # end node
            if node[self.node_number_i] == self.end_node:
                pygame.draw.rect(self.gameDisplay, self.brown ,(node[self.left_i], node[self.top_i], node[self.right_i] - node[self.left_i], node[self.bottom_i] - node[self.top_i]))

    def set_open_nodes(self):
        for node in self.all_nodes: 
            # only can open if there is not a wall
            if not node[self.is_wall_i]:
                # open node to the left
                if node[self.node_number_i] == self.current_node - 1:
                    if self.current_node % self.number_of_columns != 0: # only mark if the current node is not on the left side
                        node[self.is_open_i] = True
                # open node to the right
                if node[self.node_number_i] == self.current_node + 1:
                    if self.current_node % self.number_of_columns != self.number_of_columns - 1: # only mark if the current node is not on the right side
                        node[self.is_open_i] = True
                # open above node
                if node[self.node_number_i] == self.current_node - self.number_of_columns:
                    node[self.is_open_i] = True
                # open bottom node
                if node[self.node_number_i] == self.current_node + self.number_of_columns:
                    node[self.is_open_i] = True
                # open top left node
                if node[self.node_number_i] == self.current_node - self.number_of_columns - 1:
                    if self.current_node % self.number_of_columns != 0: # only mark if the current node is not on the left side
                        node[self.is_open_i] = True
                # open top right node
                if node[self.node_number_i] == self.current_node - self.number_of_columns + 1:
                    if self.current_node % self.number_of_columns != self.number_of_columns - 1: # only mark if the current node is not on the right side
                        node[self.is_open_i] = True
                # open bottom left node
                if node[self.node_number_i] == self.current_node + self.number_of_columns - 1:
                    if self.current_node % self.number_of_columns != 0: # only mark if the current node is not on the left side
                        node[self.is_open_i] = True             
                # open bottom right node                                    
                if node[self.node_number_i] == self.current_node + self.number_of_columns + 1:
                    if self.current_node % self.number_of_columns != self.number_of_columns - 1: # only mark if the current node is not on the right side
                        node[self.is_open_i] = True             
                if node[self.node_number_i] == self.current_node:
                    node[self.is_open_i] = True
                
    # g_cost cost so far for each node 
    def get_g_cost(self, node_index):
        node = self.all_nodes[node_index]
        # left
        if node[self.node_number_i] == self.current_node - 1:
            if self.current_node % self.number_of_columns != 0: # only mark if the current node is not on the left side
                return self.closer_path
        # right
        elif node[self.node_number_i] == self.current_node + 1:
            if self.current_node % self.number_of_columns != self.number_of_columns - 1: # only mark if the current node is not on the right side
                return self.closer_path
        # above
        elif node[self.node_number_i] == self.current_node - self.number_of_columns:
            return self.closer_path
        # bottom 
        elif node[self.node_number_i] == self.current_node + self.number_of_columns:
            return self.closer_path
        # it is a diagonal node so return farther path
        else:
            return self.farther_path       
    
    # h_cost estimated cost from curent node to goal. This is the heuristic part of the cost function, so it is like a guess.    
    def get_h_cost(self, node_index):
        # number of nodes between start and end 
        distance = self.end_node - node_index
        
        # will hold vertical distance between start and end
        vertical_distance = 0

        # calc vertical distance. once calculated distance will hold the horizontal distance
        while distance > self.number_of_columns:
            distance -= self.number_of_columns
            vertical_distance += 1

        h_cost = sqrt(vertical_distance * vertical_distance + distance * distance) * 10

        return int(h_cost)

    def get_f_cost(self):
        self.set_f_cost_for_open_nodes()
        return self.choose_lowest_f_cost()                

    def set_f_cost_for_open_nodes(self):
            
            # set current g_cost to current nodes g_cost
            for node in self.all_nodes:
                if node[self.node_number_i] == self.current_node:
                    current_g_cost = node[self.g_cost_i]
                    node[self.is_open_i] = False
                    node[self.is_closed_i] = True

            for node in self.all_nodes:
                if node[self.is_open_i]:
                    if not node[self.already_set_cost_i]:
                        node[self.g_cost_i] = current_g_cost + self.get_g_cost(node[self.node_number_i])
                        node[self.h_cost_i] = self.get_h_cost(node[self.node_number_i])
                        node[self.f_cost_i] = int(node[self.h_cost_i]) + int(node[self.g_cost_i])
                        
                        node[self.already_set_cost_i] = True
                      
    def choose_lowest_f_cost(self):

        lowest_f_cost = 1000000000
        chosen_node_number = -1
        found_lowest = False

        while not found_lowest:
            found_lowest = True
            for node in self.all_nodes:
                if node[self.is_open_i]:
                    if not node[self.is_closed_i]:
                        if node[self.f_cost_i] < lowest_f_cost:
                            found_lowest = False
                            lowest_f_cost = node[self.f_cost_i]
                            chosen_node_number = node[self.node_number_i]
        
        return chosen_node_number

    def find_path(self):
        
        self.set_open_nodes()
        self.current_node = self.get_f_cost() #choose next node
        self.set_open_nodes()
        self.get_f_cost()

        # check if path found and creat paths
        for node in self.all_nodes:
            if node[self.node_number_i] == self.current_node:
                
                print("g_cost of the current node is " + str(node[self.g_cost_i]) )
                print("h_cost of the current node is " + str(node[self.h_cost_i]) )
                print("f_cost of the current node is " + str(node[self.f_cost_i]) )

            if self.current_node == self.end_node:
                print('path found')
                self.found_path = True
                self.compile_shortest_path()
                return True

            self.last_node = self.current_node
            self.update_gui()
            return False

    def compile_shortest_path(self):

        self.shorest_path.append(self.end_node)
        search_node = self.end_node
        searching_for_start_node = True

        while searching_for_start_node:

            if search_node == self.start_node:
                searching_for_start_node = False
                break
            
            print('compile_shortest_path')

            search_node = self.get_next_node_in_path(search_node)

        print('shortest path compiled')

    # something is wrong with this function. just traverses horizontally
    # gets stuck when leaves closed node path

    # need to find connected node that has lowest f_cost
    def get_next_node_in_path(self, search_node):
        
        n_g = []  # array to store node number and f_cost

        max_index = self.number_of_rows * self.number_of_columns - 1

        # get all connected nodes                      # exclude last node because it holds the current node number
        for number in self.connected_nodes[search_node][0:-1]:

            # make sure node_number is a connected node
            if 0 <= number < max_index - 1:
                g = self.all_nodes[number][self.g_cost_i]

                # append (node number , g_cost)
                n_g.append([number, g])

        lowest_g_cost = 1000000000
        chosen_node_number = -1
        found_lowest = False
        
        # find lowest g_cost in array of connected nodes
        while not found_lowest:
            print('stuck in while loop')
            found_lowest = True
            for g in n_g:

                if g[0] == self.start_node:
                    chosen_node_number = self.start_node
                
                if  0 < g[1] < lowest_g_cost:
                    # make sure the node is not already in the shortest path
                    if g[0] not in self.shorest_path:
                        lowest_g_cost = g[1]
                        chosen_node_number = g[0]
                        found_lowest = False  
  
        self.all_nodes[chosen_node_number][self.is_shortest_path_i] = True
        self.shorest_path.append(chosen_node_number)
        return chosen_node_number


    def update_gui(self):

        self.gameDisplay.fill(self.white)
        self.draw_lines()
        self.fill_blocks()

        pygame.display.update()
