import json


class Json:
    """
    reads a json-file and can return attributes of objects saved in the file
    """
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'r') as f:
            self.file_data = json.load(f)

    def get_attribute(self, category=None, category_1=None, category_2=None):
        if category is not None:
            attribute = self.file_data[category]
            if category_1 is not None:
                attribute = attribute[category_1]
                if category_2 is not None:
                    attribute = attribute[category_2]
            return attribute
        else:
            print("error! Please enter category")
            return None


# for testing
"""
my_file = Json('config.json')
print(my_file.file_data)
my_file.get_attribute("images", "car_1", "size")

Json("config.json").get_attribute("images")
"""