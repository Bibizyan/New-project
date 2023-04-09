from pygame import *
w = 700
h = 700
back = (225, 237, 246)
window = display.set_mode((w,h))
win = transform.scale(image.load('finall.png'), (w, h))
display.set_caption('лабиринт')
pic = transform.scale(image.load('backgr.jpg'), (w, h))
run = True
finish = False
lives = 9
x1 = 480
x2 = 630
bullets = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, width, height, x, y, speed_x, speed_y):
        super().__init__(picture, width, height, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_x < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.speed_y
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        elif self.speed_y > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
    def fire(self):
        bullet = Bullet("bullet.png", 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= x1:
            self.direction = 'right'
        if self.rect.x >= x2:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, picture, width, height, x, y, speed ):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= w:
            self.kill()
wall_1 = GameSprite('platform_h.png', 350, 60, 130, 280)
wall_2 = GameSprite('platform_v.png', 60, 550, 430, 150)
player = Player('gato1.png', 80, 80, 5, 400, 0, 0)
final = GameSprite('7303-hehe.png', 80, 80, 600, 600)
enemy = Enemy('enemy.png', 80, 80, 480, 400, 2)
barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)


monsters = sprite.Group()
monsters.add(enemy)

money_group = sprite.Group()
money_group.add(money_1)
money_group.add(money_2)
money_group.add(money_3)


font.init()
font1 = font.SysFont('Verdana' , 30)
text_score = font1.render('Счет: ' + str(money), True, (0,0,0))
while run:
    if finish != True:  
        text_score = font1.render('Счет: ' + str(money), True, (0,0,0))
        window.fill(back)
        #window.blit(pic, (0,0))
        barriers.draw(window)
        player.reset()
        final.reset()
        player.update()


        monsters.update()
        monsters.draw(window)


        bullets.update()
        bullets.draw(window)
        money_group.draw(window)
        window.blit(text_score, (40, 40))
        time.delay(50)
       
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0,0))


        if sprite.spritecollide(player, monsters, True):
            finish = True
            window.blit(lose, (0,0))

        if sprite.spritecollide(player, money_group, True):
            money += 1
        

        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(monsters, bullets, True, True) #вариант 1

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.speed_y = -10
            if e.key == K_d:
                player.speed_x = 10
            if e.key == K_s:
                player.speed_y = 10
            if e.key == K_a:
                player.speed_x = -10
            if e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.speed_y = 0
            if e.key == K_d:
                player.speed_x = 0
            if e.key == K_s:
                player.speed_y = 0
            if e.key == K_a:
                player.speed_x = 0
    display.update()

