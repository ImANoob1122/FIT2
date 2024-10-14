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
        numRow = CANVAS_SIZE//(CIRCLE_RADIUS*2)
        for i in range(numRow*numRow):
            Row = i//numRow
            x = i%numRow
            culRow = Row * CIRCLE_RADIUS * 2 + CIRCLE_RADIUS
            culx = x * CIRCLE_RADIUS * 2 + CIRCLE_RADIUS
            color = (x+Row)//MAGIC
            pyxel.circ(culx, culRow, CIRCLE_RADIUS, CIRCLE_COLOR[color])
        pyxel.show()


Draw()