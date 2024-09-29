import pygame
import time
import random
#importing required modules to create our game
pygame.init()#initializes pygame
WIDTH,HEIGHT=1200,800#fixing the width and height of the window
COLOR=(255,255,255)#setting a const variable for the color white
FONT0=pygame.font.SysFont("roman",15)#setting a font for the text
FONT=pygame.font.SysFont("comicsans",40)#setting a font for the text
FONT1=pygame.font.SysFont("comicsans",50)#setting a font for the text
WIN=pygame.display.set_mode((WIDTH,HEIGHT))#declaring a variable to create a screen.
GAME=pygame.display.set_mode((WIDTH,HEIGHT))#declaring a variable to create a game screen
END=pygame.display.set_mode((WIDTH,HEIGHT))#declaring a variable to create a end screen
WIN.fill(COLOR)#fills the window with that color
SIMG=pygame.transform.scale(pygame.image.load("maze.png"),(WIDTH,HEIGHT))#giving my image to pygame
lives=5#initializing lives for level1
lives1=5#initializing lives for level2
lives2=5#initializing lives for level3
score=0#initializing score
BC=pygame.Rect(100,20,1000,700)#creating a rectangle for the game
player=pygame.Rect(310,665,25,25)#creating a rectangle for the player
player_velocity=2#setting the velocity of the player
clock=pygame.time.Clock()#creating a clock
cell_size=60#setting the size of the cell for level1
grid_width=10#setting the width of the grid for level1
grid_height=10#setting the height of the grid for level1 and similarly to the other two levels as below
cell_size1=50
grid_width1=12
grid_height1=12
cell_size2=40
grid_width2=15
grid_height2=15
level=1#game starts with a initial level 1
N,S,E,W=1,2,4,8#setting the directions for the maze
DX = {E: 1, W: -1, N: 0, S: 0}#creating dictionary for the directions in the x axis
DY = {E: 0, W: 0, N: 1, S: -1}#creating dictionary for the directions in the y axis
OPPOSITE = {E: W, W: E, N: S, S: N}#creating dictionary for the opposite directions
def passage(grid,cx,cy,grid_width,grid_height):
    """
    this is the main part of the game cause it is the function to create a random maze for the game
    first we take the directions as the list and shuffle it and go through each of them according to dfs algorithm
    """
    directions = [N, S, W, E]
    random.shuffle(directions)

    for direction in directions:
        nx, ny=cx + DX[direction], cy + DY[direction]

        if 0 <= nx < grid_width and 0 <= ny < grid_height and grid[ny][nx] == 0:
            grid[cy][cx] |= direction
            grid[ny][nx] |= OPPOSITE[direction]
            passage(grid,nx,ny,grid_width,grid_height)

pygame.display.set_caption("MAzE EsCapE")#setting the title of the game
#creating texts which we use later in game
t=FONT0.render("*instructions: use buttons to change the level as u want.after entering to game ur goal is to reach end point which is at top right of ur maze and control the movements",1,"Black")
t0=FONT0.render(" of the player by using arrow keys and please make sure to not collide to walls of maze cause u have limited lives .ok that's it,i hope u enjoy my game.",1,"Black")
t1=FONT.render("Welcome to MAzE game",1,"Black")
t3=FONT.render("press Enter to play",1,"black")
t4=FONT.render("press Q to quit",1,"black")
t5=FONT.render("Game over",1,"black")
t7=FONT.render("press space to play again",1,"black")
t8=FONT.render("press m to go to main menu",1,"black")
t9=FONT.render("press Q to quit",1,"black")
t12=FONT.render("start",1,"black")
t13=FONT.render("end",1,"black")
t14=FONT1.render("You Won!",1,"black")
t15=FONT1.render("You lost",1,"black")
#initializing last_collision_time
last_collision_time=0

class Button:
    """
    this is a button class which is used to create buttons in the game
    """
    def __init__(self, image_path, x, y, width, height):#initializing the button
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):#drawing the button
        WIN.blit(self.image, self.rect)

    def is_clicked(self, pos):#checking if the button is clicked
        return self.rect.collidepoint(pos)
up_button = Button('up_button.png',(WIDTH+t1.get_width())/2-100 , 130, 50, 50)#creating buttons to change levels in game
down_button = Button('down_button.png',(WIDTH+t1.get_width())/2-100 , 240, 50, 50)

def startscreen():#this is the startscreen of the game
    global level
    t2=FONT.render(f"Select Level     {level}",1,"black")
    WIN.blit(SIMG,(0,0))#draw the image
    #draw the texts which we created earlier
    WIN.blit(t1,(int((WIDTH-t1.get_width())/2),50))
    WIN.blit(t2,(int((WIDTH-300)/2),180))
    WIN.blit(t3,(int((WIDTH-t3.get_width())/2),300))
    WIN.blit(t4,(int((WIDTH-t4.get_width())/2),450))
    WIN.blit(t,(50,600))
    WIN.blit(t0,(135,620))
    #draw the buttons
    up_button.draw()
    down_button.draw()
