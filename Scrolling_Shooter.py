
import pygame
import random
from pygame import JOYDEVICEADDED, JOYDEVICEREMOVED, mixer
import csv
import button


#intitialize pygame
pygame.init()
mixer.init()
pygame.joystick.init()

#constants for game screen
SCREEN_WIDTH = 950
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#Create game screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Side Scroller")

clock = pygame.time.Clock()
FPS = 60

#Define game variables
GRAVITY = 0.5
SCROLL_THRESH = 300
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 24
MAX_LEVELS = 5
screen_scroll = 0
bg_scroll = 0
level = 1
choice = 0
game_state = "main_menu"
show_credits = False
start_game = False
player_alive = True
menu_music = False
level1_music = False
level2_music = False
level3_music = False
level4_music = False
level5_music = False
death_music = False
start_intro = False
controller = None
controllers = []

#Define player action variables
moving_left = False
moving_right = False
jump = False
crouching = False
shoot = False
grenade = False
grenade_thrown = False

#Define colors
BG = (144,201,120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
PINK = (235, 65,54)
BLUE = (0,0,255)
YELLOW = (255, 255, 0);

#DEFINE FONT
font = pygame.font.SysFont('Futura', 30)
stat_font = pygame.font.SysFont('Futura', 25)
char_select_font = pygame.font.SysFont('Futura', 100)

#LOAD SOUND FX
jump_fx = pygame.mixer.Sound("Assets/Audio/jump.wav")
pygame.mixer.music.set_volume(0.4)
shot_fx = pygame.mixer.Sound("Assets/Audio/shot.wav")
pygame.mixer.music.set_volume(0.4)
grenade_fx = pygame.mixer.Sound("Assets/Audio/grenade.wav")
pygame.mixer.music.set_volume(0.4)


#LOAD IMAGES
#load images for soliders
black_soldier = pygame.image.load("Assets/Images/Sprites/Black_Soldier.png").convert_alpha()
blue_soldier = pygame.image.load("Assets/Images/Sprites/Blue_Soldier.png").convert_alpha()
green_soldier = pygame.image.load("Assets/Images/Sprites/Green_Soldier.png").convert_alpha()
red_soldier = pygame.image.load("Assets/Images/Sprites/Red_Soldier.png").convert_alpha()
yellow_soldier = pygame.image.load("Assets/Images/Sprites/Yellow_Soldier.png").convert_alpha()
#feed into a list for choosing

soldiers = [black_soldier, blue_soldier, green_soldier, red_soldier, yellow_soldier]
animation_steps = [5, 6, 2, 3, 8]
playerChar = soldiers[0]
enemies = []


#load images for tiles
image_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Assets/Tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
    image_list.append(img)
    
#Load images for buttons
start_button_img = pygame.image.load("Assets/Images/Buttons/start.png").convert_alpha()
credits_button_img = pygame.image.load("Assets/Images/Buttons/credits.png").convert_alpha()
exit_button_img = pygame.image.load("Assets/Images/Buttons/exit.png").convert_alpha()
restart_button_img = pygame.image.load("Assets/Images/Buttons/restart.png").convert_alpha()
black_soldier_btn_img = pygame.image.load("Assets/Images/Buttons/Black_Soldier_Button.png").convert_alpha()
blue_soldier_btn_img = pygame.image.load("Assets/Images/Buttons/Blue_Soldier_Button.png").convert_alpha()
green_soldier_btn_img = pygame.image.load("Assets/Images/Buttons/Green_Soldier_Button.png").convert_alpha()
red_soldier_btn_img = pygame.image.load("Assets/Images/Buttons/Red_Soldier_Button.png").convert_alpha()
yellow_soldier_btn_img = pygame.image.load("Assets/Images/Buttons/Yellow_Soldier_Button.png").convert_alpha()

#Load images for background
pine1_img = pygame.image.load("Assets/Images/Background/pine1.png").convert_alpha() 
pine2_img = pygame.image.load("Assets/Images/Background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("Assets/Images/Background/mountain.png").convert_alpha()
sky_img = pygame.image.load("Assets/Images/Background/sky_cloud.png").convert_alpha()
#Load image for bullet
bullet_img = pygame.image.load("Assets/Weapons/bullet.png").convert_alpha()
#Load image for grenade
grenade_img = pygame.image.load("Assets/Weapons/grenade.png").convert_alpha()
#Load images for item pick-ups
health_box_img = pygame.image.load("Assets/Pick_ups/health_box.png").convert_alpha()
ammo_box_img = pygame.image.load("Assets/Pick_ups/ammo_box.png").convert_alpha()
grenade_box_img = pygame.image.load("Assets/Pick_ups/grenade_box.png").convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
    }

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y)) 
    
def draw_box(xsize, ysize, alpha, color, xpos, ypos):
    rect = pygame.Surface((xsize, ysize), pygame.SRCALPHA)
    rect.set_alpha(alpha)
    rect.fill(color)
    screen.blit(rect, (xpos, ypos))

