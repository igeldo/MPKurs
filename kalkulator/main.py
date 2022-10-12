import kalk as k

class Kalkulator:

    def run(self):
        k.load("data/input.json")

        a = k.read("a")
        b = k.read("b")

        r = k.add(a, b)
        k.write("a+b", r)

        c = k.const(5)
        r = k.add(a, k.add(b, c))
        k.write("a+b+c", r)

        k.write("a-b", k.sub(a, b))
        k.write("a*b", k.mul(a, b))
        k.write("a/b", k.div(a, b))

        for i in range(0, 11):
            k.write(f"{i}*a", k.mul(k.const(i), a))

        k.store("data/output.json")

if __name__ == '__main__':
    aKalkulator = Kalkulator()
    aKalkulator.run()
