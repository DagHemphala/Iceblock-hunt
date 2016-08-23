import pygame
import random

 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
 
 
class Block(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    respawn_time = 0
    def __init__(self, sprite_image, width, height, score):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(sprite_image).convert()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.image.set_colorkey(WHITE)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


        self.change_x = 0
        self.change_y = 0
        
        self.block = None
        self.wall = None
        self.block2 = None
        
        self.fall_speed = 2
        self.score = score
        
 
    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width-35)
 
    def update(self):
        """ Called each frame. """
        self.fall_speed = 2 + (self.score/50)
        # Move block down one pixel
        self.rect.y += self.fall_speed
         
        # If block is too far down, reset to top of screen.
        if self.rect.y > int(screen_height):
            self.reset_pos()

        # Respawn block after 10 sec
        if self.rect.y >= int(screen_height - 55):
            if self.respawn_time >= 10:
                self.reset_pos()
                self.respawn_time = 0            
            
            self.respawn_time += 1/60
            
 
class Player(Block):
    """ The player class derives from Block, but overrides the 'update'
    functionality with new a movement function that will move the block
    with the mouse. """
    speed = 1
    counter = 0
    lastpressed_key_right =  True
    
    def left_player_animation(self):
        animation_frames = []
        image = pygame.image.load( "sprites/player_left.png" ).convert_alpha()
        sprite_image_width, sprite_image_height = image.get_size()
            

        for i in range( int( sprite_image_width / 50 ) ):
            animation_frames.append( image.subsurface( ( i * 50, 0, 50, 64 ) ) )
                
        screen.blit( animation_frames[int(self.counter)], ( self.rect.x-14, self.rect.y -18) )
        self.counter = self.counter + (1/9)

        if self.counter >=3:
                self.explod = False
                self.counter = 0
    def right_player_animation(self):
        animation_frames = []
        image = pygame.image.load( "sprites/player_right.png" ).convert_alpha()
        sprite_image_width, sprite_image_height = image.get_size()
            

        for i in range( int( sprite_image_width / 50 ) ):
            animation_frames.append( image.subsurface( ( i * 50, 0, 50, 64 ) ) )
                
        screen.blit( animation_frames[int(self.counter)], ( self.rect.x-14, self.rect.y-10) )
        self.counter = self.counter + (1/9)
        
        if self.counter >=3:
                self.explod = False
                self.counter = 0

    def left_player_animation_still(self):
        animation_frames = []
        image = pygame.image.load( "sprites/player_left.png" ).convert_alpha()
        sprite_image_width, sprite_image_height = image.get_size()
            

        for i in range( int( sprite_image_width / 50 ) ):
            animation_frames.append( image.subsurface( ( i * 50, 0, 50, 64 ) ) )
                
        screen.blit( animation_frames[1], ( self.rect.x-14, self.rect.y -18) )
    
    def right_player_animation_still(self):
        animation_frames = []
        image = pygame.image.load( "sprites/player_right.png" ).convert_alpha()
        sprite_image_width, sprite_image_height = image.get_size()
            

        for i in range( int( sprite_image_width / 50 ) ):
            animation_frames.append( image.subsurface( ( i * 50, 0, 50, 64 ) ) )
                
        screen.blit( animation_frames[1], ( self.rect.x-14, self.rect.y-10) )

                
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
        k = pygame.key.get_pressed()
        
        # Move player left and right
        for  i in range(3):
            if self.rect.x > 0 and self.rect.x < screen_width-18:
                if k[pygame.K_RIGHT]:
                    self.rect.x = self.rect.x + self.speed
                    self.left_player_animation()
                    self.lastpressed_key_right = True
                    
                else:
                    if self.lastpressed_key_right == True:
                        self.left_player_animation_still()
                    
                if k[pygame.K_LEFT]:
                    self.rect.x = self.rect.x - self.speed
                    self.right_player_animation()
                    self.lastpressed_key_right = False
                    
                else:
                    if self.lastpressed_key_right == False:
                        self.right_player_animation_still()
                    
                
            else:
                if self.rect.x <= 0:
                    self.rect.x += 1
                if self.rect.x >= 680:
                    self.rect.x -= 1

        # place player at ground!          
        block_hit_list = pygame.sprite.spritecollide(self, self.wall, False)
        for block in block_hit_list:
            self.rect.bottom = wall.rect.top
        
            
class Wall(Block):
    
    def update (self):
        block_hit_list = pygame.sprite.spritecollide(self, self.block, False)
        for block in block_hit_list:
            block.rect.bottom = self.rect.top        
        

