# imports
import config
import pygame
import time


class Display:
    def __init__(self, name, background=None):
        # define colors in RGB form
        # self.gray = (60, 60, 60)
        self.red = (255, 0, 0)
        self.black = (255, 255, 255)
        if name == "display" or "message":
            display_attributes = config.Json("config.json").get_attribute("display")
        if name == "display":
            self.size = display_attributes["size"]
            self.window_name = display_attributes["window_name"]
        elif name == "message":
            self.message_crash = display_attributes["message_crash"]
            font = display_attributes["font"]
            self.font_name = font["name"]
            self.font_size = font["size"]
            self.font_position = font["position"]
        elif name == "background" and background is not None:
            self.img_path = config.Json("config.json").get_attribute("images", "general_img_path")
            background_attributes = config.Json("config.json").get_attribute("images", background)
            self.bg_path = background_attributes["path"]
            self.bg_size = background_attributes["size"]
            self.bg_rotation = background_attributes["rotation"]
            self.bg_position = background_attributes["position"]
        else:
            raise ValueError('Class Display is missing parameters')

    def return_display_size(self):
        display_size = self.size
        # print(display_size)
        return display_size

    def load_window(self):
        # set width and height of the display
        window = pygame.display.set_mode(self.size)
        # set name of the game window
        pygame.display.set_caption(self.window_name)
        return window

    def load_background(self):
        background_1side = pygame.image.load(self.img_path + self.bg_path)
        background_1side = pygame.transform.scale(background_1side, self.bg_size)
        background_1side = pygame.transform.rotate(background_1side, self.bg_rotation)
        bg_position = self.bg_position
        bg_size = self.bg_size
        return [background_1side, bg_position, bg_size]

    def font(self, text, style):
        if style == "strong":
            # set font size and style of the message
            large_text = pygame.font.Font(self.font_name, self.font_size)
            # set function to edit the message
            text_surface = large_text.render(text, True, self.red)
            text_rect = text_surface.get_rect()
            # set the position of the text on the screen
            text_rect.center = self.font_position
        if style == "soft":
            # set font size and style of the message
            large_text = pygame.font.Font(self.font_name, self.font_size - 30)
            # set function to edit the message
            text_surface = large_text.render(text, True, self.black)
            text_rect = text_surface.get_rect()
            # set the position of the text on the screen
            [x, y] = self.font_position
            text_rect.center = [x, y + 100]
        return text_surface, text_rect

    def message_display(self, window, texts, score=None):
        for text in texts:
            if text == "crash":
                text = self.message_crash
                style = "strong"
                text_surface, text_rect = Display.font(self, text, style)
                # display the message
                window.blit(text_surface, text_rect)
            if text == "score":
                score = str(score)
                text = "Score: " + score
                style = "soft"
                text_surface, text_rect = Display.font(self, text, style)
                # display the message
                window.blit(text_surface, text_rect)
        pygame.display.update()
        # after the car crashed wait 3s
        time.sleep(3)


def load_background_window():
    window = Display("display").load_window()
    loaded_backgrounds = [None]*2  # empty list with 2 values
    backgrounds = ["background_left", "background_right"]
    for index, name in enumerate(backgrounds):
        loaded_backgrounds[index] = Display("background", name).load_background()
    return [window, loaded_backgrounds[0], loaded_backgrounds[1]]


def disp_background(window, background_left, bg_left_pos, background_right, bg_right_pos):
    # define the gray color of the street
    gray = (60, 60, 60)
    # fill in the gray color for the street
    window.fill(gray)
    # defining the position of background image for left and right side in x axis and y axis
    window.blit(background_left, bg_left_pos)
    window.blit(background_right, bg_right_pos)


# for testing
"""
dis = Display()
print(dis.size)
print(Display().size)
"""

