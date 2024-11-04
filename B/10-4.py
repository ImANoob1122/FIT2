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
BALL_NUM = 1
SPEED_INCREACE = 0.2
FPS = 30
COOLTIME = 0.5
SHOT_COLOR = 8

"""
変更点
当たり判定の変更    10-3まではボールの中心にしか当たり判定が存在していない。
                    そこで数学的計算方法でボールの接触を感知する。
ボールの撃ち落とす  ゲームの内容をボールを自分の弾で撃ち落とす形式に変更する
                    ボール発射のクールタイム
                    ボール同士の当たり判定
"""

class Ball:
    def __init__(self, speed, startX, startY, angle):
        self.circleX, self.circleY = startX, startY #ボールの初期位置
        self.speed = speed
        self.angle = angle
        self.vx, self.vy = pyxel.cos(self.angle), pyxel.sin(self.angle)
        self.Dead = False
    def update(self):
        self.circleX += self.vx * self.speed
        self.circleY += self.vy * self.speed
        if self.circleX < 0 or self.circleX > CANVAS_SIZE:
            pyxel.play(0, 0)
            self.vx = self.vx * -1
        if self.circleY > CANVAS_SIZE or self.circleY < 0                                                              :
            self.Dead = True

class game:
    def __init__(self):
        pyxel.init(CANVAS_SIZE, CANVAS_SIZE, title="ball game", fps=FPS)
        pyxel.cls(CANVAS_COLOR)
        self.score = 0
        self.speed = 2
        self.cooltime = 0
        self.miss, self.get = 0, 0
        pyxel.sounds[0].set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
        self.balls = []
        self.shoots = []
        self.createBall(BALL_NUM)
        self.gameOver = False
        pyxel.run(self.update, self.draw)

    def createBall(self, num = 1):
        for _ in range(num):
            self.balls.append(Ball(self.speed, CANVAS_SIZE//2, 0, pyxel.rndi(30, 150)))
    def shootBall(self):
        if pyxel.mouse_x < 0 or pyxel.mouse_x > CANVAS_SIZE or pyxel.frame_count - self.cooltime < FPS * COOLTIME:
            return
        self.shoots.append(Ball(3, pyxel.mouse_x, PAD_Y, 270))
        self.cooltime = pyxel.frame_count

    def update(self):
        if self.gameOver:
            return
        self.padX = pyxel.mouse_x-HALF_PAD
        for shot in self.shoots[:]:
            shot.update()
        for Ball in self.balls[:]:
            Ball.update()
            if Ball.Dead:
                self.balls.remove(Ball)
                self.createBall()
                self.miss += 1
                if self.miss >= 10:
                    self.gameOver = True
                continue
            for shot in self.shoots[:]:
                d = pyxel.sqrt( (Ball.circleX - shot.circleX) ** 2
                               +(Ball.circleY - shot.circleY) ** 2) #弾同士の距離
                if d < CIRCLE_RADIUS * 2:
                    self.get += 1
                    self.score += 1
                    self.speed += SPEED_INCREACE
                    self.balls.remove(Ball)
                    self.shoots.remove(shot)
                    if self.get >= 10:
                        self.get = 0
                        self.createBall()
                    self.createBall()
                    break
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shootBall()

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
        for shot in self.shoots[:]:
            pyxel.circ(shot.circleX, shot.circleY, CIRCLE_RADIUS, SHOT_COLOR)
        pyxel.text(SCORE_BORD, SCORE_BORD, "score: %d" % (self.score), SCORE_COLOR)

game()