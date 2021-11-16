from random import random, randint

import pyxel

SCENE_TITLE = 0
SCENE_TUTORIAL = 1
SCENE_PLAY = 2
SCENE_GAMEOVER = 3

RAIN = 80
RAIN_COLOR_HIGH = 12
RAIN_COLOR_LOW = 3

with open('highscore.txt', 'r') as score:
    score = score.read()
high_score = int(score)
random_x = randint(0, 160)


class Rain:
    def __init__(self):
        self.rain_list = []
        for i in range(RAIN):
            self.rain_list.append(
                (random() * pyxel.width, random() * pyxel.height, random() * 1.0 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.rain_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.rain_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.rain_list:
            pyxel.pset(x, y, RAIN_COLOR_HIGH if speed > 1.5 else RAIN_COLOR_LOW)


class App:

    def __init__(self):
        pyxel.init(160, 120, caption="Pyxel game")

        pyxel.load('assets/pyxel_game.pyxres')

        self.rain = Rain()
        self.scene = SCENE_TITLE

        self.score = 0
        self.player_x = int(random() * random_x)
        self.player_y = -16
        self.player_jump = -8
        self.player_is_alive = True
        self.high_score = high_score

        self.sky = [(-10, 75), (40, 65), (90, 60)]
        self.sky1 = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, randint(8, 104), True) for i in range(4)]
        self.foods = [(i * 60, randint(5, 104), randint(0, 2), True) for i in range(4)]
        self.bomb = [(i * 40, randint(0, 90), randint(0, 1), True) for i in range(2)]

        pyxel.playm(1, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.rain.update()

        if self.scene == SCENE_TITLE:
            self.update_title_screen()
        elif self.scene == SCENE_TUTORIAL:
            self.update_tutorial_screen()
        elif self.scene == SCENE_PLAY:
            self.update_play_screen()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_screen(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_TUTORIAL

    def update_tutorial_screen(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.scene = SCENE_TITLE

    def update_play_screen(self):
        self.update_player()
        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)
        for i, v in enumerate(self.foods):
            self.foods[i] = self.update_foods(*v)
        for i, v in enumerate(self.bomb):
            self.bomb[i] = self.update_bomb(*v)

    def update_gameover_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.score = 0
        elif pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.scene = SCENE_TITLE
            self.score = 0

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player_x = max(self.player_x - 2, 0)

        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)

        self.player_y += self.player_jump
        self.player_jump = min(self.player_jump + 1, 8)

        if self.player_y > pyxel.height:
            if self.player_is_alive:
                self.player_is_alive = False
                pyxel.play(3, 5)
                self.scene = SCENE_GAMEOVER

            if self.player_y > 600:
                self.score = 0
                self.player_x = int(random() * random_x)
                self.player_y = -16
                self.player_jump = -8
                self.player_is_alive = True

    def update_floor(self, x, y, is_active):
        if is_active:
            if (
                    self.player_x + 16 >= x
                    and self.player_x <= x + 40
                    and self.player_y + 16 >= y
                    and self.player_y <= y + 8
                    and self.player_jump > 0
            ):
                is_active = False
                self.score += 20
                self.player_jump = -8
                pyxel.play(3, 3)
        else:
            y += 6

        x -= 4

        if x < -40:
            x += 240
            y = randint(8, 104)
            is_active = True

        return x, y, is_active

    def update_foods(self, x, y, kind, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.score += 100
            self.player_jump = min(self.player_jump, -8)
            pyxel.play(3, 4)

        x -= 2

        if x < -40:
            x += 240
            y = randint(0, 140)
            kind = randint(0, 3)
            is_active = True

        return x, y, kind, is_active

    def update_bomb(self, x, y, kind, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.score -= 80
            self.player_jump = min(self.player_jump, -8)
            pyxel.play(3, 4)

        x -= 2

        if x < -40:
            x += 240
            y = randint(0, 100)
            kind = randint(0, 2)
            is_active = True

        return x, y, kind, is_active

    def draw(self):
        pyxel.cls(0)

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_TUTORIAL:
            self.draw_tutorial_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        self.rain.draw()

        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)
        pyxel.text(68, 40, 'Welcome', pyxel.frame_count % 12)
        pyxel.text(62, 50, 'Pyxel game', pyxel.frame_count % 15)
        pyxel.text(12, 60, '==press space to read how to play==', 10)
        pyxel.text(30, 70, '===press enter to start====', 9)
        pyxel.text(40, 80, '===press q to quit====', 7)

    def draw_tutorial_scene(self):
        pyxel.cls(7)
        pyxel.rect(2, 2, 156, 116, 6)
        self.rain.draw()
        pyxel.text(49, 10, '--How to play--', pyxel.frame_count % 10)
        pyxel.text(20, 20, '** Button A -> going to left **', 1)
        pyxel.text(19, 30, '** Button D -> going to right **', 1)
        pyxel.text(38, 50, '--How to count score--', pyxel.frame_count % 10)
        pyxel.text(15, 60, '** Floor = 20 points **', 1)
        pyxel.text(15, 70, '** All Foods = 100 points **', 1)
        pyxel.text(15, 80, '** Bomb = -80 points **', 1)
        pyxel.text(15, 110, '==press backspace to return title==', pyxel.frame_count % 10)

    def draw_play_scene(self):
        pyxel.cls(9)
        self.rain.draw()

        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        #draw forest
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        #draw sky
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.sky:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        #draw sky
        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.sky1:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        #draw floor
        for x, y, is_active in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        #draw foods
        for x, y, kind, is_active in self.foods:
            if is_active:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

        #draw boom
        for x, y, kind, is_active in self.bomb:
            if is_active:
                pyxel.blt(x, y, 0, 96 + kind * 15, 0, 16, 16, 12)

        #draw character
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_jump > 0 else 0,
            0,
            16,
            16,
            12
        )

        h = "HIGH SCORE {:>4}".format(self.high_score)
        s = "SCORE {:>4}".format(self.score)
        pyxel.text(3, 4, h, 1)
        pyxel.text(2, 4, h, 7)
        pyxel.text(110, 4, s, 1)
        pyxel.text(109, 4, s, 7)

    def draw_gameover_scene(self):
        pyxel.cls(1)
        pyxel.rect(10, 30, 143, 57, 7)
        self.rain.draw()
        s = "SCORE {:>4}".format(self.score)
        if self.score > self.high_score:
            self.high_score = self.score
            with open('highscore.txt', 'w') as new_score:
                your_score = str(self.score)
                new_score.write(your_score)
        else:
            self.high_score = self.high_score
        pyxel.text(62, 40, 'GAME OVER', pyxel.frame_count % 15)
        pyxel.text(42, 50, f'You got {s}', pyxel.frame_count % 16)
        pyxel.text(20, 60, '===press enter to play again====', 10)
        pyxel.text(12, 70, '==press backspace to return title==', 8)
        pyxel.text(46, 80, '==press q to quit==', 9)


App()