class Bombs(Block):
    explod = False
    counter = 0
    animation_x = 0
    animation_y = 0

    def explosion(self):
        if self.explod == True:
            animation_frames = []
            image = pygame.image.load( "sprites/BombExploding.png" ).convert_alpha()
            sprite_image_width, sprite_image_height = image.get_size()
        

            for i in range( int( sprite_image_width / 32 ) ):
                animation_frames.append( image.subsurface( ( i * 32, 0, 32, 64 ) ) )
            
            screen.blit( animation_frames[int(self.counter)], ( self.animation_x, self.animation_y - 30) )
            self.counter = self.counter + (1/9)
            if self.counter >=6:
                self.explod = False
                self.counter = 0
            

    def update(self):
        self.fall_speed = 2 + (self.score/50)
        
        self.rect.y += self.fall_speed

        if self.rect.y > screen_height:
            self.reset_pos()
        self.explosion()
    
def addmine():

    # This represents a block
    
    bomb = Bombs('sprites/mine.png', 35, 35, score)
    # Set a random location for the block
    bomb.rect.x = random.randrange(screen_width-35)
    bomb.rect.y = random.randrange(-screen_width,0)

    
 
    # Add the block to the list of objects
    bomb_list.add(bomb)
    all_sprites_list.add(bomb)

def addblock():
    # This represents a block
    
    blocks = Block('sprites/block.png', 25, 25, score)
    blocks.block = block_list
    # Set a random location for the block
    blocks.rect.x = random.randrange(screen_width-25)
    blocks.rect.y = random.randrange(-screen_width,0)

    
 
    # Add the block to the list of objects
    block_list.add(blocks)
    all_sprites_list.add(blocks)

def addspeed_boost():
    # This represents a block
    
    speed_boost = Block('sprites/speed_boost.png', 25, 25, score)
    speed_boost.block = speed_boost_list
    # Set a random location for the block
    speed_boost.rect.x = random.randrange(screen_width-25)
    speed_boost.rect.y = random.randrange(-screen_width,0)

    
 
    # Add the block to the list of objects
    speed_boost_list.add(speed_boost)
    all_sprites_list.add(speed_boost)

# Placing button that is clickable.
def button(msg,x,y,w,h,ic,ac,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        
        if click[0] == 1 and action == True:
            action = False
        elif click[0] == 1:
            action = True
            
            
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    
    screen.blit(textSurf, textRect)
    return action
    

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()
            
# Initialize Pygame
pygame.init()

font = pygame.font.SysFont("comicsansms", 50)
font2 = pygame.font.SysFont("comicsansms", 25)
Gameover = font.render("Game Over!", True, RED)
Restart = font.render("Press space to restart", True, BLACK)
Highscore = font.render("Highscore", True, BLACK)

Menu = font.render("Menu", True, BLACK)
Start = font.render("Start", True, BLACK)



# Global variabals
score = 0
health = 5
addmine_score_check = 0

addblock_score_check = 0
addspeed_boost_check = 0
speed_boost_check = 0

menu = True
highscore = False
restart = False
add_score_once = False
main_menu = False
pause_menu = False

#create higscore file if not exists
file = open('highscore.txt','a')

file.close()

# Set the height and width of the screen
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])


# bg load
bg_image = pygame.image.load('bg.png').convert()
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

bomb_list = pygame.sprite.Group()

speed_boost_list = pygame.sprite.Group()
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()


for i in range(3):
    addmine()

for i in range(10):
    addblock()
    
  
# This represents a block
for i in range (int(screen_width/25)):
    wall = Wall('sprites/block.png', 25, 25, score)
    wall.rect.y = screen_height-25
    wall.rect.x += i * 25
    wall.block = block_list
    all_sprites_list.add(wall)

# Create a red player block
player = Player('sprites/empty.png', 15, 30, score)
player.wall = all_sprites_list

