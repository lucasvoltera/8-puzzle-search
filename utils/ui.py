import pygame
import pygame_gui
from .constantes import *
from .matriz import *
from .puzzle import *



#Setup
pygame.init()
## instanciando a fonte
FONTE = pygame.font.Font('utils\FiraCode-Retina.ttf',50)
pygame.display.set_caption('8 Puzzle')
## instanciando a janela
janela = pygame.display.set_mode(TAMANHO_DA_TELA)
## instanciando o background
fundo_da_tela = pygame.Surface(TAMANHO_DA_TELA)
fundo_da_tela.fill(pygame.Color(KINDA_OF_BLACK ))
## instanciando o "Gerente"
manager = pygame_gui.UIManager(TAMANHO_DA_TELA, 'theme.json')
## instanciando o icone
# Creditos: https://iconmonstr.com/puzzle-19-png/
icone = pygame.image.load('utils\logo.png')
pygame.display.set_icon(icone)
## instanciando a janela
pygame_gui.core.IWindowInterface.set_display_title(self=janela, new_title="8-Puzzle")


def exibirElementos():
    #Elementos
    ### Título do arquivo
    pygame_gui.elements.ui_label.UILabel(manager=manager, text="8-Puzzle",
                                         relative_rect=pygame.Rect((425, 40), (400, 40)),object_id="#title_box")


exibirElementos()
### botão de solucionar
botao_solucionar = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 640), (250, 45)),
                                                text='Solucionar puzzle',
                                                manager=manager,
                                                object_id="#solve_btn")


### Opções de algoritmos
algoritmos_layout_rect = pygame.Rect((970, 400), (280, 35))
## nome dos algoritmos disponíveis
opcoesAlgoritmos = ["A*", "Best-First"]
botaoAlgoritmos = pygame_gui.elements.UIDropDownMenu(options_list=opcoesAlgoritmos,
                                                     starting_option=opcoesAlgoritmos[0],
                                                     relative_rect=algoritmos_layout_rect,
                                                     manager=manager)

### Buscar
pygame_gui.elements.ui_label.UILabel(parent_element=botaoAlgoritmos,
                                     manager=manager,
                                     text="Heurística:", # (pos-width, pos-height), (width,height)
                                     relative_rect=pygame.Rect((800, 400), (170, 30)))


report_rect = pygame.Rect((1000, 210), (250, 30))


### input de estado final
EstadoFinal = pygame_gui.elements.UITextEntryLine(relative_rect=report_rect,
                                                  manager=manager)

## texto do estado final
pygame_gui.elements.ui_label.UILabel(parent_element=EstadoFinal,
                                     manager=manager,
                                     text="Estado Final:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((855, 210), (140, 30)))

### set estado final com o botão
setBotaoFinal = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 250), (250, 30)),
                                             text='Definir Estado Final',
                                             manager=manager)


### Botão de emparalhar
botao_layout_rect = pygame.Rect((1000, 350), (250, 30))
botao_embaralhar = pygame_gui.elements.UIButton(relative_rect=botao_layout_rect,
                                                text='Embaralhar',
                                                manager=manager)


### Botão de informações
info_html = "<b>Clique aqui<b> para ver as informações dos desenvolvedores"
botao_layout_rect = pygame.Rect((1250, 690), (30, 30))
botao_info = pygame_gui.elements.UIButton(relative_rect=botao_layout_rect,
                                          text='?',
                                          manager=manager,
                                          tool_tip_text=info_html)
### texto de alerta
texto_alerta = pygame_gui.elements.ui_label.UILabel(manager=manager,
                                                    text="",
                                                    relative_rect=pygame.Rect((920, 320), (250, 30)),
                                                    object_id="#accept_label")



def desenharBlocos(blocos):
    for bloco in blocos:
        if bloco['bloco'] != 0:
            pygame.draw.rect(janela, AQUA , bloco['rect'])
            textoSuperficie = FONTE.render(str(bloco['bloco']), True, DARK_BLUE )
            textoRect = textoSuperficie.get_rect()
            textoRect.center = bloco['rect'].left + 50, bloco['rect'].top + 50
            janela.blit(textoSuperficie, textoRect)
        else:
            pygame.draw.rect(janela, DARK_BLUE  , bloco['rect'])







def animacaoSolucionar(puzzle, movimentos):
    for mv in movimentos:
        zero = puzzle.matriz.procurarBloco(0)
        if mv == "direita":
            puzzle.matriz.moverDireita(zero)
        elif mv == "esquerda":
            puzzle.matriz.moverEsquerda(zero)  
        elif mv == "cima":
           puzzle.matriz.moverCima(zero)
        elif mv == "baixo":
            puzzle.matriz.moverBaixo(zero)
    
        puzzle.setBlocosMatriz()
        desenharBlocos(puzzle.blocos)
        pygame.display.update()
        time.sleep(0.2)