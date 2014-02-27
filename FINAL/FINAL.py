#Name - Aditya Bist
#Section - A
#ID - abist
#Project Name - Pysics
#Time spent ~ 80 - 85 hours

## PS -

## I tried a lot to adhere to style, keeping each line less than 80 characters,
## including the ones in this paragraph, but because of pygame does not have a
## root.mainloop() like Tkinter and since the whole program is in a while loop,
## the indentation keeps on increasing as more cases emerge. There are still
## few lines I wish I could've chopped down to 80 chars somehow, but couldn't.

#######################################################################################################################################################################
                                                                          # IMPORTS #
#######################################################################################################################################################################

import pygame
import random
import math 
import pygame.mixer

#######################################################################################################################################################################
                                                                         #  CONSTANTS  #
#######################################################################################################################################################################

########################### PROGRAM INITIATORS AND CONSTANTS ######################
                                                                                 ##
(width, height) = (1024, 685) #screen size                                       ##
drag = 1.0 #air drag (didn't use though)                                         ##
gravity = (math.pi, 1) #gravity vector                                           ##
pygame.font.init() #initiate pygame font                                         ##
pygame.mixer.init() #initiate pygame music player                                ##
myFont = pygame.font.SysFont("Verdana", 14) #type of font                        ##
menuFont = pygame.font.SysFont("Comic Sans MS", 45) #another type of font        ##
photo = pygame.image.load("lol.jpg") #background image                           ##
song = pygame.mixer.Sound("music.ogg") #background music                         ##
mainMenu = pygame.image.load("mainmenu.gif") #title logo                         ##
                                                                                 ##
###################################################################################

############################### TEXT ################################################                                                                                   ##
                                                                                   ##
squareText = myFont.render("Click to create square or Press S", 1, (255,255,0))    ##                                                                                   ##
circleText = myFont.render("Click to create circle or Press C", 1, (255,255,0))    ##
mainMenuText = myFont.render("Main Menu", 1, (255,255,0))                          ##
pauseText = myFont.render("Pause or Press P", 1, (255,255,0))                      ##
winText = menuFont.render("You win.....for now", 1, (255,255,0))                   ##
resumeText = menuFont.render("Paused!", 5, (255,255,0))                            ##
restartText = myFont.render("Restart", 5, (255,255,0))                             ##
level1 = menuFont.render("LEVEL 1", 5, (0,0,255))                                  ##
level2 = menuFont.render("LEVEL 2", 5, (255,0,0))                                  ##
play = menuFont.render("PLAY", 5, (0,0,255))                                       ##
back = menuFont.render("BACK", 5, (0,0,255))                                       ##
instructions = menuFont.render("INSTRUCTIONS", 5, (255,0,0))                       ##
ext = menuFont.render("EXIT", 5, (255,255,0))                                      ##
pauseMusicText = myFont.render("Pause Music", 10, (0,0,255))                       ##
resumeMusicText = myFont.render("Resume Music", 10, (0,0,255))                     ##
                                                                                   ##
#####################################################################################


############################## instruction text ################################
instructionTextString1 = " The objective of the game is to steer the"         ##
instructionTextString2 = " blue ball to the destination star using physics."  ##
instructionTextString3 = "Click and drag on the screen"                       ##
instructionTextString4 = "to draw different shapes."                          ##
instructionText1 = menuFont.render(instructionTextString1 , 5, (255,255,0))   ##
instructionText2 = menuFont.render(instructionTextString2 , 5, (255,255,0))   ##
instructionText3 = menuFont.render(instructionTextString3 , 5, (255,255,0))   ##
instructionText4 = menuFont.render(instructionTextString4 , 5, (255,255,0))   ##
################################################################################



################## BOOLEANS ####################
makeCircle = False                            ##
makeSquare = False                            ##
makeStaticCircle = False                      ##
makeStaticSquare = False                      ##
pause = False                                 ##
gameInProcess = False                         ##
instructionsInProcess = False                 ##
level1Running = False                         ##
level2Running = False                         ##
gameOver = False                              ##
################################################
        
#######################################################################################################################################################################
                                                                        #  GAME FUNCTIONS #
#######################################################################################################################################################################                                                                    


def wonGame(): #if the game is won
    winText = menuFont.render("You win......for now", 5, (255,255,0))
    screen.blit(winText, (310,500))

