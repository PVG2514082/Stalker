import os

import pygame

import random

from pygame import mixer

mixer.init()
pygame.init()
WIDTH = 800
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Stalker")
GRAVITY = 4
TILE_SIZE = 40
intro = True

go_left = False
go_right = False
shoot = False

jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.5)


pulya_img = pygame.image.load('imges/icons/bullet.png').convert_alpha()
health_box_img = pygame.image.load('imges/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('imges/icons/ammo_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
}


RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Progex', 25)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



class SpriteGroup(pygame.sprite.Group):

    def __init_(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


def forFon():
    screen.fill((100, 100, 100))
    pygame.draw.line(screen, (255, 255, 255), (0, 300), (WIDTH, 300))


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


sprite_group = SpriteGroup()


class Player(Sprite):
    def __init__(self, pX, pY, k, skorost, typePlayer, faza, ammo):
        super().__init__(sprite_group)
        self.a = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eighth"]
        self.sprites = list()
        self.faza_now = 0
        self.action = 0
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.zdorovie = 100
        self.vel_y = 0
        self.max_zdorovie = self.zdorovie
        self.isJump = True
        self.jumpSpeed = -75
        self.go_right = False
        self.go_left = False

        faza_type = ['calm', 'running', 'jumping', 'death']
        for h in faza_type:
            temp_list = []
            kolvo = len(os.listdir('imges/' + typePlayer + '/' + h))
            for i in range(kolvo):
                img = pygame.image.load('imges/' + typePlayer + '/' + h + '/' + self.a[i] + '.png')
                img = pygame.transform.scale(img,
                                             (int(img.get_width() * k), int(img.get_height() * k)))
                temp_list.append(img)
            self.sprites.append(temp_list)

        self.image = self.sprites[self.action][self.faza_now]
        print(len(self.sprites))
        self.rect = self.image.get_rect()
        self.rect.center = (pX, pY)
        self.pos = (pX, pY)
        self.k = k
        self.jump = False
        self.vlevoVpravo = 1
        self.menyem = False
        self.upDateTime = pygame.time.get_ticks()
        self.skorost = skorost
        self.live = True
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

    def drawPlayer(self):
        if self.vlevoVpravo == 1:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, -1, False), self.rect)

    def updatePlayer(self):
        self.image = self.sprites[self.action][self.faza_now]

        if pygame.time.get_ticks() - self.upDateTime > 100:
            self.upDateTime = pygame.time.get_ticks()
            self.faza_now += 1

        if self.faza_now >= len(self.sprites[self.action]):
            if self.action == 3:
                self.faza_now = len(self.sprites[self.action]) - 1
            else:
                self.faza_now = 0

    def proverka(self, act):
        if self.action != act:
            self.action = act
            self.faza_now = 0
            self.upDateTime = pygame.time.get_ticks()

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            pulya = Pulya(self.rect.centerx + (0.75 * self.rect.size[0] * self.vlevoVpravo), self.rect.centery,
                          self.vlevoVpravo)
            pulya_group.add(pulya)
            self.ammo -= 1
            shot_fx.play()

    def move(self):
        self.rect.y += GRAVITY
        if self.go_left:
            self.rect.x -= self.skorost
            self.menyem = True
            self.vlevoVpravo = -1
        if self.go_right:
            self.rect.x += self.skorost
            self.menyem = True
            self.vlevoVpravo = 1
        if self.jump and not self.isJump:
            self.rect.y += self.jumpSpeed
            self.jump = False
            self.isJump = True
        if self.rect.bottom > 300:
            self.rect.bottom = 300
            self.isJump = False

    def move_ai(self, go_left, go_right):
        dx = 0
        dy = 0

        if go_left:
            dx = -self.skorost
            self.menyem = True
            self.vlevoVpravo = -1
        if go_right:
            dx = self.skorost
            self.menyem = False
            self.vlevoVpravo = 1

        if self.jump == True and self.isJump == False:
            self.vel_y = -11
            self.jump = False
            self.isJump = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.isJump = False

        self.rect.x += dx
        self.rect.y += dy

    def ai(self):
        if self.live and stalker.live:
            if self.idling == False and random.randint(1, 200) == 1:
                self.proverka(0)
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(stalker.rect):
                self.proverka(0)
                self.shoot()
            else:
                if self.idling == False:
                    if self.vlevoVpravo == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move_ai(ai_moving_left, ai_moving_right)
                    self.proverka(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.vlevoVpravo, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.vlevoVpravo *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def check_alive(self):
        if self.zdorovie <= 0:
            self.zdorovie = 0
            self.skorost = 0
            self.live = False
            self.proverka(3)
    def update(self):
        self.updatePlayer()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self):
		if pygame.sprite.collide_rect(self, stalker):
			if self.item_type == 'Health':
				stalker.zdorovie += 5
				if stalker.zdorovie > stalker.max_zdorovie:
					stalker.zdorovie = stalker.max_zdorovie
			elif self.item_type == 'Ammo':
				stalker.ammo += 5
			self.kill()