def playscreen1():#this is the playscreen of the game
    global lives1#using the values globally
    global last_collision_time
    global score
    #draw the text
    t10=FONT.render(f"Time: {round(r_time)}s",1,"black")
    t11=FONT.render(f"Lives remaining :{lives1}",1,"black")
    GAME.blit(SIMG,(0,0))#draw the  background image    
    pygame.draw.rect(GAME,"lightblue",BC)   
    #draw the text
    GAME.blit(t12,(290-t12.get_width(),640))
    GAME.blit(t13,(910,90))
    GAME.blit(t11,(150,45))
    GAME.blit(t10,(700,45))
    #initializing the maze boundary and drawing it
    r1=pygame.Rect(300,100,600,1)
    r2=pygame.Rect(300,100,1,600)
    r3=pygame.Rect(300,700,600,1)
    r4=pygame.Rect(900,100,1,600)
    r=[r1,r2,r3,r4]
    for i in r:
        pygame.draw.rect(GAME,"red",i)
     #the next four if loops are for the collision of the player with the maze boundary and reducing the lives accordingly
    if player.colliderect(r1) and keys[pygame.K_UP]:
        if (time.time() - last_collision_time) > 1:
            lives1 = lives1- 1
            last_collision_time=time.time()
    if player.colliderect(r2) and keys[pygame.K_LEFT]:
        if (time.time() - last_collision_time) > 1:
            lives1 = lives1- 1
            last_collision_time=time.time()
    if player.colliderect(r3) and keys[pygame.K_DOWN]:
        if (time.time() - last_collision_time) > 1:
            lives1 = lives1- 1
            last_collision_time=time.time()
    if player.colliderect(r4) and keys[pygame.K_RIGHT]:
        if (time.time() - last_collision_time) > 1:
            lives1 = lives1- 1
            last_collision_time=time.time()

    #the following for loop draws the maze and checks for the collision of the player with the maze and reducing the lives accordingly
    for y in range(grid_height1):
            for x in range(grid_width1):
                rect = (300+x * cell_size1,100+ y * cell_size1, cell_size1, cell_size1) 
                if grid1[y][x] == 0:
                    pygame.draw.rect(GAME,"white", rect)
                else:
                    if grid1[y][x] & N == 0:
                        pygame.draw.rect(GAME,"red", (300 +(x * cell_size1), 100+ (y * cell_size1) + cell_size1,cell_size1, 1))
                        if keys[pygame.K_UP] and (100+ (y * cell_size1) + cell_size1 -1) <= player.y <= (100+ (y * cell_size1) + cell_size1 +1) and (300 + (x*cell_size1)-25) <= player.x <= (300 + (x*cell_size1) +cell_size1) and player.colliderect( (300 +(x * cell_size1), 100+ (y * cell_size1) + cell_size1,cell_size1, 1)):
                            player.y = (100+ (y * cell_size1) + cell_size1 +1)
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_DOWN] and (100+ (y * cell_size1) + cell_size1 -23) >= player.y >= (100+ (y * cell_size1) + cell_size1 -25) and (300 + (x*cell_size1)-25) <= player.x <= (300 + (x*cell_size1) +cell_size1) and player.colliderect( (300 +(x * cell_size1), 100+ (y * cell_size1) + cell_size1,cell_size1, 1)):
                            player.y=100+ (y * cell_size1) + cell_size1 -25
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_RIGHT] and(300 + (x*cell_size1)-23) >= player.x >= (300 + (x*cell_size1)-25) and ( 100+ (y * cell_size1) + cell_size1-25) < player.y < ( 100+ (y * cell_size1) + cell_size1+1) and player.colliderect( (300 +(x * cell_size1), 100+ (y * cell_size1) + cell_size1,cell_size1, 1)):
                            player.x=300 + (x*cell_size1)-25
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_LEFT] and (300 + (x*cell_size1) +cell_size1 -2) <= player.x <= (300 + (x*cell_size1) +cell_size1) and  ( 100+ (y * cell_size1) + cell_size1-25) < player.y < ( 100+ (y * cell_size1) + cell_size1+1) and player.colliderect( (300 +(x * cell_size1), 100+ (y * cell_size1) + cell_size1,cell_size1, 1)):
                            player.x=300 + (x*cell_size1)+cell_size1
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                    if grid1[y][x] & E == 0:
                        pygame.draw.rect(GAME,"red", (300 +(x * cell_size1) + cell_size1,100+ (y * cell_size1),1,cell_size1))
                        if keys[pygame.K_RIGHT] and (300 +(x * cell_size1) +cell_size1 -23) >= player.x >= (300 +(x * cell_size1)+cell_size1-25) and (100 +(y*cell_size1) -25) <= player.y <= (100+ (y * cell_size1) +cell_size1) and player.colliderect( (300 +(x * cell_size1) + cell_size1,100+ (y * cell_size1),1,cell_size1)):
                            player.x= 300 +(x * cell_size1)+cell_size1-25
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_LEFT] and (300 +(x * cell_size1) + cell_size1 +1) >= player.x >= (300 +(x * cell_size1) + cell_size1-1) and (100 +(y*cell_size1) -25) <= player.y <= (100+ (y * cell_size1) +cell_size1) and player.colliderect( (300 +(x * cell_size1) + cell_size1,100+ (y * cell_size1),1,cell_size1)):
                            player.x= 300 +(x * cell_size1) + cell_size1+1
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_UP] and (100+ (y * cell_size1)+cell_size1) >= player.y >= (100+ (y * cell_size1)+cell_size1-2) and (300 +(x * cell_size1) ) <= player.x <= (300 +(x * cell_size1) + cell_size1+1) and player.colliderect( (300 +(x * cell_size1) + cell_size1,100+ (y * cell_size1),1,cell_size1)):
                            player.y= 100 +(y*cell_size1)+cell_size1
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_DOWN] and (100+ (y * cell_size1)-23) >= player.y >= (100+ (y * cell_size1)-25) and (300 +(x * cell_size1) ) <= player.x <= (300 +(x * cell_size1) + cell_size1+1) and player.colliderect( (300 +(x * cell_size1) + cell_size1,100+ (y * cell_size1),1,cell_size1)):
                            player.y= 100 +(y * cell_size1) - 25
                            if (time.time() - last_collision_time) > 1:
                                lives1 = lives1- 1
                                last_collision_time=time.time()
                        
                        
                
    pygame.draw.rect(GAME,"red",player)

