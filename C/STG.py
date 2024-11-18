# title: Pyxel STG
# author: Ryosuke Shimizu
# desc: A Pyxel Shooting game
# version: 0.1

# グローバル変数scoreに注意

import pyxel
import math

CANVAS_SIZE_WIDTH = 200
CANVAS_SIZE_HEIGHT = 280
FPS = 30
CANVAS_COLOR = 0
SCORE_BORD = 8
SCORE_COLOR = 7

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
BULLET_RADIUS = 2

ENEMY_WIDTH = 8
ENEMY_HIGHT = 8
ENEMY_SPEED = 1
ENEMY_RADIUS = 4


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
        self.hitpoint = 5
        self.power = {'power': 10, 'power_ratio': 1.0, 'cooltime': FPS//3, 'cooltime_ratio': 1.0, 'bullet_num_ratio': 1, 'bullet_speed_ratio': 1.0,
                      'base_damage': 2, 'damage_ratio': 1.0}
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
            self.bullets.append(Bullet(self.x-2, self.y- (self.h//2), 270+add, self.power))
            self.bullets.append(Bullet(self.x+2, self.y- (self.h//2), 270-add, self.power))
    
    def give_bullet(self):
        return self.bullets

    def draw(self):
        pyxel.blt(self.x - (self.w//2), self.y - (self.h//2), 0, 0, 0, self.w, self.h, 0)
        for bullet in self.bullets[:]:
            bullet.draw()
        

class Bullet:
    def __init__(self, x, y, angle, power = {}, enemy = False):
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.x = x
        self.y = y 
        self.vx, self.vy = pyxel.cos(angle), pyxel.sin(angle)
        self.power = power
        self.is_dead = False
        self.enemy = enemy

    def update(self):
        self.x += self.vx * BULLET_SPEED * self.power['bullet_speed_ratio']
        self.y += self.vy * BULLET_SPEED * self.power['bullet_speed_ratio']

        if self.y < 0 or self.y > pyxel.height:
            self.is_dead = True

    def draw(self):
        pyxel.blt(self.x - (self.w//2), self.y - (self.h//2), 0, 8 * self.enemy, 8, self.w, self.h, 0)

class Enemy:
    def __init__(self, x, y, power: dict):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HIGHT
        self.power = power
        self.time_enemystart = pyxel.frame_count
        self.bullets = []
        self.bulletangle = [90, 105, 75, 120]

    def update(self, vx = 0, vy = 0):
        self.x += vx * ENEMY_SPEED
        self.y += vy * ENEMY_SPEED
        if self.time_enemystart - pyxel.frame_count >= self.power['cooltime'] * self.power['cooltime_ratio']:
            self.time_enemystart = pyxel.frame_count
            for i in range(self.power['bullet_num']):
                self.bullets.append(Bullet(self.x, self.y+(self.h//2), self.bulletangle[i], self.power, True))

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_dead:
                self.bullets.remove[bullet]


    def draw(self):
        pyxel.blt(self.x - (self.w//2), self.y - (self.h//2), 0, 8, 0, self.w, self.h, 0)

class Wave:
    def __init__(self):
        self.wave_count = 1
        self.wave_timelimit = FPS*60
        self.enemy_power = {'power': 1, 'cooltime': FPS//3, 'cooltime_ratio': 1.0, 'bullet_num': 1, 'bullet_speed_ratio': 1.0,
                            'base_damage': 2, 'damage_ratio': 1.0}
        self.enemys = []
        self.createWave()

    def createWave(self):
        self.time_wavestart = pyxel.frame_count
        level = self.wave_count % 5
        self.mode = 0
        enemy = math.floor(math.log2(self.wave_count)) + 3 #敵の数を増やしすぎない
        match level:
            case 1:
                self.enemy_power.update({'bullet_num': 1})
                for _ in range(enemy):
                    x = pyxel.rndi(ENEMY_WIDTH, pyxel.width - ENEMY_WIDTH)
                    y = pyxel.rndi(-10 * enemy, 0)
                    self.enemys.append(Enemy(x, y, self.enemy_power))
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 0:
                pass

    def update(self):
        match self.mode:
            case 0:
                for enemy in self.enemys[:]:
                    enemy.update(vy=1)
        pass

    def draw(self):
        for enemy in self.enemys[:]:
            enemy.draw()
        pass


class App:
    def __init__(self):
        self.score = 0
        pyxel.init(CANVAS_SIZE_WIDTH, CANVAS_SIZE_HEIGHT, title="Pyxel STG", fps=FPS, display_scale=3)
        pyxel.load('STG.pyxres')
        self.background = Background()
        self.scene = SCENE_TITLE
        self.player_bullet = []
        self.enemy_bullet = []
        self.player = Player(CANVAS_SIZE_WIDTH//2, CANVAS_SIZE_HEIGHT//2)
        self.wave = Wave()
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
        self.wave.update()

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
        self.wave.draw()
        pyxel.text(SCORE_BORD, SCORE_BORD, "score: %d" % (self.score), SCORE_COLOR)
        pyxel.text(pyxel.width-30, SCORE_BORD, "wave: %d" % (self.wave.wave_count), SCORE_COLOR)


    
            

App()