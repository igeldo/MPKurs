import json
import numpy as np
import operatoren as op

class Daten():
    input = {}
    output = {}

    def load(self, filename:str) -> None:

        #
        #   open file and auto-close it after leaving the local scope.
        #
        with open(filename) as f:
            self.input = json.load(f)["values"]

            #
            # convert int/float and list input to numpy arrays/vector
            #
            for key in self.input:
                if isinstance(self.input[key], int) or isinstance(self.input[key], float):
                    self.input[key] = np.array([self.input[key]])
                elif not isinstance(self.input[key], list):
                    raise TypeError("Error! Expected an integral datatype of list during import...")

        print(f"data loaded from '{filename}'")
        for key in self.input:
            print(f"    {key}: {self.input[key]}")

    def read(self, name:str) -> op.Wert:
        return op.Datum(name, self.input.get(name))

    def write(self, name:str, value: str or int or float) -> None:
        self.output[name] = value

    def store(self, filename:str) -> None:
        values = {}
        descriptions = {}
        print(f"data stored to '{filename}'")
        for key in self.output:
            wert = self.output[key]
            values[key] = list([float(a) for a in wert.value()]) # dev better conversion ndarray to list
            description = wert.description()
            descriptions[key] = description
            print(f"    {key}: {description}")
        data = {"values": values, "descriptions": descriptions}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