#the next four if loops are for the movement of the player
    if keys[pygame.K_UP] == True and player.y<=677 and player.y>=99+player_velocity:
        player.y-=player_velocity
    if keys[pygame.K_DOWN] ==True and player.y<=677-player_velocity and player.y>=99:
        player.y+=player_velocity
    if keys[pygame.K_LEFT] ==True and player.x<=877 and player.x>=300+player_velocity:
        player.x-=player_velocity
    if keys[pygame.K_RIGHT] ==True and player.x<=877-player_velocity and player.x>=300:
        player.x+=player_velocity
    x=player.x
    y=player.y
    #the next 10 if loops are to cover the maze according to the player's position such that only 5*5 cells are visible and that too around the maze
    if x <= 300+(3*cell_size1) and y >= 100 +(9*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100,12*cell_size1+1,7*cell_size1))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size1),100+(7*cell_size1),7*cell_size1+1,5*cell_size1+1))
    if x <=300+(3*cell_size1) and y <= 100+(3*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size1),12*cell_size1+1,7*cell_size1+1))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size1),100,7*cell_size1+1,5*cell_size1+1))
    if x>=300+(9*cell_size1) and y<=100+(3*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100,7*cell_size1,12*cell_size1+1))
        pygame.draw.rect(GAME,"lightblue",(300+(7*cell_size1),100+(5*cell_size1),5*cell_size1+1,7*cell_size1+1))
    if x>=300+(9*cell_size1) and y>= 100+(9*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100,12*cell_size1+1,(7*cell_size1)+1))
        pygame.draw.rect(GAME,"lightblue",(300,100+(7*cell_size1),7*cell_size1,5*cell_size1+1))
    if (300+(3*cell_size1))<x<(300+(9*cell_size1)):
        pygame.draw.rect(GAME,"lightblue",(300,100,x-300-(2*cell_size1),12*(cell_size1)+1))
        pygame.draw.rect(GAME,"lightblue",(x+(3*cell_size1),100,900-x-(3*cell_size1)+1,12*(cell_size1)+1))
    if (100+(3*cell_size1)) < y < (100+(9*cell_size1)):
        pygame.draw.rect(GAME,"lightblue",(300,100,12*cell_size1+1,y-(2*cell_size1)-100))
        pygame.draw.rect(GAME,"lightblue",(300,y+(3*cell_size1),12*cell_size1+1,700-y-(3*cell_size1)+1))
    if (300+(3*cell_size1))<x<(300+(9*cell_size1)) and  y >= 100 +(9*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100,12*cell_size1+1,7*cell_size1))
    if (300+(3*cell_size1))<x<(300+(9*cell_size1)) and  y <= 100 +(3*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size1),12*cell_size1+1,7*cell_size1))
    if (100+(3*cell_size1)) < y < (100+(9*cell_size1)) and x <= 300+(3*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size1),100,7*cell_size1+1,12*cell_size1+1))
    if (100+(3*cell_size1)) < y < (100+(9*cell_size1)) and x >= 300+(9*cell_size1):
        pygame.draw.rect(GAME,"lightblue",(300,100,7*cell_size1,12*cell_size1+1))    
