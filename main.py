import pygame
import pygame_gui
import time
from utils import *
from utils.puzzle import Puzzle


        
janela.blit(fundo_da_tela, (0, 0))
pygame.display.update()
clock = pygame.time.Clock()
puzzle = Puzzle.new(250, 220, 330, 330)
puzzle.inicializar()
algoritmo = "Best-First"
estFinal= "1,2,3,4,5,6,7,8,0"
rodando = True

while rodando:
    delta = clock.tick(60)/1000.0
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.USEREVENT:
            if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == botao_embaralhar:
                    puzzle.blocosAleatorios()

                elif evento.ui_element == setBotaoFinal:
                    if not puzzle.setBlocos(EstadoFinal.get_text()):
                        texto_alerta.set_text("Estado final inválido!")
                    else:
                        texto_alerta.set_text("Estado final inválido!")
                        puzzle.estadoFinal = EstadoFinal.get_text()

                elif evento.ui_element == botao_info:
                    Info_msg = '<b>8-Puzzle<br><br>Autores:</b><br>Lucas Vinícius Voltera<br>Carlos Eduardo Santana'
                    # Information Box - Info
                    info_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                            manager = manager,
                                                                                            action_long_desc = Info_msg,
                                                                                            window_title ='Informações dos desenvolvedores',
                                                                                            )
                elif evento.ui_element == botao_solucionar:
                    if algoritmo == "Best-First":
                        movimentos = puzzle.bestFirst()
                        tempo = "{temp: .5f} segundos".format(temp = puzzle.tempoUltimoResolvido)
                        report_msg = '<b>Nós visitados:</b> '+ str(puzzle.custo)+'        <b>Tempo:</b>'+tempo+ '        <b>Resolução:</b> '+str(len(movimentos))+' Passos'
                        # Confirmation Box - Algorithm Report
                        janela_confirmacao = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algoritmo.split(" ")[0] + ' Report da busca',)
                        animacaoSolucionar(puzzle, movimentos)
                        
                    elif algoritmo == "A*":
                        movimentos = puzzle.a_star()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.tempoUltimoResolvido)
                        report_msg = '<b>Nós visitados:</b> '+str(puzzle.custo)+'        <b>Tempo:</b>'+tempo+ '        <b>Resolução:</b> '+str(len(movimentos))+' Passos'
                        # Confirmation Box - Algorithm Report
                        janela_confirmacao = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                            manager = manager,
                                                                                                            action_long_desc = report_msg,
                                                                                                            window_title =algoritmo.split(" ")[0] + ' Report da busca',)
                        animacaoSolucionar(puzzle, movimentos)
                        
            elif evento.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == botaoAlgoritmos:
                    algoritmo = evento.text

            elif evento.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED and evento.ui_element == EstadoFinal:
                print("")

        manager.process_events(evento)
        
        
    manager.update(delta)
    janela.blit(fundo_da_tela, (0, 0))
    manager.draw_ui(janela)
    desenharBlocos(puzzle.blocos)
    pygame.display.update()
