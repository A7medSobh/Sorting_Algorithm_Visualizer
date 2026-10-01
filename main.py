import pygame as pg
import random as rand
from buttons import Button
from Algorithms.mergeSort import merge_sort_visual


pg.init()

#create a window
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
pg.display.set_caption("Sorting Algorithm Visualizer")

clock = pg.time.Clock()

#screen size
WIDTH, HEIGHT = screen.get_size()

#Fonts
title_font = pg.font.Font("fonts/PressStart2P.ttf", 50)
subtitle_font = pg.font.Font("fonts/PressStart2P.ttf", 20)

#Sounds
hover_sound = pg.mixer.Sound("soundEffects/hoverSound.wav")
start_sound = pg.mixer.Sound("soundEffects/UI_START.wav")
select_sound = pg.mixer.Sound("soundEffects/UI_SELECT.wav")


#intro timing
alpha = 0
fade_speed = 3

intro_done = False
intro_timer = 0

game_state = "intro"


#numbers that will be visualized & Array sizes:
array_size = 50
numbers = [
    rand.randint(10, 100)
    for _ in range(array_size)
]

sorting = False
merge_comparisons = 0
sort_generator = None


#variables to control sorting
sorting = False
sort_finished = False

sort_generator = None
comparing = []

sort_timer = 0
sorted_timer = 0
sorted_count = 0

sort_speed = 1
green_speed = 2

def intro_screen():
    global alpha, intro_done, intro_timer, game_state

    #transparent surface
    title_surface = title_font.render(
        "SORTING ALGORITHM VISUALIZER!",
        True,
        (255, 255, 100)
    )

    subtitle_surface = subtitle_font.render(
        "Learn • Compare • Sort",
        True,
        (180, 180, 180)
    )

    #Apply transparency
    title_surface.set_alpha(alpha)
    subtitle_surface.set_alpha(alpha)

    #background
    screen.fill((20, 20, 30))

    #center title
    title_rect = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 80)
    )

    subtitle_rect = subtitle_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 80)
    )

    screen.blit(title_surface, title_rect)
    screen.blit(subtitle_surface, subtitle_rect)

    #increase transparency
    alpha = alpha + fade_speed

    if alpha >= 255:
        alpha = 255

    intro_timer = intro_timer + 1

    #stay on intro for about 2 secs after fading in
    if intro_timer >= 240:
        intro_done = True
        game_state = "menu"

    # -------------------------
    # BUTTONS
    # -------------------------

button_width = 350
button_height = 80

button_x_pos = WIDTH // 2 - button_width // 2

start_button = Button(
    "START",
    button_x_pos,
    350,
    button_width,
    button_height
    )

options_button = Button(
    "OPTIONS",
    button_x_pos,
    460,
    button_width,
    button_height
    )


exit_button = Button(
    "EXIT",
    button_x_pos,
    570,
    button_width,
    button_height
    )


# ------------------------------------------------------------
# ARAY SIZE BUTTONS, to choose the size of array from OPTIONS
# ------------------------------------------------------------
button_width = 140
button_height = 60
button_gap = 20

sizes = [25, 50, 100, 200]

size_buttons = []

for i, size in enumerate(sizes):
    x = (
        WIDTH // 2
        - (4 * button_width + 3 * button_gap) // 2
        + i * (button_width + button_gap)
    )

    button = Button(
        str(size),
        x,
        320,
        button_width,
        button_height
        )
    size_buttons.append(button)


#button to exit OPTIONS
back_button = Button(
    "BACK",
    WIDTH // 2 - 175,
    500,
    350,
    70
)