def draw_background():
    screen.fill(BG) 
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img,((x * width) - bg_scroll * 0.3,0))
        screen.blit(mountain_img,((x * width) - bg_scroll * 0.4, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img,((x * width) - bg_scroll * 0.5, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img,((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - pine1_img.get_height() - 75))
    
def draw_inventory():
    #Show ammo
    draw_text('AMMO: ', font, WHITE, 10, 35)
    for x in range(player.ammo):
        screen.blit(bullet_img,(90 + (x * 10), 39))
    draw_text('GRENADES: ', font, WHITE, 10, 60)
    #Show grenades
    for x in range(player.grenades):
        screen.blit(grenade_img,(135 + (x * 15), 61))
    draw_text('ENEMIES: ' + str(len(enemy_group)), font, RED,10, 80)
    
#function to reset level
def reset_level():
    enemy_group.empty()
    basic_enemy_group.empty()
    grenadier_enemy_group.empty()
    elite_enemy_group.empty()
    boss_enemy_group.empty()
    player_bullet_group.empty()
    enemy_bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
   
    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
        
    return data

def play_game(choice):
    start_game = True
    start_intro = True
    playerChar = soldiers.pop(choice)
    enemies = draw_enemies(soldiers)
    world = World(playerChar, enemies)
    player, player_health_bar = world.process_data(world_data)
    
    return start_game, start_intro, playerChar, enemies, world, player, player_health_bar 

def draw_enemies(soldiers):
    enemy_list = soldiers
    enemies_shuffled = []

    basic_enemy_char = enemy_list.pop(random.randint(0,3))
    enemies_shuffled.append(basic_enemy_char)
    grenadier_enemy_char = enemy_list.pop(random.randint(0,2))
    enemies_shuffled.append(grenadier_enemy_char)
    elite_enemy_char = enemy_list.pop(random.randint(0,1))
    enemies_shuffled.append(elite_enemy_char)
    boss_char = enemy_list[0]
    enemies_shuffled.append(boss_char)
    
    
    return enemies_shuffled

def get_keyboard_input(controller, crouching, moving_left, moving_right, shoot, grenade, grenade_thrown, jump, play, player, game_state,show_credits):
    #player = player
    controller = controller
    for event in pygame.event.get():
        
        if event.type == JOYDEVICEADDED:
            controller = pygame.joystick.Joystick(event.device_index)
            controllers.append(controller)
            #print(controllers)
        if event.type == JOYDEVICEREMOVED:
            controller = None
            controllers.clear()

    #Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                crouching = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_g:
                grenade = True    
            if event.key == pygame.K_w and player.alive:
                player.jump = False

                    
                
                
            if event.key == pygame.K_ESCAPE:
                if show_credits:
                    game_state = "main_menu"
                    show_credits = False
                else:
                    play = False
                
        #Keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                crouching = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_g:
                grenade = False  
                grenade_thrown = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                player.jump_count += 1
           
        if event.type == pygame.QUIT:
            play = False
        if controller is not None:
            crouching, moving_left, moving_right, shoot, grenade, grenade_thrown = get_game_pad_input(controllers[0], crouching, moving_left, moving_right, shoot, grenade, grenade_thrown, player)

    return controller, crouching, moving_left, moving_right, shoot, grenade, grenade_thrown, jump, play, game_state, show_credits

def get_game_pad_input(controller, crouching, moving_left, moving_right, shoot, grenade, grenade_thrown, player):
   # print(player.jump_count, player.jump, player.double_jump)
    if controller is not None:        
        horiz_move = controller.get_axis(0)
        if controller.get_button(1):
            crouching = True
        if controller.get_button(1) == 0:
            crouching = False    
        if horiz_move < -0.5:
                moving_left = True  
        if horiz_move > 0.5:
                moving_right = True   
        if horiz_move <= 0.5 and horiz_move >= -0.5:
                moving_right = False
                moving_left = False
        if controller.get_button(2):    
                shoot = True
        if controller.get_button(2) == 0:
                shoot = False
        if controller.get_button(3):
                grenade = True
        if  controller.get_button(3) == 0:
                grenade = False
                grenade_thrown = False  
        return crouching, moving_left, moving_right, shoot, grenade, grenade_thrown
    
def show_controls(controller):
    draw_box(210,150, 125, WHITE, 390, 45)
    if controller is not None:
        draw_text("MOVE - Left Analog",font, BLACK, 400, 50)
        draw_text("JUMP - A",font, BLACK, 400, 80)
        draw_text("CROUCH - B",font, BLACK, 400, 110)
        draw_text("SHOOT - X",font, BLACK, 400, 140)
        draw_text("GRENADE - Y",font, BLACK, 400, 170)
    else:
        draw_text("MOVE - < A D >", font, BLACK, 400, 50)
        draw_text("JUMP - W", font, BLACK, 400, 80)
        draw_text("CROUCH - C", font, BLACK, 400, 110)
        draw_text("SHOOT - SPACEBAR", font, BLACK, 400, 140)
        draw_text("GRENADE - G", font, BLACK, 400, 170)

def show_current_level():
    draw_text("Level " + str(level), font, BLACK, 460, 20)

          ##########   SOLDIER CLASS   ##########
    
def draw_char_stats():
    draw_text("Health ==",stat_font,BLACK, SCREEN_WIDTH // 2 - 460, SCREEN_HEIGHT // 2 - 160)
    draw_text("Ammo ++",stat_font,BLACK, SCREEN_WIDTH // 2 - 460, SCREEN_HEIGHT // 2 - 140)
    draw_text("Grenades --",stat_font,BLACK, SCREEN_WIDTH // 2 - 460, SCREEN_HEIGHT // 2 - 120)
    draw_text("Speed ==",stat_font,BLACK, SCREEN_WIDTH // 2 - 460, SCREEN_HEIGHT // 2 - 100)
    draw_text("Health ==",stat_font,BLUE, SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 160)
    draw_text("Ammo --",stat_font,BLUE, SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 140)
    draw_text("Grenades ++",stat_font,BLUE, SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 120)
    draw_text("Speed ==",stat_font,BLUE, SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 100)
    draw_text("Health ++",stat_font,GREEN, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 160)
    draw_text("Ammo ==",stat_font,GREEN, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 140)
    draw_text("Grenades ==",stat_font,GREEN, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 120)
    draw_text("Speed ==",stat_font,GREEN, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 100)
    draw_text("Health ==",stat_font,RED, SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 - 160)
    draw_text("Ammo ==",stat_font,RED, SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 - 140)
    draw_text("Grenades ==",stat_font,RED, SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 - 120)
    draw_text("Speed ==",stat_font,RED, SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 - 100)
    draw_text("Health ==",stat_font,YELLOW, SCREEN_WIDTH // 2 + 340, SCREEN_HEIGHT // 2 - 160)
    draw_text("Ammo ==",stat_font,YELLOW, SCREEN_WIDTH // 2 + 340, SCREEN_HEIGHT // 2 - 140)
    draw_text("Grenades ==",stat_font,YELLOW, SCREEN_WIDTH // 2 + 340, SCREEN_HEIGHT // 2 - 120)
    draw_text("Speed ++",stat_font,YELLOW, SCREEN_WIDTH // 2 + 340, SCREEN_HEIGHT // 2 - 100)
    
def draw_credits():
    draw_box(500, 620, 175, WHITE, SCREEN_WIDTH//2 - 250 , SCREEN_HEIGHT//2 - 300)
    draw_text("Final Design and Development:", stat_font, BLACK, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 280)
    draw_text("Cornelius Holt", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 250)
    draw_text("Artists:", stat_font, BLACK,SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 210)
    draw_text("Characters: Secret Hideout", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 180)
    draw_text("Backgrounds: sanctumpixel", stat_font,BLUE,SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 150)
    draw_text("Tileset: Eray Zesen", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 120)
    draw_text("Audio:", stat_font, BLACK, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 80)
    draw_text("BulletSound: Mike Koenig", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 50)
    draw_text("Music:", stat_font, BLACK, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 10)
    draw_text("DOS88", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 20)
    draw_text("MENU - Song Title: Raging Inferno", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 50)
    draw_text("LEVEL 1 - Song Title: Main Objective", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 75)
    draw_text("LEVEL 2 - Song Title: Race to Mars", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 100)
    draw_text("LEVEL 3 - Song Title: Fight to Win", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 125)
    draw_text("LEVEL 4 - Song Title: Underground Concourse", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 150)
    draw_text("LEVEL 5 - Song Title: Critical Hit", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 175)
    draw_text("Death - Song Title: Liquid Metal", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 200)
    draw_text("Honorable Mention for Inital Tutorial", stat_font,BLACK, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 225)
    draw_text("& TIles For Pick-Ups:", stat_font,BLACK, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 255) 
    draw_text("CodingWithRuss", stat_font, BLUE, SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 + 285)

def play_background_music(player_alive, menu_music, level1_music, level2_music, level3_music, level4_music, level5_music, death_music):
    if player_alive:
        if not start_game:
            if level1_music or level2_music or level3_music or level4_music or level5_music or death_music:
                pygame.mixer.music.unload()
                level_music = False  
                death_music = False
            if not pygame.mixer.music.get_busy():           
                pygame.mixer.music.load("Assets/Audio/BackgroundMusic/RagingInferno.mp3")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                menu_music = True  
        else:
            if level == 1:
                if menu_music or death_music:
                    pygame.mixer.music.unload()
                    menu_music = False
                    death_music = False
                if not pygame.mixer.music.get_busy():     
                        pygame.mixer.music.load("Assets/Audio/BackgroundMusic/MainObjective.mp3")
                        pygame.mixer.music.play(-1,0.0,5)
                        pygame.mixer.music.set_volume(0.3)
                        level1_music = True   
            if level == 2:
                if menu_music or death_music or level1_music:
                    pygame.mixer.music.unload()
                    menu_music = False
                    death_music = False
                    level1_music = False
                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load("Assets/Audio/BackgroundMusic/RacetoMars.wav")
                        pygame.mixer.music.play(-1,0.0,5)
                        pygame.mixer.music.set_volume(0.3)
                        level2_music = True 
            if level == 3:
                if menu_music or death_music or level2_music:
                    pygame.mixer.music.unload()
                    menu_music = False
                    death_music = False
                    level2_music = False
                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load("Assets/Audio/BackgroundMusic/FighttoWIn.mp3")
                        pygame.mixer.music.play(-1,0.0,5)
                        pygame.mixer.music.set_volume(0.3)
                        level3_music = True            
            if level == 4:
                if menu_music or death_music or level3_music:
                    pygame.mixer.music.unload()
                    menu_music = False
                    death_music = False
                    level3_music = False
                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load("Assets/Audio/BackgroundMusic/UndergroundConcourse.mp3")
                        pygame.mixer.music.play(-1,0.0,5)
                        pygame.mixer.music.set_volume(0.3)
                        level4_music = True              
            if level == 5:
                if menu_music or death_music or level4_music:
                    pygame.mixer.music.unload()
                    menu_music = False
                    death_music = False
                    level4_music = False
                if not pygame.mixer.music.get_busy():    
                        pygame.mixer.music.load("Assets/Audio/BackgroundMusic/Critical Hit.mp3")
                        pygame.mixer.music.play(-1,0.0,5)
                        pygame.mixer.music.set_volume(0.3)
                        level5_music = True 
    else:
        if level1_music or level2_music or level3_music or level4_music or level5_music:
            pygame.mixer.music.unload()
            level_music = False
            menu_music = False
            level1_music = False
            level2_music = False
            level3_music = False
            level4_music = False
            level5_music = False 
        if not pygame.mixer.music.get_busy():    
                pygame.mixer.music.load("Assets/Audio/BackgroundMusic/LiquidMetal.mp3")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                death_music = True
    
    return player_alive, menu_music, level1_music, level2_music, level3_music, level4_music, level5_music, death_music

class Soldier(pygame.sprite.Sprite):
    def __init__(self, player, sprite_sheet, x, y, scale, animation_steps, health, speed, ammo, grenades):    
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.x = x
        self.y = y
        self.speed = speed
        self.shoot_cooldown = 0
        self.flip = False
        self.direction = 1
        self.scale = scale
        self.size = 48
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.max_ammo = ammo
        self.max_grenades = grenades
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.update_time = pygame.time.get_ticks()
        #will determine animation #0:idle 1:Run 2:Jump 3:Crouch 4:Death
        self.action = 0
        self.frame_index = 0
        image = self.animation_list[self.action][self.frame_index]
        self.image = pygame.transform.scale(image, (self.size * self.scale, self.size * self.scale))
        self.width = 32 * self.scale 
        self.height = 32 * self.scale 
        self.rect = self.image.get_rect(size=(self.width - 22 ,self.height),center=(x,y))
        self.running = False
        self.jump = False
        self.in_air = False
        self.double_jump = True
        self.jump_count = 0
        self.health = health
        self.max_health = self.health
        self.alive = True
        self.vel_y = 0
        #AI Variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.rect.Rect(0,0,150,20)
        self.boss_vision = pygame.rect.Rect(0,0,500,20)
        #variable for deleting ai after death
        self.death_count = 100
        self.throw_cooldown = 0
        
    def load_images(self, sprite_sheet, animation_steps):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size * self.scale, self.size * self.scale)))   
            animation_list.append(temp_img_list)       
        return animation_list
    
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1
        if self.health >= self.max_health:
            self.health = self.max_health
          
    def move(self, moving_left, moving_right, controller): 
        screen_scroll = 0
        dx = 0
        dy = 0
        self.running = False

        if crouching == False:
            #movement
            if moving_left:
                dx = -self.speed
                self.running = True
                self.flip = True
                self.direction = -1
            
            if moving_right:
                dx = self.speed
                self.running = True
                self.flip = False
                self.direction = 1
            #jump
            if self.player and self.alive: 
                    if pygame.key.get_pressed()[pygame.K_w] and self.jump == False and self.in_air == False:
                        self.vel_y = -11  
                        self.in_air = True
                        self.jump = True
                        jump_fx.play()
                    elif pygame.key.get_pressed()[pygame.K_w] and self.jump_count == 1 and self.double_jump:
                        self.vel_y = -11  
                        self.in_air = True
                        self.double_jump = False
                        jump_fx.play()
                    elif self.jump_count > 2:
                        self.jump = False
                        self.double_jump = False
                    if controller is not None:   
                       if controller.get_button(0) and self.jump == False and self.in_air == False:
                            self.vel_y = -11  
                            self.in_air = True     
                            jump_fx.play()
                       elif controller.get_button(0) == 0:
                           self.jump = True   
                       elif controller.get_button(0) and self.in_air and self.jump  and self.double_jump:
                            self.vel_y = -11  
                            self.double_jump = False
                            jump_fx.play()
             
            
        #Apply GRAVITY
        self.vel_y += GRAVITY 
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
       # dy += GRAVITY
        
        #check collision with floor
        for tile in world.obstacle_list:
            #check for collsion in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #If AI hit a wall turn a round
                if player == False:
                    self.direction *= -1
                    self.move_counter = 0
            #check for collsion in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if player is below ground(jumping)
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground(falling)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.double_jump = True
                    self.jump_count = 0
                    dy = tile[1].top - self.rect.bottom
                    self.jump = False
                
        #Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
         
        #Check for collsion with exit
        level_compete = False    
        if pygame.sprite.spritecollide(self, exit_group, False) and len(enemy_group) == 0:
            level_compete = True
            

        #Check if player fell off map
        if self.rect.top  > SCREEN_HEIGHT:
            self.health = 0

        #Check if player is going of screen
        if self.player:
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
            
        #update rectangle's position
        self.rect.x += dx
        self.rect.y += dy   
       # print(f'\t\t\t{dx}')
        #update scroll based on player positon
        if self.player:
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
            or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
    
                

       # print(screen_scroll)        
        return screen_scroll , level_compete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet((self.rect.centerx + (0.6 * self.rect.size[0]) * self.direction), self.rect.centery, self.direction)
            self.ammo -= 1
            shot_fx.play()
            if self.player:
                player_bullet_group.add(bullet)
            else:
                enemy_bullet_group.add(bullet)
            
    def ai_throw_grenade(self):
        if self.throw_cooldown == 0 and self.grenades > 0:
            self.throw_cooldown = 125
            grenade = Grenade(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction),
                                  self.rect.top,4, self.direction)
            grenade_group.add(grenade)
            self.grenades -= 1
        
     
    def ai(self):
        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
        if self.alive and player.alive:
            #pygame.draw.rect(screen,RED,self.vision)
            if self.idling == False and random.randint(1,200) == 1:
                self.idling = True
                
                self.idling_counter = random.randint(50,150)
                self.update_action(0)
                #check if AI sees player
            if self.vision.colliderect(player.rect):
                #Stop running and face the player
                if self.rect.x < player.rect.x:
                    self.flip = False
                    self.direction = 1
                elif self.rect.x > player.rect.x:
                    self.flip = True
                    self.direction = -1
                self.update_action(0)
                self.shoot()
                self.ai_throw_grenade()
            else:   
                
                if self.idling == False: 
            
                   if self.direction == 1:
                       ai_moving_right = True
                   else:
                       ai_moving_right = False
                   ai_moving_left = not ai_moving_right
                   self.move(ai_moving_left, ai_moving_right, controller)
                   self.update_action(1)
                   self.move_counter += 1
                    #update ai vision as enemy moves
                  #self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                   if self.move_counter > TILE_SIZE:
                       self.direction *= -1
                       self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        
            

        self.rect.x += screen_scroll    
        
    def boss_ai(self):
        self.boss_vision.center = (self.rect.centerx, self.rect.centery - 20)
        dist_to_target = abs(self.rect.centerx - player.rect.centerx)
       # pygame.draw.rect(screen,RED,self.boss_vision)
        if self.alive:
        #make sure boss sees the players#check if AI sees player
            if self.boss_vision.colliderect(player.rect):
                #check collision with floor
                for tile in world.obstacle_list:
                    #check for collsion in the x direction
                    if tile[1].colliderect(self.rect.x + boss.speed, self.rect.y, self.width, self.height):
                        self.update_action(2)
                        self.rect.y -= 11
                        if boss.vel_y < 0:
                            self.vel_y = 0
                            self.rect.bottom = tile[1].top - self.rect.bottom
                #makes sure boss is facing the player
                if player.rect.centerx < self.rect.centerx:
                    self.direction = -1
                    self.flip = True
                else:
                    self.direction = 1
                    self.flip = False                  
                #makes the boss chase the player
                if dist_to_target > 100:   
                    self.update_action(1)
                    self.rect.x += self.speed * self.direction
                elif dist_to_target <= 100:
                    self.update_action(0)
                self.shoot()
                self.ai_throw_grenade()
            else:            
                if self.alive and player.alive:
                    if self.idling == False and random.randint(1,200) == 1:
                        self.idling = True
                        self.idling_counter = random.randint(50,150)
                        self.update_action(0)
                    else:   
                        if self.idling == False: 
            
                           if self.direction == 1:
                               ai_moving_right = True
                           else:
                               ai_moving_right = False
                           ai_moving_left = not ai_moving_right
                           self.move(ai_moving_left, ai_moving_right, controller)
                           self.update_action(1)
                           self.move_counter += 1
                           if self.move_counter > TILE_SIZE * 2:
                               self.direction *= -1
                               self.move_counter *= -1
                        else:
                            self.idling_counter -= 1
                            if self.idling_counter <= 0:
                                self.idling = False
           
        self.rect.x += screen_scroll
        
    def draw_boss_health_bar(self):
        boss_health_bar = HealthBar(self.rect.x - 15, self.rect.centery - 75, 100, 10, self.health, self.max_health)
        boss_health_bar.draw(self.health)

    def update_animation(self):
        animation_cooldown = 100
        #update image
        self.image = self.animation_list[self.action][self.frame_index] 
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation is done
        if self.frame_index >= len(self.animation_list[self.action]):
            #check if the player is dead the end animation
            if self.alive == False or crouching:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0     
  
    def update_action(self, new_action):
        #check if new action different to previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
     
    def check_alive(self):
        if self.player:
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(4)
        else:
            self.kill_ai()
                       
    def kill_ai(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)
            self.death_count -= 1
           # print(self.death_count)
            if self.death_count < 0:
                self.kill()
                    
    def draw(self):
        img = pygame.transform.flip(self.image, self.flip, False)
        if self.flip:
            screen.blit(img,(self.rect.x - 30, self.rect.y - 10))
        else:    
            screen.blit(img,(self.rect.x - 18, self.rect.y - 10))
 
          ##########   WORLD CLASS   ##########        
class World():
    def __init__(self, player_char, enemy_list):
        self.obstacle_list = []
        self.playerChar = player_char
        self.enemy_list = enemy_list
        
    

    def process_data(self, data):
        self.level_length = len(data[0])
        boss_health_bar = None
        #basic_enemy_char, grenadier_enemy_char, elite_enemy_char, boss_char = self.draw_enemies()
        #Iterate through each value in level data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                   img = image_list[tile]
                   img_rect = img.get_rect()
                   img_rect.x = x * TILE_SIZE
                   img_rect.y = y * TILE_SIZE
                   tile_data = (img, img_rect)
                   if tile >= 0 and tile <= 8:
                      self.obstacle_list.append(tile_data)
                   elif tile >= 9  and tile <= 10:
                       water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                       water_group.add(water)
                   elif tile >= 11  and tile <= 14:
                       decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                       decoration_group.add(decoration)
                   elif tile == 15:#Create player
                       if self.playerChar == black_soldier:
                            player = Soldier(True, black_soldier, x * TILE_SIZE, y * TILE_SIZE, 1.62 , animation_steps, 100, 5, 30, 3)
                            #print(f'{player.health} \t {player.max_health}')
                       elif self.playerChar == blue_soldier:
                            player = Soldier(True, blue_soldier, x * TILE_SIZE, y * TILE_SIZE, 1.62 , animation_steps, 100, 5, 15, 8)
                       elif self.playerChar == green_soldier:
                            player = Soldier(True,green_soldier, x * TILE_SIZE, y * TILE_SIZE, 1.62 , animation_steps, 125, 5, 20, 5)
                       elif self.playerChar == red_soldier:
                            player = Soldier(True,red_soldier, x * TILE_SIZE, y * TILE_SIZE, 1.62 , animation_steps, 100, 5, 20, 5) 
                       elif self.playerChar == yellow_soldier:
                            player = Soldier(True,yellow_soldier, x * TILE_SIZE, y * TILE_SIZE, 1.62 , animation_steps, 100, 7, 20, 5)
                       #print(player.health)
                       player_health_bar = HealthBar(10, 10, 200, 20, player.health, player.max_health)
                   elif tile == 16:#Create basic enemies
                       basic_enemy = Soldier(False, self.enemy_list[0], x * TILE_SIZE, y * TILE_SIZE, 1.62, animation_steps, 100, 2, 20, 0)
                       basic_enemy_group.add(basic_enemy)
                       enemy_group.add(basic_enemy)
                   elif tile == 17:#Create grenadier enemies
                       grenadier_enemy = Soldier(False, self.enemy_list[1], x * TILE_SIZE, y * TILE_SIZE, 1.62, animation_steps, 100, 2, 0, 5)
                       grenadier_enemy_group.add(grenadier_enemy)
                       enemy_group.add(grenadier_enemy)
                   elif tile == 18:#Create elite enemies
                       elite_enemy = Soldier(False, self.enemy_list[2], x * TILE_SIZE, y * TILE_SIZE, 1.62, animation_steps, 200, 2, 20, 5)
                       elite_enemy_group.add(elite_enemy)
                       enemy_group.add(elite_enemy)
                   elif tile == 19:#Create BOSSES enemies
                       boss = Soldier(False, self.enemy_list[3], x * TILE_SIZE, y * TILE_SIZE, 2.5, animation_steps, 750, 4, 100, 20)
                       boss_enemy_group.add(boss)
                       enemy_group.add(boss)  
                   elif tile == 20:#Create Ammo boxes
                        ammo_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE) 
                        item_box_group.add(ammo_box) 
                   elif tile == 21: #create grenade boxes 
                        grenade_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(grenade_box)
                   elif tile == 22:
                        health_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(health_box)
                   elif tile == 23:
                       exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                       exit_group.add(exit)
                       
                   
        return player, player_health_bar#, boss_health_bar
    

    def draw_enemies(self):
        basic_enemy_char = self.enemy_list.pop(random.randint(0,3))
       # print(self.enemy_list)
        grenadier_enemy_char = self.enemy_list.pop(random.randint(0,2))
        elite_enemy_char = self.enemy_list.pop(random.randint(0,1))
        boss_char = self.enemy_list[0]
        
        return basic_enemy_char, grenadier_enemy_char, elite_enemy_char, boss_char

    def draw(self):
        for  tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            

           
          ##########   DECORATION CLASS   ##########  
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self):
        self.rect.x += screen_scroll
   
          ##########   WATER CLASS   ########## 
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height())) 
        
    def update(self):
        self.rect.x += screen_scroll
        
          ##########   EXIT CLASS   ########## 
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        self.rect.x += screen_scroll

          ##########   ITEMBOX CLASS   ########## 
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)        
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE// 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self):
        self.rect.x += screen_scroll
        #Check if player has picked up box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box
            if self.item_type == 'Health' and player.health < player.max_health:
                player.health += 25
                #delete box
                self.kill()
                if player.health > player.max_health:
                    player.health = player.max_health 
                
            elif self.item_type == 'Ammo' and player.ammo < player.max_ammo:
                player.ammo += 15
                #delete box
                self.kill()
                if player.ammo > player.max_ammo:
                    player.ammo = player.max_ammo 
                
            elif self.item_type == 'Grenade' and player.grenades < player.max_grenades:
                player.grenades += 3
                #delete box
                self.kill()
                if player.grenades > player.max_grenades:
                    player.grenades = player.max_grenades
                
                
            #delete box
           # self.kill()
   
          ##########   HEALTH BAR CLASS   ##########            
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, sizex, sizey, health, max_health):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.health = health
        self.max_health = max_health
        
    
    def draw(self, health):
        #update with new health
        self.health = health
        #calculation health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, ((self.x - 2), (self.y - 2), (self.sizex + 4), (self.sizey + 4)))
        pygame.draw.rect(screen, RED, (self.x, self.y, self.sizex, self.sizey))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.sizex * ratio, self.sizey))

          ##########   BULLET CLASS   ##########
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 15
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        
    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        
        #Check if bullet goes off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        #Check for collison with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
                
        #Check if bullet hits player
        
        
           
        if pygame.sprite.spritecollide(player, enemy_bullet_group, False):
            
            if player.alive:
            # self.hit_count += 1
                player.health -= 5
                self.kill()
            
        #Check if bullet hits enemy       
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, player_bullet_group, False):
                if enemy.alive:
                  
                    enemy.health -= 25
                    self.kill()
                 
           ##########   GRENADE CLASS   ##########
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.speed = speed
        self.vel_y = -11
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self):
        self.vel_y += GRAVITY
        dx = (self.direction * self.speed)
        dy = self.vel_y
        
        #check for collision with level
        for tile in world.obstacle_list:
		    #check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
			#check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
				#check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        

        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        
        #Check collsion with walls
        
            
        #countdowntimer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.8)
            explosion_group.add(explosion)
            #do damage to anyone nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50
                  #  print(enemy.health)

          ##########   EXPLOSION CLASS   ##########
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = pygame.image.load(f"Assets/Weapons/explosion.png").convert_alpha()
        self.animation_list = self.load_images(sprite_sheet)
        self.frame = 0
        self.frame_index = 0
        self.image = self.animation_list[self.frame][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet):
        #extract images from sprite sheet
        steps = [1,1,1,1,1]
        animation_list = []
        for y, animation in enumerate(steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * 80, y * 80, 80, 80)
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
                
        return animation_list

    #Updates the background image based off of spritsheet loaded in
    def update (self):
        self.rect.x += screen_scroll
        animation_cooldown = 40
        self.image = self.animation_list[self.frame][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.frame]): 
             if self.frame_index >= len(self.animation_list[self.frame]) - 1:
                 self.frame_index = 0
                 self.frame += 1
             if self.frame >= len(self.animation_list):
                 self.kill()
 
                 
          ##########   SCREEN FADE CLASS   ##########
