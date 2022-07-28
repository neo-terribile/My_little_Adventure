import pygame, sys
from settings import *
from support import *
from debug import debug
from world import World
from ui import Button

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font('graphics/font/Pixel.ttf', 32)
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_pressed = pygame.mouse.get_pressed()

		self.level = World()
	
	def play(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

	def menu(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			image_path = pygame.image.load('graphics/img/menu_background.png')
			self.menu_background = pygame.transform.scale(image_path, (WIDTH,HEIGTH))
			title = self.font.render('Main Menu', True, black)
			title_rect = title.get_rect(x=10, y=10)

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			play_button = Button(50, 100, 250, 50, white, black, 'Start Game', 20)
			load_button = Button(50, 200, 250, 50, white, black, 'Load Game', 20)
			options_button = Button(50, 300, 250, 50, white, black, 'Options', 20)
			credits_button = Button(50, 400, 250, 50, white, black, 'Credits', 20)
			exit_button = Button(50, 500, 250, 50, white, black, 'Exit Game', 20)
			
			if play_button.is_pressed(mouse_pos, mouse_pressed):
				game.play()
			if load_button.is_pressed(mouse_pos, mouse_pressed):
				pass
			if exit_button.is_pressed(mouse_pos, mouse_pressed):
				pygame.quit()
				sys.exit()
			
			self.screen.blit(self.menu_background, (0, 0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.screen.blit(load_button.image, load_button.rect)
			self.screen.blit(options_button.image, options_button.rect)
			self.screen.blit(credits_button.image, credits_button.rect)
			self.screen.blit(exit_button.image, exit_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

	def title(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN or  pygame.mouse.get_pressed()[0]:
					game.menu()

			self.screen.fill('black')

			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.title()