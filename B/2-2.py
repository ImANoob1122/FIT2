import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_COUNT = 21
LINE_INTERVAL = 10

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        for i in range(LINE_COUNT):
            start_x = i * LINE_INTERVAL
            end_y = CANVAS_SIZE - start_x
            print(start_x, end_y)
            pyxel.line(start_x, 0, 0, end_y, 0)
        pyxel.show()

Draw()