class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
    
        
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#whole screen fade down
            draw_box(SCREEN_WIDTH//2, SCREEN_HEIGHT, 255, BLACK, 0 - self.fade_counter, 0)
            draw_box(SCREEN_WIDTH//2, SCREEN_HEIGHT, 255, BLACK, SCREEN_WIDTH//2 + self.fade_counter, 0)
            draw_box(SCREEN_WIDTH, SCREEN_HEIGHT//2, 255, BLACK, 0, 0 - self.fade_counter)
            draw_box(SCREEN_WIDTH, SCREEN_HEIGHT//2, 255, BLACK, 0, SCREEN_HEIGHT//2 + self.fade_counter)
            #pygame.draw.rect(screen,self.color,(0 - self.fade_counter,0,SCREEN_WIDTH//2, SCREEN_HEIGHT))
        if self.direction == 2:#vertical screen fade down
            pygame.draw.rect(screen,self.color,(0,0,SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
                self.fade_counter = SCREEN_WIDTH
                fade_complete = True
            
        return fade_complete
        
#create screen fades
intro_fade = ScreenFade(1, BLACK, 6)    
death_fade = ScreenFade(2, PINK, 4)


#Create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 200, start_button_img, .4) 
exit_button = button.Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 75, exit_button_img, .4)
credits_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, credits_button_img, .3)
restart_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50, restart_button_img, .4)
black_soldier_btn = button.Button(SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 100, black_soldier_btn_img, 3)
blue_soldier_btn = button.Button(SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 100, blue_soldier_btn_img, 3)
green_soldier_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 100, green_soldier_btn_img, 3)
red_soldier_btn = button.Button(SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT // 2 - 100, red_soldier_btn_img, 3)
yellow_soldier_btn = button.Button(SCREEN_WIDTH // 2 + 320, SCREEN_HEIGHT // 2 - 100, yellow_soldier_btn_img, 3)
        
#create sprite group
enemy_group = pygame.sprite.Group()
basic_enemy_group = pygame.sprite.Group()
grenadier_enemy_group = pygame.sprite.Group()
elite_enemy_group = pygame.sprite.Group()
boss_enemy_group = pygame.sprite.Group()
boss_health_bar_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()            
grenade_group = pygame.sprite.Group()    
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
 
#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world    
with open(f'Assets/Levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
            


play = True
          ##########   MAIN GAME LOOP   ##########
player = Soldier(True,playerChar, x * TILE_SIZE, y * TILE_SIZE, 1.62 , animation_steps, 100, 5, 20, 5)
while play:
    player_alive, menu_music, level1_music, level2_music, level3_music, level4_music, level5_music, death_music = play_background_music(player_alive,menu_music, level1_music, level2_music, level3_music, level4_music, level5_music, death_music)
    clock.tick(FPS)
    #Draw world background
    draw_background()
    if start_game == False:
        

        draw_box(SCREEN_WIDTH, SCREEN_HEIGHT, 150, BLACK, 0, 0)
        #Main Menu
        if game_state == "main_menu":
            if start_button.draw(screen):
                game_state = "character_select"
            if credits_button.draw(screen):
                game_state = "credits"
                show_credits = True
            if exit_button.draw(screen):
                play = False  
        if game_state == "credits":
           # draw_text("CREDITS", char_select_font, WHITE, SCREEN_WIDTH// 6, SCREEN_HEIGHT//5)
           draw_credits() 
        if game_state == "character_select":  
            draw_text("CHOOSE SOLDIER", char_select_font, WHITE, SCREEN_WIDTH// 6, SCREEN_HEIGHT//5)
            draw_char_stats()
            if black_soldier_btn.draw(screen):
                choice = 0
                start_game, start_intro, playerChar, enemies, world, player, player_health_bar = play_game(choice) 
            if blue_soldier_btn.draw(screen):
                choice = 1
                start_game, start_intro, playerChar, enemies, world, player, player_health_bar = play_game(choice) 
            if green_soldier_btn.draw(screen):
                choice = 2
                start_game, start_intro, playerChar, enemies, world, player, player_health_bar = play_game(choice) 
            if red_soldier_btn.draw(screen):
                choice = 3
                start_game, start_intro, playerChar, enemies, world, player, player_health_bar = play_game(choice) 
            if yellow_soldier_btn.draw(screen):
                choice = 4
                start_game, start_intro, playerChar, enemies, world, player, player_health_bar = play_game(choice) 
    else:
        
        
        
        #Draw world map
        world.draw()
        #Show ammo and grenades
        draw_inventory()
        #show player controls
        show_controls(controller)
        show_current_level()
       # pygame.draw.rect(screen,RED,player.rect)
        player.draw()
        #Draw health bar
        player_health_bar.draw(player.health)
        player.update()
        
        for basic_enemy in basic_enemy_group:
            basic_enemy.draw()
            basic_enemy.ai()
            basic_enemy.update()
        for grenadier_enemy in grenadier_enemy_group:
            grenadier_enemy.draw()
            grenadier_enemy.ai()
            grenadier_enemy.update()
        for elite_enemy in elite_enemy_group:
            elite_enemy.draw()
            elite_enemy.ai()
            elite_enemy.update()    
        for boss in boss_enemy_group:
            boss.draw()
            boss.draw_boss_health_bar()
            boss.boss_ai() 
            boss.update()
           
        #Update and draw sprite groups
        player_bullet_group.update()    
        enemy_bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        player_bullet_group.draw(screen)
        enemy_bullet_group.draw(screen)
        enemy_bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
    
        #show intro
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0
        #Update player actions
        if player.alive:
            player_alive = True
            #shoot bullets
            if shoot:
                player.shoot()
                #print(f'{bullet}')
            #throw grenade
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top,7,player.direction)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
            if crouching:
                player.update_action(3)#Crouching
            elif player.in_air:
                player.update_action(2)#jump
            elif moving_left or moving_right:
                player.update_action(1)#run
            else:
                player.update_action(0)#idle
            screen_scroll, level_complete = player.move(moving_left, moving_right, controller)    
            bg_scroll -= screen_scroll
            #Check if player completed level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load in level data and create world 
                    with open(f'Assets/Levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile,delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World(playerChar, enemies)
                    player, player_health_bar = world.process_data(world_data)
                    
                    ###FIXED!!!!!!###
                #####if level > MAX_LEVELS:####
                else:
                     start_game = False
                     game_state = "main_menu"
                     screen_scroll = 0
                     bg_scroll = 0
                     world_data = reset_level()
                     level = 1
                     soldiers = [black_soldier, blue_soldier, green_soldier, red_soldier, yellow_soldier]
                     
                     with open(f'Assets/Levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile,delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                  
                   
                    
        else:
            player_alive = False
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    bg_scroll = 0
                    world_data = reset_level()
                    #load in level data and create world    
                    with open(f'Assets/Levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile,delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World(playerChar, enemies)
                    player, player_health_bar = world.process_data(world_data)
    
    
    

    #Get player input for controls
    controller, crouching, moving_left, moving_right, shoot, grenade, grenade_thrown, jump, play,game_state, show_credits  = get_keyboard_input(controller, crouching, moving_left, moving_right, shoot, grenade, grenade_thrown, jump, play, player,game_state,show_credits)    
    pygame.display.update()  
    
pygame.quit()