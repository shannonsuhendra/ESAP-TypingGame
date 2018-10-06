import pygame, math, sys, random, string
from enum import Enum
from pygame.locals import *
from math import cos, sin, pi
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

highest_score = 0

class Score():
	
	def __init__(self):
		pygame.font.init()
		self.font = pygame.font.SysFont("Courier", 60)
		
		self.score = 0
		self.width = 50
		self.height = 50
		

	def update(self, deltat):
		self.textSurf = self.font.render(str(self.score), 1, (255, 255, 255))
		W = self.textSurf.get_width()
		H = self.textSurf.get_height()
		screen.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])

	def add_score(self):
		self.score += 1
		# self.render_score()

	def get_score(self):
		return self.score

	def reset(self):
		self.score = 0
		# self.render_score()


class Clouds(pygame.sprite.Sprite):

	def __init__(self, image, position, speed, endImage):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.src_image = pygame.image.load(image)
		self.speed = speed
		self.image = self.src_image
		self.rect = self.image.get_rect()
		self.initialSpeed = speed
		self.end_image = pygame.image.load(endImage)
		self.original_image = pygame.image.load(image)

	def update(self, deltat):
		x, y = self.position
		y += self.speed
		self.position = (x, y)
		#print("(" + str(x) + ", " + str(y) + ")")
		
		self.rect.center = self.position
		self.text.rect.center = (x,y+50)

	def add_text(self, text):
		self.text = text

	def reset(self):
		randomX = random.randint(1, 9)
		x = randomX * 100
		y = 0
		self.position = (x,y)
		self.text.set_random_word()
		self.speed = self.initialSpeed

	def end(self):
		x, y = self.position
		return y > 700

	def endImage(self):
		self.image = self.end_image
		#x, y = self.position
		#x += 100
		#y += 50

	def originalImage(self):
		self.image = self.original_image
		

class Text(pygame.sprite.Sprite):
	def __init__(self, size, color, width, height):
		pygame.sprite.Sprite.__init__(self)
		pygame.font.init()

		self.length = 5

		#load words frm file word.txt
		text_file = open("words.txt", "r")
		self.words = text_file.read().splitlines()
		self.words1 = [x for x in self.words if len(x) == self.length]
		

		self.color = color
		self.width = width
		self.height = height
		self.word = self.get_random_word()
		self.index = 0

		surface = pygame.Surface((self.width, self.height))
		surface.fill((255, 255, 255))
		self.image = surface
		
		self.font = pygame.font.SysFont("Courier", size)
		self.rect = self.image.get_rect()
		self.set_random_word()

	
	def get_random_word(self):
		self.word = random.choice(self.words1)
		return self.word

	def get_word(self):
		return self.word

	def get_index(self):
		return self.index

	def set_index(self, index):
		self.index = index
		newTextSurf = self.font.render(self.word[:index], 1, (255,0,0))
		W = self.textSurf.get_width()
		H = self.textSurf.get_height()
		self.image.blit(newTextSurf, [self.width/2 - W/2, self.height/2 - H/2])


	def set_random_word(self):
		self.textSurf = self.font.render(self.get_random_word(), 1, self.color)
		W = self.textSurf.get_width()
		H = self.textSurf.get_height()
		self.image.fill((255, 255, 255))
		self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])

	def add_length(self):
		self.length += 2
		self.words1 = [x for x in self.words if len(x) == self.length]

	def reset_length(self):
		self.length = 5
		self.words1 = [x for x in self.words if len(x) == self.length]

class Animation_End(pygame.sprite.Sprite):
	def __init__(self, dx, dy, image, displacement, scale, angle):
		pygame.sprite.Sprite.__init__(self)
		self.idx = dx
		self.idy = dy
		self.dx = self.idx
		self.dy = self.idy
		self.src_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(image), scale), angle)
		self.image = self.src_image
		self.rect = self.image.get_rect()
		self.displacementX = displacement[0]
		self.displacementY = displacement[1]
		self.startPosition = [0,0]
		self.theta = 0
		self.r = 0

	def update(self, deltat):
		randomXY = random.randint(-9, 9)
		x, y = self.startPosition
		if y <= 0:
			self.dx = self.dx + randomXY
			self.dy = -self.dy + randomXY
		if x <= 0:
			self.dx = -self.dx + randomXY
			self.dy = self.dy + randomXY
		if y >= 768:
			self.dx = self.dx + randomXY
			self.dy = -self.dy + randomXY
		if x >= 1024:
			self.dx = -self.dx + randomXY
			self.dy = self.dy + randomXY
		y += self.dy 
		x += self.dx
		#x += self.dx + 5*((pygame.time.get_ticks()//100)%10-5)
		self.startPosition = (x, y)
		self.rect.center = self.startPosition

	def updateSpiral(self, deltat, a, b, step):
		x, y = self.startPosition
		self.theta += step
		self.r = a + b*self.theta
		self.dx = int(self.r*cos(self.theta))
		self.dy = int(self.r*sin(self.theta))

		
	def setPosition(self, position):
		if self.startPosition == [0,0]:
			self.startPosition = [position[0] + self.displacementX, position[1] + self.displacementY]

	def reset(self):
		self.startPosition = [0,0]
		self.dx = self.idx
		self.dy = self.idy