class HealthBar():
	def __init__(self, x, y, zdorovie, max_zdorovie):
		self.x = x
		self.y = y
		self.zdorovie = zdorovie
		self.max_zdorovie = max_zdorovie

	def draw(self, zdorovie):
		self.zdorovie = zdorovie
		ratio = self.zdorovie / self.max_zdorovie
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Pulya(pygame.sprite.Sprite):
	def __init__(self, x, y, napravlenie):
		pygame.sprite.Sprite.__init__(self)
		self.skorost = 10
		self.image = pulya_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.napravlenie = napravlenie

	def update(self):
		self.rect.x += (self.napravlenie * self.skorost)
		if self.rect.right < 0 or self.rect.left > WIDTH:
			self.kill()

		if pygame.sprite.spritecollide(stalker, pulya_group, False):
			if stalker.alive:
				stalker.zdorovie -= 5
				self.kill()
		if pygame.sprite.spritecollide(enemy, pulya_group, False):
			if enemy.alive:
				enemy.zdorovie -= 100
				self.kill()

class ScreenFade():
	def __init__(self, napravlenie, colour, skorost):
		self.napravlenie = napravlenie
		self.colour = colour
		self.skorost = skorost
		self.fade_counter = 0


	def fade(self):
		fade_complete = False
		self.fade_counter += self.skorost
		if self.napravlenie == 1:
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, WIDTH // 2, HEIGHT))
			pygame.draw.rect(screen, self.colour, (WIDTH // 2 + self.fade_counter, 0, WIDTH, HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, WIDTH, HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, HEIGHT // 2 +self.fade_counter, WIDTH, HEIGHT))
		if self.napravlenie == 2:
			pygame.draw.rect(screen, self.colour, (0, 0, WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= WIDTH:
			fade_complete = True

		return fade_complete

intro_begin = ScreenFade(1, BLACK, 4)

enemy_group = pygame.sprite.Group()
pulya_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

item_box = ItemBox('Health', 200, 260)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400, 260)
item_box_group.add(item_box)


stalker = Player(50, 50, 2, 5, "stalker", 0, 20)
health_bar = HealthBar(10, 10, stalker.zdorovie, stalker.zdorovie)
enemy = Player(200, 200, 2, 5, "enemy", 0, 120)
enemy_group.add(enemy)
running = True
while running:

    health_bar.draw(stalker.zdorovie)
    draw_text('Припасы: ', font, WHITE, 10, 35)
    for x in range(stalker.ammo):
        screen.blit(pulya_img, (90 + (x * 10), 40))

    stalker.update()
    stalker.drawPlayer()

    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.drawPlayer()

    pulya_group.update()
    item_box_group.update()
    pulya_group.draw(screen)
    item_box_group.draw(screen)

    if intro == True:
        if intro_begin.fade():
            intro = False
            intro_begin.fade_counter = 0

    if stalker.live:
        if shoot:
            stalker.shoot()
        if stalker.isJump:
            stalker.proverka(2)
        elif stalker.go_left or stalker.go_right:
            stalker.proverka(1)
        else:
            stalker.proverka(0)
        stalker.move()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if stalker.live:
                if ev.key == pygame.K_a:
                    stalker.go_left = True
                if ev.key == pygame.K_d:
                    stalker.go_right = True
                if ev.key == pygame.K_ESCAPE:
                    running = False
                if ev.key == pygame.K_SPACE:
                    shoot = True
                if ev.key == pygame.K_w:
                    stalker.jump = True
                    jump_fx.play()

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_a:
                stalker.go_left = False
            if ev.key == pygame.K_d:
                stalker.go_right = False
            if ev.key == pygame.K_SPACE:
                shoot = False
    stalker.updatePlayer()
    pygame.display.update()

    clock.tick(FPS)
    forFon()

pygame.quit()