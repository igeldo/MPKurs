# imports
import pygame
import config
import random


class Car:
    def __init__(self):
        self.json = config.Json("config.json")
        self.car_size_player = config.get_car_img_paths_or_size("car_player", "size")
        self.car_size_enemy = config.get_car_img_paths_or_size("car_enemy", "size")
        self.car_imgs_player = config.get_car_img_paths_or_size("car_player", "path")
        self.car_imgs_enemy = config.get_car_img_paths_or_size("car_enemy", "path")

    def car_info(self, enemyorplayer):
        player_attributes = self.json.get_attribute("images", "cars", enemyorplayer)
        rotation = player_attributes["rotation"]
        starting_position = player_attributes["position"]
        speed = player_attributes["speed"]
        if enemyorplayer == "car_player":
            size = self.car_size_player
            car_img = Car.load_car(self, "car_player", rotation, 0)
        else:
            size = self.car_size_enemy
            car_img = None
        return [rotation, starting_position, speed, size, car_img]

    def car_img_path_or_size(self, enemyorplayer, which_car, pathorsize):
        if enemyorplayer == "car_player":
            if pathorsize == "path":
                img_pathorsize = self.car_imgs_player[which_car]
            else:
                img_pathorsize = self.car_size_player[which_car]
        else:
            if pathorsize == "path":
                img_pathorsize = self.car_imgs_enemy[which_car]
            else:
                img_pathorsize = self.car_size_enemy[which_car]
        return img_pathorsize

    def load_car(self, enemyorplayer, rotation, which_car=None):
        img_path = Car.car_img_path_or_size(self, enemyorplayer, which_car, "path")
        car_img = pygame.image.load(img_path)
        img_size = Car.car_img_path_or_size(self, enemyorplayer, which_car, "size")
        car_img = pygame.transform.scale(car_img, img_size)
        car_img = pygame.transform.rotate(car_img, rotation)
        return car_img


# create car function
def disp_car(carclass, window, x, y, car_img, enemy=None):
    # set position of the car
    if enemy is not None:
        car_img = Car.load_car(carclass, "car_enemy", 180, enemy)
    window.blit(car_img, (x, y))
    return car_img


# define how the user input moves the players car
def players_movement(event):
    move_car_player = 0
    # defining the arrow keys
    if event.type == pygame.KEYDOWN:
        # if user is pressing the left arrow
        if event.key == pygame.K_LEFT:
            # car will move to the left side
            move_car_player = -3
        if event.key == pygame.K_RIGHT:
            # car will move to the right side
            move_car_player = 3
    # if any key is not being pressed then stop the car
    if event.type == pygame.KEYUP:
        move_car_player = 0
    return move_car_player


def move_enemies_car(enemies_pos, display_size, car_size, which_car, enemy_current_pos):
    x_range = enemies_pos[0]
    enemies_pos_x = enemy_current_pos[0]
    enemies_pos_y = enemy_current_pos[1]#
    car_size = car_size[which_car]
    if enemies_pos_y > (display_size[1] - car_size[1]):
        enemies_pos_y = 0 - car_size[1]
        # then other car will come
        enemies_pos_x = random.randrange(x_range[0], (x_range[1] - car_size[0]))
        # set which car will come
        which_car = random.randrange(2, 4)
    enemies_pos_y += 6
    enemies_new_pos = [enemies_pos_x, enemies_pos_y]
    return enemies_new_pos, which_car


# for testing
'''
Car()
'''