#sin and cos are switched because y axis in python is reversed :(
def addVectors((angle1, magnitude1), (angle2, magnitude2)): 
    x  = math.sin(angle1) * magnitude1 + math.sin(angle2) * magnitude2
    y  = math.cos(angle1) * magnitude1 + math.cos(angle2) * magnitude2
    angle = math.pi/2 - math.atan2(y, x) #angle of resulting vector
    magnitude  = (x**2 + y**2)**0.5 #magnitude of vector 
    return (angle, magnitude)


def collide(p1, p2): #collision detection
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = (dx**2 + dy**2)**0.5
    #if the distance between their centres
    #is smaller than their individual sizes
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi #arctan dy/dx
        totalMass = p1.mass + p2.mass

        #after collision, v1 = (m1-m2)u1/(m1+m2) + 2m2u2/(m1+m2)
        # where v1 is the final velocity of particle 1
        # u1 is the initial veolcity of particle 1
        # u2 is the intitial veolcity of particle 2
        (p1.angle, p1.speed) = addVectors((p1.angle,
                                           p1.speed*(p1.mass-p2.mass)/
                                           totalMass),
                                          (angle, 2*p2.speed*p2.mass/totalMass))
        #similarly, for particle 2
        (p2.angle, p2.speed) = addVectors((p2.angle,
                                           p2.speed*(p2.mass-p1.mass)/
                                           totalMass),
                                          (angle+math.pi,
                                           2*p1.speed*p1.mass/totalMass))
        #here angle+math.pi because the direction is opposite
        p1.speed *= p2.elasticity #change in particle1's speed
        p2.speed *= p1.elasticity #change in particle2's speed

        #overlap is close to (p1.size + p2.size - dist)
        # but not equal to that because in the case
        # when overlap = 0, the particles don't
        #change positions at all
        overlap = 0.5*(p1.size + p2.size - dist+1) #not accurate overlap remove
        p1.x += math.sin(angle)*overlap #horizontal position for particle 1
        p1.y -= math.cos(angle)*overlap #vertical position for particle 1
        p2.x -= math.sin(angle)*overlap #horizontal position for particle 2
        p2.y += math.cos(angle)*overlap #vertical position for particle 2
        
class Shape(object): #class to make a physics following shape
    def __init__(self, (x, y), size, mass = 400):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.colour = (255, 255, 255)
        self.thickness = 1
        self.speed = 0 
        self.angle = 0 
        self.elasticity = 0.8 #elasticity or coefficient of resitution

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed #change in x
        self.y -= math.cos(self.angle) * self.speed #change in y
        #change in y is negative because y increases downwards in python
        self.speed *= drag #speed * drag

    def bounce(self): #the four boundaries of the screen
        if self.x > width - self.size: #right wall
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle #opposite direction of angle
            self.speed *= self.elasticity #change in speed
            

        elif self.x < self.size: #left wall
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity 
            

        if self.y > height - self.size: #the bottom
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity  
            

        elif self.y < self.size: #the top
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity 


class Ball(Shape): #make the game ball with physics
    def __init__(self, (x, y), size, mass = 1000):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.colour = (0, 0, 255)
        self.thickness = 5
        self.speed = 0
        self.angle = 0
        self.elasticity = 0.8 

    def draw(self):
        pygame.draw.circle(screen, self.colour,
                           (int(self.x),int(self.y)),
                           self.size, self.thickness)
    

class Circle(Shape): #draw circle with physics
    def draw(self):
        pygame.draw.circle(screen, self.colour,
                           (int(self.x),int(self.y)),
                           self.size, self.thickness)

class Square(Shape): #draw square with physics
    def draw(self):
        pygame.draw.rect(screen, self.colour,
                         (int(self.x-self.size),int(self.y-self.size),
                          2*self.size,2*self.size), self.thickness)

class Star(object): #class to make star
    def __init__(self,(x,y), mass = 99**99):
        self.x = x
        self.y = y
        self.size = 5
        self.mass = mass
        self.angle = 0
        self.speed = 0
        self.elasticity = 0.8

    def move(self): #doesn't move
        pass

    def bounce(self): #doesn't bounce
        pass
    
    def draw(self): #draw function
        self.picture = pygame.image.load("foo.gif")
        screen.blit(self.picture,(self.x,self.y))


