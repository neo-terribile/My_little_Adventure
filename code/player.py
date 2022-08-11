import pygame 
from settings import *
from support import *
from debug import debug


class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
		super().__init__(groups)
		self.image = get_sprite(0,TILESIZE * 9,TILESIZE,TILESIZE,ss_player)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-20)

		# graphics setup
		self.import_player_assets()
		self.status = 'south'

		# movement 
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites

		# weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200

		# magic 
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		# stats
		self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
		self.health = self.stats['health'] * 0.8
		self.energy = self.stats['energy'] * 0.2
		self.speed = self.stats['speed']
		self.exp = 123

		# loot
		self.gold = 0


	# import player assets
	def import_player_assets(self):
		sheet = pygame.image.load(ss_player).convert_alpha()
		self.animations =	{'north': [],'south': [],'west': [],'east': [],
							'northeast': [],'northwest': [],'southeast': [], 'southwest': [],
							'north_idle':[],'south_idle':[],'west_idle':[],'east_idle':[],
							'northeast_idle':[],'northwest_idle':[],'wsoutheast_idle':[],'esouthwest_idle':[],
							'north_attack':[],'south_attack':[],'west_attack':[],'east_attack':[],
							'northeast_attack':[],'northwest_attack':[],'southeast_attack':[],'southwest_attack':[]}
		j = 0
		for animation in self.animations.keys():
			self.animations[animation] = import_animations(sheet,TILESIZE,TILESIZE,3,j)
			j += 1

		
		#for animation in self.animations.keys():
		#	if animation == 'north'					: j = 0
		#	if animation == 'south'					: j = 1
		#	if animation == 'west'					: j = 2
		#	if animation == 'east'					: j = 3
		#
		#	if animation == 'northeast'				: j = 4
		#	if animation == 'northwest'				: j = 5
		#	if animation == 'southeast'				: j = 6
		#	if animation == 'southwest'				: j = 7
		#
		#	if animation == 'north_attack'			: j = 8
		#	if animation == 'south_attack'			: j = 9
		#	if animation == 'west_attack'			: j = 10
		#	if animation == 'east_attack'			: j = 11
		#
		#	if animation == 'northeast_attack'		: j = 12
		#	if animation == 'northwest_attack'		: j = 13
		#	if animation == 'southeast_attack'		: j = 14
		#	if animation == 'southwest_attack'		: j = 15
		#
		#	if animation == 'north_idle'			: j = 16
		#	if animation == 'south_idle'			: j = 17
		#	if animation == 'west_idle'				: j = 18
		#	if animation == 'east_idle'				: j = 19
		#		
		#	if animation == 'northeast_idle'		: j = 20
		#	if animation == 'northwest_idle'		: j = 21
		#	if animation == 'southeast_idle'		: j = 22
		#	if animation == 'southwest'				: j = 23
		#
		#	self.animations[animation] = import_animations(sheet,TILESIZE,TILESIZE,3,j)

	# player input
	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_UP]:
				if keys[pygame.K_RIGHT]:
					self.direction.x = 1
					self.direction.y = -1
					self.status = 'northeast'
				elif keys[pygame.K_LEFT]:
					self.direction.x = -1
					self.direction.y = -1
					self.status = 'northwest'
				else:
					self.direction.x = 0
					self.direction.y = -1
					self.status = 'north'

			elif keys[pygame.K_DOWN]:
				if keys[pygame.K_RIGHT]:
					self.direction.x = 1
					self.direction.y = 1
					self.status = 'southeast'
				elif keys[pygame.K_LEFT]:
					self.direction.x = -1
					self.direction.y = 1
					self.status = 'southwest'
				else:
					self.direction.x = 0
					self.direction.y = 1
					self.status = 'south'

			else:	self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				if keys[pygame.K_UP]:
					self.direction.x = 1
					self.direction.y = -1
					self.status = 'northeast'
				elif keys[pygame.K_DOWN]:
					self.direction.x = 1
					self.direction.y = 1
					self.status = 'southeast'
				else:
					self.direction.x = 1
					self.direction.y = 1
					self.status = 'east'

			elif keys[pygame.K_LEFT]:
				if keys[pygame.K_UP]:
					self.direction.x = -1
					self.direction.y = -1
					self.status = 'northwest'
				elif keys[pygame.K_DOWN]:
					self.direction.x = -1
					self.direction.y = 1
					self.status = 'southwest'
				else:
					self.direction.x = -1
					self.direction.y = 1
					self.status = 'west'
			else:
				self.direction.x = 0

			# attack input 
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()

			# magic input 
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style,strength,cost)

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
					
				self.weapon = list(weapon_data.keys())[self.weapon_index]

			if keys[pygame.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				
				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0

				self.magic = list(magic_data.keys())[self.magic_index]

	# get player status
	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	# cooldowns
	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True

		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				self.can_switch_magic = True

	# animate player
	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
	
	# update player
	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)