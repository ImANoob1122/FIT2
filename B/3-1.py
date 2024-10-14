import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_INTERVAL = 20

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        for i in range(0, CANVAS_SIZE+1, LINE_INTERVAL):
            for j in range(0, CANVAS_SIZE+1, LINE_INTERVAL):
                pyxel.line(i, 0, j, CANVAS_SIZE, 0)
        pyxel.show()


Draw()