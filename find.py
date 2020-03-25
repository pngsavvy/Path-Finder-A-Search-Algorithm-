
from path_finder_gui import Gui
import pygame
    
gui = Gui()

running = True
mouse_button_down = False
found_path = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gui.select_walls(mx, my)
            mouse_button_down = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False

        elif mouse_button_down:
            mx, my = pygame.mouse.get_pos()
            gui.select_walls(mx, my)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('press space bar')
                if not found_path:
                    while not gui.find_path():
                        found_path = True 
            
            if event.key == pygame.K_RIGHT:
                if not found_path:
                    if gui.find_path():
                        found_path = True

        gui.update_gui()




