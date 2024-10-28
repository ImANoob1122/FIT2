import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = 6
PAD_LENGTH = 40
HALF_PAD = PAD_LENGTH//2
PAD_Y = 195
PAD_HIGHT = 5
PAD_COLOR = 14
SCORE_BORD = 10
SCORE_COLOR = 0

class Draw:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="event loop")
        pyxel.cls(CANVAS_COLOR)
        self.score = 0
        self.circleX, self.circleY = 100, 0
        self.speed = 3
        self.vx, self.vy = 0.866, 0.5 #cos and sin of 30dgree
        pyxel.run(self.update, self.draw)
    def reset(self):
        self.circleX, self.circleY = 100, 0
        self.speed += 0.2
    def update(self):
        self.circleX += self.vx * self.speed
        self.circleY += self.vy * self.speed
        self.padX = pyxel.mouse_x-HALF_PAD
        if self.circleX < 0 or self.circleX > CANVAS_SIZE:
            self.vx = self.vx * -1
        if self.circleY > PAD_Y:
            if self.padX < self.circleX and self.circleX < self.padX + PAD_LENGTH:
                self.score += 1
                self.reset()
            if self.circleY > CANVAS_SIZE:
                self.reset()

    def draw(self):
        pyxel.cls(CANVAS_COLOR)
        pyxel.circ(self.circleX, self.circleY, CIRCLE_RADIUS, CIRCLE_COLOR)
        pyxel.rect(self.padX, PAD_Y, PAD_LENGTH, PAD_HIGHT, PAD_COLOR)
        pyxel.text(SCORE_BORD, SCORE_BORD, "score: %d" % (self.score), SCORE_COLOR)




Draw()