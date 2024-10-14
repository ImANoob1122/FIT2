import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_COUNT = 11
LINE_INTERVAL = 10

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        for i in range(LINE_COUNT):
            start_x = i*LINE_INTERVAL
            end_x = i*LINE_INTERVAL + CANVAS_SIZE//2
            print(start_x, end_x)
            pyxel.line(start_x, 0, end_x, CANVAS_SIZE, 0)
        pyxel.show()

Draw()