class GameState(Enum):
	TITLE = 1
	GAME = 2
	END = 3

rect = screen.get_rect()
clouds = Clouds('../finalcloud.png', (500,0), 10, '../cloud.png')
text = Text(30, (0,0,0), 120,50)
clouds_group = pygame.sprite.Group()
score = Score()

clouds_group.add(clouds)
clouds_group.add(text)
# clouds_group.add(score)

clouds.add_text(text)
score = Score()
victor = Animation_End(0, -15, '../Victor.png', [6, -48], [100, 90], 0)
animationEnd_group = pygame.sprite.Group()
animationEnd_group.add(victor)
adel = Animation_End(-1, -15, '../Adel.png', [-50, -35], [80, 95], 25)
animationEnd_group.add(adel)
eduardo = Animation_End(3, -15, '../Eduardo.png', [120, 20], [80, 95], -35)
animationEnd_group.add(eduardo)
hannah = Animation_End(2, -15, '../Hannah.png', [90, -15], [100, 85], -35)
animationEnd_group.add(hannah)
changwook = Animation_End(-3, -15, '../changwook.png', [-103, 18], [160, 170], 43)
animationEnd_group.add(changwook)
helen = Animation_End(-2, -15, '../Helen.png', [-70, -10], [160, 150], 20)
animationEnd_group.add(helen)
sadhana = Animation_End(1, -15, '../Sadhana.png', [46, -40], [140, 150], -20)
animationEnd_group.add(sadhana)
arvind = Animation_End(-2, -15, '../Arvind.png', [80,10], [100,105], 0)
animationEnd_group.add(arvind)

screen.fill((255,255,255))
pygame.display.flip()


gameState = GameState.TITLE
gameOver = False



def renderText(text, font, fontSize, color, yOffSet):
	font = pygame.font.SysFont(font, fontSize)
	textSurf = font.render(text, True, color)
	W = textSurf.get_width()
	H = textSurf.get_height()
	screen_width, screen_height = pygame.display.get_surface().get_size()
	screen.blit(textSurf,[screen_width/2 - W/2, screen_height/2 - H/2 + yOffSet])

while 1:

	deltat = clock.tick(30)

	if gameState == GameState.TITLE:
		screen.fill((0,0,0))
		pygame.font.init()
		renderText("TYPO._.", "Arial", 100, (255,255,100), 0)
		renderText("Press enter to start", "Arial", 30, (255,100,100), 50)
		renderText("High Score: " + str(highest_score), "Arial", 50, (255,100,100), 90)

		for event in pygame.event.get():

			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE:
				sys.exit(0)
			if event.key == K_RETURN:
				gameState = GameState.GAME
				clouds.reset()
				score.reset()
				victor.reset()
				adel.reset()
				eduardo.reset()
				hannah.reset()
				changwook.reset()
				helen.reset()
				sadhana.reset()
				arvind.reset()

	elif gameState == GameState.GAME:


		word = text.get_word()
		screen.fill((255, 255, 255))
		bg = pygame.transform.scale(pygame.image.load("../background.jpg"), [1024,768])
		screen.blit(bg, (0,0))
		clouds_group.update(deltat)
		clouds_group.draw(screen)
		score.update(deltat)

		if clouds.end() == True:
			clouds.speed = 0
			victor.setPosition(clouds.position)
			adel.setPosition(clouds.position)
			eduardo.setPosition(clouds.position)
			hannah.setPosition(clouds.position)
			changwook.setPosition(clouds.position)
			helen.setPosition(clouds.position)
			sadhana.setPosition(clouds.position)
			arvind.setPosition(clouds.position)
			animationEnd_group.update(deltat)
			animationEnd_group.draw(screen)
			clouds.endImage()
			gameOver = True


			
			text.reset_length()
			if highest_score < score.get_score():
				highest_score = score.get_score()
			pygame.font.init()
			renderText("GAME OVER", "Arial", 100, (255,255,100), 0)
			renderText("Press space to continue", "Arial", 30, (255,100,100), 50)
			renderText("High Score: " + str(highest_score), "Arial", 50, (255,100,100), 90)



		for event in pygame.event.get():

			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE:
				sys.exit(0)

			if event.key == K_SPACE and gameOver == True:
				gameState = GameState.TITLE
				clouds.reset()
				score.reset()
				clouds.originalImage()

			if not hasattr(event, 'unicode'): continue
			index = text.get_index()
			if event.unicode == word[index]:
				if index == len(word) - 1:
					text.set_index(0)
					clouds.reset()
					score.add_score()
					if score.get_score() % 5 == 0:
						text.add_length()
				else:
					text.set_index(text.get_index() + 1)

	
		

	#RENDERING
	pygame.display.flip()

	#car_group.update(deltat)



