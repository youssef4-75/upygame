


from typing import Any
from pygame import Color
from multipledispatch import dispatch





class uColor(Color):
    @dispatch(...)
    def __init__(self, R=255, G=255, B=255, A=255, *, p=1) -> None:
        super().__init__(R, G, B, A)
        # print(self.__init__.funcs.keys())     
        self.__p = p
  
    @dispatch(Color)
    def __init__(self, col: Color) -> None: 
        self.__init__(col.r, col.g, col.b, p=1)

    @dispatch(str)
    def __init__(self, color_value):
        c = getattr(uColor, color_value)()
        self.__init__(c)

    @property
    def R(self):
        return self.r
    
    @R.setter
    def R(self, value):
        self.r = uColor.delimiter(value)
        
    @property
    def G(self):
        return self.g
    
    @G.setter
    def G(self, value):
        self.g = uColor.delimiter(value)

    @property
    def B(self):
        return self.b
    
    @B.setter
    def B(self, value):
        self.b = uColor.delimiter(value)

    @property
    def A(self):
        return self.a
    
    @A.setter
    def A(self, value):
        self.a = uColor.delimiter(value)

    @property
    def p(self):
        return getattr(self, '_uColor__p', 1)
    
    @p.setter
    def p(self, value):
        if value > 1: value = 1
        elif value < 0: value = 0
        self.__p = value

    @staticmethod
    def delimiter(n):
        return int(min(max(0, n), 255))

    def __repr__(self) -> str:
        return f"Color({self.R}, {self.G}, {self.B}, p={self.p})"

    def __radd__(self, Col):
        Col = uColor(*Col)
        return self + Col

    def __add__(self, Col):
        if not isinstance(Col, uColor):
            return self.__radd__(Col)
        f = []; my_weight = self.p; oth_weight = Col.p
        t_weight = my_weight + oth_weight
        
        f += [((self.__get(my_weight, i) + 
                Col.__get(oth_weight, i))
                    / t_weight) 
                        ** (1/2)
            for i in range(4)
            ]
        return uColor(*map(round, f))
    
    def __rmul__(self, p):
        return uColor(R=self.R,G=self.G,B=self.B, A=self.A,p=self.p*p)

    def __sub__(self, other):
        return uColor(R=(self.R-other.R)%255,G=(self.G-other.G)%255
            ,B=(self.B-other.B)%255,p=(self.p-other.p))

    def __rotate(self):
        self.R,self.G,self.B = self.G,self.B,self.R
    
    def __call__(self) -> Any:
        return (self.R, self.G, self.B) 

    def rotate(self, p=0):
        self.__rotate()
        if p==1:self.__rotate()

    def get(self, n):
        if n==0:return self.R
        if n==1:return self.G
        if n==2:return self.B
        return self.A 
    
    def __get(self, h, i):
        return h*self.get(i)**2

    def color_ify(self, color = (255, 255, 255), p=None):
        if p is not None:l = p**(1/2)
        else:l = self.p**(1/2)
        a = [(1 - l) * c for c in color]
        self.R = a[0] + l*self.R;
        self.G = a[1] + l*self.G;
        self.B = a[2] + l*self.B;
        
    def opac_ify(self, *, p=0):
        if p is not None:l = p**(1/2)
        else:l = self.p**(1/2)
        self.A = l*self.A;
    
    @classmethod
    def opacity(cls, color, opacity: int):
        assert isinstance(color, uColor)
        return cls(color.R, color.G, color.B, int(255*opacity), p=color.p)
    
    @classmethod
    def black(cls, p = 1):return cls(0,0,0,p=p)

    @classmethod
    def white(cls, p = 1):return cls(255,255,255,p=p)

    @classmethod
    def red(cls, p = 1):return cls(255,0,0,p=p)

    @classmethod
    def green(cls, p = 1):return cls(0,255,0,p=p)

    @classmethod
    def blue(cls, p = 1):return cls(0,0,255,p=p)

    @classmethod
    def yellow(cls, p = 1):return cls(255,255,0,p=p)


if __name__ == "__main__":
    c = uColor('red')
    red0 = uColor(c)
    red1 = uColor(255, G=0, B=0)
    red2 = uColor(255, 0, B=0)
    red3 = uColor(255, 0, 0)
    # blue = uColor(0, G=0, B=255, p=1)
    # red.color_ify((0, 0, 0), 1/3)
    # red.R = 0
    print(c, red0, red1, red2, red3)