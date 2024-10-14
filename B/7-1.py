import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = 0

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="event loop")
        self.a = 0
        self.way = 1
        pyxel.run(self.update, self.draw)
    def update(self):
        self.a += self.way
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.way = self.way * -1
    def draw(self):
        pyxel.cls(CANVAS_COLOR)
        pyxel.circ(self.a, self.a, CIRCLE_RADIUS, CIRCLE_COLOR)



Draw()