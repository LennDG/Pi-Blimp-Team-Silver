from math import sqrt
from Field import Field

figures = []
figures.append(("green", "circle"))
figures.append(("green", "rectangle"))
figures.append(("green", "heart"))
figures.append(("green", "star"))
figures.append(("blue", "circle"))



positions = []
positions.append((1.0,0))
positions.append((2.0,0))
positions.append((0.5,-1*sqrt(0.75)))
positions.append((1.5,-1*sqrt(0.75)))
positions.append((2.5,-1*sqrt(0.75)))

node = Field.define_structure(figures, positions)
i = 2