#the next two functions are also for game screen but for another two levels and in that another two levels just the no of grids are changed and i changed the code accordingly
def playscreen2():

    global lives2
    global last_collision_time
    global score
    t10=FONT.render(f"Time: {round(r_time)}s",1,"black")
    t11=FONT.render(f"Lives remaining :{lives2}",1,"black")
    GAME.blit(SIMG,(0,0))
    pygame.draw.rect(GAME,"lightblue",BC)
    GAME.blit(t12,(290-t12.get_width(),640))
    GAME.blit(t13,(910,90))

    GAME.blit(t11,(150,45))
    GAME.blit(t10,(700,45))
    r1=pygame.Rect(300,100,600,1)
    r2=pygame.Rect(300,100,1,600)
    r3=pygame.Rect(300,700,600,1)
    r4=pygame.Rect(900,100,1,600)
    r=[r1,r2,r3,r4]
    for i in r:
        pygame.draw.rect(GAME,"red",i)
    if player.colliderect(r1) and keys[pygame.K_UP]:
        if (time.time() - last_collision_time) > 1:
            lives2 = lives2- 1
            last_collision_time=time.time()
    if player.colliderect(r2) and keys[pygame.K_LEFT]:
        if (time.time() - last_collision_time) > 1:
            lives2 = lives2- 1
            last_collision_time=time.time()
    if player.colliderect(r3) and keys[pygame.K_DOWN]:
        if (time.time() - last_collision_time) > 1:
            lives2 = lives2- 1
            last_collision_time=time.time()
    if player.colliderect(r4) and keys[pygame.K_RIGHT]:
        if (time.time() - last_collision_time) > 1:
            lives2 = lives2- 1
            last_collision_time=time.time()

    for y in range(grid_height2):
            for x in range(grid_width2):
                rect = (300+x * cell_size1,100+ y * cell_size2, cell_size2, cell_size2) 
                if grid2[y][x] == 0:
                    pygame.draw.rect(GAME,"white", rect)
                else:
                    if grid2[y][x] & N == 0:
                        pygame.draw.rect(GAME,"red", (300 +(x * cell_size2), 100+ (y * cell_size2) + cell_size2,cell_size2, 1))
                        if keys[pygame.K_UP] and (100+ (y * cell_size2) + cell_size2 -1) <= player.y <= (100+ (y * cell_size2) + cell_size2 +1) and (300 + (x*cell_size2)-25) <= player.x <= (300 + (x*cell_size2) +cell_size2) and player.colliderect( (300 +(x * cell_size2), 100+ (y * cell_size2) + cell_size2,cell_size2, 1)):
                            player.y = (100+ (y * cell_size2) + cell_size2 +1)
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_DOWN] and (100+ (y * cell_size2) + cell_size2 -23) >= player.y >= (100+ (y * cell_size2) + cell_size2 -25) and (300 + (x*cell_size2)-25) <= player.x <= (300 + (x*cell_size2) +cell_size2) and player.colliderect( (300 +(x * cell_size2), 100+ (y * cell_size2) + cell_size2,cell_size2, 1)):
                            player.y=100+ (y * cell_size2) + cell_size2 -25
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_RIGHT] and(300 + (x*cell_size2)-23) >= player.x >= (300 + (x*cell_size2)-25) and ( 100+ (y * cell_size2) + cell_size2-25) < player.y < ( 100+ (y * cell_size2) + cell_size2+1) and player.colliderect( (300 +(x * cell_size2), 100+ (y * cell_size2) + cell_size2,cell_size2, 1)):
                            player.x=300 + (x*cell_size2)-25
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_LEFT] and (300 + (x*cell_size2) +cell_size2 -2) <= player.x <= (300 + (x*cell_size2) +cell_size2) and  ( 100+ (y * cell_size2) + (cell_size2) -45 ) < player.y < ( 100+ (y * cell_size2) + cell_size2+1) and player.colliderect( (300 +(x * cell_size2), 100+ (y * cell_size2) + cell_size1,cell_size2, 1)):
                            player.x=300 + (x*cell_size2)+cell_size2
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                    if grid2[y][x] & E == 0:
                        pygame.draw.rect(GAME,"red", (300 +(x * cell_size2) + cell_size2,100+ (y * cell_size2),1,cell_size2))
                        if keys[pygame.K_RIGHT] and (300 +(x * cell_size2) +cell_size2 -23) >= player.x >= (300 +(x * cell_size2)+cell_size2-25) and (100 +(y*cell_size2) -25) <= player.y <= (100+ (y * cell_size2) +cell_size2) and player.colliderect( (300 +(x * cell_size2) + cell_size2,100+ (y * cell_size2),1,cell_size2)):
                            player.x= 300 +(x * cell_size2)+cell_size2-25
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_LEFT] and (300 +(x * cell_size2) + cell_size2 +1) >= player.x >= (300 +(x * cell_size2) + cell_size2-1) and (100 +(y*cell_size2) -25) <= player.y <= (100+ (y * cell_size2) +cell_size2) and player.colliderect( (300 +(x * cell_size2) + cell_size2,100+ (y * cell_size2),1,cell_size2)):
                            player.x= 300 +(x * cell_size2) + cell_size2+1
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_UP] and (100+ (y * cell_size2)+cell_size2) >= player.y >= (100+ (y * cell_size2)+cell_size2-2) and (300 +(x * cell_size2) ) <= player.x <= (300 +(x * cell_size2) + cell_size2+1) and player.colliderect( (300 +(x * cell_size2) + cell_size2,100+ (y * cell_size2),1,cell_size2)):
                            player.y= 100 +(y*cell_size2)+cell_size2
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_DOWN] and (100+ (y * cell_size2)-23) >= player.y >= (100+ (y * cell_size2)-25) and (300 +(x * cell_size2) ) <= player.x <= (300 +(x * cell_size2) + cell_size2+1) and player.colliderect( (300 +(x * cell_size2) + cell_size2,100+ (y * cell_size2),1,cell_size2)):
                            player.y= 100 +(y * cell_size2) - 25
                            if (time.time() - last_collision_time) > 1:
                                lives2 = lives2- 1
                                last_collision_time=time.time()
                        
                        
                
    pygame.draw.rect(GAME,"red",player)


    if keys[pygame.K_UP] == True and player.y<=677 and player.y>=99+player_velocity:
        player.y-=player_velocity
    if keys[pygame.K_DOWN] ==True and player.y<=677-player_velocity and player.y>=99:
        player.y+=player_velocity
    if keys[pygame.K_LEFT] ==True and player.x<=877 and player.x>=300+player_velocity:
        player.x-=player_velocity
    if keys[pygame.K_RIGHT] ==True and player.x<=877-player_velocity and player.x>=300:
        player.x+=player_velocity
    x=player.x
    y=player.y

    
    if x <= 300+(3*cell_size2) and y >= 100 +(12*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100,15*cell_size2+1,10*cell_size2))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size2),100+(10*cell_size2),10*cell_size2+1,5*cell_size2+1))
    if x <=300+(3*cell_size2) and y <= 100+(3*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size2),15*cell_size2+1,10*cell_size2+1))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size2),100,10*cell_size2+1,5*cell_size2+1))
    if x>=300+(12*cell_size2) and y<=100+(3*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100,10*cell_size2,15*cell_size2+1))
        pygame.draw.rect(GAME,"lightblue",(300+(10*cell_size2),100+(5*cell_size2),5*cell_size2+1,10*cell_size2+1))
    if x>=300+(12*cell_size2) and y>= 100+(12*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100,15*cell_size2+1,(10*cell_size2)+1))
        pygame.draw.rect(GAME,"lightblue",(300,100+(10*cell_size2),10*cell_size2,5*cell_size2+1))
    if (300+(3*cell_size2))<x<(300+(12*cell_size2)):
        pygame.draw.rect(GAME,"lightblue",(300,100,x-300-(2*cell_size2),15*(cell_size2)+1))
        pygame.draw.rect(GAME,"lightblue",(x+(3*cell_size2),100,900-x-(3*cell_size2)+1,15*(cell_size2)+1))
    if (100+(3*cell_size2)) < y < (100+(12*cell_size2)):
        pygame.draw.rect(GAME,"lightblue",(300,100,15*cell_size2+1,y-(2*cell_size2)-100))
        pygame.draw.rect(GAME,"lightblue",(300,y+(3*cell_size2),15*cell_size2+1,700-y-(3*cell_size2)+1))
    if (300+(3*cell_size2))<x<(300+(12*cell_size2)) and  y >= 100 +(12*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100,15*cell_size2+1,10*cell_size2))
    if (300+(3*cell_size2))<x<(300+(12*cell_size2)) and  y <= 100 +(3*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size2),15*cell_size1+1,10*cell_size2))
    if (100+(3*cell_size2)) < y < (100+(12*cell_size2)) and x <= 300+(3*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size2),100,10*cell_size2+1,15*cell_size2+1))
    if (100+(3*cell_size2)) < y < (100+(12*cell_size2)) and x >= 300+(12*cell_size2):
        pygame.draw.rect(GAME,"lightblue",(300,100,10*cell_size2,15*cell_size2+1))    

    
      
    
   
   
