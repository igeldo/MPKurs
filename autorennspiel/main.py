# author: Tessa Vogt
# date: 12.11.2022

# Importieren der erforderlichen Bibliotheken
import pygame
import time
import random
import car
import config
import display


pygame.init()


# DEFINE CAR AND BACKGROUND IMAGES
# load background
# set width and height of the display
window = pygame.display.set_mode(display.Display().size)
# set name of the game window
pygame.display.set_caption(display.Display().window_name)
# load background image for the left and right side
backgroundLeft = display.Display("background_left").load_background()
backgroundRight = display.Display("background_right").load_background()
# load car image
car_img = car.Car("car_1", "car_player").load_car()
# define car width
car_width = car.Car("car_1", "car_player").car_width


# all the function are called using this function
def loop():
    # set car position for x and y axis
    [x, y] = car.Car("car_1", "car_player").car_position
    # set changing position of the car
    x_change = 0
    y_change = 0
    # set enemies car speed
    enemy_car_speed = car.Car("car_2", "car_enemy").car_speed
    # set starting stage for the enemies car
    enemy = 0
    # with this the enemies car will come randomly
    [[start_x1, start_x2], start_y] = car.Car("car_2", "car_enemy").car_position
    enemy_startx = random.randrange(start_x1, (start_x2 - car_width))
    # enemies car will come from negative y axis as it comes from opposite direction
    enemy_starty = start_y
    # set enemies car height and width
    [enemy_width, enemy_height] = car.Car("car_2", "car_enemy").car_size

    # Bewegung des Fahrzeugs einstellen
    # if the game doesn't have any problem to start
    bumped = False
    # start the game
    while not bumped:
        # defining the input of the game
        for event in pygame.event.get():
            # if quit input is given
            if event.type == pygame.QUIT:
                # bumped = True and game will stop
                pygame.quit()
                quit()
            # defining the arrow keys
            if event.type == pygame.KEYDOWN:
                # if user is pressing the left arrow
                if event.key == pygame.K_LEFT:
                    # car will move to the left side
                    x_change = -1
                if event.key == pygame.K_RIGHT:
                    # car will move to the right side
                    x_change = 1
            # if any key is not being pressed then stop the car
            if event.type == pygame.KEYUP:
                x_change = 0
        x += x_change

        # Beschränkungen auf das Fahrzeug anwenden
        # setting the color of the road
        window.fill(display.Display().gray)
        # car speed that are coming from opposite side (y axis)
        display.background(window, backgroundLeft, backgroundRight)
        enemy_starty -= (enemy_car_speed / 1.2)
        car.enemy_car(window, enemy_startx, enemy_starty, enemy)
        # enemies car speed will increase slowly
        enemy_starty += enemy_car_speed
        car.car(window, x, y)
        # if the car goes out of range (sidewall of the road)
        if x < 130 or x > 700 - car_width:
            # crash
            display.Display().message_display(window, "crash")
            # call the loop function to restart the game
            loop()
        # Feindliche Autos werden zufällig kommen
        # setting how far the enemies car will go
        if enemy_starty > 600:
            # only one car will cross the road in one time
            enemy_starty = 0 - enemy_height
            # then other car will come
            enemy_startx = random.randrange(start_x1, (start_x2 - car_width))
            # set how many car will come
            enemy = random.randrange(0, 2)

        # if the enemies car doesn't cross the road then crash the car
        if y < enemy_starty + enemy_height:
            if enemy_startx < x < enemy_startx + enemy_width \
                    or enemy_startx < x + car_width < enemy_startx + enemy_width:
                # crash
                display.Display().message_display(window, "crash")
                # call the loop function to restart the game
                loop()

            # Quit-Code zum Beenden des Spiels
            # restart the game
            pygame.display.update()


loop()
pygame.quit()
quit()
