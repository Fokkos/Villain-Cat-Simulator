import pygame
import random
from pygame import mixer

from scripts import render_inventory, sprites
import constants

# initialise pygame
pygame.init()

# create the screen
screenX = constants.SCREEN_X
screenY = constants.SCREEN_Y
screen = pygame.display.set_mode((screenX, screenY))
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))  # make cursor invisible
start = False
show_inventory = False
scene = "title"  # look into setting as a dictionary?

font = pygame.font.Font('freesansbold.ttf', 32)
subtitle_font = pygame.font.Font('freesansbold.ttf', 22)

# caption and icon
pygame.display.set_caption("kitty simulator >:3")
icon = pygame.image.load('img/icon.jpg')
pygame.display.set_icon(icon)

# inventory
inventory_bar = pygame.image.load("img/inventory/inventory.png")
inventory = []

# paw initial values
paw_img = pygame.image.load('img/player/Paw.png')
pawX = 0
pawY = 0
claw_mark = []

# SFX
cat_sound = mixer.Sound("sounds/miau.wav")
tear_sound = mixer.Sound("sounds/tear.wav")
chomp_sound = mixer.Sound("sounds/chomp.wav")
door_sound = mixer.Sound("sounds/door.wav")
water_sound = mixer.Sound("sounds/water.wav")
glass_sound = mixer.Sound("sounds/glass.wav")
thud_sound = mixer.Sound("sounds/thud.wav")

# title screen assets
title_screen = pygame.image.load("img/title_screen/title_screen.png")
start_button = sprites.StartButton()

# lore page assets
lore_music = mixer.Sound("sounds/space-odyssey.wav")
lore = pygame.image.load("img/lore_screen/lore.png")
skip = pygame.image.load("img/lore_screen/skip.png")
loreY = 75

# living room assets
state_bookshelf = "default"
state_bookshelf_bottom = "default"
state_blue_book = "invisible"
state_sage_book = "invisible"
state_armchair = "default"
state_living_room_right_door = "default"
state_keypad = "default"
state_keypad_visible = False
keypad_input = ""
state_secret = False
state_secret_door = "default"

bookshelf = sprites.Bookshelf()
blue_book = sprites.BlueBook()
sage_book = sprites.SageBook()
armchair = sprites.Armchair()
living_room_right_door = sprites.RightDoor()
keypad = sprites.Keypad()
secret_door = sprites.SecretDoorLeft()

# kitchen assets
state_fridge = "default"
state_salmon = "default"
state_salmon_visible = False
state_sink = "default"
state_sink_tap = False
state_cabinet = "default"
state_cabinet_visible = False
state_lighter = False
state_plant_pot = "default"
state_kitchen_left_door = "default"
state_flower = "default"

fridge = sprites.Fridge()
salmon_minigame = sprites.Salmon()
sink = sprites.Sink()
cabinet = sprites.Cabinet()
oven = sprites.Oven()
kitchen_left_door = sprites.LeftDoor()
flower = sprites.Flower()

# secret lab assets
state_secret_lab_door = "default"
state_lab_table = "default"
state_blood_minigame_visible = False
state_blood_minigame = "default"
state_blood_get = False
state_shelf = "default"
state_candle_get = False

secret_lab_door = sprites.SecretDoorRight()
lab_table = sprites.LabTable()
blood_minigame = sprites.BloodMinigame()
shelf = sprites.Shelf()

timerCount = sprites.Countdown()

# chaos meter
chaos_bar = sprites.Chaosbar(constants.HOUSE_HEALTH)

# ending assets
regular_ending_flag = False
true_ending_flag = False    # when the pentagram appears
true_ending_start_flag = False  # when you click the pentagram
true_ending_start_flag_2 = False
state_pentagram = "default"
state_true_ending = "default"

pentagram = sprites.Pentagram()
true_ending = sprites.Ending()


def regular_ending():
    screen.blit(pygame.image.load("img/endings/regular_ending.png"), (0, 0))
    score_text = font.render(
        ("Score: " + str(constants.HOUSE_HEALTH - chaos_bar.clean_house) + "/" + str(constants.HOUSE_HEALTH)), True,
        (255, 255, 255))
    screen.blit(score_text, (50, 100))
    summary = subtitle_font.render(chaos_bar.damageReport(), True, (255, 255, 255))
    screen.blit(summary, (0, 525))


