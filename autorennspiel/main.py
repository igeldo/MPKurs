# author: Tessa Vogt
# date: 30.01.2023

# Import libraries
import pygame
import car
import display
import time


def loop(player_start_pos, player_pos, move_car_player, enemies_pos, which_car, enemies_new_pos, start_timer):
    # display the background in the window
    display.disp_background(window, bg_left, bg_left_pos, bg_right, bg_right_pos)
    # define the user's keyboard inputs and move and display the players car
    player_pos, move_car_player = user_input(move_car_player, player_pos, player_start_pos)
    # update the timer
    timer = time.time() - start_timer
    # check if the car is still on the road
    crash_barrier(player_pos, enemies_new_pos, which_car, timer)
    enemies_new_pos, which_car \
        = car.move_enemies_car(enemies_pos, display_size, size_enemy, which_car, enemies_new_pos)
    # display the enemies car
    car.disp_car(carclass, window, enemies_new_pos[0], enemies_new_pos[1], None, which_car)
    # check if the cars crashed into each other
    crash_cars(player_start_pos, player_pos, enemies_new_pos, which_car, timer)
    # update the display with the declared elements
    pygame.display.update()
    return player_pos, move_car_player, which_car, enemies_new_pos


def user_input(move_car_player, player_pos, player_start_pos):
    for event in pygame.event.get():
        # close the window and stop the loop if the window gets closed
        if event.type == pygame.QUIT:
            # quit the game
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                # restart the game
                start_game(player_start_pos)
            else:
                # arrows where pressed to move the players car
                move_car_player = car.players_movement(event)
    player_pos += move_car_player
    # display the players car
    car.disp_car(carclass, window, player_pos, pos_player[1], player_img)
    return player_pos, move_car_player


def crash_barrier(player_pos, enemies_new_pos, which_car, timer):
    # when car leaves the street and drives onto the grass and bike lane
    size_player = size[0]
    if player_pos < road_size[0] or player_pos > (road_size[1] - size_player[0]):
        # crash
        crash(timer, player_pos, enemies_new_pos, which_car)


def crash_cars(player_start_pos, player_pos, enemies_pos, which_car, timer):
    # as soon as both cars are on the same height they are able to crash
    player_pos_y = player_start_pos[1]
    player_pos_x = player_pos
    enemies_size = size_enemy[which_car]
    size_player = size[0]
    if (enemies_pos[1] + enemies_size[1]) >= player_pos_y:
        if (enemies_pos[0] + enemies_size[0]) >= player_pos_x and enemies_pos[0] <= (player_pos_x + size_player[0]):
            # crash
            crash(timer, player_pos, enemies_pos, which_car)


def crash(timer, player_pos, enemies_new_pos, which_car):
    timer = round(timer, 4)
    # print("Score:", timer)
    crash_animation(player_pos, enemies_new_pos, which_car)
    display.Display("message").message_display(window, ["crash", "score"], timer)
    # wait for the player to start a new game, else close the window
    seconds_start = time.time()
    seconds = 0
    shutofftime = 60
    while seconds < shutofftime:
        player_pos, move_car_player = user_input(0, 0, pos_player)
        seconds_end = time.time()
        seconds = seconds_end - seconds_start
    # quit the game
    print("shut down the game due to no user input for longer than 1 minute")
    pygame.quit()
    quit()


def crash_animation(player_pos, enemies_new_pos, which_car):
    i = 1
    while i < 3:
        display.disp_background(window, bg_left, bg_left_pos, bg_right, bg_right_pos)
        car.disp_car(carclass, window, enemies_new_pos[0], enemies_new_pos[1], None, which_car)
        crash_img = carclass.load_car("car_player", 20, i)
        if i == 1:
            shift = [57, 87]
        else:
            shift = [5, 10]
        car.disp_car(carclass, window, (player_pos - shift[0]), (pos_player[1] - shift[1]), crash_img)
        pygame.display.update()
        # time.sleep(0.25)
        i += 1


def start_game(car_pos):
    # begin loop
    player_start_pos = car_pos
    car_pos_x = car_pos[0]
    move_player = 0
    move_enemy = [400, 0]
    which_car = 2
    start_timer = time.time()
    while True:
        try:
            car_pos_x, move_player, which_car, move_enemy\
                = loop(player_start_pos, car_pos_x, move_player, pos_enemy, which_car, move_enemy, start_timer)
        except AttributeError:
            print("oops, found an error")
            break


# Run this as the main module
if __name__ == '__main__':
    pygame.init()
    # load the background images
    [window, [bg_left, bg_left_pos, bg_left_size], [bg_right, bg_right_pos, bg_right_size]] \
        = display.load_background_window()
    # road starts with the end of the left_background until the right_background starts
    display_size = display.Display("display").return_display_size()
    road_size = [bg_left_size[0], bg_right_pos[0]]
    # load players car
    carclass = car.Car()
    [rotation, pos_player, speed, size, player_img] = carclass.car_info("car_player")  # [x,y]=players car starting pos
    [rotation_enemy, pos_enemy, speed_enemy, size_enemy, no_img] = carclass.car_info("car_enemy")
    start_game(pos_player)


