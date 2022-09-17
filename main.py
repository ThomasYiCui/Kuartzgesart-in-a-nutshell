# setup
import pygame, math, random

pygame.init()
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
mouseX, mouseY = pygame.mouse.get_pos()
saveCode = [False]
clicked = False
planets = []
enemys = []
pMouseX = mouseX
pMouseY = mouseY
oil = 1000
energy = 2000
metal = 1000
water = 1000
food = 1000
tut = 0
tutX = 315
tutY = 200
scene = "menu"
xtab = 0
windM = 1
sunM = 1
waterM = 1
font = pygame.font.Font('freesansbold.ttf', 16)
font2 = pygame.font.Font('freesansbold.ttf', 64)
font3 = pygame.font.Font('freesansbold.ttf', 14)
ships = []
projectiles = []
stars = []
for i in range(30):
    stars.append([random.randint(0, 800), random.randint(0, 600), random.randint(2, 10)])
selectedShip = "n"
selectedPlanet = 0
enemyPlanetOwned = 1
playerPlanetOwned = 1
shop = False
matsTxt = font.render('Oil: ' + str(round(oil)) + " || Energy: " + str(round(energy)) + " || Metal: " + str(round(metal)) + " || Water: " + str(round(water)) + " || Food: " + str(round(food)), True, (255, 255, 255))
menuTxt = font2.render("Space Game", True, (255, 255, 255))
gameOverTxt = font2.render("Game Over", True, (255, 255, 255))
playTxt = font.render("Play", True, (255, 255, 255))
shopTxt = font.render("Shop", True, (255, 255, 255))
settingsTxt = font.render("Settings", True, (255, 255, 255))
backTxt = font.render("Back", True, (255, 255, 255))
tutTxt = font3.render("Welcome to space war!", True, (255, 255, 255))
cam = {
    "x": 0,
    "y": 0,
}

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)
def lerp(x, y, t):
    return x + (y - x) * t
# projectile class
class projectile():
    def __init__(self, x, y, type, r, team):
        self.x = x
        self.y = y
        self.type = type
        self.r = r
        if self.type == "basic laser":
            self.dmg = 10
            self.spd = 10
            self.s = 5
            self.range = 100
        elif self.type == "tank bullet":
            self.dmg = 30
            self.spd = 5
            self.s = 15
            self.range = 150
        self.team = team

    def draw(self):
        pygame.draw.ellipse(screen, (224, 231, 34), (self.x + cam["x"], self.y + cam["y"], self.s, self.s))

    def update(self):
        self.x += math.cos(self.r) * self.spd
        self.y += math.sin(self.r) * self.spd
        self.range -= 1

    def collide(self, t):
        if math.dist([self.x + self.s / 2, self.y + self.s / 2], [t.x + t.s / 2, t.y + t.s / 2]) < self.s * 4 + t.s * 4 and self.team != t.team:
            if t.type == "jester":
                t.x-=clamp((self.x - t.x)/5, -2, 2) - 0.1
                t.y-=clamp((self.y - t.y)/5, -2, 2) - 0.1
            if math.dist([self.x + self.s / 2, self.y + self.s / 2], [t.x + t.s / 2, t.y + t.s / 2]) < self.s + t.s:
                t.hp -= self.dmg
                self.range = 0


