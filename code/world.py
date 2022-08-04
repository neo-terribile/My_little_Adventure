import pygame 
from settings import *
from support import *
from random import choice
from player import Player
from enemy import Enemy
from npc import NPC
from weapon import Weapon
from ui import UI


# creates World
class World:
	def __init__(self):
		# get the display surface 
		self.screen = pygame.display.get_surface()
		self.lvl = 'hometown'

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.player_sprite = pygame.sprite.Group()
		self.enemie_sprites = pygame.sprite.Group()
		self.trigger_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		# sprite setup
		self.create_map()
		# user interface 
		self.ui = UI()

	# create map
	def create_map(self):	
		layouts = {
			'block': import_csv_layout('maps/' + self.lvl + '/' + self.lvl + '_blocks.csv'),
			'grass': import_csv_layout('maps/' + self.lvl + '/' + self.lvl + '_grass.csv'),
			'object': import_csv_layout('maps/' + self.lvl + '/' + self.lvl + '_objects.csv'),
			'entities': import_csv_layout('maps/' + self.lvl + '/' + self.lvl + '_entities.csv')}
		graphics = {
			'grass': import_folder('graphics/grass'),
			'objects': import_folder('graphics/objects')}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'block':
							if col == '0': Tile((x,y),[self.obstacle_sprites],'invisible')
							else:
								if col == '1': Tile((x,y),[self.trigger_sprites],'world1')
								elif col == '2':
									pass
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
						if style == 'entities':
							if col == '0':
								if len(self.player_sprite) == 0:
									self.player = Player(
										(x,y),
										[self.visible_sprites,
										self.player_sprite],
										self.obstacle_sprites,
										self.create_attack,
										self.remove_attack,
										self.create_magic)
								else:
									self.player.hitbox.x = x
									self.player.hitbox.y = y	


							else:
								if col == '1': monster_name = 'bamboo'
								elif col == '2': monster_name = 'spirit'
								elif col == '3': monster_name ='raccoon'
								else: monster_name = 'squid'
								Enemy(monster_name,
								(x,y),
								[self.visible_sprites],
								self.obstacle_sprites)

	# create attack
	def create_attack(self):	
		self.current_attack = Weapon(self.player,[self.visible_sprites])

	# remove attack
	def remove_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	# create magic
	def create_magic(self,style,strength,cost):
		print(style)
		print(strength)
		print(cost)

	# remove magic magic
	def remove_magic(self):
		if self.current_magic:
			self.current_magic.kill()
		self.current_magic = None

	# change map
	def change_map(self,level):
		self.lvl = level
		for sprite in self.obstacle_sprites:
			sprite.kill()
		for sprite in self.trigger_sprites:
			sprite.kill()

		self.create_map()


	# player interactions
	def player_interactions(self):
		if self.trigger_sprites:
			for player_sprite in self.player_sprite:
				collision_sprites = pygame.sprite.spritecollide(player_sprite,self.trigger_sprites,False)
				for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'world1':
							self.change_map(target_sprite.sprite_type)

	# update and draw the game
	def run(self):
		self.visible_sprites.custom_draw(self.player,self.lvl)
		self.visible_sprites.update()
		self.visible_sprites.enemy_update(self.player)
		self.player_interactions()
		self.ui.display(self.player)

# sorts the sprites for 3D effect
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup 
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.half_width = self.screen.get_size()[0] // 2
		self.half_height = self.screen.get_size()[1] // 2
		self.offset = pygame.math.Vector2()


	# creating the floor
		self.hometown_surf = pygame.image.load('maps/hometown/hometown.png').convert()
		self.hometown_rect = self.hometown_surf.get_rect(topleft = (0,0))

		self.world1_surf = pygame.image.load('maps/world1/world1.png').convert()
		self.world1_rect = self.world1_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player,level):
		self.lvl = level

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		if self.lvl == 'hometown':
			hometown_offset_pos = self.hometown_rect.topleft - self.offset
			self.screen.blit(self.hometown_surf,hometown_offset_pos)

		if self.lvl == 'world1':
			world1_offset_pos = self.world1_rect.topleft - self.offset
			self.screen.blit(self.world1_surf,world1_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image,offset_pos)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)