class StaticShape(object): #class to make a non moving shape
    def __init__(self, (x, y), size, mass = 1600):
        self.x = x
        self.y = y
        self.mass = mass
        self.size = size
        self.colour = (255, 255, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.elasticity = 1.0 #perfectly elastic

    def move(self): #doesn't move
        pass

    def bounce(self): #doesn't bounce
        pass
        
class StaticCircle(StaticShape): #draw a non moving circle
    def draw(self):
        pygame.draw.circle(screen, self.colour,
                           (int(self.x),int(self.y)), self.size, self.thickness)

class StaticSquare(StaticShape): #draw a non moving square
    def draw(self):
        pygame.draw.rect(screen, self.colour,
                         (int(self.x-self.size),int(self.y-self.size),
                          2*self.size,2*self.size), self.thickness)
    
def instructionSet(): #instruction set to show in each level
    screen.blit(photo, (0,0))
    pygame.draw.rect(screen, (0,0,0), (50,20,255,50), 2)
    pygame.draw.rect(screen, (0,0,0), (340,20,230,50), 2)
    pygame.draw.rect(screen, (0,0,0), (605,20,100,50), 2)
    pygame.draw.rect(screen, (0,0,0), (740,20,140,50), 2)
    pygame.draw.rect(screen, (0,0,0), (915,20,100,50), 2)
    screen.blit(restartText, (925, 35))
    screen.blit(pauseText, (750,35))
    screen.blit(mainMenuText, (615, 35))
    screen.blit(squareText, (60, 35))
    screen.blit(circleText, (350, 35))

def directionSet(): #directions on how to play game
    screen.blit(photo,(0,0))
    screen.blit(instructionText1, (50,100))
    screen.blit(instructionText2, (50,200))
    screen.blit(instructionText3, (50,300))
    screen.blit(instructionText4, (50,400))
    screen.blit(back, (420,550)) 
    
def mainMenuSet(): #main menu
    screen.blit(photo,(0,0))
    screen.blit(ext, (450,440))
    screen.blit(instructions, (340, 370))
    screen.blit(play, (450, 300))
    screen.blit(mainMenu, (290, 20))
    screen.blit(pauseMusicText, (710,20))
    screen.blit(resumeMusicText, (860,20))
    pygame.draw.rect(screen, (0,0,0), (700,20,105,30), 2)
    pygame.draw.rect(screen, (0,0,0), (850,20,125,30), 2)
    

def gamePlayMenu(): #game play menu
    screen.blit(photo,(0,0))
    screen.blit(level1, (420,200))
    screen.blit(level2, (420,400))
    screen.blit(back, (430,550))
    
def pauseMenu(): #pause screen
    screen.blit(resumeText, (420,200))   
        
screen = pygame.display.set_mode((width, height)) #generate screen
pygame.display.set_caption('Pysics') #title bar caption

########################################################################################################################################################################
                                                                        # GAME LOOP #
#######################################################################################################################################################################
                                                                        
while True:
    mainMenuSet()
    song.play(-1) #play music indeifnitely
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #quit pygame
            
        elif event.type == pygame.KEYDOWN: #keypressed
            if event.key == pygame.K_p: #pause game
                if pause == False:
                    pause = True
                else: pause = False

        elif event.type == pygame.MOUSEMOTION: #if mouse movement
            (mouseX,mouseY) = pygame.mouse.get_pos()
            if ((mouseX > 440 ) and (mouseX < 570 ) and
                (mouseY > 300 ) and (mouseY < 360)):
                pygame.draw.rect(screen, (0,0,0),
                                 (440,300,130,60), 2) # play

            elif ((mouseX > 330) and (mouseX < 755) and
                  (mouseY > 370) and (mouseY < 430)):
                pygame.draw.rect(screen, (0,0,0),
                                 (330,370,385,60), 2) #instructions

            elif ((mouseX > 440) and (mouseX < 570) and
                  (mouseY > 440) and (mouseY < 500)): 
                pygame.draw.rect(screen, (0,0,0),
                                 (440,440,130,60), 2) #exit

        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            (mouseX,mouseY) = pygame.mouse.get_pos()
            if ((mouseX > 440) and (mouseX < 570) and
                (mouseY > 440) and (mouseY < 500)):
                pygame.quit() #exit

            elif ((mouseX > 700) and (mouseX < 805) and
                  (mouseY > 20) and (mouseY < 50)):
                pygame.mixer.pause() #pause music

            elif ((mouseX > 850) and (mouseX < 975) and
                  (mouseY > 20) and (mouseY < 50)):
                pygame.mixer.unpause() #resume music

            elif ((mouseX > 330) and (mouseX < 755) and
                  (mouseY > 370) and (mouseY < 430)):
                instructionsInProcess = True #instructions
                while instructionsInProcess == True:
                    directionSet() #show instructions                        
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()

                        elif event.type == pygame.MOUSEMOTION: 
                            (mouseX,mouseY) = pygame.mouse.get_pos()
                            #back highlight
                            if ((mouseX > 410) and (mouseX < 550) and
                                (mouseY > 555) and (mouseY < 605)):
                                pygame.draw.rect(screen, (0,0,0),
                                                 (410,555,140,50), 2) 
                                pygame.display.flip()

                        elif event.type == pygame.MOUSEBUTTONDOWN: #back
                            (mouseX,mouseY) = pygame.mouse.get_pos()
                            #back click
                            if ((mouseX > 410) and (mouseX < 550) and
                                (mouseY > 555) and (mouseY < 605)):
                                instructionsInProcess = False
                                
            elif ((mouseX > 440) and (mouseX < 570) and
                  (mouseY > 300) and (mouseY < 360)):
                gameInProcess = True #game mode start
                pause = False
                while gameInProcess == True:
                    gamePlayMenu() #show game menu
                    pygame.display.flip() 
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()

                            elif event.type == pygame.MOUSEMOTION:
                                (mouseX,mouseY) = pygame.mouse.get_pos()

                                if ((mouseX > 410) and (mouseX < 590) and
                                    (mouseY > 200) and (mouseY < 260)):
                                    pygame.draw.rect(screen, (0,0,0),
                                                     (410,200,180,60), 2)
                                    pygame.display.flip() #level1

                                elif ((mouseX > 410) and (mouseX < 600) and
                                      (mouseY > 400) and (mouseY < 460)):
                                    pygame.draw.rect(screen, (0,0,0),
                                                     (410,400,190,60), 2)
                                    pygame.display.flip() #level2

                                elif ((mouseX > 420) and (mouseX < 560) and
                                      (mouseY > 555) and (mouseY < 605)):
                                    pygame.draw.rect(screen, (0,0,0),
                                                     (420,555,140,50), 2)
                                    pygame.display.flip() #back

                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                (mouseX,mouseY) = pygame.mouse.get_pos()
                                if ((mouseX > 420) and (mouseX < 560) and
                                    (mouseY > 555) and (mouseY < 605)):
                                    gameInProcess = False #back

                                elif ((mouseX > 410) and (mouseX < 600) and
                                      (mouseY > 400) and (mouseY < 460)):
                                    level2Running = True
                                    
###########################################################################################################################################################################
                                                                  #  LEVEL 2  #
#######################################################################################################################################################################
                                    #all shapes to start with
                                    square1 = StaticSquare((600,
                                                            600),
                                                           30)
                                    circle = Circle((200,
                                                     200),
                                                    20)
                                    circle2 = Circle((700,
                                                      200),
                                                     20)
                                    circle2.speed = 0.8
                                    circle2.elasticity = 1
                                    circle.speed = 0.8
                                    circle.elasticity = 1
                                    square2 = StaticSquare((300,
                                                            600),
                                                           30)
                                    ball = Ball((100,100),20)
                                    star = Star((920,600))
                                    #list of shapes
                                    myParticles = [ball,
                                                   star,
                                                    square1,
                                                   circle,
                                                   square2,
                                                    circle2]
                                    while level2Running == True:
                                        instructionSet() #level 2 loop
                                        pygame.display.flip()
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                            
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                (mouseX,mouseY) = pygame.mouse.get_pos()
                                                if ((mouseX > 50) and
                                                    (mouseX < 305) and
                                                    (mouseY > 20) and
                                                    (mouseY < 70)):
                                                    makeSquare = True #square
                                                    makeCircle = False
                                                elif ((mouseX > 340) and
                                                      (mouseX < 570) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    makeSquare = False #circle
                                                    makeCircle = True
                                                elif ((mouseX > 605) and
                                                      (mouseX < 705) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    gameInProcess = False #menu
                                                    level2Running = False
                                                    gameOver = False
                                                elif ((mouseX > 740) and
                                                      (mouseX < 880) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    if pause == False: #pause
                                                        pause = True
                                                    else: pause = False
                                                elif ((mouseX > 915) and
                                                      (mouseX < 1015) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    level2running = False #restart
                                                    level2running = True
                                                    gameOver = False
                                                    pause = False
                                                    #load particles again
                                                    square1 = StaticSquare((600,
                                                                            600),
                                                                           30)
                                                    circle = Circle((200,
                                                                     200),
                                                                    20)
                                                    circle2 = Circle((700,
                                                                      200),
                                                                     20)
                                                    circle2.speed = 0.8
                                                    circle2.elasticity = 1
                                                    circle.speed = 0.8
                                                    circle.elasticity = 1
                                                    square2 = StaticSquare((300,
                                                                            600),
                                                                           30)
                                                    ball = Ball((100,100),20)
                                                    star = Star((920,600))
                                                    #list of shapes
                                                    myParticles = [ball,
                                                                   star,
                                                                    square1,
                                                                   circle,
                                                                   square2,
                                                                   circle2]                                                                                         

                                            elif event.type == pygame.MOUSEBUTTONUP:
                                                (dX,dY) = pygame.mouse.get_pos()
                                                
                                                if ((makeSquare == True) and
                                                    (makeCircle == False)):
                                                    #make square
                                                    particle2 = Square((mouseX, mouseY), abs(mouseX-dX)+1,(abs(mouseX-dX)+1)**2)
                                                    particle2.speed = 0
                                                    particle2.angle =  math.pi*2 
                                                    myParticles.append(particle2)            

                                                elif ((makeSquare == False) and
                                                      (makeCircle == True)):
                                                    #make circle
                                                    particle3 = Circle((mouseX, mouseY), abs(mouseX-dX)+1, (abs(mouseX-dX)+1)**2)
                                                    particle3.speed = 0
                                                    particle3.angle = math.pi*2
                                                    myParticles.append(particle3)
                                                    
                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_s:
                                                    makeSquare = True #square
                                                    makeCircle = False
                                                elif event.key == pygame.K_c:
                                                    makeSquare = False #circle
                                                    makeCircle = True
                                                elif event.key == pygame.K_p:
                                                    if pause == False: #pause
                                                        pause = True
                                                    else: pause = False
                                                elif event.key == pygame.K_r:
                                                    #restart
                                                    level2running = False
                                                    level2running = True
                                                    square1 = StaticSquare((600,
                                                                            600),
                                                                           30)
                                                    circle = Circle((200,
                                                                     200),
                                                                    20)
                                                    circle2 = Circle((700,
                                                                      200),
                                                                     20)
                                                    circle2.speed = 0.8
                                                    circle2.elasticity = 1
                                                    circle.speed = 0.8
                                                    circle.elasticity = 1
                                                    square2 = StaticSquare((300,
                                                                            600),
                                                                           30)
                                                    ball = Ball((100,100),20)
                                                    star = Star((920,600))
                                                    #list of shapes
                                                    myParticles = [ball,
                                                                   star,
                                                                    square1,
                                                                   circle,
                                                                   square2,
                                                                   circle2] 
                                                    
                                                    
                                        if pause == False and gameOver == False:
                                            #adding shapes to list for collision
                                            for i,particle in enumerate(myParticles): #for multiple collisions
                                                particle.move()
                                                particle.bounce()
                                                for particle2 in myParticles[i+1:]:
                                                    collide(particle, particle2)                                                                                                                                                                     
                                                particle.draw()
                                            #if ball and star collide    
                                            if ((ball.x + ball.size >
                                                 star.x + star.size) and
                                                (ball.y + ball.size >
                                                 star.y + star.size)):
                                                gameOver = True
                                            pygame.display.flip()

                                        elif ((gameOver == False) and
                                              (pause == True)):
                                            #paused
                                                pauseMenu()
                                                pygame.display.flip()

                                        elif (gameOver == True):
                                            #game over
                                            screen.blit(winText, (350,500))
                                            pygame.display.flip()
                                            pause = True
                                                             
                                        
#####################################################################################################################################################################
                                                                     # LEVEL 1 #
#####################################################################################################################################################################


                                elif ((mouseX > 410) and
                                      (mouseX < 590) and
                                      (mouseY > 200) and
                                      (mouseY < 260)):
                                    level1Running = True
                                    ball = Ball((100,100),20)
                                    star = Star((920,600))
                                    myParticles = [ball,star]
                                    
                                    while level1Running == True:
                                        #level 1 loop
                                        instructionSet()
                                        pygame.display.flip()
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                            
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                (mouseX,mouseY) = pygame.mouse.get_pos()
                                                if ((mouseX > 50) and
                                                    (mouseX < 305) and
                                                    (mouseY > 20) and
                                                    (mouseY < 70)):
                                                    makeSquare = True #square
                                                    makeCircle = False
                                                elif ((mouseX > 340) and
                                                      (mouseX < 570) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    makeSquare = False #circle
                                                    makeCircle = True
                                                elif ((mouseX > 605) and
                                                      (mouseX < 705) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    gameInProcess = False #menu
                                                    level1Running = False
                                                    gameOver = False
                                                    
                                                elif ((mouseX > 740) and
                                                      (mouseX < 880) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    if pause == False: #pause
                                                        pause = True
                                                    else: pause = False
                                                elif ((mouseX > 915) and
                                                      (mouseX < 1015) and
                                                      (mouseY > 20) and
                                                      (mouseY < 70)):
                                                    #restart
                                                    level1running = False 
                                                    level1running = True
                                                    gameOver = False
                                                    pause = False
                                                    ball = Ball((100,100),20)
                                                    star = Star((920,600))
                                                    myParticles = [ball,star]                                                      

                                            elif event.type == pygame.MOUSEBUTTONUP:
                                                (dX,dY) = pygame.mouse.get_pos()
                                                
                                                if ((makeSquare == True) and
                                                    (makeCircle == False)):
                                                    #make square
                                                    particle2 = Square((mouseX,mouseY),abs(mouseX-dX)+1,(abs(mouseX-dX)+1)**2)
                                                    particle2.speed = 0
                                                    particle2.angle =  math.pi*2 
                                                    myParticles.append(particle2)            

                                                elif ((makeSquare == False) and
                                                      (makeCircle == True)):
                                                    #make circle
                                                    particle3 = Circle((mouseX,mouseY),abs(mouseX-dX)+1,(abs(mouseX-dX)+1)**2)
                                                    particle3.speed = 0
                                                    particle3.angle = math.pi*2
                                                    myParticles.append(particle3)
                                                    
                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_s:
                                                    #square
                                                    makeSquare = True
                                                    makeCircle = False
                                                elif event.key == pygame.K_c:
                                                    #circle
                                                    makeSquare = False
                                                    makeCircle = True
                                                elif event.key == pygame.K_p:
                                                    #pause
                                                    if pause == False:
                                                        pause = True
                                                    else: pause = False
                                                elif event.key == pygame.K_r:
                                                    #restart
                                                    level1running = False
                                                    level1running = True
                                                    ball = Ball((100,100),20)
                                                    star = Star((920,600))
                                                    myParticles = [ball,star]
                                                    
                                                    
                                        if pause == False and gameOver == False:
                                            #for multiple collisions
                                            #add all particles to list
                                            for i,particle in enumerate(myParticles): 
                                                particle.move()
                                                particle.bounce()
                                                for particle2 in myParticles[i+1:]:
                                                    collide(particle,
                                                            particle2)                                                                                                                                                                     
                                                particle.draw()
                                            #if ball and star collide    
                                            if ((ball.x + ball.size >
                                                 star.x + star.size)
                                                and (ball.y + ball.size >
                                                     star.y + star.size)):
                                                gameOver = True
                                            pygame.display.flip()

                                        elif ((gameOver == False) and
                                              (pause == True)):
                                            #paused
                                                pauseMenu()
                                                pygame.display.flip()

                                        elif (gameOver == True):
                                            screen.blit(winText, (350,500))
                                            pygame.display.flip()
                                            pause = True                                                                                           

    pygame.display.flip()

####################################################################################################################################################################
####################################################################################################################################################################