# enemy class
class enemy():
    def __init__(self, x, y, type, team):
        self.x = x
        self.y = y
        self.tX = x
        self.tY = y
        self.r = 0
        self.type = type
        self.doCool = random.randint(0, 2000)
        self.pClosest = 1000000
        self.a = 0
        if type == "miner":
            self.maxHp = 100
            self.s = 10
            self.spd = 1
            self.atkCool = -1
            self.rld = self.atkCool
            self.range = -100
        elif type == "soldier":
            self.maxHp = 100
            self.hp = self.maxHp
            self.s = 10
            self.spd = 1.5
            self.atkCool = 100
            self.rld = self.atkCool
            self.range = 100
        elif type == "tank":
            self.maxHp = 300
            self.s = 30
            self.spd = 1.5
            self.atkCool = 200
            self.rld = self.atkCool
            self.range = 300
            self.turnSpd = 0.03
            self.b = "tank bullet"
        elif type == "jester":
            self.maxHp = 70
            self.s = 10
            self.spd = 3
            self.atkCool = 90
            self.rld = self.atkCool
            self.range = 80
            self.turnSpd = 0.03
            self.b = "basic laser"
        self.ttX = self.x
        self.ttY = self.y
        self.d = 2
        self.closest = self.range
        self.hp = self.maxHp
        self.team = team

    def draw(self):
        if self.type == "miner":
            pygame.draw.ellipse(screen, (50, 50, 50), (self.x + cam["x"], self.y + cam["y"], self.s, self.s))
        elif self.type == "soldier":
            pygame.draw.polygon(screen, (50, 50, 50), [
                (3 + self.x + cam["x"] + math.cos(self.r + math.pi) * (self.s/2 + 5), 3 + self.y + cam["y"] + math.sin(self.r + math.pi) * (self.s/2 + 10)),
                (3 + self.x + cam["x"] + math.cos(self.r - 1) * (self.s + 2.5), 3 + self.y + cam["y"] + math.sin(self.r - 0.8) * (self.s + 2.5)),
                (3 + self.x + cam["x"] + math.cos(self.r + 1) * (self.s + 2.5), 3 + self.y + cam["y"] + math.sin(self.r + 0.8) * (self.s + 2.5))])
        pygame.draw.rect(screen, (200, 0, 0), (self.x + cam["x"] - self.s / 2, self.y + self.s + 5 + cam["y"], self.s * 2, 5))
        pygame.draw.rect(screen, (0, 200, 0), (self.x + cam["x"] - self.s / 2, self.y + self.s + 5 + cam["y"], (self.s * 2 / self.maxHp) * self.hp, 5))
        pygame.draw.rect(screen, (200, 0, 0), (self.x + cam["x"] - self.s / 2, self.y + self.s + 5 + cam["y"], self.s * 2, 5))
        pygame.draw.rect(screen, (0, 200, 0), (self.x + cam["x"] - self.s / 2, self.y + self.s + 5 + cam["y"], (self.s * 2 / self.maxHp) * self.hp, 5))

    def update(self):
        #self.r = math.atan2(self.y - self.tY, self.x - self.tX)
        self.r = math.atan2(self.y - self.tY, self.x - self.tX)
        if self.spd > self.a:
            self.a += 0.1
        if math.dist([self.x, self.y], [self.tX, self.tY]) < 20 and self.type == "miner":
            self.a -= 0.12
            if self.a < 0:
                self.a = 0
        self.x -= math.cos(self.r) * self.a
        self.y -= math.sin(self.r) * self.a
        self.d-=1
        self.atkCool -= 1
        self.doCool -= 1
        if self.doCool <= 0:
            self.doCool = random.randint(50, 200)
        self.pClosest = 100000
        if self.atkCool == 0:
            projectiles.append(projectile(self.x, self.y, "basic laser", self.r + math.pi, self.team))
            self.atkCool = self.rld
        self.closest = self.range

    def collide(self, t):
        if math.dist([self.x + self.s/2, self.y + self.s/2], [t.x + t.s/2, t.y + t.s/2]) < self.closest:
            self.closest = math.dist([self.x + self.s/2, self.y + self.s/2], [t.x + t.s/2, t.y + t.s/2])
            self.tX = t.x
            self.tY = t.y
        if math.dist([self.x + self.s/2, self.y + self.s/2], [t.x + t.s/2, t.y + t.s/2]) < t.closest:
            t.closest = math.dist([self.x + self.s/2, self.y + self.s/2], [t.x + t.s/2, t.y + t.s/2])
            t.tX = self.x
            t.tY = self.y


# ship class
class ship():
    def __init__(self, x, y, type, team):
        self.x = x
        self.y = y
        self.tX = x
        self.tY = y
        self.r = 0
        self.type = type
        self.a = 0
        self.atkR = 0
        if type == "miner":
            self.maxHp = 100
            self.s = 10
            self.spd = 1
            self.atkCool = -1
            self.rld = self.atkCool
            self.range = -10
            self.turnSpd = 0.05
        elif type == "soldier":
            self.maxHp = 100
            self.s = 10
            self.spd = 1.5
            self.atkCool = 100
            self.rld = self.atkCool
            self.range = 300
            self.turnSpd = 0.05
            self.b = "basic laser"
            self.h = "fire"
        elif type == "tank":
            self.maxHp = 300
            self.s = 30
            self.spd = 1.5
            self.atkCool = 200
            self.rld = self.atkCool
            self.range = 300
            self.turnSpd = 0.03
            self.b = "tank bullet"
            self.h = "fire"
        elif type == "jester":
            self.maxHp = 70
            self.s = 10
            self.spd = 3
            self.atkCool = 90
            self.rld = self.atkCool
            self.range = 80
            self.turnSpd = 0.03
            self.b = "basic laser"
            self.h = "fire"
        elif type == "spacecarrier":
            self.maxHp = 70
            self.s = 10
            self.spd = 3
            self.atkCool = 90
            self.rld = self.atkCool
            self.range = 80
            self.turnSpd = 0.03
            self.b = "basic laser"
            self.h = "summoner"
        self.closest = self.range
        self.hp = self.maxHp
        self.team = team

    def draw(self):
        if self.type == "miner":
            pygame.draw.ellipse(screen, (50, 50, 50), (self.x + cam["x"], self.y + cam["y"], self.s, self.s))
        elif self.type == "soldier" or self.type == "tank" or self.type == "jester":
            pygame.draw.polygon(screen, (50, 50, 50), [
                (3 + self.x + cam["x"] + math.cos(self.r + math.pi) * (self.s/2 + 5), 3 + self.y + cam["y"] + math.sin(self.r + math.pi) * (self.s/2 + 10)),
                (3 + self.x + cam["x"] + math.cos(self.r - 1) * (self.s + 2.5), 3 + self.y + cam["y"] + math.sin(self.r - 0.8) * (self.s + 2.5)),
                (3 + self.x + cam["x"] + math.cos(self.r + 1) * (self.s + 2.5), 3 + self.y + cam["y"] + math.sin(self.r + 0.8) * (self.s + 2.5))])
        pygame.draw.rect(screen, (200, 0, 0), (self.x + cam["x"] - self.s / 2, self.y + self.s + 5 + cam["y"], self.s * 2, 5))
        pygame.draw.rect(screen, (0, 200, 0), (self.x + cam["x"] - self.s / 2, self.y + self.s + 5 + cam["y"], (self.s * 2 / self.maxHp) * self.hp, 5))

    def update(self, i):
        global selectedShip
        global clicked
        self.r += math.atan2(self.y - self.tY, self.x - self.tX) - self.r
        i
        if self.spd > self.a:
            self.a += 0.1
        if math.dist([self.x, self.y], [self.tX, self.tY]) < 20 and self.type == "miner":
            self.a -= 0.12
            if self.a < 0:
                self.a = 0
        self.x -= math.cos(self.r) * self.a
        self.y -= math.sin(self.r) * self.a
        self.atkCool-=1
        if math.dist([self.x + self.s/2, self.y + self.s/2], [-cam["x"] + mouseX, -cam["y"] + mouseY]) < self.s * 1.5 and clicked:
            selectedShip = i
            clicked = False
        if self.atkCool == 0:
            projectiles.append(projectile(self.x, self.y, self.b, self.r + math.pi, self.team))
            self.atkCool = self.rld
        self.closest = self.range


