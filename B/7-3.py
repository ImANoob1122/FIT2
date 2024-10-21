import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_COLOR = 0

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="mouse line")
        pyxel.cls(CANVAS_COLOR)
        self.now = False
        pyxel.run(self.update, self.draw)
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.now = True
            self.startX, self.startY = pyxel.mouse_x, pyxel.mouse_y
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.now = False
    def draw(self):
        if self.now:
            pyxel.cls(CANVAS_COLOR)
            pyxel.line(self.startX, self.startY, pyxel.mouse_x, pyxel.mouse_y, LINE_COLOR)



Draw()