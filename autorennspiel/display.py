# imports
import config
import pygame
import time


class Display:
    def __init__(self, name, background=None):
        # define colors in RGB form
        # self.gray = (60, 60, 60)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        if name == "display" or "message":
            display_attributes = config.Json("config.json").get_attribute("display")
            self.size = display_attributes["size"]
            self.window_name = display_attributes["window_name"]
            self.message_crash = display_attributes["message_crash"]
            font = display_attributes["font"]
            self.font_name = font["name"]
            self.font_size = font["size"]
            self.font_position = font["position"]
        if name == "background" and background is not None:
            self.img_path = config.Json("config.json").get_attribute("images", "general_img_path")
            background_attributes = config.Json("config.json").get_attribute("images", background)
            self.bg_path = background_attributes["path"]
            self.bg_size = background_attributes["size"]
            self.bg_rotation = background_attributes["rotation"]
            self.bg_position = background_attributes["position"]
        #else:
        #    raise ValueError('Class Display is missing parameters')

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
            font_size = self.font_size
            color = self.red
            font_position = self.font_position
        elif style == "soft":
            font_size = self.font_size - 30
            color = self.white
            font_position = self.font_position
            font_position[1] = font_position[1] + 100
        elif style == "highscore" or "last_scores":
            font_size = self.font_size - 60
            color = self.white
            font_position = self.font_position
            font_position[1] = font_position[1] + 30
            if style == "last_scores":
                font_position[1] = font_position[1]
        # set font size and style of the message
        large_text = pygame.font.Font(self.font_name, font_size)
        # set function to edit the message
        text_surface = large_text.render(text, True, color)
        text_rect = text_surface.get_rect()
        # set the position of the text on the screen
        text_rect.center = font_position
        return text_surface, text_rect

    def message_display(self, window, texts, score=None, highest_score=None, last_scores=None):
        for text in texts:
            if text == "crash":
                message = self.message_crash
                style = "strong"
                text_surface, text_rect = Display.font(self, message, style)
                # display the message
                window.blit(text_surface, text_rect)
            if text == "score" and score is not None:
                score = str(score)
                message = "Score: " + score
                style = "soft"
                text_surface, text_rect = Display.font(self, message, style)
                # display the message
                window.blit(text_surface, text_rect)
            if text == "highscore":
                if highest_score is None and score is not None:
                    highest_score = score
                message = "your personal highscore: " + str(highest_score[0])
                style = "highscore"
                text_surface, text_rect = Display.font(self, message, style)
                # display the message
                window.blit(text_surface, text_rect)
            if text == "last_scores" and last_scores is not None:
                for message in last_scores:
                    style = "last_scores"
                    text_surface, text_rect = Display.font(self, message, style)
                    # display the message
                    window.blit(text_surface, text_rect)
        pygame.display.update()
        # after the car crashed wait 3s
        time.sleep(3)

    def start_button(self, window, game_started):
        # render at position stated in arguments
        if game_started is False:
            color_rect = self.white
            color_text = self.red
        else:
            color_rect = self.red
            color_text = self.white
        text = "START"
        large_text = pygame.font.Font(self.font_name, self.font_size)
        text_surface = large_text.render(text, True, color_text)
        text_rect = text_surface.get_rect()
        text_rect.center = self.font_position
        # create rectangle
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(window, color_rect, text_rect)
        window.blit(text_surface, text_rect)
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
        if game_started is True:
            time.sleep(1)
        return text_rect


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