def check_for_true_ending():
    if "candle" in inventory and "lighter" in inventory and "blood" in inventory and "salmon" in inventory:
        return True
    else:
        return False


# sets the background size and position taking inventory bar into account
def set_background(img_link):
    screen.blit(pygame.transform.scale(pygame.image.load(img_link), (800, 500)), (0, 0))


# plays the meow sound with a probability of 1/n+1
def meow_rng(n):
    roll = random.randint(0, n)
    if roll == 0:
        cat_sound.play()


def paw(x, y):
    screen.blit(paw_img, (x + 70, y))


def show_lore(y):
    screen.blit(lore, (0, y))
    screen.blit(skip, (0, 520))


def draw_inventory():
    screen.blit(inventory_bar, (0, screenY - inventory_bar.get_height()))


start_ticks = 0

# Game Loop

running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEMOTION:
            mousePosX, mousePosY = pygame.mouse.get_pos()
            pawX = mousePosX - (paw_img.get_width() / 2)
            pawY = mousePosY - 50
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            paw_img = pygame.image.load('img/player/paw_claw.png')
            meow_rng(8)
            claw_mark.append(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            paw_img = pygame.image.load('img/player/Paw.png')
            cat_sound.stop()
            claw_mark = []

        # pentagram logic
        if true_ending_flag:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(615, 500, 100, 85).collidepoint(pygame.mouse.get_pos()):
                    true_ending_start_flag = True
            else:
                if pygame.Rect(615, 500, 100, 85).collidepoint(pygame.mouse.get_pos()):
                    state_pentagram = "light"
                else:
                    state_pentagram = "default"
            pentagram.changeState(state_pentagram)

        if scene == "title":
            if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("start button pressed")
                    lore_music.play()
                    scene = "exposition"
                else:
                    start_button.setImage("img/title_screen/start_button-hover.png", (150, 90))
            else:
                start_button.setImage("img/title_screen/start_button.png", (150, 90))

        elif scene == "exposition":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_ticks = pygame.time.get_ticks()
                    print("space button pressed")
                    scene = "living_room"
                    lore_music.stop()

        elif scene == "living_room":
            # book state logic
            if state_blue_book == "visible":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(100, 50, 600, 400).collidepoint(pygame.mouse.get_pos()):
                        state_blue_book = "eaten"
                        chaos_bar.hit(1)
                        chomp_sound.play()
                        inventory.append("blue_scrap")
            elif state_blue_book == "eaten":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not pygame.Rect(100, 50, 600, 400).collidepoint(pygame.mouse.get_pos()):
                        state_blue_book = "invisible-eaten"

            if state_sage_book == "visible":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(100, 50, 600, 400).collidepoint(pygame.mouse.get_pos()):
                        state_sage_book = "torn"
                        chaos_bar.hit(2)
                        tear_sound.play()
                        inventory.append("sage_scrap")
            elif state_sage_book == "torn":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not pygame.Rect(100, 50, 600, 400).collidepoint(pygame.mouse.get_pos()):
                        state_sage_book = "invisible-torn"

            # bookshelf logic
            if event.type == pygame.MOUSEBUTTONDOWN and not state_keypad_visible:
                if pygame.Rect(138, 193, 35, 60).collidepoint(pygame.mouse.get_pos()):
                    if state_blue_book == "invisible":
                        state_blue_book = "visible"
                    else:

                        state_blue_book = "eaten"
                elif pygame.Rect(187, 265, 40, 75).collidepoint(pygame.mouse.get_pos()):
                    if state_sage_book == "invisible":
                        state_sage_book = "visible"
                    else:
                        state_sage_book = "torn"

            if state_bookshelf_bottom == "default":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(77, 334, 279, 421).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf_bottom = "knocked"
                        chaos_bar.hit(2)
                    else:
                        state_bookshelf = "default"
                else:  # hover
                    if pygame.Rect(73, 341, 200, 65).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf = "init_light_bottom_shelf"
                    elif pygame.Rect(138, 193, 35, 60).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf = "init_light_dark_blue"
                    elif pygame.Rect(187, 265, 40, 75).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf = "init_light_sage"
                    else:
                        state_bookshelf = "default"
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(208, 344, 50, 50).collidepoint(pygame.mouse.get_pos()):
                        state_keypad_visible = True
                else:  # hover
                    if pygame.Rect(208, 344, 50, 50).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf = "final_light_keypad"
                    elif pygame.Rect(138, 193, 35, 60).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf = "final_light_dark_blue"
                    elif pygame.Rect(187, 265, 40, 75).collidepoint(pygame.mouse.get_pos()):
                        state_bookshelf = "final_light_sage"
                    else:
                        state_bookshelf = "final_nolight"
            bookshelf.changeState(state_bookshelf)

            # armchair logic
            if event.type == pygame.MOUSEBUTTONDOWN and not state_keypad_visible:
                if pygame.Rect(520, 340, 100, 50).collidepoint(pygame.mouse.get_pos()):
                    regular_ending_flag = True
            else:  # hover
                if pygame.Rect(520, 340, 100, 50).collidepoint(pygame.mouse.get_pos()):
                    state_armchair = "highlighted"
                else:
                    state_armchair = "default"
            armchair.changeState(state_armchair)

            # right living room door logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(740, 160, 60, 300).collidepoint(pygame.mouse.get_pos()):
                    door_sound.play()
                    scene = "kitchen"
            else:  # hover
                if pygame.Rect(740, 160, 60, 300).collidepoint(pygame.mouse.get_pos()):
                    state_living_room_right_door = "highlighted"
                else:
                    state_living_room_right_door = "default"
            living_room_right_door.changeState(state_living_room_right_door)

            # keypad logic
            if state_keypad_visible:
                if state_keypad == "correct" or state_keypad == "incorrect":
                    pygame.time.wait(1000)
                    if state_keypad == "correct":
                        state_keypad_visible = False
                        state_secret = True
                    state_keypad = "default"
                    keypad_input = ""

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(150, 100, 500, 300).collidepoint(pygame.mouse.get_pos()):
                        if pygame.Rect(180, 122, 130, 60).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "1"
                        elif pygame.Rect(344, 122, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "2"
                        elif pygame.Rect(493, 122, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "3"
                        elif pygame.Rect(180, 189, 130, 60).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "4"
                        elif pygame.Rect(344, 189, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "5"
                        elif pygame.Rect(493, 189, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "6"  # 255 321
                        elif pygame.Rect(180, 255, 130, 60).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "7"
                        elif pygame.Rect(344, 255, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "8"
                        elif pygame.Rect(493, 255, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "9"
                        elif pygame.Rect(180, 321, 130, 60).collidepoint(pygame.mouse.get_pos()):
                            keypad_input = ""
                        elif pygame.Rect(344, 321, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            keypad_input += "0"
                        elif pygame.Rect(493, 321, 130, 65).collidepoint(pygame.mouse.get_pos()):
                            if keypad_input == "11037":  # funny number
                                state_keypad = "correct"
                            else:
                                state_keypad = "incorrect"

                        print(keypad_input)
                    else:
                        state_keypad_visible = False
            keypad.changeState(state_keypad)

            # secret door logic
            if state_secret:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(0, 120, 70, 330).collidepoint(pygame.mouse.get_pos()):
                        door_sound.play()
                        scene = "secret_lab"
                else:  # hover
                    if pygame.Rect(0, 120, 70, 330).collidepoint(pygame.mouse.get_pos()):
                        state_secret_door = "highlighted"
                    else:
                        state_secret_door = "default"
                secret_door.changeState(state_secret_door)

        elif scene == "kitchen":

            # fridge logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(580, 130, 145, 295).collidepoint(pygame.mouse.get_pos()) and not state_cabinet_visible:
                    state_salmon_visible = True
                    door_sound.play()
                    print("fridge clicked")

            else:  # hover
                if pygame.Rect(580, 130, 145, 295).collidepoint(pygame.mouse.get_pos()):
                    state_fridge = "highlighted"
                else:
                    state_fridge = "default"
            fridge.changeState(state_fridge)

            # salmon minigame logic
            if state_salmon_visible:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(150, 100, 500, 300).collidepoint(pygame.mouse.get_pos()):
                        if pygame.Rect(250, 175, 300, 175).collidepoint(pygame.mouse.get_pos()):
                            match state_salmon:
                                case "default":
                                    state_salmon = "one_bite"
                                    chaos_bar.hit(1)
                                    chomp_sound.play()
                                    break
                                case "one_bite":
                                    state_salmon = "two_bites"
                                    chaos_bar.hit(1)
                                    chomp_sound.play()
                                    break
                                case "two_bites":
                                    state_salmon = "finish"
                                    chaos_bar.hit(1)
                                    chomp_sound.play()
                                    # chaos_bar.hit(3)
                                    inventory.append("salmon")
                                    break
                                case "finish":

                                    break
                    else:
                        state_salmon_visible = False
            salmon_minigame.changeState(state_salmon)

            # sink logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(430, 165, 100, 80).collidepoint(pygame.mouse.get_pos()) and not state_sink_tap:
                    water_sound.play()
                    chaos_bar.hit(1)
                    state_sink_tap = True
                elif pygame.Rect(440, 300, 140, 120).collidepoint(pygame.mouse.get_pos()) and not state_salmon_visible:
                    state_cabinet_visible = True
                    door_sound.play()

            else:  # hover
                if pygame.Rect(430, 165, 100, 80).collidepoint(pygame.mouse.get_pos()):
                    if not state_sink_tap:
                        state_sink = "tap_light"
                elif pygame.Rect(440, 300, 140, 120).collidepoint(pygame.mouse.get_pos()):
                    if state_sink_tap:
                        state_sink = "sink_on_door_light"
                    else:
                        state_sink = "sink_door_light"
                else:
                    if state_sink_tap:
                        state_sink = "default_tap_on"
                    else:
                        state_sink = "default"
            sink.changeState(state_sink)

            # cabinet logic
            if state_cabinet_visible:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(150, 100, 500, 300).collidepoint(pygame.mouse.get_pos()):
                        if pygame.Rect(550, 250, 45, 100).collidepoint(pygame.mouse.get_pos()) and not state_lighter:
                            state_cabinet = "empty"
                            inventory.append("lighter")
                            state_lighter = True

                    else:
                        state_cabinet_visible = False
                else:
                    if pygame.Rect(550, 250, 45, 100).collidepoint(pygame.mouse.get_pos()) and not state_lighter:
                        state_cabinet = "lighter_light"
                    elif state_lighter:
                        state_cabinet = "empty"
                    else:
                        state_cabinet = "default"
            cabinet.changeState(state_cabinet)

            # left kitchen door logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(0, 120, 70, 330).collidepoint(pygame.mouse.get_pos()):
                    door_sound.play()
                    scene = "living_room"
            else:  # hover
                if pygame.Rect(0, 120, 70, 330).collidepoint(pygame.mouse.get_pos()):
                    state_kitchen_left_door = "highlighted"
                else:
                    state_kitchen_left_door = "default"
            kitchen_left_door.changeState(state_kitchen_left_door)

            # flower logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(170, 165, 80, 85).collidepoint(pygame.mouse.get_pos()):
                    glass_sound.play()
                    chaos_bar.hit(2)
                    state_flower = "smash"
            else:
                if pygame.Rect(170, 165, 80, 85).collidepoint(pygame.mouse.get_pos()) and not state_flower == "smash":
                    state_flower = "light"
                elif not state_flower == "smash":
                    state_flower = "default"
            flower.changeState(state_flower)

        elif scene == "secret_lab":

            # secret lab door logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(740, 160, 60, 300).collidepoint(pygame.mouse.get_pos()):
                    door_sound.play()
                    scene = "living_room"
            else:  # hover
                if pygame.Rect(740, 160, 60, 300).collidepoint(pygame.mouse.get_pos()):
                    state_secret_lab_door = "highlighted"
                else:
                    state_secret_lab_door = "default"
            secret_lab_door.changeState(state_secret_lab_door)

            # secret lab table logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(160, 295, 65, 80).collidepoint(pygame.mouse.get_pos()):
                    state_blood_minigame_visible = True
            else:  # hover
                if pygame.Rect(160, 295, 65, 80).collidepoint(pygame.mouse.get_pos()):
                    state_lab_table = "light"
                else:
                    state_lab_table = "default"
            lab_table.changeState(state_lab_table)

            # blood minigame logic
            if state_blood_minigame_visible:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(150, 100, 500, 300).collidepoint(pygame.mouse.get_pos()):
                        if pygame.Rect(335, 150, 60, 120).collidepoint(pygame.mouse.get_pos()) and not state_blood_get:
                            state_blood_minigame = "finish"
                            glass_sound.play()
                            state_blood_get = True
                            inventory.append("blood")
                            chaos_bar.hit(2)
                    else:
                        state_blood_minigame_visible = False
                else:
                    if pygame.Rect(335, 150, 60, 120).collidepoint(pygame.mouse.get_pos()) and not state_blood_get:
                        state_blood_minigame = "light"
                    elif not state_blood_get:
                        state_blood_minigame = "default"
            blood_minigame.changeState(state_blood_minigame)

            # shelf logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(455, 145, 110, 125).collidepoint(pygame.mouse.get_pos()) and not state_candle_get:
                    thud_sound.play()
                    chaos_bar.hit(1)
                    state_shelf = "fall"
                    inventory.append("candle")
                    state_candle_get = True
            else:
                if pygame.Rect(455, 145, 110, 125).collidepoint(pygame.mouse.get_pos()) and not state_shelf == "fall":
                    state_shelf = "light"
                elif not state_shelf == "fall":
                    state_shelf = "default"
            shelf.changeState(state_shelf)
        if true_ending_start_flag_2:
            if event.type == pygame.MOUSEBUTTONDOWN and state_true_ending == "default":
                state_true_ending = "second"
        true_ending.changeState(state_true_ending)

    if scene == "title":
        screen.blit(title_screen, (0, 0))
        start_button.draw(screen)
    elif scene == "exposition":
        show_lore(loreY)
        loreY -= .3

    else:
        seconds_remaining = (pygame.time.get_ticks() - start_ticks) / 1000

        if seconds_remaining > constants.MAX_TIME:
            regular_ending_flag = True

        if scene == "living_room":

            set_background('img/living_room/living_room.png')
            bookshelf.draw(screen)
            armchair.draw(screen)
            living_room_right_door.draw(screen)
            chaos_bar.default_bar(screen)
            # pygame.draw.rect(screen, (255,0,0), (600, 10, 150, 30))
            show_inventory = True

            if state_keypad_visible:
                keypad.draw(screen)

            if state_secret:
                secret_door.draw(screen)

            chaos_bar.update(screen)
            timerCount.update(seconds_remaining, screen)

            if state_blue_book == "visible" or state_blue_book == "eaten":
                blue_book.draw(screen)
            if state_blue_book == "eaten":
                blue_book.changeState("eaten")

            if state_sage_book == "visible" or state_sage_book == "torn":
                sage_book.draw(screen)
            if state_sage_book == "torn":
                sage_book.changeState("torn")

        elif scene == "kitchen":
            set_background('img/kitchen/kitchen.png')
            fridge.draw(screen)
            sink.draw(screen)
            oven.draw(screen)
            kitchen_left_door.draw(screen)
            flower.draw(screen)

            if state_salmon_visible:
                salmon_minigame.draw(screen)
            elif state_cabinet_visible:
                cabinet.draw(screen)

            chaos_bar.update(screen)
            timerCount.update(seconds_remaining, screen)

        elif scene == "secret_lab":
            set_background('img/secret_lab/secret_lab.png')

            secret_lab_door.draw(screen)
            lab_table.draw(screen)
            shelf.draw(screen)

            if state_blood_minigame_visible:
                blood_minigame.draw(screen)
            timerCount.update(seconds_remaining, screen)

            chaos_bar.update(screen)

    if show_inventory:
        draw_inventory()
        if len(inventory) > 0:
            render_inventory.render_inventory_bar(screen, inventory)

    if regular_ending_flag:
        show_inventory = False
        regular_ending()

    true_ending_flag = check_for_true_ending()

    if true_ending_flag:
        pentagram.draw(screen)

    if true_ending_start_flag:
        true_ending.draw(screen)
        true_ending_start_flag_2 = True

    paw(pawX, pawY)

    pygame.display.update()