# planet class
class planet():
    def __init__(self, x, y, s, team):
        self.x = x
        self.y = y
        self.s = s
        self.do = 1000
        self.team = team
        self.t = 0
        self.ta = 2
        self.give = {
            "oil": random.randint(1, 2),
            "metal": random.randint(1, 2),
            "wind": random.randint(1, 5),
            "sun": random.randint(1, 2),
            "o2": random.randint(1, 5),
            "water": random.randint(1, 10),
        }
        self.texture = random.randint(0,0 )
        self.giveCool = 50
        self.col = [
            63.75 * self.give["sun"], 25.5 * self.give["o2"], 25.5 * self.give["water"]
        ]

    def draw(self):
        if self.x > -cam["x"] - self.s and self.y > -cam["y"] - self.s and self.x < -cam["x"] + 800 + self.s and self.y < -cam["y"] + 600 + self.s:
            pygame.draw.ellipse(screen, (self.col[0], self.col[1], self.col[2]), (self.x + cam["x"], self.y + cam["y"], self.s, self.s))
            if self.texture == 0:
                pygame.draw.ellipse(screen, (clamp(self.col[0] - 10, 0, 255), clamp(self.col[1] - 10, 0, 255), clamp(self.col[2] - 10, 0, 255)), (self.x + cam["x"] + self.s/2 + math.cos(self.x * 0.5 + self.y/1.5) * ((self.y + 2700)/5700) * self.s/2.5, self.y + cam["y"] + self.s/2 + math.sin(self.x + self.y) * ((self.x + 2700)/5700) * self.s/2.5, self.s/5, self.s/5))
                pygame.draw.ellipse(screen, (clamp(self.col[0] - 10, 0, 255), clamp(self.col[1] - 10, 0, 255), clamp(self.col[2] - 10, 0, 255)), (self.x + cam["x"] + self.s/2 + math.cos(self.x * 2.15 + self.y/1.65) * ((self.y + 2700)/5700) * self.s/2.5, self.y + cam["y"] + self.s/2.5 + math.sin(self.x * 2.7 + self.y * 1.9) * ((self.x + 2700)/5700) * self.s/2, self.s/5, self.s/5))
                pygame.draw.ellipse(screen, (clamp(self.col[0] - 10, 0, 255), clamp(self.col[1] - 10, 0, 255), clamp(self.col[2] - 10, 0, 255)), (self.x + cam["x"] + self.s/2 + math.cos(self.x * 7.5 + self.y * 1.5) * ((self.y + 2700)/5700) * self.s/2.5, self.y + cam["y"] + self.s/2 + math.sin(self.x + self.y) * ((self.x + 2700)/5700) * self.s/2.5, self.s/5, self.s/5))
                pygame.draw.ellipse(screen, (clamp(self.col[0] - 10, 0, 255), clamp(self.col[1] - 10, 0, 255), clamp(self.col[2] - 10, 0, 255)), (self.x + cam["x"] + self.s/2 + math.cos(self.x * 3.15 + self.y * 1.65) * ((self.y + 2700)/5700) * self.s/2.5, self.y + cam["y"] + self.s/2.5 + math.sin(self.x * 20.7 + self.y * 3.9) * ((self.x + 2700)/5700) * self.s/2, self.s/5, self.s/5))

    def update(self, i):
        global enemyPlanetOwned
        global playerPlanetOwned
        global selectedPlanet
        self.giveCool -= 1
        if self.giveCool <= -1:
            self.giveCool = 50
        if self.team <= -0.5:
            self.do-=1
            enemyPlanetOwned+=1
        elif self.team >= 0.5:
            playerPlanetOwned+=1
            if math.dist([mouseX - cam["x"], mouseY - cam["y"]], [self.x + self.s/2, self.y + self.s/2]) < self.s/2 and clicked:
                selectedPlanet = i
        self.team = clamp(self.team, -1, 1)
        self.t+=self.ta
        if self.t >= 20 or self.t <= 0:
            self.ta*=-1
        if self.team < 0:
            pygame.draw.arc(screen, (255, 0, 0, 1/20 * self.t), (self.x + cam["x"] - 10 - self.t/2, self.y + cam["y"] - 10 - self.t/2, self.s + 20 + self.t, self.s + 20 + self.t), 0, (-self.team * math.pi) * 2, 5)
        elif self.team > 0:
            pygame.draw.arc(screen, (0, 0, 255, 1/20 * self.t), (self.x + cam["x"] - 10 - self.t/2, self.y + cam["y"] - 10 - self.t/2, self.s + 20 + self.t, self.s + 20 + self.t), 0, (self.team * math.pi) * 2, 5)
        if self.do <= 0:
            self.do = 10000
            do = random.randint(0, 100)
            if len(enemys) < enemyPlanetOwned * 8 and do < 75:
                if do < 50:
                    enemys.append(enemy(planets[i].x + random.randint(0, planets[i].s), planets[i].y + random.randint(0, planets[0].s), "soldier", -1))
                elif do < 60:
                    enemys.append(enemy(planets[i].x + random.randint(0, planets[i].s), planets[i].y + random.randint(0, planets[0].s), "miner", -1))
                elif do < 80:
                    enemys.append(enemy(planets[i].x + random.randint(0, planets[i].s), planets[i].y + random.randint(0, planets[0].s), "tank", -1))
                elif do <= 100:
                    enemys.append(enemy(planets[i].x + random.randint(0, planets[i].s), planets[i].y + random.randint(0, planets[i].s), "jester", -1))

    def collide(self, t, p):
        global oil
        global energy
        global metal
        global water
        global food
        global matsTxt
        if math.dist([t.x, t.y], [self.x + self.s / 2, self.y + self.s / 2]) < self.s:
            if p and self.giveCool == 0 and t.type == "miner":
                oil += self.give["oil"]
                energy += self.give["wind"] * windM + self.give[
                    "sun"] * sunM + self.give["water"] * waterM
                metal += self.give["metal"]
                water += self.give["water"]
                food += (self.give["water"] * self.give["o2"]) / 10
                matsTxt = font.render('Oil: ' + str(round(oil)) + " || Energy: " + str(round(energy)) + " || Metal: " + str(round(metal)) + " || Water: " + str(round(water)) + " || Food: " + str(round(food)), True, (255, 255, 255))
            self.team+=t.team/1000
        if t.team == -1 and self.team > -0.99:
            if math.dist([t.x, t.y], [self.x + self.s / 2, self.y + self.s / 2]) < t.pClosest:
                if t.doCool <= 1:
                    t.tX = self.x + random.randint(0, self.s)
                    t.tY = self.y + random.randint(0, self.s)
                    t.pClosest = math.dist([t.x, t.y], [self.x + self.s / 2, self.y + self.s / 2])
                    
                
            


