import os

import pygame

pygame.init()
WIDTH = 700
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Stalker")
GRAVITY = 4


class SpriteGroup(pygame.sprite.Group):

    def __init_(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


def forFon():
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), (0, 300), (WIDTH, 300))


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


sprite_group = SpriteGroup()


class Player(Sprite):
    def __init__(self, pX, pY, k, skorost, typePlayer, faza, am):
        super().__init__(sprite_group)
        self.a = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eighth"]
        self.sprites = list()
        self.faza_now = 0
        self.action = 0
        self.isJump = True
        self.strelba = False
        self.noe_am = am
        self.am = am
        self.jumpSpeed = -75
        self.go_right = False
        self.go_left = False
        self.health = 5
        self.Maxhealth = 5
        self.kolvoPul = 0
        faza_type = ['calm', 'running', 'jumping', 'death']
        for h in faza_type:
            temp_list = []
            kolvo = len(os.listdir('imges/' + typePlayer + '/' + h))
            for i in range(kolvo):
                img = pygame.image.load('imges/' + typePlayer + '/' + h + '/' + self.a[i] + '.png').convert_alpha()
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

    def drawPlayer(self):
        if self.vlevoVpravo == 1:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, -1, False), self.rect)

    def update(self):
        self.updatePlayer()
        self.check_live()
        if self.kolvoPul > 0:
            self.kolvoPul -= 1

    def updatePlayer(self):
        self.image = self.sprites[self.action][self.faza_now]

        if pygame.time.get_ticks() - self.upDateTime > 100:
            self.faza_now += 1
            self.upDateTime = pygame.time.get_ticks()
        if self.faza_now >= len(self.sprites[self.action]):
            if self.action == 3:
                self.faza_now = len(self.sprites[self.action]) - 1
            else:

                self.faza_now = 0


    def check_live(self):
        if self.health < 0:
            self.live = False
            self.health = 0
            self.skorost = 0
            self.proverka(3)

    def proverka(self, act):
        if self.action != act:
            self.action = act
            self.faza_now = 0
            self.upDateTime = pygame.time.get_ticks()

    def strelb(self):
        if self.kolvoPul == 0 and self.noe_am > 0:
            self.kolvoPul = 20
            puly1 = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.vlevoVpravo),
                           self.rect.centery, self.vlevoVpravo)
            puly_group.add(puly1)
            self.noe_am -= 1

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


class Bullet(Sprite):
    def __init__(self, x, y, napravlenie):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('imges/icons/qbullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vlevovpavo = napravlenie

    def update(self):
        self.rect.x += (self.vlevovpavo * self.speed)
        if self.rect.right < 0 or self.rect.left > WIDTH - 100:
            self.kill()
        if pygame.sprite.spritecollide(stalker, puly_group, False):
            if stalker.live:
                stalker.health -= 1
                self.kill()
        if pygame.sprite.spritecollide(enemy, puly_group, False):
            if stalker.live:
                enemy.health -= 1
                self.kill()


puly_group = pygame.sprite.Group()

stalker = Player(50, 50, 4, 15, "stalker", 0, 20)
enemy = Player(150, 150, 4, 15, "stalker", 0, 20)
running = True

while running:
    print(stalker.strelba)
    enemy.drawPlayer()
    enemy.update()
    stalker.drawPlayer()
    puly_group.update()
    puly_group.draw(screen)
    if stalker.live:
        if stalker.strelba:
            stalker.strelb()
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
                if ev.key == pygame.K_w:
                    stalker.jump = True
                if ev.key == pygame.K_SPACE:
                    stalker.strelba = True
                    print(445)

                if ev.key == pygame.K_ESCAPE:
                    running = False

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_a:
                stalker.go_left = False
            if ev.key == pygame.K_d:
                stalker.go_right = False
            if ev.key == pygame.K_SPACE:
                stalker.strelba = False
    stalker.update()
    pygame.display.update()
    puly_group.update()
    puly_group.draw(screen)
    clock.tick(FPS)
    forFon()

pygame.quit()
