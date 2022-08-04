from turtle import title
import pygame, sys
from settings import *
from support import *
from world import World

world = None

class Game:
	def __init__(self):
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font('graphics/font/Pixel.ttf', 32)
		self.level = World()

	# play the game
	def play(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if pygame.key.get_pressed()[pygame.K_ESCAPE]:
				game.paus()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

	# paus menu
	def paus(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			image_path = pygame.image.load('graphics/img/menu_background.png')
			menu_background = pygame.transform.scale(image_path, (WIDTH,HEIGTH))
			title = self.font.render('Paus', True, black)
			title_rect = title.get_rect(x=TILESIZE, y=10)

			resume	= button(TILESIZE, TILESIZE * 2,	get_sprite(0, TILESIZE * 2, TILESIZE * 4, TILESIZE, ss_ui),'Resume')
			load	= button(TILESIZE, TILESIZE * 4,	get_sprite(0, TILESIZE * 2, TILESIZE * 4, TILESIZE, ss_ui),'Save / Load')
			quit	= button(TILESIZE, TILESIZE * 6,	get_sprite(0, TILESIZE * 2, TILESIZE * 4, TILESIZE, ss_ui),'Quit')

			if is_pressed(mouse()[0], mouse()[1], resume[1]):
				game.play()
			if is_pressed(mouse()[0], mouse()[1], load[1]):
				print ('click')
			if is_pressed(mouse()[0], mouse()[1], quit[1]):
				game.menu()

			self.screen.blit(menu_background, (0, 0))
			self.screen.blit(title, title_rect)

			self.screen.blit(resume[0],	resume[1])
			self.screen.blit(resume[2],	resume[3])
			self.screen.blit(load[0],	load[1])
			self.screen.blit(load[2],	load[3])
			self.screen.blit(quit[0],	quit[1])
			self.screen.blit(quit[2],	quit[3])

			self.clock.tick(FPS)
			pygame.display.update()

	# options menu
	def options(self):
		pass

	# save/load
	def save_load():
		pass

	# main menu
	def menu(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			image_path = pygame.image.load('graphics/img/menu_background.png')
			menu_background = pygame.transform.scale(image_path, (WIDTH,HEIGTH))
			title = self.font.render('Main Menu', True, black)
			title_rect = title.get_rect(x=TILESIZE, y=10)

			new		= button(TILESIZE, TILESIZE * 2, get_sprite(0, TILESIZE * 2, TILESIZE * 4,TILESIZE, ss_ui),'New Game')
			load	= button(TILESIZE, TILESIZE * 4, get_sprite(0, TILESIZE * 2, TILESIZE * 4,TILESIZE, ss_ui),'Save/Load')
			exit	= button(TILESIZE, TILESIZE * 6, get_sprite(0, TILESIZE * 2, TILESIZE * 4,TILESIZE, ss_ui),'Exit')

			
			if is_pressed(mouse()[0], mouse()[1], new[1]):
				game.play()
			if is_pressed(mouse()[0], mouse()[1], load[1]):
				print ('click')
			if is_pressed(mouse()[0], mouse()[1], exit[1]):
				pygame.quit()
				sys.exit()

			self.screen.blit(menu_background,(0, 0))
			self.screen.blit(title, title_rect)
			self.screen.blit(new[0], new[1])
			self.screen.blit(new[2], new[3])
			self.screen.blit(load[0], load[1])
			self.screen.blit(load[2], load[3])
			self.screen.blit(exit[0], exit[1])
			self.screen.blit(exit[2], exit[3])

			self.clock.tick(FPS)
			pygame.display.update()

	# title screen
	def title(self):
		maxy = HEIGTH
		i = 0
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0]:
					game.menu()

			image_path = pygame.image.load('graphics/img/titlescreen.png')
			titlescreen = pygame.transform.scale(image_path, (WIDTH,HEIGTH*2))

			self.screen.fill('black')
			self.screen.blit(titlescreen,(0,-i))

			if i == maxy:
				self.screen.blit(titlescreen,(0,maxy))
				i = maxy - 5
				
			i += 5


			title = self.font.render('Press any key to continue', True, black)
			title_rect = title.get_rect(x=TILESIZE, y=300)

			self.screen.blit(title, title_rect)

			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.title()