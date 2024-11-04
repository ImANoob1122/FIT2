import pyxel
CANVAS_SIZE = 200
CANVAS_COLOR = 7
CIRCLE_RADIUS = 10
CIRCLE_COLOR = 6
PAD_LENGTH = 40
HALF_PAD = PAD_LENGTH//2
PAD_Y = 195
PAD_HIGHT = CANVAS_SIZE - PAD_Y
PAD_COLOR = 14
SCORE_BORD = 10
SCORE_COLOR = 0
BALL_NUM = 3
SPEED_INCREACE = 0.1

class Ball:
    def __init__(self, speed):
        self.circleX, self.circleY = 100, 0 #ボールの初期位置
        self.speed = speed
        self.angle = pyxel.rndi(30, 150)
        self.vx, self.vy = pyxel.cos(self.angle), pyxel.sin(self.angle)
        self.onPAD, self.Dead = False, False
    def update(self):
        self.circleX += self.vx * self.speed
        self.circleY += self.vy * self.speed
        if self.circleX < 0 or self.circleX > CANVAS_SIZE:
            pyxel.play(0, 0)
            self.vx = self.vx * -1
        if self.circleY > PAD_Y:
            self.onPAD = True
            if self.circleY > CANVAS_SIZE:
                self.Dead = True

class game:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="ball game")
        pyxel.cls(CANVAS_COLOR)
        self.score = 0
        self.speed = 1
        self.miss = 0
        pyxel.sounds[0].set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
        self.balls = []
        self.createBall(BALL_NUM)
        self.gameOver = False
        pyxel.run(self.update, self.draw)

    def createBall(self, num = 1):
        for _ in range(num):
            self.balls.append(Ball(self.speed))

    def update(self):
        if self.gameOver:
            return
        self.padX = pyxel.mouse_x-HALF_PAD
        for Ball in self.balls[:]:
            Ball.update()
            if Ball.Dead:
                self.balls.remove(Ball)
                self.createBall()
                self.miss += 1
                if self.miss >= 10:
                    self.gameOver = True
            elif Ball.onPAD and self.padX < Ball.circleX and Ball.circleX < self.padX + PAD_LENGTH:
                self.balls.remove(Ball)
                self.createBall()
                pyxel.play(0, 0)
                self.score += 1
                self.speed += SPEED_INCREACE

    def draw(self):
        if self.gameOver:
            pyxel.cls(0)
            pyxel.text(55, 41, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(SCORE_BORD, SCORE_BORD, "score: %d" % (self.score), 7)
            return
        pyxel.cls(CANVAS_COLOR)
        pyxel.rect(self.padX, PAD_Y, PAD_LENGTH, PAD_HIGHT, PAD_COLOR)
        for Ball in self.balls[:]:
            pyxel.circ(Ball.circleX, Ball.circleY, CIRCLE_RADIUS, CIRCLE_COLOR)
        pyxel.text(SCORE_BORD, SCORE_BORD, "score: %d" % (self.score), SCORE_COLOR)

game()