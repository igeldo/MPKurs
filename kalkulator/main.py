import sys
from kalk import const, read, write, load, store

class Kalkulator:

    def run(self, InputFilename, OutputFilename):
        '''
            @brief  Run the calculator.
            @param[in] InputFilename    - Path to the input .json file.
            @param[in] OutputFilename   - Path to the outpu .json file.
            @post Overrides the output file if it exists.
        '''
        
        load(InputFilename)

        a = read("a")
        b = read("b")

        write("a", a)

        r = a + b
        write("a+b", r)

        c = const(5)
        r = a + b + c
        write("a+b+c", r)

        write("a-b", a - b)
        write("a*b", a * b)
        write("a div b", a / b)

        write("result", (a - b * c) / (a + b))

        for i in range(0, 11):
            write(f"{i}", const(i) * a)

        store(OutputFilename)


if __name__ == '__main__':
    '''
        It is required to call the program with exectaly 2 arguments!
        1. is the input file name
        2. is the output file name.
    '''
    kalkulator = Kalkulator()
    kalkulator.run(sys.argv[1], sys.argv[2])
