import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_INTERVAL = 10

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="manyLine")
        pyxel.cls(CANVAS_COLOR)
        end_x_start = CANVAS_SIZE//2
        for i in range(0, end_x_start+1, LINE_INTERVAL):
            end_x = i+end_x_start
            pyxel.line(i, 0, end_x, CANVAS_SIZE, 0)
        pyxel.show()

Draw()
