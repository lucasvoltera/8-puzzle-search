import pygame
import pygame_gui
from .constantes import *
from .matriz import *
from .puzzle import *

#Setup
pygame.init()
BASICFONT = pygame.font.Font('utils\FiraCode-Retina.ttf',50)

pygame.display.set_caption('8 Puzzle')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(BABY_BLUE))
manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')

# Rights: https://iconmonstr.com/puzzle-19-png/
programIcon = pygame.image.load('utils\logo.png')
pygame.display.set_icon(programIcon)
pygame_gui.core.IWindowInterface.set_display_title(self=window_surface,new_title="8-Puzzle")



def display_elements():
    #Elements
    ### Title Label
    pygame_gui.elements.ui_label.UILabel(manager=manager,
                                        text="8-Puzzle Game",
                                        relative_rect=pygame.Rect((540, 10), (300, 70)),
                                        object_id="#title_box"
                                        )
    


display_elements()
### solve button
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 640), (250, 45)),
                                             text='Solve Puzzle',
                                             manager=manager,
                                             object_id="#solve_btn")

### algorithmOptions DropDown
dropdown_layout_rect = pygame.Rect((970, 600), (280, 35))
algorithmOptions = ["A* (Manhatan Distance)","Best-First (Manhatan Distance)"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

### Search label
pygame_gui.elements.ui_label.UILabel(parent_element=algorithmDropDown,
                                     manager=manager,
                                     text="Heuristic Search:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((800, 600), (170, 30)))

### Final state input
report_rect = pygame.Rect((1000, 210), (250, 30))
Final_state = pygame_gui.elements.UITextEntryLine(relative_rect=report_rect,
                                                  manager=manager)

### Final state label
pygame_gui.elements.ui_label.UILabel(parent_element=Final_state,
                                     manager=manager,
                                     text="Final State:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((855, 210), (140, 30)))

### set final state with button
set_final_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 250), (250, 30)),
                                                text='Set Final State',
                                                manager=manager)
### shuffle button
button_layout_rect = pygame.Rect((1000, 290), (250, 30))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Shuffle',
                                             manager=manager)

### info button
info_html = "<b>Click Here<b>To see developers info!!!"
button_layout_rect = pygame.Rect((1250, 690), (30, 30))
info_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='?',
                                             manager=manager,
                                             tool_tip_text=info_html)
### alert label
alert_label = pygame_gui.elements.ui_label.UILabel(
                                     manager=manager,
                                     text="",
                                     relative_rect=pygame.Rect((920, 320), (250, 30)),
                                     object_id="#accept_label")


def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, BLUE_GROTTO, block['rect'])
            textSurf = BASICFONT.render(str(block['block']), True, NAVY_BLUE)
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].left+50,block['rect'].top+50
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface, ROYAL_BLUE, block['rect'])

def solveAnimation(moves):
    for mv in moves:
        zero = puzzle.matriz.searchBlock(0)
        if mv == "right":
            puzzle.matriz.moverDireita(zero)
        elif mv == "left":
            puzzle.matriz.moverEsquerda(zero)  
        elif mv == "up":
            puzzle.matriz.moverCima(zero)
        elif mv == "down":
            puzzle.matriz.moverBaixo(zero)
            
        puzzle.setBlocosMatriz()
        draw_blocks(puzzle.blocos)
        pygame.display.update()
        time.sleep(0.2)