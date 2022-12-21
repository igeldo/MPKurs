# imports
import pygame
import config
import random


class Car:
    def __init__(self):
        self.json = config.Json("config.json")
        self.car_size = self.json.get_attribute("images", "cars", "general", "size")
        self.car_width = self.car_size[0]
        self.car_height = self.car_size[1]
        self.car_imgs = config.get_car_img_paths(4)
        # print(self.car_size, self.car_width, self.car_height, self.car_imgs)

    def player_car_info(self, enemyorplayer):
        player_attributes = self.json.get_attribute("images", "cars", enemyorplayer)
        rotation = player_attributes["rotation"]
        position = player_attributes["position"]
        speed = player_attributes["speed"]
        return [rotation, position, speed]

    def car_info_for_loading(self, enemyorplayer, which_car=None):
        if which_car is None:
            if enemyorplayer == "car_player":
                which_car = 1
            else:
                which_car = random.randint(1, 4)
        img_path = self.car_imgs[which_car]
        [car_rotation, car_position, car_speed] = self.player_car_info(enemyorplayer)
        return[img_path, self.car_size, car_rotation]


def load_car(carclass, enemyorplayer, which_car=None):
    [img_path, car_size, car_rotation] = carclass.car_info_for_loading(enemyorplayer, which_car)
    car_img = pygame.image.load(img_path)
    car_img = pygame.transform.scale(car_img, car_size)
    car_img = pygame.transform.rotate(car_img, car_rotation)
    return car_img


# Kabinenposition einstellen
# create car function
def player_car(carclass, window, x, y):
    # set position of the car
    car_img = load_car(carclass, "car_player")
    window.blit(car_img, (x, y))


# define car functions that are coming from the opposite side
def enemy_car(carclass, window, enemy_startx, enemy_starty, enemy):
    enemy_there = load_car(carclass, "car_enemy", enemy)
    # display the enemies car
    window.blit(enemy_there, (enemy_startx, enemy_starty))
    return enemy_there


# for testing
'''
Car()
'''

