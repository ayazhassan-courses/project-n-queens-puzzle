import pygame
from pygame import mixer
from pygame.locals import *
import time

# initialize the pygame
pygame.init()

def main():
    mixer.music.load('background.mp3')
    mixer.music.play(-1)
screen = pygame.display.set_mode((600, 600))

pygame.display.set_caption('Queens Puzzle')

icon = pygame.image.load ('logo.png')
pygame.display.set_icon(icon)


###########################################################################
# GAME SCREEN
def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font("CinzelDecorative-Regular.ttf", 30)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (0, 0, 0)),
                    (100, (screen.get_height() // 2) - 10))
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = ""
    display_box(screen, question + ": " + current_string)
    while True:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            break
        elif inkey == K_MINUS:
            current_string += ("_")
        elif inkey <= 127:
            current_string += (chr(inkey))
        display_box(screen, question + ": " + "".join(current_string))
    return "".join(current_string)


def clashes(inserted, queens):
    # Column clashes
    insertedrow, insertedcolumn = inserted
    for row, column in queens:
        if row == insertedrow:
            return True
        if column == insertedcolumn:
            return True
        if abs(insertedcolumn - column) == abs(insertedrow - row):
            return True
    return False


def draw_board(screen, n):
    running = True
    queenat = []
    HowManyWrong = 0
    errormessage = ""
    GameOver = False
    IllegalMove = False
    while running:
        if GameOver:
            gameOver_text(200, 200,(0, 0, 0))
            pygame.display.update()
            continue
        if IllegalMove:
            if time.time() - timer > 1:
                IllegalMove = False
            else:
                message(200, 200, "Illegal Move", (0, 0, 0))
                pygame.display.update()
                continue
        colors = [(80,80,80), (255, 255, 255)]
        surface_sz = 600
        sq_sz = surface_sz // n
        surface_sz = n * sq_sz
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                column = int(x / sq_sz)
                row = int(y / sq_sz)
                insertQueenat = (row, column)
                if (row, column) not in queenat:
                    if clashes(insertQueenat, queenat):
                        HowManyWrong += 1
                        if HowManyWrong == 2:
                            GameOver = True
                            game_over()
                            pygame.quit()
                            running = False
                        else:
                            IllegalMove = True
                            timer = time.time()
                    else:
                        queenat.append(insertQueenat)
                        if len(queenat) == n:
                            completed()
                            running = False
                else:
                    queenat.remove(insertQueenat)

        for i in range(n):
            c_indx = i % 2
            for j in range(n):
                the_square = (j * sq_sz, i * sq_sz, sq_sz, sq_sz)
                screen.fill(colors[c_indx], the_square)
                c_indx = (c_indx + 1) % 2
        for row, column in queenat:
            queen_icon(column * sq_sz, row * sq_sz)

        pygame.display.update()


queen = pygame.image.load('queen1.png')


def queen_icon(x=260, y=260):
    global queen
    screen.blit(queen, (x, y))


game_font = pygame.font.Font('CinzelDecorative-Regular.ttf', 20)


def message(x, y, msg, color):
    instruction = game_font.render(msg, True, color)
    screen.blit(instruction, (x, y))


def game_screen():
    screen = pygame.display.set_mode((600, 600))
    running = True
    while running:
        screen.fill((255, 255, 255))
        # screen.fill((150,150,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        instruction1 = 'Place  "N"  Queens in such a way that no two'  # how to play text
        message(50, 50, instruction1, (0, 0, 0))
        instruction2 = 'queens threaten each other; thus, a solution'
        message(35, 80, instruction2, (0, 0, 0))
        instruction3 = 'requires that no two queens share the same'
        message(40, 110, instruction3, (0, 0, 0))
        instruction4 = 'row, column, or diagonal.'
        message(150, 140, instruction4, (0, 0, 0))
        instruction5 = 'Choose "N" between 4 and 20'
        message(130, 170, instruction5, (0, 0, 0))

        n = int(ask(screen, "Enter Board Size (N)"))  # user input
        global queen
        queen = pygame.transform.scale(queen, (600 // n, 600 // n))
        if n >= 4 and n <= 20:
            draw_board(screen, n)
            running = False
        else:
            running = False
        pygame.display.update()


###########################################################################
font3 = pygame.font.Font('CinzelDecorative-Regular.ttf', 20)


def gameOver_text(x, y, color):
    game_over_font = pygame.font.Font('CinzelDecorative-Regular.ttf', 40)
    text3 = game_over_font.render("Game Over!", True, color)
    screen.blit(text3, (x, y))


def game_over():
    screen = pygame.display.set_mode((400, 200))
    mixer.music.load('game over sound.mp3')
    mixer.music.play()
    running = True
    while running:
        screen.fill((0, 0, 0))
        gameOver_text(80, 90, (255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu_screen()
        pygame.display.update()


# game_over()


###########################################################################
def completed_text(x, y):
    text4 = font3.render("Congratulations!", True, (255, 255, 255))
    screen.blit(text4, (x, y))
    text5 = font3.render("You have found the solution", True, (255, 255, 255))
    screen.blit(text5, (30, 105))


def completed():
    global screen
    screen = pygame.display.set_mode((400, 200))
    mixer.music.load('level completed.mp3')
    mixer.music.play()
    running = True
    while running:
        screen.fill((0, 0, 0))
        completed_text(90, 80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_screen()
                running = False
        pygame.display.update()


# completed()


###################################################################################

# MENU SCREEN
menu = pygame.image.load('menu.png')

font = pygame.font.Font('Ruritania.ttf', 60)
font2 = pygame.font.Font('CinzelDecorative-Regular.ttf', 25)


def text(x, y):
    text = font.render("Queens Puzzle", True, (255, 255, 255))
    screen.blit(text, (x, y))


def start(x, y):
    text2 = font2.render("Start Game", True, (0, 0, 0))
    screen.blit(text2, (x, y))


def menu_screen():
    main()
    screen = pygame.display.set_mode((600, 600))
    running = True
    while running:
        screen.fill((200, 240, 240))
        screen.blit(menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        text(95, 120)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 200 + 200 > mouse[0] > 200 and 230 + 50 > mouse[1] > 230:
            pygame.draw.rect(screen, (220, 220, 220), (200, 230, 200, 50))
            start(215, 240)  # displays 'start game' text
            if click[0] == 1:
                game_screen()  # loads another screen
                running = False  # exists screen
        else:
            pygame.draw.rect(screen, (255, 255, 255), (200, 230, 200, 50))
            start(215, 240)  # displays 'start game' text
        pygame.display.update()


menu_screen()

