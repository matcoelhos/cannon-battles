import sys, pygame
from random import randint
from math import pi, sin, cos, atan2
import matplotlib.path as mplPath
import numpy as np

pygame.init()

GRAVITY = [0,120]
MAXVEL = 450
MAXLEN = 100

class Cannon:
	health = 100
	RADIUS = 9
	LENGTH = 20
	def __init__(self,x,y,direction=45):
		self.center = (x+15,y-18)
		self.base = []

		self.base.append([x,y])
		y-=10
		self.base.append([x,y])
		x+=10
		self.base.append([x,y])
		y-=10
		self.base.append([x,y])
		x+=10
		self.base.append([x,y])
		y+=10
		self.base.append([x,y])
		x+=10
		self.base.append([x,y])
		y+=10
		self.base.append([x,y])

		self.update(direction)

	def update(self,direction):
		direction = max(direction,0)
		direction = min(direction,180)
		self.direction = int(direction)
		p1 = [self.center[0] + self.RADIUS*cos((90+self.direction)/180*pi),self.center[1] - self.RADIUS*sin((90+self.direction)/180*pi)]
		p2 = [self.center[0] + self.RADIUS*cos((-90+self.direction)/180*pi),self.center[1] - self.RADIUS*sin((-90+self.direction)/180*pi)]
		p3 = [p2[0] + self.LENGTH*cos((self.direction+10)/180*pi),p2[1] - self.LENGTH*sin((self.direction+10)/180*pi)]
		p4 = [p1[0] + self.LENGTH*cos((self.direction-10)/180*pi),p1[1] - self.LENGTH*sin((self.direction-10)/180*pi)]
		self.poly = [p1,p2,p3,p4]

		self.mouth = ((p3[0]+p4[0])/2,(p3[1]+p4[1])/2)

	def get_base(self,):
		return self.base

class Cannonball:
	RADIUS = 5
	tick = 1/30

	def __init__(self,x,y,vx,vy):
		self.pos = (x,y)
		self.vel = (vx,vy)

	def update(self,):
		x = self.pos[0] + self.vel[0]*self.tick
		y = self.pos[1] + self.vel[1]*self.tick
		self.pos = (x,y)
		vy = self.vel[1] + GRAVITY[1]*self.tick
		self.vel = (self.vel[0],vy)

class Ground:
	def __init__(self,points):
		self.points = points
		self.points = []
		self.points.append([0,480])
		self.points.append([0,400])

		mark = 40
		for point in points:
			self.points.append([mark,400-point])
			mark += 40

		self.points.append([640,400])
		self.points.append([640,480])

	def get_polygon(self,):
		return self.points


class Grass:
	def __init__(self,points):
		self.points = points
		self.points = []
		self.points.append([0,480])
		self.points.append([0,400])

		mark = 40
		for point in points:
			self.points.append([mark,400-point])
			mark += 40

		points.reverse()
		mark -= 40
		for point in points:
			self.points.append([mark,410-point])
			mark -= 40
		self.points.append([0,410])
		points.reverse()

	def get_polygon(self,):
		return self.points

class Fire:
	def __init__(self,px,py):
		self.pos = (px,py)
		self.poly1 = []
		self.poly2 = []
		self.poly1.append(self.pos)
		py-=20
		self.poly1.append((px,py))
		py+=10
		px+=7
		self.poly1.append((px,py))
		py-=15
		px+=8
		self.poly1.append((px,py))
		py+=15
		px+=8
		self.poly1.append((px,py))
		py-=10
		px+=7
		self.poly1.append((px,py))
		py+=20
		self.poly1.append((px,py))

		px-=27
		self.poly2.append((px,py))
		py-=10
		self.poly2.append((px,py))
		py+=10
		px+=4
		self.poly2.append((px,py))
		self.poly2.append((px,py))
		py-=10
		px+=8
		self.poly2.append((px,py))
		py+=10
		px+=8
		self.poly2.append((px,py))
		py-=10
		px+=4
		self.poly2.append((px,py))
		py+=10
		self.poly2.append((px,py))



size = width, height = 640, 480

