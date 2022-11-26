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
algoritmo = "Heuristica Pessoal"
estFinal= "1,2,3,4,5,6,7,8,0"
rodando = True

while rodando:
    delta = clock.tick(60)/1000.0
    ## sair do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        ## verifica algum evento
        if evento.type == pygame.USEREVENT:
            ## se algum botão da ui for clicado
            if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                ## se o botao clicado foi o de embaralhar, entao embaralha
                if evento.ui_element == botao_embaralhar:
                    puzzle.blocosAleatorios()

                ## se o botao clicado for para adicionar o estado final
                elif evento.ui_element == setBotaoFinal:
                    ## verifica se não há textos
                    if not puzzle.setBlocos(EstadoFinal.get_text()):
                        texto_alerta.set_text("Estado final inválido!")
                    else:
                        texto_alerta.set_text("Estado final inválido!")
                        puzzle.estadoFinal = EstadoFinal.get_text()

                ## verifica o botão de informação
                elif evento.ui_element == botao_info:
                    Info_msg = '<b>8-Puzzle<br><br>Autores:</b><br>Lucas Vinícius Voltera<br>Carlos Eduardo Santana'
                    # Information Box - Info
                    info_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = Info_msg,
                                                                                                window_title ='Informações dos desenvolvedores',)

                ## verifica se é o botao de solucionar                                                                            
                elif evento.ui_element == botao_solucionar:
                    ## se for o algoritmo best-first, executa ele
                    if algoritmo == "Heuristica 1":
                        ## pega o nro de movimento
                        movimentos = puzzle.heuristica1()
                        ## pega o tempo
                        tempo = "{temp: .5f} segundos".format(temp = puzzle.tempoUltimoResolvido)
                        ## manda uma mnesagem de aviso
                        report_msg = '<b>Nós visitados:</b> '+ str(puzzle.custo)+'\n<b>Tempo:</b>'+ tempo + '\n<b>Resolução:</b> '+str(len(movimentos))+' Passos'
                        janela_confirmacao = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                            manager = manager,
                                                                                                            action_long_desc = report_msg,
                                                                                                            window_title =algoritmo.split(" ")[0] + ' Report da busca',)
                        ## faz a animacao
                        animacaoSolucionar(puzzle, movimentos)
                    
                    ## se for o algoritmo da heuristica 2
                    elif algoritmo == "Heuristica 2":
                        ## pega o nro de movimentos
                        movimentos = puzzle.heuristica2()
                        ## pega o tempo
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.tempoUltimoResolvido)
                        ## manda uma mensagem de aviso
                        report_msg = '<b>Nós visitados:</b> '+str(puzzle.custo)+'\n<b>Tempo:</b>'+ tempo + '\n<b>Resolução:</b>'+str(len(movimentos))+' Passos'
                        janela_confirmacao = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                            manager = manager,
                                                                                                            action_long_desc = report_msg,
                                                                                                            window_title =algoritmo.split(" ")[0] + ' Report da busca',)

                        animacaoSolucionar(puzzle, movimentos)

                    elif algoritmo == "Heuristica Pessoal":
                        ## pega o nro de movimentos
                        movimentos = puzzle.heristicaPessoal()
                        ## pega o tempo
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.tempoUltimoResolvido)
                        ## manda uma mensagem de aviso
                        report_msg = '<b>Nós visitados:</b> '+str(puzzle.custo)+'\n<b>Tempo:</b>'+ tempo + '\n<b>Resolução:</b>'+str(len(movimentos))+' Passos'
                        janela_confirmacao = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                            manager = manager,
                                                                                                            action_long_desc = report_msg,
                                                                                                            window_title =algoritmo.split(" ")[0] + ' Report da busca',)

                        ## faz a animacao
                        animacaoSolucionar(puzzle, movimentos)
            
            ## verifica o algoritmo que o usuario escolheu
            elif evento.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == botaoAlgoritmos:
                    algoritmo = evento.text

            ## verifica a entrada de dados do usuario
            elif evento.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED and evento.ui_element == EstadoFinal:
                print("")
        
        manager.process_events(evento)
        
        
    manager.update(delta)
    janela.blit(fundo_da_tela, (0, 0))
    manager.draw_ui(janela)
    desenharBlocos(puzzle.blocos)
    pygame.display.update()
