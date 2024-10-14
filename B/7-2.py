import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
LINE_COLOR = 0

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="mouse line")
        pyxel.cls(CANVAS_COLOR)
        pyxel.run(self.update, self.draw)
    def update(self):
        pass
    def draw(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.cls(CANVAS_COLOR)
            pyxel.line(0, 0, pyxel.mouse_x, pyxel.mouse_y, LINE_COLOR)



Draw()