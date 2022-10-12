from abc import ABC, abstractmethod

class Wert(ABC):
    '''
        @class  Abstract interface class.
    '''
    def __init__(self):

        super().__init__()
        pass

    @abstractmethod
    def value(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class Konstante(Wert):
    '''
        @class  A constant.
    '''
    def __init__(self, value:float or int):

        super().__init__()
    
        self.v = value

    def value(self) -> float:
        '''
            @brief  Returns the evaluated constant expression.
        '''
        return self.v

    def description(self) -> str:
        '''
            @brief  Returns the stringified expression.
        '''
        return f"{self.v}"


class Datum(Wert):

    def __init__(self, name:str, value: float or int or Wert):
        
        super().__init__()
        
        self.n = name
        self.v = value

    def value(self) -> float:
        '''
            @brief  Evaluate the internal expression.
        '''
        return self.v

    def description(self) -> str:
        '''
            @brief  Return the expression.
        '''
        return f"{self.n}[{self.v}]"


class Addition(Wert):

    def __init__(self, left, right):
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> float:
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


class Subtraktion(Wert):

    def __init__(self, left, right):
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> float:
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


class Multiplikation(Wert):

    def __init__(self, left, right):
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> float:
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


class Division(Wert):

    def __init__(self, left, right): 
        
        super().__init__()
        
        if isinstance(left, int) or isinstance(left, float):
            self.left = Konstante(left)
        else:
            self.left = left
        
        if isinstance(right, int) or isinstance(right, float):
            self.right = Konstante(right)
        else:
            self.right = right

        pass

    def value(self) -> float:
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
