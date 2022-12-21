import json


class Json:
    """
    reads a json-file and can return attributes of objects saved in the file
    """
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'r') as f:
            self.file_data = json.load(f)

    def get_attribute(self, category=None, category_1=None, category_2=None, category_3=None):
        if category is not None:
            attribute = self.file_data[category]
            if category_1 is not None:
                attribute = attribute[category_1]
                if category_2 is not None:
                    attribute = attribute[category_2]
                    if category_3 is not None:
                        attribute = attribute[category_3]
            return attribute
        else:
            print("error! Please enter category")
            return None


def get_car_img_paths(car_num):
    file = Json('config.json')
    general_path = file.get_attribute("images", "general_img_path")
    paths = [None] * car_num
    num = 1
    while num <= car_num:
        img_path = file.get_attribute("images", "cars", ("car_" + str(num)), "path")
        paths[num-1] = general_path + img_path
        num += 1
    return paths


# for testing
'''
my_file = Json('config.json')
# print(my_file.file_data)
print(my_file.get_attribute("images", "cars", "general", "size"))
filename = my_file.get_attribute("images", "general_img_path") + my_file.get_attribute("images", "cars", "car_1", "path")
print(filename)
# Json("config.json").get_attribute("images")
print(get_car_img_paths(3))
'''