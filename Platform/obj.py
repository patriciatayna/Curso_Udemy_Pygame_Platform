import pygame

class Obj(pygame.sprite.Sprite):

    def __init__(self, image, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

class Hero(Obj):

    def __init__(self, image, x, y, *groups):
        super().__init__(image, x, y, *groups)

        self.vel = 4
        self.grav = 1

        self.right = False
        self.left = False
        self.jump = False

        self.ticks = 0
        self.img = 0

        self.collections = 0
        self.lives = 3

    def update(self, *args):
        self.gravity()
        self.movements()
        self.drop()

    def gravity(self):
        self.vel += self.grav
        self.rect[1] += self.vel

        if self.vel >= 10:
            self.vel = 10

    def collisions(self, group, kill, name):

        col = pygame.sprite.spritecollide(self, group, kill)

        if col and name == "platform":
            if self.rect[1] + 50 < col[0].rect.top:
                if self.rect.left + 40 <= col[0].rect.right:
                    if self.rect.right - 40 >= col[0].rect.left:
                        self.rect.bottom = col[0].rect.top

        if col and name == "crystal":
            self.collections += 1

        if col and name == "enemy":
            if self.rect.y + 90< col[0].rect.top:
                self.vel *= -1
                col[0].kill()
            else:
                self.vel *= -1
                self.rect[0] -= 25
                self.lives -= 1
                col[0].kill()

    def events(self, events):
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RIGHT:
                self.right = True
            elif events.key == pygame.K_LEFT:
                self.left = True
            elif events.key == pygame.K_UP:
                self.vel *= -1.5

        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_RIGHT:
                self.right = False
            elif events.key == pygame.K_LEFT:
                self.left = False

    def movements(self):
        if self.right:
            self.rect[0] += 8
            self.anim("walk", 4, 3)
            self.image = pygame.transform.flip(self.image, False, False)

        elif self.left:
            self.rect[0] -= 8
            self.anim("walk", 4, 3)
            self.image = pygame.transform.flip(self.image, True, False)

        else:
            self.anim("idle", 4, 3)

    def anim(self, name, ticks, limit):
        self.ticks += 1
        if self.ticks >= ticks:
            self.ticks = 0
            self.img += 1
        if self.img > limit:
            self.img = 0

        self.image = pygame.image.load("assets/" + name + str(self.img) + ".png")

    def drop(self):
        if self.lives > 0:
            if self.rect.y > 720:
                self.rect.x = 100
                self.rect.y = 250
                self.lives -= 1

class Enemy(Obj):

    def __init__(self, image, x, y, *groups):
        super().__init__(image, x, y, *groups)

        self.ticks = 0
        self.img = 0

    def update(self, *args):
        self.anim("enemy", 4, 3)

    def anim(self, name, ticks, limit):
        self.ticks += 1
        if self.ticks >= ticks:
            self.ticks = 0
            self.img += 1
        if self.img > limit:
            self.img = 0

        self.image = pygame.image.load("assets/" + name + str(self.img) + ".png")

