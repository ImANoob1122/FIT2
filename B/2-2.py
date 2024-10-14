import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_INTERVAL = 10

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        for i in range(0, CANVAS_SIZE+1, LINE_INTERVAL):
            end_y = CANVAS_SIZE - i
            pyxel.line(i, 0, 0, end_y, 0)
        pyxel.show()

Draw()