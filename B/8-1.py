import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = 6

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="event loop")
        pyxel.cls(CANVAS_COLOR)
        self.circleX, self.circleY = 100, 0
        self.vx, self.vy = 0.866, 0.5 #cos and sin of 30dgree
        pyxel.run(self.update, self.draw)
    def update(self):
        self.circleX += self.vx
        self.circleY += self.vy
        if self.circleX < 0 or self.circleX > CANVAS_SIZE:
            self.vx = self.vx * -1
    def draw(self):
        pyxel.cls(CANVAS_COLOR)
        pyxel.circ(self.circleX, self.circleY, CIRCLE_RADIUS, CIRCLE_COLOR)





Draw()