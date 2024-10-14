import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = (2,3,6,14)
MAGIC = 5 #マジックナンバー

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE)
        pyxel.cls(CANVAS_COLOR)
        row, num  = 0, 0
        for i in range(CIRCLE_RADIUS, CANVAS_SIZE, CIRCLE_RADIUS*2):
            for j in range(CIRCLE_RADIUS, CANVAS_SIZE, CIRCLE_RADIUS*2):
                color = (row+num) // MAGIC
                pyxel.circ(i, j, CIRCLE_RADIUS, CIRCLE_COLOR[color])
                num += 1
            num = 0
            row += 1
        pyxel.show()


Draw()