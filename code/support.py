from csv import reader
from os import walk
import pygame
from settings import *

# import csv
def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

# import folder
def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

# import animations
def import_animations(sheet,width,height,frames,j):
	surface_list = []
	i = 0
	while i <= frames:
			sprite = pygame.Surface([width, height])
			sprite.blit(sheet, (0,0), (width * i, height * j, width, height))
			sprite.set_colorkey(black)  # sprite_background off
			surface_list.append(sprite)
			i +=1
	return surface_list

	

# get sprite
def get_sprite(x,y,width,height,path):
	sheet = pygame.image.load(path).convert_alpha() 
	sprite = pygame.Surface([width, height])
	sprite.blit(sheet, (0, 0), (x, y, width, height))
	sprite.set_colorkey(black)  # sprite_background off

	return sprite

# create butten
def button(x,y,sprite,content):
	button = []
	rect = sprite.get_rect()
	rect.x = x
	rect.y = y
	width = rect.width
	height = rect.height

	font = pygame.font.Font('graphics/font/Pixel.ttf', 20)
	text = font.render(content, True, black)
	text_rect = text.get_rect(center=(x + (width / 2), (height / 2) + y))

	button.append(sprite)
	button.append(rect)
	button.append(text)
	button.append(text_rect)

	return button

# check if pressed
def is_pressed(pos, pressed, rect):
	if rect.collidepoint(pos):
		if pressed[0]:
			return True
		return False
	return False

# get mouse states
def mouse():
	mouse =[]
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()

	mouse.append(mouse_pos)
	mouse.append(mouse_pressed)

	return mouse
