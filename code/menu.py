import pygame, sys
from settings import *
from support import *

class MainMenu():
	def __init__(self):
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
			options	= button(TILESIZE, TILESIZE * 6, get_sprite(0, TILESIZE * 2, TILESIZE * 4,TILESIZE, ss_ui),'Options')
			exit	= button(TILESIZE, TILESIZE * 8, get_sprite(0, TILESIZE * 2, TILESIZE * 4,TILESIZE, ss_ui),'Exit')

			
			if is_pressed(mouse()[0], mouse()[1], new[1]):
				self.playing = True
				game.play()
			if is_pressed(mouse()[0], mouse()[1], load[1]):
				print ('click')
			if is_pressed(mouse()[0], mouse()[1], options[1]):
				game.options()
			if is_pressed(mouse()[0], mouse()[1], exit[1]):
				pygame.quit()
				sys.exit()

			self.screen.blit(menu_background,(0, 0))
			self.screen.blit(title, title_rect)
			self.screen.blit(new[0], new[1])
			self.screen.blit(new[2], new[3])
			self.screen.blit(load[0], load[1])
			self.screen.blit(load[2], load[3])
			self.screen.blit(options[0], options[1])
			self.screen.blit(options[2], options[3])
			self.screen.blit(exit[0], exit[1])
			self.screen.blit(exit[2], exit[3])

			self.clock.tick(FPS)
			pygame.display.update()
