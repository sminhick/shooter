#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont('Arial', 36)
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 500:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)

chet = 0
lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50,600)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y <= 0:
            self.kill()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(50,620), -30, randint(1,2), 80,50)
    asteroids.add(asteroid)

bullets = sprite.Group()

player = Player('rocket.png', 20, 395, 5, 100, 100)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(50,620), -30, randint(1,3), 80,50)
    monsters.add(monster)

num_fire = 0
rel_time = False

life = 3
clock = time.Clock()
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
    
    if finish != True:
        window.blit(background, (0,0))
        player.reset()  
        player.update()
        monsters.draw(window)
        monsters.update()
        
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update() 
        if rel_time == True:
            time_t = timer()
            time_o = time_t - last_time
            if time_o >= 3:
                rel_time = False
                num_fire = 0
            else:
                text_time = font1.render('Wait, reload...', 1, (255, 255,255))
                window.blit(text_time, (255, 450))
        sprites_collide = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_collide:
            chet += 1
            monster = Enemy('ufo.png', randint(50,620), -30, randint(1,2), 80,50)
            monsters.add(monster)
        if chet >= 10:
            finish = True
            win_text = font1.render('Вы победили!', 1, (255, 247, 8))
            window.blit(win_text, (255, 255))

        sprites_collide = sprite.spritecollide(player, monsters, False)
        if sprites_collide or sprite.spritecollide(player, asteroids, False):
            life -= 1
        if life == 0 or lost >= 6:
            finish = True
            lose_text = font1.render('Вы проиграли!', 1, (255, 247, 8))
            window.blit(lose_text, (255, 255))
        life_text = font1.render('Жизни: ' + str(life), 1, (255, 255, 255)) 
        window.blit(life_text, (570, 10))
        text_chet = font1.render('Счет: ' + str(chet), 1, (255, 255, 255))
        text_lose = font1.render('Пропущено: '+ str(lost), 1, (255, 255, 255))
        window.blit(text_chet, (10, 10))
        window.blit(text_lose, (10, 40))
    
        

    display.update()
    clock.tick(60)


