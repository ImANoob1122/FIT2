import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = (6,14)

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        numRow = CANVAS_SIZE//(2*CIRCLE_RADIUS)
        for i in range(numRow*numRow):
            Row = (i//numRow) * CIRCLE_RADIUS * 2 + CIRCLE_RADIUS
            x = (i%numRow) * CIRCLE_RADIUS * 2 + CIRCLE_RADIUS
            pyxel.circ(x, Row, CIRCLE_RADIUS, CIRCLE_COLOR[(i//numRow)%2^(i%numRow)%2])
        pyxel.show()


Draw()