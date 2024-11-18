# title: Pyxel STG
# author: Ryosuke Shimizu
# desc: A Pyxel Shooting game
# version: 0.1

# グローバル変数scoreに注意

import pyxel

CANVAS_SIZE_WIDTH = 300
CANVAS_SIZE_HEIGHT = 400
CANVAS_COLOR = 0

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_SELECT = 3

NUM_STARS = 150
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
PLAYER_RADIUS = 3

BULLET_SPEED = 3
BULLET_ADD_RANGE = 10
BULLET_WIDTH = 4
BULLET_HEIGHT = 4


class Background: # サンプルコードからのコピペ
    def __init__(self):
        self.stars = []
        for i in range(NUM_STARS):
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2.5),
                )
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)

class Player:
    def __init__(self, x, y):
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.x = x + (self.w // 2)
        self.y = y + (self.h // 2)
        self.is_alive = True
        self.hitpoint = 100
        self.power = {'power': 10, 'power_ratio': 1.0, 'cooltime': 10, 'cooltime_ratio': 1.0, 'bullet_num_ratio': 1, 'bullet_speed_ratio': 1.0}
        self.bullets = []
        self.cooltime = 0

    def update(self):
        vec = [0.0, 0.0]
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            vec[0] -= 1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            vec[0] += 1
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            vec[1] -= 1
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            vec[1] += 1

        vec_size = pyxel.sqrt(pow(vec[0], 2) + pow(vec[1], 2)) #斜め移動の速度がsqrt(2)倍になってしまうので移動をベクトルとして単位ベクトルにする
        if vec_size != 0: # 0除算回避
            for i in range(2):
                vec[i] /= vec_size
        self.x += vec[0] * PLAYER_SPEED
        self.y += vec[1] * PLAYER_SPEED

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height)

        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)) and pyxel.frame_count - self.cooltime > self.power['cooltime'] * self.power['cooltime_ratio']: #射撃クールタイム
            self.cooltime = pyxel.frame_count
            self.shootbullet()
        
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_dead:
                self.bullets.remove(bullet)

    def shootbullet(self):
        for i in range(self.power['bullet_num_ratio']):
            add = BULLET_ADD_RANGE * i #弾が倍増されるたびにBULLET_ADD_RANGE度づつ外向きに打たれる
            self.bullets.append(Bullet(self.x-4, self.y- (self.h//2), 270+add, self.power))
            self.bullets.append(Bullet(self.x+1, self.y- (self.h//2), 270-add, self.power))
    
    def give_bullet(self):
        return self.bullets

    def draw(self):
        pyxel.blt(self.x - (self.w//2), self.y - (self.h//2), 0, 0, 0, self.w, self.h, 0)
        for bullet in self.bullets[:]:
            bullet.draw()
        

class Bullet:
    def __init__(self, x, y, angle, power = {}):
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.x = x + (self.w // 2)
        self.y = y + (self.h // 2)
        self.vx, self.vy = pyxel.cos(angle), pyxel.sin(angle)
        self.power = power
        self.is_dead = False

    def update(self):
        self.x += self.vx * BULLET_SPEED * self.power['bullet_speed_ratio']
        self.y += self.vy * BULLET_SPEED * self.power['bullet_speed_ratio']

        if self.y < 0 or self.y > pyxel.height:
            self.is_dead = True

    def draw(self):
        pyxel.blt(self.x - (self.w//2), self.y - (self.h//2), 0, 0, 8, self.w, self.h, 0)

class App:
    def __init__(self):
        global score # score変数のみグローバル化
        pyxel.init(CANVAS_SIZE_WIDTH, CANVAS_SIZE_HEIGHT, title="Pyxel STG", fps=30)
        pyxel.load('STG.pyxres')
        self.background = Background()
        self.scene = SCENE_TITLE
        self.player_bullet = []
        self.enemy_bullet = []
        self.player = Player(CANVAS_SIZE_WIDTH//2, CANVAS_SIZE_HEIGHT//2)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        self.background.update()
        if self.scene == SCENE_TITLE:
            self.update_scene_title()
        if self.scene == SCENE_PLAY:
            self.update_scene_play()


    def update_scene_title(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_scene_play(self):
        self.player.update()
        self.player_bullet = self.player.give_bullet()

    def draw(self):
        pyxel.cls(CANVAS_COLOR)

        self.background.draw()
        if self.scene == SCENE_TITLE:
            self.draw_scene_title()
        elif self.scene == SCENE_PLAY:
            self.draw_scene_play()

    def draw_scene_title(self):
        pyxel.text(CANVAS_SIZE_WIDTH // 2 - 25, CANVAS_SIZE_HEIGHT // 2 -14, "Pyxel Shooter", pyxel.frame_count % 16) #頑張って微調整する
        pyxel.text(CANVAS_SIZE_WIDTH // 2 - 30, CANVAS_SIZE_HEIGHT // 2 -46, "- PRESS ENTER -", 13)

    def draw_scene_play(self):
        self.player.draw()

    
            

App()