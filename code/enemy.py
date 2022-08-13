import pygame
from settings import *
from support import *

class Enemy(Entity):
	def __init__(self,monster_name,monster_moves,pos,groups,obstacle_sprites):

		# general setup
		super().__init__(groups)
		self.sprite_type = 'enemy'

		# graphics setup
		self.import_graphics(monster_name,monster_moves)
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]

		# movement
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites

		# player interaction
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
	
	# import graphics
	def import_graphics(self,name,moves):
		sheet = pygame.image.load(name + '.png').convert_alpha()
		self.animations = moves

		j = 0
		for animation in self.animations.keys():
			self.animations[animation] = import_animations(sheet,TILESIZE,TILESIZE*2,3,j)
			j += 1

	def get_player_distance_direction(self,player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self,player):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			print('attack')
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def cooldown(self):
		if not self.can_attack:
			current_time = pygame.time.get_ticks()
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

	def update(self):
		self.move(self.speed)
		self.animate()
		self.cooldown()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)

class Blob(Enemy):
	def __init__(self,pos,groups,obstacle_sprites):
		monster_name = 'blob'
		monster_move = {'idle':[],'move':[],'attack': []}
		super().__init__(monster_name,monster_move,pos,groups,obstacle_sprites)
		self.health = 10
		self.exp = 10
		self.speed = 3
		self.attack_damage = 1
		self.resistance = 0
		self.attack_radius = TILESIZE * 2
		self.notice_radius = TILESIZE * 4
		self.attack_type = 'basic'

class Rat(Enemy):
	def __init__(self,pos,groups,obstacle_sprites):
		monster_name = 'rat'
		monster_move = {'north': [],'south': [],'west': [],'east': [],
						'northeast': [],'northwest': [],'southeast': [], 'southwest': [],
						'north_attack':[],'south_attack':[],'west_attack':[],'east_attack':[],
						'northeast_attack':[],'northwest_attack':[],'southeast_attack':[],'southwest_attack':[],
						'north_idle':[],'south_idle':[],'west_idle':[],'east_idle':[],
						'northeast_idle':[],'northwest_idle':[],'southeast_idle':[],'southwest_idle':[]}
		super.__init__(monster_name,monster_move,pos,groups,obstacle_sprites)
		self.health = 10
		self.exp = 10
		self.speed = 3
		self.attack_damage = 1
		self.resistance = 0
		self.attack_radius = TILESIZE * 2
		self.notice_radius = TILESIZE * 4
		self.attack_type = 'basic'