#button to exit sorting bars screen
sort_exit_button = Button(
    "BACK",
    WIDTH // 2 - 175,
    HEIGHT - 80,
    350,
    70
)
def main_menu(event):

    screen.fill((20, 20, 30))

    # -------------------------
    # TITLE
    # -------------------------

    title = title_font.render(
        "SORTING ALGORITHM",
        True,
        (255, 255, 100)
    )

    title2 = title_font.render(
        "VISUALIZER",
        True,
        (255, 255, 100)
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 180)
    )

    title2_rect = title2.get_rect(
        center=(WIDTH // 2, 250)
    )

    screen.blit(title, title_rect)
    screen.blit(title2, title2_rect)

#------------
#DRAW BUTTONS
#--------------
    start_button.draw(screen, subtitle_font, hover_sound)
    options_button.draw(screen, subtitle_font, hover_sound)
    exit_button.draw(screen, subtitle_font, hover_sound)

    # -------------------------
    # HANDLE MOUSE CLICK
    # -------------------------
    if start_button.is_clicked(event):
        return "sorting"

    if options_button.is_clicked(event):
        return "options"

    if exit_button.is_clicked(event):
        return "exit"

    return "menu"


def sorting_screen(event=None):
    screen.fill((20, 20, 30))

    title = title_font.render(
        "SORTING VISUALIZER",
        True,
        (255, 255, 255)
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 80)
    )

    screen.blit(title, title_rect)

    # Area where the bars will be displayed
    graph_top = 150
    graph_bottom = HEIGHT - 100

    # Width of each bar
    bar_width = WIDTH // len(numbers)

    for i, number in enumerate(numbers):

        # Convert number (10-100) into a height
        bar_height = int(
            number / 100 * (graph_bottom - graph_top)
        )

        x = i * bar_width
        y = graph_bottom - bar_height

        # Color the bars based on whether they are being compared
        if i < sorted_count:
            color = (100, 255, 100)  # Green for sorted bars
        elif i in comparing:
            color = (255, 100, 100)  # Red for bars being compared
        else:
            color = (255, 255, 100)

        pg.draw.rect(
            screen,
            color,
            (x, y, bar_width - 2, bar_height)
        )

    sort_exit_button.draw(screen, subtitle_font, hover_sound)
    if sort_exit_button.is_clicked(event):
        return "menu"
    return "sorting"

def options_screen(event=None):
    global array_size, numbers

    # Background
    screen.fill((20, 20, 30))

    # -------------------------
    # TITLE
    # -------------------------
    title = title_font.render(
        "OPTIONS",
        True,
        (255, 255, 100)
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 120)
    )

    screen.blit(title, title_rect)


    # -------------------------
    # ARRAY SIZE TEXT
    # -------------------------
    array_text = subtitle_font.render(
        "ARRAY SIZE",
        True,
        (255, 255, 255)
    )

    array_rect = array_text.get_rect(
        center=(WIDTH // 2, 250)
    )

    screen.blit(array_text, array_rect)

    #Draw array size buttons
    for button in size_buttons:
        button.draw(screen, subtitle_font, hover_sound)

    #Back button
    back_button.draw(screen, subtitle_font, hover_sound)

    #handle clicks
    for button in size_buttons:
        if button.is_clicked(event):
            array_size = int(button.text)
            numbers = [
                rand.randint(10, 100)
                for _ in range(array_size)
            ]
            return "menu"

    if back_button.is_clicked(event):
        return "menu"
    return "options"


#------------------------------------------------------------------------------------
# Keep the window open
running = True

while running:

    # -------------------------
    # HANDLE EVENTS
    # -------------------------
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if game_state == "menu":
            game_state = main_menu(event)

        elif game_state == "options":
            game_state = options_screen(event)

        elif game_state == "sorting":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not sorting:
                    #Shuffle the array if sorting is completed
                    if sort_finished and sorted_count == len(numbers):
                        rand.shuffle(numbers)
                        sorted_timer = 0
                        sorted_count = 0
                        comparing = []
                        sort_finished = False

                    sort_generator = merge_sort_visual(numbers)
                    sorting = True


    #Run sorting one step at a time
    if sorting:

        sort_timer += 1

        if sort_timer >= sort_speed:
            sort_timer = 0
            try:
                new_numbers, comparing = next(sort_generator)
                numbers[:] = new_numbers
            except StopIteration:
                sorting = False
                comparing = []
                sort_finished = True

    if sort_finished and sorted_count < len(numbers):
        sorted_timer += 1

        if sorted_timer >= green_speed:
            sorted_timer = 0
            sorted_count += 1


    # -------------------------
    # DRAW CURRENT SCREEN
    # -------------------------
    if game_state == "intro":
        intro_screen()

    elif game_state == "menu":
        main_menu(None)
        pass

    elif game_state == "options":
        options_screen(None)

    elif game_state == "sorting":
        game_state = sorting_screen(event)

    #EXIT THE GAME
    if game_state == "exit":
        running = False

    pg.display.flip()

    clock.tick(60)

pg.quit()