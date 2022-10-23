from abc import ABC, abstractmethod
import numpy as np

class Wert(ABC):
    '''
        @class  Abstract interface class.
    '''
    def __init__(self):

        super().__init__()
        pass
    
    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraktion(self, other)

    def __mul__(self, other):
        return Multiplikation(self, other)

    def __truediv__(self, other):
        return Division(self, other)

    @abstractmethod
    def value(self) -> np.ndarray:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def latex(self) -> str:
        pass

    def overset(self, remaining) -> str:
        if len(remaining) == 1:
            return str(remaining[0])
        return r"\overset{" + str(remaining[0]) + r"}{" + self.overset(remaining[1:]) + r"}"

    def latexVector(self, array) -> str:
        return r"\left[" + self.overset(array.tolist()) + r"\right]"


class Konstante(Wert):
    '''
        @class  A constant.
    '''
    def __init__(self, value):
        '''
            @brief  Construct a constant.
            @param[in] value    - "value" must have on of the types: int, float, list[int/float], np.ndarray
        '''
        if not isinstance(value, np.ndarray):
            try:
                if not isinstance(value, list):
                    value = np.array([value])
                else:
                    value = np.array(value)
            except:
                raise TypeError("the given argument is not of type numpy.array!")

        super().__init__()
    
        self.v = value

    def value(self) -> np.ndarray:
        '''
            @brief  Returns the evaluated constant expression.
        '''
        return self.v

    def description(self) -> str:
        '''
            @brief  Returns the stringified expression.
        '''
        return f"{self.v}"

    def latex(self) -> str:
        return self.latexVector(self.v)


class Datum(Wert):

    def __init__(self, name:str, value):
        '''
            @brief  Construct a variable.
            @param[in] value    - "value" must have on of the types: int, float, list[int/float], np.ndarray
        '''
        
        super().__init__()
        
        if not isinstance(value, np.ndarray):
            try:
                if not isinstance(value, list):
                    value = np.array([value])
                else:
                    value = np.array(value)
            except:
                raise TypeError("the given argument is not of type numpy.array!")
        
        self.n = name
        self.v = value

    def value(self) -> np.ndarray:
        '''
            @brief  Evaluate the internal expression.
        '''
        return self.v

    def description(self) -> str:
        '''
            @brief  Return the expression.
        '''
        return f"{self.n}{self.v}"

    def latex(self) -> str:
        return self.n + self.latexVector(self.v)


class Addition(Wert):

    def __init__(self, left, right):
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float) or isinstance(left, np.ndarray):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float) or isinstance(right, np.ndarray):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> np.ndarray:
        '''
            @brief  evaluate the given subexpressions.
            @return the sum of subexpressions.
        '''
        return self.left.value() + self.right.value()

    def description(self) -> float:
        '''
            @brief  Return the expression.
        '''
        return f"({self.value()} = {self.left.description()} + {self.right.description()})"

    def latex(self) -> str:
        return self.left.latex() + "+" + self.right.latex()


class Subtraktion(Wert):

    def __init__(self, left, right):
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float) or isinstance(left, np.ndarray):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float) or isinstance(right, np.ndarray):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> np.ndarray:
        '''
            @brief  evaluate the given subexpressions.
            @return the difference of subexpressions.
        '''
        return self.left.value() - self.right.value()

    def description(self) -> str:
        '''
            @brief  Return the expression.
        '''
        return f"({self.value()} = {self.left.description()} - {self.right.description()})"

    def latex(self) -> str:
        return self.left.latex() + "-" + self.right.latex()


class Multiplikation(Wert):

    def __init__(self, left, right):
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float) or isinstance(left, np.ndarray):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float) or isinstance(right, np.ndarray):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> np.ndarray:
        '''
            @brief  evaluate the given subexpressions.
            @return the product of subexpressions.
        '''
        return self.left.value() * self.right.value()

    def description(self) -> str:
        '''
            @brief  Return the expression.
        '''
        return f"({self.value()} = {self.left.description()} * {self.right.description()})"

    def latex(self) -> str:
        return self.left.latex() + " " + self.right.latex()


class Division(Wert):

    def __init__(self, left, right): 
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float) or isinstance(left, np.ndarray):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float) or isinstance(right, np.ndarray):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> np.ndarray:
        '''
            @brief  evaluate the given subexpressions.
            @return the quotient of subexpressions.
        '''
        return self.left.value() / self.right.value()

    def description(self) -> str:
        '''
            @brief  Return the expression.
        '''
        return f"({self.value()} = {self.left.description()} / {self.right.description()})"
    
    def latex(self) -> str:
        return r"\frac{" + self.left.latex() + r"}{" + self.right.latex() + r"}"