def playscreen():

    global lives
    global last_collision_time
    global score
    t10=FONT.render(f"Time: {round(r_time)}s",1,"black")
    t11=FONT.render(f"Lives remaining :{lives}",1,"black")
    GAME.blit(SIMG,(0,0))
    pygame.draw.rect(GAME,"lightblue",BC)
    GAME.blit(t12,(290-t12.get_width(),640))
    GAME.blit(t13,(910,90))

    GAME.blit(t11,(150,45))
    GAME.blit(t10,(700,45))
    r1=pygame.Rect(300,100,600,1)
    r2=pygame.Rect(300,100,1,600)
    r3=pygame.Rect(300,700,600,1)
    r4=pygame.Rect(900,100,1,600)
    r=[r1,r2,r3,r4]
    for i in r:
        pygame.draw.rect(GAME,"red",i)
    pygame.draw.rect(GAME,"red",player)
    if player.colliderect(r1) and keys[pygame.K_UP]:
        if (time.time() - last_collision_time) > 1:
            lives = lives- 1
            last_collision_time=time.time()
    if player.colliderect(r2) and keys[pygame.K_LEFT]:
        if (time.time() - last_collision_time) > 1:
            lives = lives- 1
            last_collision_time=time.time()
    if player.colliderect(r3) and keys[pygame.K_DOWN]:
        if (time.time() - last_collision_time) > 1:
            lives = lives- 1
            last_collision_time=time.time()
    if player.colliderect(r4) and keys[pygame.K_RIGHT]:
        if (time.time() - last_collision_time) > 1:
            lives = lives- 1
            last_collision_time=time.time()

    for y in range(grid_height):
            for x in range(grid_width):
                rect = (300+x * cell_size,100+ y * cell_size, cell_size, cell_size) 
                if grid[y][x] == 0:
                    pygame.draw.rect(GAME,"white", rect)
                else:
                    if grid[y][x] & N == 0:
                        pygame.draw.rect(GAME,"red", (300 +(x * cell_size), 100+ (y * cell_size) + cell_size,cell_size, 1))
                        if keys[pygame.K_UP] and (100+ (y * cell_size) + cell_size -1) <= player.y <= (100+ (y * cell_size) + cell_size +1) and (300 + (x*cell_size)-25) <= player.x <= (300 + (x*cell_size) +cell_size) and player.colliderect( (300 +(x * cell_size), 100+ (y * cell_size) + cell_size,cell_size, 1)):
                            player.y = (100+ (y * cell_size) + cell_size +1)
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_DOWN] and (100+ (y * cell_size) + cell_size -23) >= player.y >= (100+ (y * cell_size) + cell_size -25) and (300 + (x*cell_size)-25) <= player.x <= (300 + (x*cell_size) +cell_size) and player.colliderect( (300 +(x * cell_size), 100+ (y * cell_size) + cell_size,cell_size, 1)):
                            player.y=100+ (y * cell_size) + cell_size -25
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_RIGHT] and(300 + (x*cell_size)-23) >= player.x >= (300 + (x*cell_size)-25) and ( 100+ (y * cell_size) + cell_size-25) < player.y < ( 100+ (y * cell_size) + cell_size+1) and player.colliderect( (300 +(x * cell_size), 100+ (y * cell_size) + cell_size,cell_size, 1)):
                            player.x=300 + (x*cell_size)-25
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_LEFT] and (300 + (x*cell_size) +cell_size -2) <= player.x <= (300 + (x*cell_size) +cell_size) and  ( 100+ (y * cell_size) + cell_size-25) < player.y < ( 100+ (y * cell_size) + cell_size+1) and player.colliderect( (300 +(x * cell_size), 100+ (y * cell_size) + cell_size,cell_size, 1)):
                            player.x=300 + (x*cell_size)+cell_size
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                    if grid[y][x] & E == 0:
                        pygame.draw.rect(GAME,"red", (300 +(x * cell_size) + cell_size,100+ (y * cell_size),1,cell_size))
                        if keys[pygame.K_RIGHT] and (300 +(x * cell_size) +cell_size -23) >= player.x >= (300 +(x * cell_size)+cell_size-25) and (100 +(y*cell_size) -25) <= player.y <= (100+ (y * cell_size) +cell_size) and player.colliderect( (300 +(x * cell_size) + cell_size,100+ (y * cell_size),1,cell_size)):
                            player.x= 300 +(x * cell_size)+cell_size-25
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_LEFT] and (300 +(x * cell_size) + cell_size +1) >= player.x >= (300 +(x * cell_size) + cell_size-1) and (100 +(y*cell_size) -25) <= player.y <= (100+ (y * cell_size) +cell_size) and player.colliderect( (300 +(x * cell_size) + cell_size,100+ (y * cell_size),1,cell_size)):
                            player.x= 300 +(x * cell_size) + cell_size+1
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_UP] and (100+ (y * cell_size)+cell_size) >= player.y >= (100+ (y * cell_size)+cell_size-2) and (300 +(x * cell_size) ) <= player.x <= (300 +(x * cell_size) + cell_size+1) and player.colliderect( (300 +(x * cell_size) + cell_size,100+ (y * cell_size),1,cell_size)):
                            player.y= 100 +(y*cell_size)+cell_size
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        if keys[pygame.K_DOWN] and (100+ (y * cell_size)-23) >= player.y >= (100+ (y * cell_size)-25) and (300 +(x * cell_size) ) <= player.x <= (300 +(x * cell_size) + cell_size+1) and player.colliderect( (300 +(x * cell_size) + cell_size,100+ (y * cell_size),1,cell_size)):
                            player.y= 100 +(y * cell_size) - 25
                            if (time.time() - last_collision_time) > 1:
                                lives = lives- 1
                                last_collision_time=time.time()
                        
                        
                



    if keys[pygame.K_UP] == True and player.y<=677 and player.y>=99+player_velocity:
        player.y-=player_velocity
    if keys[pygame.K_DOWN] ==True and player.y<=677-player_velocity and player.y>=99:
        player.y+=player_velocity
    if keys[pygame.K_LEFT] ==True and player.x<=877 and player.x>=300+player_velocity:
        player.x-=player_velocity
    if keys[pygame.K_RIGHT] ==True and player.x<=877-player_velocity and player.x>=300:
        player.x+=player_velocity
    x=player.x
    y=player.y
    if x <= 300+(3*cell_size) and y >= 100 +(7*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100,10*cell_size+1,5*cell_size))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size),100+(5*cell_size),5*cell_size+1,5*cell_size+1))
    if x <=300+(3*cell_size) and y <= 100+(3*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size),10*cell_size+1,5*cell_size+1))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size),100,5*cell_size+1,5*cell_size+1))
    if x>=300+(7*cell_size) and y<=100+(3*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100,5*cell_size,10*cell_size+1))
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size),100+(5*cell_size),5*cell_size+1,5*cell_size+1))
    if x>=300+(7*cell_size) and y>= 100+(7*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100,10*cell_size+1,(5*cell_size)+1))
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size),5*cell_size,5*cell_size+1))
    if (300+(3*cell_size))<x<(300+(7*cell_size)):
        pygame.draw.rect(GAME,"lightblue",(300,100,x-300-(2*cell_size),10*(cell_size)+1))
        pygame.draw.rect(GAME,"lightblue",(x+(3*cell_size),100,900-x-(3*cell_size)+1,10*(cell_size)+1))
    if (100+(3*cell_size)) < y < (100+(7*cell_size)):
        pygame.draw.rect(GAME,"lightblue",(300,100,10*cell_size+1,y-(2*cell_size)-100))
        pygame.draw.rect(GAME,"lightblue",(300,y+(3*cell_size),10*cell_size+1,700-y-(3*cell_size)+1))
    if (300+(3*cell_size))<x<(300+(7*cell_size)) and  y >= 100 +(7*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100,10*cell_size+1,5*cell_size))
    if (300+(3*cell_size))<x<(300+(7*cell_size)) and  y <= 100 +(3*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100+(5*cell_size),10*cell_size+1,5*cell_size))
    if (100+(3*cell_size)) < y < (100+(7*cell_size)) and x <= 300+(3*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300+(5*cell_size),100,5*cell_size+1,10*cell_size+1))
    if (100+(3*cell_size)) < y < (100+(7*cell_size)) and x >= 300+(7*cell_size):
        pygame.draw.rect(GAME,"lightblue",(300,100,5*cell_size,10*cell_size+1))    

    