# spawn planets

for i in range(20):
    if i == 0:
        planets.append(planet(random.randint(-2400, 3000), random.randint(-2400, 3000), random.randint(50, 250), 1))
    elif i == 5:
        planets.append(planet(random.randint(-2400, 3000), random.randint(-2400, 3000), random.randint(50, 250), -1))
    else:
        planets.append(planet(random.randint(-2400, 3000), random.randint(-2400, 3000), random.randint(50, 250), 0))
planets.append(planet(random.randint(-2400, 3000), random.randint(-2400, 3000), random.randint(50, 250), 0))

# center camera to home planet
cam["x"] = -planets[0].x + 400 - planets[0].s / 2
cam["y"] = -planets[0].y + 300 - planets[0].s / 2

# spawn starter ship
for i in range(3):
    ships.append(ship(planets[0].x + random.randint(0, planets[0].s), planets[0].y + random.randint(0, planets[0].s), "miner", 1))
ships.append(ship(planets[0].x + random.randint(0, planets[0].s), planets[0].y + random.randint(0, planets[0].s), "soldier", 1))

# spawn enemy starter ship
for i in range(3):
    enemys.append(enemy(planets[5].x + random.randint(0, planets[0].s), planets[5].y + random.randint(0, planets[0].s), "miner", -1))
    enemys.append(enemy(planets[5].x + random.randint(0, planets[0].s), planets[5].y + random.randint(0, planets[0].s), "soldier", -1))

