# imports
import pygame
import config


class Car:
    def __init__(self, name, player):
        self.car_name = name
        name_attributes = config.Json("config.json").get_attribute("images", name)
        self.car_size = name_attributes["size"]
        self.car_width = self.car_size[0]
        self.car_height = self.car_size[1]
        self.img_path = config.Json("config.json").get_attribute("images", "general_img_path")
        self.car_img = name_attributes["path"]
        player_attributes = config.Json("config.json").get_attribute("images", player)
        self.car_rotation = player_attributes["rotation"]
        self.car_position = player_attributes["position"]
        self.car_speed = player_attributes["speed"]
        # print(self.car_name, self.car_width, self.car_height, self.car_img, self.car_rotation, self.car_position,
        # self.car_speed)

    def load_car(self):
        car_img = pygame.image.load(self.img_path + self.car_img)
        car_img = pygame.transform.scale(car_img, self.car_size)
        car_img = pygame.transform.rotate(car_img, self.car_rotation)
        return car_img


# Kabinenposition einstellen
# create car function
def car(window, x, y):
    # set position of the car
    car_img = Car("car_1", "car_player").car_img
    # window.blit(car_img, (x, y))


# define car functions that are coming from the opposite side
def enemy_car(window, enemy_startx, enemy_starty, enemy):
    if enemy == 0:
        # for enemy car no. 2
        enemy_there = Car("car_2", "car_enemy").load_car()
    if enemy == 1:
        enemy_there = Car("car_2", "car_enemy").load_car()
    if enemy == 2:
        enemy_there = Car("car_1", "car_enemy").load_car()

    # display the enemies car
    window.blit(enemy_there, (enemy_startx, enemy_starty))
    return enemy_there


# for testing
"""
car_1 = Car("car_1", "car_player")
print(car_1.car_width)
"""

