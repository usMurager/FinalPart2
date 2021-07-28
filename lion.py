import pygame as pg
import random
import time
pg.init()

WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Hungry Lion')
FPS = pg.time.Clock()


RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

font = pg.font.Font('font.ttf', 30)
speed = 5
score = 0

px, py = 100, 100
class Player(pg.sprite.Sprite):
    def move(self):
        global px, py, speed
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and px > 0: px -= speed
        elif keys[pg.K_RIGHT] and px < 590: px += speed
        elif keys[pg.K_UP] and py > 0: py -= speed
        elif keys[pg.K_DOWN] and py < 390: py += speed

    def draw(self):
        pg.draw.rect(screen, BLUE, (px, py, 10, 10))

enemy_points = []
for i in range(0, 510, 100):
    for _ in range(10):
        x, y = random.randint(i, i + 100), random.randint(0, HEIGHT)
        enemy_points.append([x, y])

class Enemy(pg.sprite.Sprite):
    def draw(self):
        for i in enemy_points:
            pg.draw.rect(screen, RED, (i[0], i[1], 15, 10))

    def move(self):
        global enemy_points
        for i in range(len(enemy_points)):
            enemy_points[i][1] += 1
    
    def spawn(self):
        global enemy_points
        for i in range(len(enemy_points)):
            if enemy_points[i][1] >= HEIGHT: enemy_points[i][1] -= HEIGHT


food_points = []
for i in range(10):
    food_points.append([random.randint(0, WIDTH / 2), random.randint(0, HEIGHT- 30)])
    food_points.append([random.randint(WIDTH / 2, WIDTH - 30), random.randint(0, HEIGHT - 30)])

vibr = {1 : 'L', 2 : 'R', 3 : 'U', 4 : 'D'}

class Food(pg.sprite.Sprite):
    def draw(self):
        for i in food_points:
            pg.draw.rect(screen, GREEN, (i[0], i[1], 15, 10))
    
    def move(self):
        global food_points, vibr
        for i in range(len(food_points)):
            x = random.randint(1, 4)
            if vibr[x] == 'L' and food_points[i][0] > 0: food_points[i][0] -= 1
            elif vibr[x] == 'R' and food_points[i][0] < 585: food_points[i][0] += 1
            elif vibr[x] == 'U' and food_points[i][1] > 0: food_points[i][1] -= 1
            elif vibr[x] == 'D' and food_points[i][1] < 390: food_points[i][1] += 1

def eating():
    global food_points, enemy_points, score
    i = 0
    while i < len(food_points):
        if food_points[i][0] - 10 < px < food_points[i][0] + 15 and food_points[i][1] - 10 < py < food_points[i][1] + 10:
            score += 1
            food_points.pop(i)
        else: i += 1

    i = 0
    while i < len(enemy_points):
        if enemy_points[i][0] - 10 < px < enemy_points[i][0] + 15 and enemy_points[i][1] - 10 < py < enemy_points[i][1] + 10:
            score -= 1
            enemy_points.pop(i)
        else: i += 1


player = Player()
enemy = Enemy()
food = Food()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    screen.fill(WHITE)

    if len(food_points) != 0:
        screen.blit(font.render(f'SCORE: {score}', 0, BLACK), (5, 5))

        player.draw()
        player.move()
        enemy.draw()
        enemy.move()
        enemy.spawn()
        food.draw()
        food.move()
        eating()
    else:
        font = pg.font.Font('font.ttf', 150)
        screen.blit(font.render('You finished', 0, BLACK), (70, 100))
        font = pg.font.Font('font.ttf', 90)
        screen.blit(font.render(f'your score: {score}', 0, BLACK), (150, 200))


    pg.display.update()
    FPS.tick(30)