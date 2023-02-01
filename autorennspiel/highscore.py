import config


class Highscore:
    def __init__(self):
        filepath = config.Json('config.json').get_attribute("highscore", "path")
        filename = config.Json('config.json').get_attribute("highscore", "name")
        self.file = filepath + filename

    def read_file(self, username):
        f = open(self.file, "r")
        print(f.read())

