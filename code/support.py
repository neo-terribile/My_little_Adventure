from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def get_image(x,y,width,height):
	def __init__(self):
		self.sheet = pygame.image.load('graphics/player/ui.png').convert()
		self.sprite = pygame.Surface([width, height])
		self.sprite.blit(self.sheet, (0, 0), (x, y, width, height))
		self.sprite.set_colorkey(black)  # sprite_background off
		return self.sprite
