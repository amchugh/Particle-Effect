
import random
import math
import pygame
import sys
from pygame.locals import *

BLUE = pygame.Color(0,0,255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
WHITE = pygame.Color(255,255,255)

SPEED = 0.01
SIZE = [3,3]
PARTICLE_SIZE = [1,1]
MIN_DISTANCE = 0
MAX_DISTANCE = 40
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
PARTICLE_LIFE = 6
CIRCLE_PARTICLE_LIFE = 200
PARTICLE_LIFE_DEVIATION = 6
PARTICLE_DEVIATION = 4
DRAW_OFFSET_X = 1
DRAW_OFFSET_Y = 1
Y_SPEED = 1.2
#NUMBERS = [10,11,12,13,14,15,16,17,18,19,20]
#CHANCES = [12,10,8 ,6 ,4 ,2 ,4 , 6, 8,10,12]

class BeamParticle():
    def __init__(self,posX,posY,color):
        self.posX = posX
        self.posY = posY
        self.image = pygame.Surface(PARTICLE_SIZE)
        self.image.fill(color)
        self.updates_left = PARTICLE_LIFE + random.randint(0,PARTICLE_LIFE_DEVIATION+1)
       
    def total_update(self,window):
        if self.update():
            self.draw(window)
            return True
        else:
            return False
       
    def update(self):
        if self.updates_left == 0:
            return False
        self.updates_left -= 1
        return True
        
    def draw(self, window):
        window.blit(self.image, [self.posX,self.posY])

class Circle():
    def __init__(self):
        self.centerX = 100
        self.centerY = 100
        self.radius = 20
        self.partsPerOctant = 14
        self.image = pygame.Surface(PARTICLE_SIZE)
        self.image.fill(GREEN)
        
        self.rotateImage = pygame.Surface(SIZE)
        self.rotateImage.fill(RED)
        
        self.step = 0
        
    def draw_part(self,X,Y,window):
        window.blit(self.image, [X,Y])
        
    def draw_rotate_image(self,X,Y,window):
        window.blit(self.rotateImage, [X-1,Y-1])
        
    def do_first_method(self):
        offsetY = 0
        offsetX = self.radius
        self.rangeStep = self.step%self.partsPerOctant
        #print self.rangeStep
        for i in range(self.rangeStep):
            firstResult  = offsetX*offsetX + offsetY*offsetY
            secondResult = (offsetX-1)*(offsetX-1) + offsetY*offsetY
            radiusSquared = self.radius * self.radius
            
            subtractedfirstResult  = firstResult - radiusSquared
            subtractedsecondResult = secondResult - radiusSquared
            finalfirstResult  = math.fabs(subtractedfirstResult)
            finalsecondResult = math.fabs(subtractedsecondResult)
            if finalfirstResult >= finalsecondResult:
                offsetX -= 1
            offsetY -= 1
            
        return offsetX
        
    def do_second_method(self):
        offsetY = 0
        offsetX = self.radius
        self.rangeStep = self.step%self.partsPerOctant
        self.rangeStep = self.partsPerOctant-self.rangeStep
        #print self.rangeStep
        for i in range(self.rangeStep):
            firstResult  = offsetX*offsetX + offsetY*offsetY
            secondResult = (offsetX-1)*(offsetX-1) + offsetY*offsetY
            radiusSquared = self.radius * self.radius
            
            subtractedfirstResult  = firstResult - radiusSquared
            subtractedsecondResult = secondResult - radiusSquared
            finalfirstResult  = math.fabs(subtractedfirstResult)
            finalsecondResult = math.fabs(subtractedsecondResult)
            if finalfirstResult >= finalsecondResult:
                offsetX -= 1
            offsetY -= 1
            
        return offsetX
        
    def draw(self,window):
        self.outline_draw(window)
        self.rotate_image_draw(window)
        
    def outline_draw(self,window):
        offsetX = self.radius
        offsetY = 0
        
        self.draw_part(self.centerX+self.radius,self.centerY,window)
        self.draw_part(self.centerX-self.radius,self.centerY,window)
        self.draw_part(self.centerX,self.centerY+self.radius,window)
        self.draw_part(self.centerX,self.centerY-self.radius,window)
        
        for i in range(self.partsPerOctant):
            offsetY -= 1
            firstResult  = offsetX*offsetX + offsetY*offsetY
            secondResult = (offsetX-1)*(offsetX-1) + offsetY*offsetY
            radiusSquared = self.radius * self.radius
            
            subtractedfirstResult  = firstResult - radiusSquared
            subtractedsecondResult = secondResult - radiusSquared
            finalfirstResult  = math.fabs(subtractedfirstResult)
            finalsecondResult = math.fabs(subtractedsecondResult)
            if finalfirstResult < finalsecondResult:
                pass
                #print i,": First Result closer to zero!"
                #print "Data: ", offsetX,offsetY,firstResult,secondResult,radiusSquared,subtractedfirstResult,subtractedsecondResult,finalfirstResult,finalsecondResult
            else:
                #print i,"Second Result closer to zero!", firstResult, secondResult
                #print "Data: ", offsetX,offsetY,firstResult,secondResult,radiusSquared,subtractedfirstResult,subtractedsecondResult,finalfirstResult,finalsecondResult
                offsetX -= 1
                
# OffsetX OffsetY firstResult secondResult radiusSquared subtractedfirstResult subtractedsecondResult
# finalfirstResult finalsecondResult
                
            self.draw_part(self.centerX+offsetX,self.centerY+offsetY,window)
            self.draw_part(self.centerX-offsetY,self.centerY-offsetX,window)
            self.draw_part(self.centerX-offsetX,self.centerY-offsetY,window)
            self.draw_part(self.centerX+offsetY,self.centerY+offsetX,window)
            
            self.draw_part(self.centerX-offsetX,self.centerY+offsetY,window)
            self.draw_part(self.centerX+offsetX,self.centerY-offsetY,window)
            self.draw_part(self.centerX-offsetY,self.centerY+offsetX,window)
            self.draw_part(self.centerX+offsetY,self.centerY-offsetX,window)
        
    def rotate_image_draw(self,window):
        
        if self.step > 0 and self.step < self.partsPerOctant:
            offsetX = self.do_first_method()
            self.draw_rotate_image(self.centerX+offsetX,self.centerY-self.rangeStep,window)
            
        elif self.step >= self.partsPerOctant and self.step < self.partsPerOctant * 2:
            offsetX = self.do_second_method()
            self.draw_rotate_image(self.centerX+self.rangeStep,self.centerY-offsetX,window)
            
        elif self.step >= self.partsPerOctant * 2 and self.step < self.partsPerOctant * 3:
            offsetX = self.do_first_method()
            self.draw_rotate_image(self.centerX-self.rangeStep,self.centerY-offsetX,window)
            
        elif self.step >= self.partsPerOctant * 3 and self.step < self.partsPerOctant * 4:
            offsetX = self.do_second_method()
            self.draw_rotate_image(self.centerX-offsetX,self.centerY-self.rangeStep,window)
            
        elif self.step >= self.partsPerOctant * 4 and self.step < self.partsPerOctant * 5:
            offsetX = self.do_first_method()
            self.draw_rotate_image(self.centerX-offsetX,self.centerY+self.rangeStep,window)
            
        elif self.step >= self.partsPerOctant * 5 and self.step < self.partsPerOctant * 6:
            offsetX = self.do_second_method()
            self.draw_rotate_image(self.centerX-self.rangeStep,self.centerY+offsetX,window)
            
        elif self.step >= self.partsPerOctant * 6 and self.step < self.partsPerOctant * 7:
            offsetX = self.do_first_method()
            self.draw_rotate_image(self.centerX+self.rangeStep,self.centerY+offsetX,window)
            
        elif self.step >= self.partsPerOctant * 7 and self.step < self.partsPerOctant * 8:
            offsetX = self.do_second_method()
            self.draw_rotate_image(self.centerX+offsetX,self.centerY+self.rangeStep,window)
            
            
        self.step += 1
        if self.step >= self.partsPerOctant * 8:
            self.step = 0
        
class CircleParticle(Circle):
    def __init__(self, centerX, centerY):
        Circle.__init__(self)
        self.updates_left = CIRCLE_PARTICLE_LIFE
        self.centerX = centerX
        self.centerY = centerY
        self.radius = 20
        self.drawOutline = False
        self.partsPerOctant = int(self.radius * 2 * 3.14 / 8)
        
    def total_update(self,window):
        if self.update():
            if self.drawOutline: self.outline_draw(window)
            self.rotate_image_draw(window)
            return True
        return False
        
    def update(self):
        if self.updates_left == 0:
            return False
        self.updates_left -= 1
        return True
        
class Beam():
    def __init__(self,position,destination,slope,color,speed):
        self.drawX = position[0]
        self.drawY = position[1]
        self.posX  = float(position[0])
        self.posY  = float(position[1])
        self.destX = destination[0]
        self.destY = destination[1]
        self.slope = slope
        self.speed = speed
        self.isDead = False
        
        self.particles = []
        if self.posX > self.destX: self.doAdd = False
        else: self.doAdd = True
        
        self.image = pygame.Surface(SIZE)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    def data(self):
        return ["Draw X: " + str(self.drawX),
                "Draw Y: " + str(self.drawY),
                "Real X: " + str(self.posX),
                "Real Y: " + str(self.posY),
                "Dest X: " + str(self.destX),
                
                "Dest Y: " + str(self.destY),
                "Slope : " + str(self.slope)]
        
    def total_update(self,window):
        if not self.isDead:
            rturn = self.update()
            for particle in self.particles:
                doKeep = particle.total_update(window)
                if not doKeep:
                    particle_index = self.particles.index(particle)
                    self.particles = self.particles[:particle_index] + self.particles[particle_index+1:]
            self.draw(window)
            return rturn
        else:
            for particle in self.particles:
                doKeep = particle.total_update(window)
                if not doKeep:
                    particle_index = self.particles.index(particle)
                    self.particles = self.particles[:particle_index] + self.particles[particle_index+1:]
                    if len(self.particles) == 0:
                        return False
        
    def update(self):
    
        if self.doAdd:
            self.posX += math.fabs(self.slope)
        else:
            self.posX -= math.fabs(self.slope)
            
        self.posY += Y_SPEED
        
        if self.posX < 0 or self.posX > WINDOW_WIDTH or self.posY > WINDOW_HEIGHT:
            self.isDead = True
            if len(self.particles) == 0:
                return False
        
        self.drawX = self.posX
        self.drawY = self.posY
        
        if random.randint(0,2) == 1:
            for i in range(1):
                """
                self.particles.append(BeamParticle(
                    self.posX + random.randint(0, PARTICLE_DEVIATION) - PARTICLE_DEVIATION/2,
                    self.posY + random.randint(0, PARTICLE_DEVIATION) - PARTICLE_DEVIATION/2,
                    WHITE
                ))
                """
                self.particles.append(CircleParticle(
                    self.posX + random.randint(0, PARTICLE_DEVIATION) - PARTICLE_DEVIATION/2,
                    self.posY + random.randint(0, PARTICLE_DEVIATION) - PARTICLE_DEVIATION/2
                ))
        
        return True
        
    def draw(self, window):
        window.blit(self.image, [self.drawX-DRAW_OFFSET_X, self.drawY-DRAW_OFFSET_Y])

def find_X_slope(pos,destination,slope,color,speed):
    slopeX = 0
    posX = pos[0]
    posY = pos[1]
    destX = destination[0]
    destY = destination[1]
    
    slopeX = 1 / slope
    #print "Old Slope:",slope,"New Slope:",slopeX
    
    return slopeX
        
def findDistance():
    return (random.randint(MIN_DISTANCE,MAX_DISTANCE) - ( (MAX_DISTANCE + MIN_DISTANCE) / 2)) * 2
    
def placeBeam():
    position = [0,-1]
    #print
    #print "Going to place the beam"
    
    distance = findDistance()
    
    destination = pygame.mouse.get_pos()
    
    position[0] = destination[0] + distance
    
    if position[0] == destination[0]:
        slope = destination[1]
    else:
        slope = float(position[1] - destination[1]) / float(position[0] - destination[0])
        
    r = int(0 + math.fabs(distance) * 4)
    g = int(0 + math.fabs(distance) * 4)
    b = 255
    color = pygame.Color(r,g,b)
        
    if distance != 0:
        speed = SPEED * math.fabs(distance)
    else: speed = SPEED
        
    slope = find_X_slope(position,destination,slope,color,speed)
        
    #print "Destination: ", destination
    #print "Distance Variation: ", distance
    #print "Position: ", position
    #print "Slope: ", slope
    return Beam(position,destination,slope,color,speed)

def display_beam_data(beams):
    print
    if len(beams) != 1:
        print "There are " + str(len(beams)) + " beams."
    else:
        print "There is one beam."
    print
    for beam in beams:
        print "--- BEAM DATA ---"
        for data in beam.data():
            print data
        print
    
def erase(beam, beams):
    beam_index = beams.index(beam)
    return beams[:beam_index] + beams[beam_index+1:]
    
def setup():
    print "Hello World"
    pygame.init()
    window = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    pygame.display.set_caption("game")
    fpsClock = pygame.time.Clock()
    
    run = True
    buttonDown = False
    button2Down = False
    beams = []
    
    circle = Circle()
    circleParticle = CircleParticle(50,100)
    circleParticle.updates_left = -1
    
    while run:
        
        window.fill(0)
   
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                break
               
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and buttonDown == False:
            for i in range(1):
                beams.append(placeBeam())
            buttonDown = True
        elif not buttons[0]:
            buttonDown = False
            
        if buttons[2] and button2Down == False:
            display_beam_data(beams)
            button2Down = True
        elif not buttons[2]:
            button2Down = False
        
        for beam in beams:
            doErase = beam.total_update(window)
            if doErase == False:
                beams = erase(beam, beams)
                
        circle.draw(window)
        circleParticle.total_update(window)
                
        pygame.display.flip()
        fpsClock.tick(60)
    
if __name__ == "__main__":
    setup()