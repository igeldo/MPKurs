import os
import config
from datetime import date


class Highscore:
    def __init__(self):
        filepath = config.Json('config.json').get_attribute("highscore", "path")
        filename = config.Json('config.json').get_attribute("highscore", "name")
        self.file = filepath + filename

    def read_file(self):
        # check if the file exists, if not create it first
        if os.path.exists(self.file) is False:
            f = open(self.file, "w")
            f.close()
        # open existing file and store in highscores_all_users
        f = open(self.file, "r")
        highscores_all_users = f.read()
        f.close()
        return highscores_all_users

    def add_to_file(self, line):
        f = open(self.file, "a")
        f.write(line)
        f.close()

    def rewrite_file(self, new_content):
        f = open(self.file, "w")
        # with the method "w" the whole file is overwritten
        f.write(new_content)
        f.close()


def create_user(username):
    username_line = "\nusername: " + username + "\n"
    Highscore().add_to_file(username_line)


def add_score(username, score):
    string_to_add = str(date.today()) + "\t" + str(score) + "\n"
    # print(string_to_add)
    users_score = score_user(username)
    paragraph_user = users_score + string_to_add
    # print(paragraph_user)
    h = Highscore()
    whole_text = h.read_file()
    # replace the existing paragraph of the user with the new paragraph with one more score
    new_text = whole_text.replace(users_score, paragraph_user)
    # print(new_text)
    h.rewrite_file(new_text)
    # control if it added it successfully
    users_score_new = score_user(username)
    if users_score == users_score_new:  # user is last user in file and score couldn't be added
        h.add_to_file(string_to_add)


def find_user(username):
    h = Highscore()
    scores_all_users = h.read_file()
    found_user = False
    found_user_end = False
    user = None
    user_end = None
    for line_num, line in enumerate(scores_all_users.split("\n")):
        if username in line:
            # print(line.strip())   # username
            # print("found username in line:", line_num)
            user = line_num
            found_user = True
        elif found_user is True and found_user_end is False:
            if "username" in line:
                # print("found next user in line.", line_num)
                user_end = line_num - 1
                found_user_end = True
                break
    return scores_all_users, found_user, user, found_user_end, user_end


def score_user(username):
    users_score = ""
    scores_all_users, found_user, user, found_user_end, user_end = find_user(username)
    if found_user is False:
        # username must be created first, then try again
        print("crating new username...")
        create_user(username)
        scores_all_users, found_user, user, found_user_end, user_end = find_user(username)
    if found_user_end is False:
        # username is last input
        # print("user_end ist end of string")
        user_end = len(scores_all_users.split("\n"))
        # print(user_end)
    # return only the lines concerning the user
    n = user
    while n < user_end:
        users_score = users_score + scores_all_users.split("\n")[n] + "\n"
        n += 1
    # print(users_score)
    return users_score


def get_score(line):
    start = line.find("\t") + 1
    score = float(line[start:])
    # print(score)
    return score


def return_users_highscore(username):
    users_score = score_user(username)
    scores = []
    for line_num, line in enumerate(users_score.split("\n")):
        if line_num == 0:
            if username not in line:
                raise Exception("Username does not match")
        if line_num > 0 and line != "":
            scores.append(get_score(line))
    # print(scores)
    highscore = max(scores)
    for line_num, line in enumerate(users_score.split("\n")):
        if str(highscore) in line:
            highscore_line = line
    highscore_line = highscore_line.replace("\t", "   ")
    return highscore, highscore_line



'''
print(Highscore().read_file())

# score_user("maximilianbrinkhoff10101995")
# score_user("tessavogt19031998")
# score_user("christinebehrens08071966")
# score_user("carolinwulfers14111997")


print(return_users_highscore("tessavogt19031998"))
# return_users_highscore("christinebehrens08071966")
'''
add_score("christinebehrens08071966", 7.9374)
add_score("tessavogt19031998", 28.7829)
add_score("carolinwulfers14111997", 11.2905)