import pyxel
import random
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = (2,3,6,14)

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        numRow = CANVAS_SIZE//(2*CIRCLE_RADIUS)
        for i in range(CIRCLE_RADIUS, CANVAS_SIZE, CIRCLE_RADIUS*2):
            for j in range(CIRCLE_RADIUS, CANVAS_SIZE, CIRCLE_RADIUS*2):
                pyxel.circ(j, i, CIRCLE_RADIUS, random.randint(0,16))
        pyxel.show()


Draw()