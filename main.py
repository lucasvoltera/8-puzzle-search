import pygame
import pygame_gui
import time
from utils import *
from utils.puzzle import Puzzle


        
window_surface.blit(background, (0, 0))
pygame.display.update()
clock = pygame.time.Clock()
puzzle = Puzzle.new(250, 220, 330, 330)
puzzle.inicializar()
algorithm = "Best-First (Manhatan Distance)"
fstate= "1,2,3,4,5,6,7,8,0"
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    puzzle.blocosAleatorios()
                elif event.ui_element == set_final_button:
                    if not puzzle.setBlocos(Final_state.get_text()):
                        alert_label.set_text("Final state invalid!")
                    else:
                        alert_label.set_text("Final state valid!")
                        puzzle.estadoFinal = Final_state.get_text()
                elif event.ui_element == info_button:
                    Info_msg = '<b>8-Puzzle Solver<br><br>Authors:</b><br>Mateus Mendonça Monteiro<br>Vinicius Santana Ramos'
                    # Information Box - Info
                    info_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                            manager = manager,
                                                                                            action_long_desc = Info_msg,
                                                                                            window_title ='Developers Info',
                                                                                            )
                elif event.ui_element == solve_button:
                    
                    if algorithm == "Best-First (Manhatan Distance)":
                        moves = puzzle.bestFirst()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.tempoUltimoResolvido)
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.custo)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                        # Confirmation Box - Algorithm Report
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                )
                        solveAnimation(moves)
                        
                    elif algorithm == "A* (Manhatan Distance)":
                        moves = puzzle.a_star()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.tempoUltimoResolvido)
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.custo)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                        # Confirmation Box - Algorithm Report
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                )
                        solveAnimation(moves)
                        
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithmDropDown:
                    algorithm = event.text
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == Final_state:
                print("")
        manager.process_events(event)
        
        
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_blocks(puzzle.blocos)
    pygame.display.update()
