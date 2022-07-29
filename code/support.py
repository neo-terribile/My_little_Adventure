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

def get_sprite(x,y,width,height,path):
	sheet = pygame.image.load(path).convert_alpha() 
	sprite = pygame.Surface([width, height])
	sprite.blit(sheet, (0, 0), (x, y, width, height))
	sprite.set_colorkey('black')  # sprite_background off

	return sprite

def button(x,y,sprite):
	button = []
	rect = sprite.get_rect()
	rect.x = x
	rect.y = y

	button.append(sprite)
	button.append(rect)
	
	return button

def is_pressed(pos, pressed, rect):
	if rect.collidepoint(pos):
		if pressed[0]:
			return True
		return False
	return False
