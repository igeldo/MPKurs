# imports
import config
import pygame
import time


class Display:
    def __init__(self, name=None):
        display_attributes = config.Json("config.json").get_attribute("display")
        self.size = display_attributes["size"]
        self.window_name = display_attributes["window_name"]
        self.message_crash = display_attributes["message_crash"]
        font = display_attributes["font"]
        self.font_name = font["name"]
        self.font_size = font["size"]
        self.font_position = font["position"]

        # define colors in RGB form
        self.gray = (60, 60, 60)
        self.black = (255, 0, 0)

        # background
        if name is not None:
            self.img_path = config.Json("config.json").get_attribute("images", "general_img_path")
            background_attributes = config.Json("config.json").get_attribute("images", name)
            self.bg_path = background_attributes["path"]
            self.bg_size = background_attributes["size"]
            self.bg_rotation = background_attributes["rotation"]
            self.bg_position = background_attributes["position"]

    def load_background(self):
        background_1side = pygame.image.load(self.img_path + self.bg_path)
        background_1side = pygame.transform.scale(background_1side, self.size)
        background_1side = pygame.transform.rotate(background_1side, self.bg_rotation)
        return background_1side

    def message_display(self, window, text):
        if text == "crash":
            text = self.message_crash
        # set font size and style of the message
        large_text = pygame.font.Font(self.font_name, self.font_size)
        # set function to edit the message
        text_surface = large_text.render(text, True, self.black)
        text_rect = text_surface.get_rect()
        # set the position of the text on the screen
        text_rect.center = self.font_position
        # display the message
        window.blit(text_surface, text_rect)
        pygame.display.update()
        # after the car crashed wait 3s
        time.sleep(3)


def background(window, background_left, background_right):
    # defining the position of background image for left and right side in x axis and y axis
    window.blit(background_left, (0, 0))
    window.blit(background_right, (630, 0))





# for testing
"""
dis = Display()
print(dis.size)
print(Display().size)
"""