def endscreen():
    """
    this is the game over screen and it displays the score and the other small requirements as needed
    """
    END.blit(SIMG,(0,0))
    END.blit(t5,(int((WIDTH-t5.get_width())/2),50))
    END.blit(t6,(int((WIDTH-t6.get_width())/2),250))
    END.blit(t7,(int((WIDTH-t7.get_width())/2),350))
    END.blit(t8,(int((WIDTH-t8.get_width())/2),450))
    END.blit(t9,(int((WIDTH-t9.get_width())/2),550))
    END.blit(j,(int((WIDTH-j.get_width())/2),int(150-(j.get_height()/2))))
    
currentscreen=startscreen
run=True
#initializing the three mazes 
grid=[[0 for _ in range(grid_width)] for _ in range(grid_height)]
passage(grid,0,0,grid_width,grid_height)
grid1=[[0 for _ in range(grid_width1)] for _ in range(grid_height1)]
passage(grid1,0,0,grid_width1,grid_height1)
grid2=[[0 for _ in range(grid_width2)] for _ in range(grid_height2)]
passage(grid2,0,0,grid_width2,grid_height2)

while run:

    clock.tick(60)#setting the frame rate
    keys = pygame.key.get_pressed()#checking if that key is pressed
    if keys[pygame.K_q] == True:#if the q key is pressed then the game quits
        run=False
    if keys[pygame.K_RETURN] == True and currentscreen == startscreen and level==1:#if the enter key is pressed and the current screen is the start screen and the level is 1 then the current screen is the play screen and it is similar to the other two levels
        currentscreen=playscreen
        player.x=310
        player.y=665
        start_time=time.time()
    if keys[pygame.K_RETURN] == True and currentscreen == startscreen and level==2:
        currentscreen=playscreen1
        player.x=310
        player.y=665
        start_time=time.time()
    if keys[pygame.K_RETURN] == True and currentscreen == startscreen and level==3:
        currentscreen=playscreen2
        player.x=310
        player.y=665
        start_time=time.time()
    if currentscreen==startscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#if the event is quit then the game quits
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:#if the event is mouse button down then the mouse position is set to the mouse position
                mouse_pos = pygame.mouse.get_pos()
                if up_button.is_clicked(mouse_pos) and level < 3:#if the up button is clicked and the level is less than 3 then the level is increased
                    level += 1  # Increase level and not allowing more than 3
                if down_button.is_clicked(mouse_pos):
                    level = max(1, level - 1)  # Decrease level, not allowing less than 1
    if keys[pygame.K_SPACE] == True and currentscreen == endscreen:#if the space key is pressed and the current screen is the end screen then the current screen changes to play screens according to the level u choose
        if level==1:
            currentscreen=playscreen
        if level==2:
            currentscreen=playscreen1
        if level==3:
            currentscreen=playscreen2
        player.x=310
        player.y=665
        start_time=time.time()
    if keys[pygame.K_m] == True and currentscreen == endscreen:#if the m key is pressed and the current screen is the end screen then the current screen changes to the start screen
        level=1
        currentscreen=startscreen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#if the event is quit then the game quits
            run=False
    if currentscreen==playscreen:#setting a timer and if the timer is 0 calculating the score and print it on end screen nd this same goes for the other two levels
        elapsed_time=time.time() - start_time
        r_time = 60-round(elapsed_time)
        if r_time==0:
            currentscreen=endscreen
            j=t15
            x=(player.x-300)//cell_size
            y=(700-player.y)//cell_size
            score=(x+y)*(lives+1)
            t6=FONT.render(f"Score :{score}",1,"black")
            grid=[[0 for _ in range(grid_width)] for _ in range(grid_height)]
            passage(grid,0,0,grid_width,grid_height)
            lives=5
            
    if currentscreen==playscreen1:
        elapsed_time=time.time() - start_time
        r_time = 100-round(elapsed_time)
        if r_time==0:
            currentscreen=endscreen
            j=t15
            x=(player.x-300)//cell_size1
            y=(700-player.y)//cell_size1
            score=(x+y)*(lives1+1)
            t6=FONT.render(f"Score :{score}",1,"black")
            grid1=[[0 for _ in range(grid_width1)] for _ in range(grid_height1)]
            passage(grid1,0,0,grid_width1,grid_height1)
            lives1=5
    if currentscreen==playscreen2:
        elapsed_time=time.time() - start_time
        r_time = 170-round(elapsed_time)
        if r_time==0:
            currentscreen=endscreen
            j=t15
            x=(player.x-300)//cell_size2
            y=(700-player.y)//cell_size2
            score=(x+y)*(lives2+1)
            t6=FONT.render(f"Score :{score}",1,"black")
            grid2=[[0 for _ in range(grid_width2)] for _ in range(grid_height2)]
            passage(grid2,0,0,grid_width2,grid_height2)
            lives2=5
    if (300+(9*cell_size)) < player.x < (300+(10*cell_size)) and 101 < player.y < (100 +cell_size) and currentscreen== playscreen:#if player reaches the end of the maze and so calculating score and changing the currentscreen to end screen and resetting the maze andthis same goes for other two levels
        currentscreen=endscreen
        j=t14
        score = (20*(lives+1))+r_time
        t6=FONT.render(f"Score :{score}",1,"black")
        grid=[[0 for _ in range(grid_width)] for _ in range(grid_height)]
        passage(grid,0,0,grid_width,grid_height)
        lives=5
    if (300+(11*cell_size1)) < player.x < (300+(12*cell_size1)) and 101 < player.y < (100 +cell_size1) and currentscreen== playscreen1:
        currentscreen=endscreen
        j=t14
        score = (24*(lives1+1))+r_time
        t6=FONT.render(f"Score :{score}",1,"black")
        grid1=[[0 for _ in range(grid_width1)] for _ in range(grid_height1)]
        passage(grid1,0,0,grid_width1,grid_height1)
        lives1=5
    if (300+(14*cell_size2)) < player.x < (300+(15*cell_size2)) and 101 < player.y < (100 +cell_size2) and currentscreen== playscreen2:
        currentscreen=endscreen
        j=t14
        score = (30*(lives2+1))+r_time
        t6=FONT.render(f"Score :{score}",1,"black")
        grid2=[[0 for _ in range(grid_width2)] for _ in range(grid_height2)]
        passage(grid2,0,0,grid_width2,grid_height2)
        lives2=5
    if currentscreen==playscreen and lives==0:#player loses the game but giving some score to make him happy 
        currentscreen=endscreen
        j=t15
        x=(player.x-300)//(cell_size)
        y=(700-player.y)//(cell_size)
        score=x+y
        t6=FONT.render(f"Score :{score}",1,"black")
        grid=[[0 for _ in range(grid_width)] for _ in range(grid_height)]
        passage(grid,0,0,grid_width,grid_height)
        lives=5
    if currentscreen==playscreen1 and lives1==0:
        currentscreen=endscreen
        j=t15
        x=(player.x-300)//(cell_size1)
        y=(700-player.y)//(cell_size1)
        score=x+y
        t6=FONT.render(f"Score :{score}",1,"black")
        grid1=[[0 for _ in range(grid_width1)] for _ in range(grid_height1)]
        passage(grid1,0,0,grid_width1,grid_height1)
        lives1=5
    if currentscreen==playscreen2 and lives2==0:
        currentscreen=endscreen
        j=t15
        x=(player.x-300)//(cell_size2)
        y=(700-player.y)//(cell_size2)
        score=x+y
        t6=FONT.render(f"Score :{score}",1,"black")
        grid2=[[0 for _ in range(grid_width2)] for _ in range(grid_height2)]
        passage(grid2,0,0,grid_width2,grid_height2)
        lives2=5
   
    
    currentscreen()#call the current screen function
    pygame.display.update()#update the display after every iteration
pygame.quit()#quit pygame