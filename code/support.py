import pygame
from settings import *
from csv import reader
from os import walk

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
			sprite.blit(sheet, (0,0), (width *i, height * j, width, height))
			sprite.set_colorkey(black)  # sprite_background off
			surface_list.append(sprite)
			i +=1
	return surface_list
	
# get sprite
def get_sprite(x,y,width,height,path):
	sheet = pygame.image.load(path).convert_alpha() 
	sprite = pygame.Surface([width, height])
	sprite.blit(sheet,(0,0), (x, y, width, height))
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

# tile class
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
			self.hitbox = self.rect.inflate(0,-20)
		elif sprite_type == 'world1':
			self.rect = self.image.get_rect(topleft = pos)
			self.hitbox = self.rect	
		else:
			self.rect = self.image.get_rect(topleft = pos)
			self.hitbox = self.rect.inflate(0,-10)

# entity class
class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pygame.math.Vector2()
	# moves the sprite
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
	
	# detects collisions
	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