BLACK = (0,0,0)
BLUE = (22,112,184)
GREEN = (0,77,0)
BROWN = (128,64,0)
DARK_BROWN = (77,38,0)
GRAY = (77,77,51)
RED = (230, 0, 0)
ORANGE = (255, 153, 0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

plist = []
for i in range(8):
	n = randint(0,160)
	plist.append(n)
	plist.append(n)

ground = Ground(plist)
grass = Grass(plist)
cannon1 = Cannon(45,400-plist[1],45)
fire1 = Fire(45,400-plist[1])
cannon2 = Cannon(640-3*40+5,400-plist[-3],180-45)
fire2 = Fire(640-3*40+5,400-plist[-3])

poly_path = mplPath.Path(np.array(ground.get_polygon()))
c1_path = mplPath.Path(np.array(cannon1.base))
c2_path = mplPath.Path(np.array(cannon2.base))

turn = 0
shot = False
play = True
fire_1 = False
fire_2 = False
dist = 0

while True:
	clock.tick(60)    
	screen.fill(BLUE)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if play == False:
				fire_1 = False
				fire_2 = False
				play = True
				plist = []
				for i in range(8):
					n = randint(0,160)
					plist.append(n)
					plist.append(n)

				ground = Ground(plist)
				grass = Grass(plist)
				cannon1 = Cannon(45,400-plist[1],45)
				fire1 = Fire(45,400-plist[1])
				cannon2 = Cannon(640-3*40+5,400-plist[-3],180-45)
				fire2 = Fire(640-3*40+5,400-plist[-3])

				poly_path = mplPath.Path(np.array(ground.get_polygon()))
				c1_path = mplPath.Path(np.array(cannon1.base))
				c2_path = mplPath.Path(np.array(cannon2.base))
			else:
				shot = True
				factor = dist/MAXLEN
				if turn == 0:
					cannonball = Cannonball(cannon1.mouth[0],cannon1.mouth[1],factor*MAXVEL*cos(cannon1.direction/180*pi),-1*factor*MAXVEL*sin(cannon1.direction/180*pi))
				else:
					cannonball = Cannonball(cannon2.mouth[0],cannon2.mouth[1],factor*MAXVEL*cos(cannon2.direction/180*pi),-1*factor*MAXVEL*sin(cannon2.direction/180*pi))
				turn = int(not(turn))

	if (not shot) and play:
		pos = pygame.mouse.get_pos()
		if turn == 0:
			angle = atan2(-1*pos[1]+cannon1.center[1],pos[0]-cannon1.center[0])/pi*180
			dist = ((pos[1]-cannon1.mouth[1])**2 + (pos[0]-cannon1.mouth[0])**2)**0.5
			dist = min(dist,MAXLEN)
			aux = 0.8*dist
			cannon1.update(angle)
			arrow_pos = (cannon1.mouth[0]+dist*cos(cannon1.direction*pi/180),cannon1.mouth[1]-dist*sin(cannon1.direction*pi/180))
			pygame.draw.line(screen,BLACK,cannon1.mouth,arrow_pos,3)
			pygame.draw.polygon(screen,BLACK,
				[arrow_pos,
				(cannon1.mouth[0]+aux*cos((cannon1.direction+3)*pi/180),cannon1.mouth[1]-aux*sin((cannon1.direction+3)*pi/180)),
				(cannon1.mouth[0]+aux*cos((cannon1.direction-3)*pi/180),cannon1.mouth[1]-aux*sin((cannon1.direction-3)*pi/180))])

		else:
			angle = atan2(-1*pos[1]+cannon2.center[1],pos[0] - cannon2.center[0])/pi*180
			dist = ((pos[1]-cannon2.mouth[1])**2 + (pos[0]-cannon2.mouth[0])**2)**0.5
			dist = min(dist,MAXLEN)
			aux = 0.8*dist
			cannon2.update(angle)
			arrow_pos = (cannon2.mouth[0]+dist*cos(cannon2.direction*pi/180),cannon2.mouth[1]-dist*sin(cannon2.direction*pi/180))
			pygame.draw.line(screen,BLACK,cannon2.mouth,arrow_pos,3)
			pygame.draw.polygon(screen,BLACK,
				[arrow_pos,
				(cannon2.mouth[0]+aux*cos((cannon2.direction+3)*pi/180),cannon2.mouth[1]-aux*sin((cannon2.direction+3)*pi/180)),
				(cannon2.mouth[0]+aux*cos((cannon2.direction-3)*pi/180),cannon2.mouth[1]-aux*sin((cannon2.direction-3)*pi/180))])


	
	pygame.draw.polygon(screen, BROWN, ground.get_polygon())
	pygame.draw.polygon(screen, GREEN, grass.get_polygon())

	pygame.draw.circle(screen,GRAY,cannon1.center,cannon1.RADIUS)
	pygame.draw.polygon(screen,GRAY,cannon1.poly)
	pygame.draw.polygon(screen, DARK_BROWN, cannon1.base)

	pygame.draw.circle(screen,GRAY,cannon2.center,cannon1.RADIUS)
	pygame.draw.polygon(screen,GRAY,cannon2.poly)
	pygame.draw.polygon(screen, DARK_BROWN, cannon2.base)

	if fire_2:
		pygame.draw.polygon(screen, RED, fire2.poly1)
		pygame.draw.polygon(screen, ORANGE, fire2.poly2)
	if fire_1:
		pygame.draw.polygon(screen, RED, fire1.poly1)
		pygame.draw.polygon(screen, ORANGE, fire1.poly2)

	if shot:
		pygame.draw.circle(screen,BLACK,cannonball.pos,cannonball.RADIUS)
		cannonball.update()
		if poly_path.contains_point(cannonball.pos):
			del cannonball
			shot = False
		elif (cannonball.pos[0]<0 or cannonball.pos[0]>640):
			del cannonball
			shot = False
		elif c1_path.contains_point(cannonball.pos):
			play = False
			fire_1 = True
			shot = False
			del cannonball
		elif c2_path.contains_point(cannonball.pos):
			play = False
			fire_2 = True
			shot = False
			del cannonball
	pygame.display.flip()