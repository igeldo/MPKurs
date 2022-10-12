import json
import operatoren as op

class Daten():
    input = {}
    output = {}

    def load(self, filename:str) -> None:
        f = open("data/input.json")
        self.input = json.load(f)["values"]
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
            values[key] = wert.value()
            description = wert.description()
            descriptions[key] = description
            print(f"    {key}: {description}")
        data = {"values": values, "desriptions": descriptions}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
