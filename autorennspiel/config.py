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


def get_car_img_paths_or_size(car_type, pathorsize):
    """
    this function lists the img-paths and sizes of the cars getting them from the config.json file
    :param car_type: must be "car_player" or "car_enemy"
    :param pathorsize: must be "path" or "size
    :return: list of either the img-paths or the img-sizes
    """
    file = Json('config.json')
    if pathorsize == "path":
        general_path = file.get_attribute("images", "general_img_path")
    if car_type == "car_player":
        car_names = ["car_1", "car_1_crash", "car_1_wrecked"]
        paths_sizes = [None] * 3
        for index, cars in enumerate(car_names):
            if pathorsize == "size":
                paths_sizes[index] = file.get_attribute("images", "cars", cars, pathorsize)
            else:
                paths_sizes[index] = general_path + file.get_attribute("images", "cars", cars, pathorsize)
    if car_type == "car_enemy":
        car_num = 4
        paths_sizes = [None] * car_num
        num = 1
        while num <= car_num:
            if pathorsize == "size":
                paths_sizes[num-1] = file.get_attribute("images", "cars", ("car_" + str(num + 1)), pathorsize)
            else:
                paths_sizes[num-1] = general_path + \
                                     file.get_attribute("images", "cars", ("car_" + str(num+1)), pathorsize)
            num += 1
    return paths_sizes


# for testing
'''
my_file = Json('config.json')
# print(my_file.file_data)
print(my_file.get_attribute("images", "cars", "general", "size"))
filename = my_file.get_attribute("images", "general_img_path") + my_file.get_attribute("images", "cars", "car_1", "path")
print(filename)
# Json("config.json").get_attribute("images")
print(get_car_img_paths(3))

print(get_car_img_paths_or_size("car_player", "path"))
print(get_car_img_paths_or_size("car_player", "size"))
'''