all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 

 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu == False:
                    if pause_menu == False:
                        pause_menu = True
                    else:
                        pause_menu = False
        
                
     
    # Clear the screen
    screen.blit(bg_image, [0, 0])
    if menu == False and highscore == False:
        if health > 0 and pause_menu == False:
            # Calls update() method on every sprite in the list
            all_sprites_list.update()
         
            # See if the player block has collided with block.
            blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)
         
            # Check the list of collisions.
            for block in blocks_hit_list:
                score += 1
                 
                # Reset block to the top of the screen to fall again.
                block.reset_pos()

            # See if the player block has collided with a mine/bomb.
            bomb_hit_list = pygame.sprite.spritecollide(player, bomb_list, False)
         
            # Check the list of collisions.
            for bomb in bomb_hit_list:
                health -= 1
                bomb.animation_y = bomb.rect.y
                bomb.animation_x = bomb.rect.x
                bomb.explod = True
                # Reset block to the top of the screen to fall again.
                bomb.reset_pos()

            # See if the player block has collided with a mine/bomb.
            speed_hit_boost_list = pygame.sprite.spritecollide(player, speed_boost_list, True)
         
            # Check the list of collisions.
            for speed_boost in speed_hit_boost_list:
                
                if speed_boost_check == 0:
                    player.speed += 1
                    speed_boost_check += 1
                else:
                    speed_boost_check = 0

            # add mines for every 10 score
            if (score/10).is_integer():
                if score != 0:
                    if addmine_score_check == 0:
                        addmine()
                        addmine_score_check += 1
            else:
                addmine_score_check = 0

            # add block every 20 score
            if (score/20).is_integer():
                if score != 0:
                    if addblock_score_check == 0:
                        addblock()
                        addblock_score_check += 1
            else:
                addblock_score_check = 0

            # Add speed boost every 100 score
            if (score/100).is_integer():
                if score != 0:
                    if addspeed_boost_check == 0:
                        addspeed_boost()
                        addspeed_boost_check += 1
            else:
                addspeed_boost_check = 0

        elif pause_menu == True:
            pause_menu = button("Resume",(screen_width/2)-40,120,100,50,GREEN,BLUE,pause_menu)
            menu = button("Main menu",(screen_width/2)-40,180,100,50,GREEN,BLUE,menu)
                
                
            
        else:
            screen.blit(Gameover,[(screen_width/2)-100,50])
            restart = button("Restart",(screen_width/2)-40,120,100,50,GREEN,BLUE,restart)
            menu = button("Main menu",(screen_width/2)-40,180,100,50,GREEN,BLUE,menu)


            if add_score_once == False:
                f = open('highscore.txt','a')
                f.write(str(score) + '\n')
                f.close()
                add_score_once = True
            if restart == True:
                if health == 0:
                    score = 0
                    health = 5
                    add_score_once = False
                    restart = False
                     # clering sprite group
                    block_list.empty() 
                    bomb_list.empty() 
                    speed_boost_list.empty() 
                    all_sprites_list.empty() 

                    # reseting sprite group
                    for i in range(3):
                        addmine()

                    for i in range(10):
                        addblock()
                        
                      
                    # This represents a block
                    for i in range (50):
                        wall = Wall('sprites/block.png', 25, 25, score)
                        wall.rect.y = screen_height-25
                        wall.rect.x += i * 25
                        wall.block = block_list
                        all_sprites_list.add(wall)

                    # Create a red player block
                    player = Player('sprites/empty.png', 15, 30, score)
                    player.wall = all_sprites_list

                    all_sprites_list.add(player)
            
        # Draw all the spites
        all_sprites_list.draw(screen)     
            
        
        # Write score and helth
        score_txt = font2.render("Score: "+str(score),1,BLUE)
        screen.blit(score_txt, (50, 5))
            
        health_image = pygame.image.load('sprites/health'+str(health)+'.png').convert_alpha()
        health_image = pygame.transform.scale(health_image, (100, 30))
        screen.blit(health_image, (screen_width-150, 5))
    elif menu == True:
        screen.blit(Menu,[(screen_width/2)-50,-10])
        menu = button("Start",(screen_width/2)-40,60,100,50,GREEN,BLUE,menu)
        highscore = button("Highscore",(screen_width/2)-40,120,100,50,GREEN,BLUE,highscore)
        if highscore == True:
            menu = False
            
    elif highscore == True:
        file = open('highscore.txt','r+')
        highscore_array = file.readlines()
        file.close ()

        highscore_array = list(map(lambda x:x.strip(),highscore_array))

        highscore_array.sort(key=int)
        highscore_array = list(reversed(highscore_array))

        if len(highscore_array) < 7:
            highscore_amount = len(highscore_array)
        else:
            highscore_amount = 7
            
        menu = button("Return",5,5,100,50,GREEN,BLUE,menu)
        screen.blit(Highscore,[(screen_width/2)-60,-10])
        for i in range (highscore_amount):
            highscore_txt = font2.render(str(i+1) +'.  ' + highscore_array[i],1,BLUE)
            screen.blit(highscore_txt, ((screen_width/2)-120, 60 +(i*40) ))
            if menu == True:
                highscore = False
            
    
    # Limit to 20 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()