def button(x, y, w, h):
    if mouseX > x and mouseY > y and mouseX < w + x and mouseY < y + h:
        return True
    return False

# everything

while True:
    # setup
    mouseX, mouseY = pygame.mouse.get_pos()

    # events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = True
            dragged = False
    if scene == "menu":
        screen.fill((0, 0, 0)) 
        for i in range(len(stars)):
            pygame.draw.ellipse(screen, (255, 255, 255), (stars[i][0], stars[i][1], stars[i][2], stars[i][2]))
            if keys[pygame.K_LEFT] and cam["x"] < 2400 or keys[pygame.K_a] and cam["x"] < 2400:
                stars[i][0]+=stars[i][2]
            if keys[pygame.K_RIGHT] and cam["x"] > -2600 or keys[pygame.K_d] and cam["x"] > -2600:
                stars[i][0]-=stars[i][2]
            if keys[pygame.K_UP] and cam["y"] < 2400 or keys[pygame.K_w] and cam["y"] < 2400:
                stars[i][1]+=stars[i][2]
            if keys[pygame.K_DOWN] and cam["y"] > -2600 or keys[pygame.K_s] and cam["y"] > -2600:
                stars[i][1]-=stars[i][2]
        pygame.draw.rect(screen, (90, 90, 90), (350, 275, 100, 50))
        pygame.draw.rect(screen, (90, 90, 90), (350, 350, 100, 50))
        pygame.draw.rect(screen, (90, 90, 90), (350, 425, 100, 50))
        screen.blit(menuTxt, (200, 130))
        screen.blit(playTxt, (378, 291))
        screen.blit(shopTxt, (378, 366))
        screen.blit(settingsTxt, (365, 443))
        if button(350, 275, 100, 50) and clicked:
            scene = "game"
        if button(350, 350, 100, 50) and clicked:
            scene = "shop"
        if button(350, 425, 100, 50) and clicked:
            scene = "settings"
    elif scene == "shop":
        screen.fill((0, 0, 0))
        for i in range(len(stars)):
            pygame.draw.ellipse(screen, (255, 255, 255), (stars[i][0], stars[i][1], stars[i][2], stars[i][2]))
            if keys[pygame.K_LEFT] and cam["x"] < 2400 or keys[pygame.K_a] and cam["x"] < 2400:
                stars[i][0]+=stars[i][2]
            if keys[pygame.K_RIGHT] and cam["x"] > -2600 or keys[pygame.K_d] and cam["x"] > -2600:
                stars[i][0]-=stars[i][2]
            if keys[pygame.K_UP] and cam["y"] < 2400 or keys[pygame.K_w] and cam["y"] < 2400:
                stars[i][1]+=stars[i][2]
            if keys[pygame.K_DOWN] and cam["y"] > -2600 or keys[pygame.K_s] and cam["y"] > -2600:
                stars[i][1]-=stars[i][2]
        pygame.draw.rect(screen, (90, 90, 90), (10, 525, 100, 50))
        screen.blit(backTxt, (45, 541))
        if button(10, 525, 100, 50) and clicked:
            scene = "menu"
    elif scene == "settings":
        screen.fill((0, 0, 0))
        for i in range(len(stars)):
            pygame.draw.ellipse(screen, (255, 255, 255), (stars[i][0], stars[i][1], stars[i][2], stars[i][2]))
            if keys[pygame.K_LEFT] and cam["x"] < 2400 or keys[pygame.K_a] and cam["x"] < 2400:
                stars[i][0]+=stars[i][2]
            if keys[pygame.K_RIGHT] and cam["x"] > -2600 or keys[pygame.K_d] and cam["x"] > -2600:
                stars[i][0]-=stars[i][2]
            if keys[pygame.K_UP] and cam["y"] < 2400 or keys[pygame.K_w] and cam["y"] < 2400:
                stars[i][1]+=stars[i][2]
            if keys[pygame.K_DOWN] and cam["y"] > -2600 or keys[pygame.K_s] and cam["y"] > -2600:
                stars[i][1]-=stars[i][2]
        pygame.draw.rect(screen, (90, 90, 90), (10, 525, 100, 50))
        screen.blit(backTxt, (45, 541))
        if button(10, 525, 100, 50) and clicked:
            scene = "menu"
    elif scene == "game":
        # camera movement
        if keys[pygame.K_LEFT] and cam["x"] < 2400 or keys[pygame.K_a] and cam["x"] < 2400:
            cam["x"] += 10
        if keys[pygame.K_RIGHT] and cam["x"] > -2600 or keys[pygame.K_d] and cam["x"] > -2600:
            cam["x"] -= 10
        if keys[pygame.K_UP] and cam["y"] < 2400 or keys[pygame.K_w] and cam["y"] < 2400:
            cam["y"] += 10
        if keys[pygame.K_DOWN] and cam["y"] > -2600 or keys[pygame.K_s] and cam["y"] > -2600:
            cam["y"] -= 10
    
        # space
        screen.fill((0, 0, 0))
        for i in range(len(stars)):
            pygame.draw.ellipse(screen, (255, 255, 255), (stars[i][0], stars[i][1], stars[i][2], stars[i][2]))
            if keys[pygame.K_LEFT] and cam["x"] < 2400 or keys[pygame.K_a] and cam["x"] < 2400:
                stars[i][0]+=stars[i][2]
            if keys[pygame.K_RIGHT] and cam["x"] > -2600 or keys[pygame.K_d] and cam["x"] > -2600:
                stars[i][0]-=stars[i][2]
            if keys[pygame.K_UP] and cam["y"] < 2400 or keys[pygame.K_w] and cam["y"] < 2400:
                stars[i][1]+=stars[i][2]
            if keys[pygame.K_DOWN] and cam["y"] > -2600 or keys[pygame.K_s] and cam["y"] > -2600:
                stars[i][1]-=stars[i][2]
            if stars[i][0] < -10:
                stars[i][0] = 810
            if stars[i][0] > 810:
                stars[i][0] = -10
            if stars[i][1] < -10:
                stars[i][1] = 610
            if stars[i][1] > 610:
                stars[i][1] = -10
        # minimap
        pygame.draw.rect(screen, (40, 40, 40), (10, 410, 105, 105))
        pygame.draw.rect(screen, (0, 200, 0), (97 + (-2400 - cam["x"])/54, 502 + (-2400 - cam["y"])/54, 14, 11), 1)
        # planets
        for i in range(len(planets)):
            planets[i].draw()
            for j in range(len(ships)):
                planets[i].collide(ships[j], True)
            for p in range(len(enemys)):
                planets[i].collide(enemys[p], False)
            planets[i].update(i)
            pygame.draw.ellipse(screen, (100, 100, 100), (99 + (-2400 + planets[i].x)/54, 500 + (-2400 + planets[i].y)/54, 3 + planets[i].s/60, 3 + planets[i].s/60))
    
        # ships
        for i in range(len(ships)):
            ships[i].draw()
            ships[i].update(i)
            pygame.draw.ellipse(screen, (0, 0, 200), (99 + (-2400 + ships[i].x)/54, 500 + (-2400 + ships[i].y)/54, 3 + ships[i].s/60, 3 + ships[i].s/60))
    
        # enemys
        for i in range(len(enemys)):
            enemys[i].draw()
            enemys[i].update()
            for j in range(len(ships)):
                enemys[i].collide(ships[j])
            pygame.draw.ellipse(screen, (200, 0, 0), (99 + (-2400 + enemys[i].x)/54, 500 + (-2400 + enemys[i].y)/54, 3 + enemys[i].s/60, 3 + enemys[i].s/60))
    
        # projectiles
        for i in range(len(projectiles)):
            projectiles[i].draw()
            projectiles[i].update()
            for j in range(len(ships)):
                projectiles[i].collide(ships[j])
            for o in range(len(enemys)):
                projectiles[i].collide(enemys[o])
    
        # movement of the ships
        if selectedShip != "n" and selectedShip >= len(ships):
            selectedShip = "n"
        if selectedShip != "n":
            pygame.draw.ellipse(screen, (0, 100, 200), (ships[selectedShip].x + cam["x"] - 7.5, ships[selectedShip].y + cam["y"] - 7.5, ships[selectedShip].s + 15, ships[selectedShip].s + 15), 2)
            if clicked:
                ships[selectedShip].tX = -cam["x"] + mouseX
                ships[selectedShip].tY = -cam["y"] + mouseY
                selectedShip = "n"
        if selectedPlanet != "n":
            pygame.draw.rect(screen, (100, 100, 100), (10, 85, 150, 150))
            pygame.draw.rect(screen, (90, 90, 90), (15, 90, 40, 40))
            pygame.draw.rect(screen, (90, 90, 90), (60, 90, 40, 40))
            pygame.draw.rect(screen, (90, 90, 90), (105, 90, 40, 40))
            pygame.draw.rect(screen, (90, 90, 90), (105, 90, 40, 40))
            pygame.draw.rect(screen, (90, 90, 90), (15, 135, 40, 40))
            pygame.draw.rect(screen, (90, 90, 90), (11, 195, 71, 10))
            pygame.draw.rect(screen, (0, 0, 0), (12, 195, (71)/2 * planets[selectedPlanet].give["oil"], 10))
            pygame.draw.rect(screen, (90, 90, 90), (85, 195, 71, 10))
            pygame.draw.rect(screen, (50, 50, 50), (84, 195, (71)/2 * planets[selectedPlanet].give["metal"], 10))
            pygame.draw.rect(screen, (90, 90, 90), (11, 210, 71, 10))
            pygame.draw.rect(screen, (250, 250, 250), (12, 210, (71)/5 * planets[selectedPlanet].give["wind"], 10))
            pygame.draw.rect(screen, (90, 90, 90), (85, 210, 71, 10))
            pygame.draw.rect(screen, (250, 200, 0), (84, 210, (71)/2 * planets[selectedPlanet].give["sun"], 10))
            pygame.draw.rect(screen, (90, 90, 90), (11, 225, 71, 10))
            pygame.draw.rect(screen, (100, 100, 250), (12, 225, (71)/5 * planets[selectedPlanet].give["o2"], 10))
            pygame.draw.rect(screen, (90, 90, 90), (85, 225, 71, 10))
            pygame.draw.rect(screen, (0, 0, 200), (84, 225, (71)/10 * planets[selectedPlanet].give["water"], 10))
            """
            self.give = {
                "oil": random.randint(1, 2),
                "metal": random.randint(1, 2),
                "wind": random.randint(1, 5),
                "sun": random.randint(1, 2),
                "o2": random.randint(1, 5),
                "water": random.randint(1, 10),
            }
            """
            pygame.draw.ellipse(screen, (90, 90, 90), (planets[selectedPlanet].x + cam["x"] - 10 - planets[selectedPlanet].t/2, planets[selectedPlanet].y + cam["y"] - 10 -  planets[selectedPlanet].t/2, planets[selectedPlanet].s + 20 + planets[selectedPlanet].t, planets[selectedPlanet].s + 20 + planets[selectedPlanet].t), 6)
            if button(15, 90, 40, 40) and clicked and metal >= 100 and water >= 300 and food >= 200 and energy >= 500 and oil >= 100 and len(ships) < playerPlanetOwned * 8:
                metal -= 100
                water -= 300
                food -= 200
                energy -= 500
                oil -= 100
                matsTxt = font.render('Oil: ' + str(round(oil)) + " || Energy: " + str(round(energy)) + " || Metal: " + str(round(metal)) + " || Water: " + str(round(water)) + " || Food: " + str(round(food)), True, (255, 255, 255))
                ships.append(ship(planets[selectedPlanet].x, planets[selectedPlanet].y, "miner", 1))
            elif button(60, 90, 40, 40) and clicked and metal >= 100 and water >= 300 and food >= 200 and energy >= 500 and oil >= 100 and len(ships) < playerPlanetOwned * 8:
                metal -= 100
                water -= 300
                food -= 200
                energy -= 500
                oil -= 100
                matsTxt = font.render('Oil: ' + str(round(oil)) + " || Energy: " + str(round(energy)) + " || Metal: " + str(round(metal)) + " || Water: " + str(round(water)) + " || Food: " + str(round(food)), True, (255, 255, 255))
                ships.append(ship(planets[selectedPlanet].x, planets[selectedPlanet].y, "soldier", 1))
            elif button(105, 90, 40, 40) and clicked and metal >= 150 and water >= 500 and food >= 300 and energy >= 500 and oil >= 150 and len(ships) < playerPlanetOwned * 8:
                metal -= 150
                water -= 500
                food -= 300
                energy -= 500
                oil -= 150
                matsTxt = font.render('Oil: ' + str(round(oil)) + " || Energy: " + str(round(energy)) + " || Metal: " + str(round(metal)) + " || Water: " + str(round(water)) + " || Food: " + str(round(food)), True, (255, 255, 255))
                ships.append(ship(planets[selectedPlanet].x, planets[selectedPlanet].y, "tank", 1))
            elif button(15, 135, 40, 40) and clicked and metal >= 100 and water >= 300 and food >= 200 and energy >= 500 and oil >= 100 and len(ships) < playerPlanetOwned * 8:
                metal -= 100
                water -= 300
                food -= 200
                energy -= 500
                oil -= 100
                matsTxt = font.render('Oil: ' + str(round(oil)) + " || Energy: " + str(round(energy)) + " || Metal: " + str(round(metal)) + " || Water: " + str(round(water)) + " || Food: " + str(round(food)), True, (255, 255, 255))
                ships.append(ship(planets[selectedPlanet].x, planets[selectedPlanet].y, "jester", 1))
        # misc
        projectiles = [x for x in projectiles if not x.range <= 0]
        ships = [x for x in ships if not x.hp <= 0]
        enemys = [x for x in enemys if not x.hp <= 0]
    
        # mat bar
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 800, 75))
        screen.blit(matsTxt, (5, 5))
        pygame.draw.rect(screen, (50, 50, 50), (0, 525, 800, 75))
        if button(0, 525, 30, 75):
            xtab+=4
        elif button(770, 525, 30, 75):
            xtab-=4
        for i in range(len(ships)):
            if selectedShip == i:
                pygame.draw.rect(screen, (100, 100, 100), (10 + i * 90 + xtab, 525, 80, 75))
            else:
                pygame.draw.rect(screen, (75, 75, 75), (10 + i * 90 + xtab, 525, 80, 75))
            pygame.draw.rect(screen, (200, 0, 0), (10 + i * 90 + xtab, 585, 80, 10))
            pygame.draw.rect(screen, (0, 200, 0), (10 + i * 90 + xtab, 585, (80 / ships[i].maxHp) * ships[i].hp, 10))
            if ships[i].type == "miner":
                pygame.draw.rect(screen, (0, 0, 0), (10 + i * 90 + 40 + xtab, 530, 5, 50))
                pygame.draw.line(screen, (0, 0, 0), (10 + i * 90 + 18 + xtab, 542), (10 + i * 90 + 26 + xtab, 534), 4)
                pygame.draw.line(screen, (0, 0, 0), (10 + i * 90 + 24 + xtab, 536), (10 + i * 90 + 40 + xtab, 534), 5)
                pygame.draw.line(screen, (0, 0, 0), (10 + i * 90 + 40 + xtab, 536), (10 + i * 90 + 54 + xtab, 534), 5)
                pygame.draw.line(screen, (0, 0, 0), (10 + i * 90 + 60 + xtab, 542), (10 + i * 90 + 54 + xtab, 534), 4)
            elif ships[i].type == "soldier":
                pygame.draw.rect(screen, (0, 0, 0), (10 + i * 90 + 30 + xtab, 542.5, 25, 38))
                pygame.draw.ellipse(screen, (0, 0, 0), (10 + i * 90 + 30 + xtab, 530, 25, 25))
                pygame.draw.rect(screen, (75, 75, 75), (10 + i * 90 + 30 + xtab, 544, 25, 3))
            elif ships[i].type == "tank":
                pygame.draw.ellipse(screen, (0, 0, 0), (10 + i * 90 + 17.5 + xtab, 530, 50, 50))
            if mouseX > 5 + i * 90 and mouseY > 525 and mouseX < 85 + i * 90 and mouseY < 600 and clicked:
                selectedShip = i
                clicked = False
        # tutorail
        if not saveCode[0] and tut <= 4:
            screen.blit(tutTxt, (tutX, tutY))
            if button(350, 375, 100, 50) and clicked:
                tut+=1
                clicked = False
                if tut == 1:
                    tutTxt = font3.render("<- To start off click this button to make a miner", True, (255, 255, 255))
                    tutX = 60
                    tutY = 100
                elif tut == 2:
                    tutTxt = font3.render("<- Next click this button to make a soldier", True, (255, 255, 255))
                    tutX = 110
                    tutY = 100
                elif tut == 3:
                    tutTxt = font3.render("Finnaly the buttons on the bottom are to select ships. If you click anywhere while selecting a ship it will move", True, (255, 255, 255))
                    tutX = 25
                    tutY = 220
                elif tut == 4:
                    tutTxt = font3.render("WASD to move the camera and good luck.", True, (255, 255, 255))
                    tutX = 240
                    tutY = 200
            pygame.draw.rect(screen, (150, 150, 150), (350, 375, 100, 50))
        
        # ship bar
        if playerPlanetOwned == 0:
            scene = "gameOver"
            clicked = False
            planets = []
            enemys = []
            oil = 1000
            energy = 2000
            metal = 1000
            water = 1000
            food = 1000
            tutX = 315
            tutY = 200
            windM = 1
            sunM = 1
            waterM = 1
            ships = []
            projectiles = []
            selectedShip = "n"
            selectedPlanet = 0
            enemyPlanetOwned = 1
            playerPlanetOwned = 1
            # spawn planets
            for i in range(20):
                if i == 0:
                    planets.append(planet(random.randint(-1200, 1800), random.randint(-1200, 1800), random.randint(50, 250), 1))
                elif i == 5:
                    planets.append(planet(random.randint(-1200, 1800), random.randint(-1200, 1800), random.randint(50, 250), -1))
                else:
                    planets.append(planet(random.randint(-1200, 1800), random.randint(-1200, 1800), random.randint(50, 250), 0))
            
            # center camera to home planet
            cam["x"] = -planets[0].x + 400 - planets[0].s / 2
            cam["y"] = -planets[0].y + 300 - planets[0].s / 2
            
            # spawn starter ship
            for i in range(3):
                ships.append(ship(planets[0].x + random.randint(0, planets[0].s), planets[0].y + random.randint(0, planets[0].s), "miner", 1))
            ships.append(ship(planets[0].x + random.randint(0, planets[0].s), planets[0].y + random.randint(0, planets[0].s), "soldier", 1))
            
            # spawn enemy starter ship
            for i in range(3):
                enemys.append(enemy(planets[5].x + random.randint(0, planets[0].s), planets[5].y + random.randint(0, planets[0].s), "miner", -1))
                enemys.append(enemy(planets[5].x + random.randint(0, planets[0].s), planets[5].y + random.randint(0, planets[0].s), "soldier", -1))
        enemyPlanetOwned = 0
        playerPlanetOwned = 0
    elif scene == "gameOver":
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (90, 90, 90), (350, 350, 100, 50))
        screen.blit(gameOverTxt, (315, 250))
        screen.blit(backTxt, (380, 367))
        if button(350, 350, 100, 50) and clicked:
            scene = "menu"
        

    pygame.display.update()
    clicked = False
    clock.tick(30)
pygame.quit()
