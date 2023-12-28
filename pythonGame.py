import pygame
import random
pygame.init()

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(640,360))
        self.speed = 5
        self.dir = None
        self.body = []                
        self.snakeLength = 0
        self.isAlive = True      

    def playerMovement(self):

        movX = 0
        movY = 0
     
        if self.rect.y < 0:
            self.rect.y = 720
        if self.rect.y > 720:
            self.rect.y = 0
        if self.rect.x < 0:
            self.rect.x = 1280
        if self.rect.x > 1280:
            self.rect.x = 0
        
        keys = pygame.key.get_pressed()
        
        if self.isAlive:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.dir = "UP"   
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.dir = "LEFT"
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.dir = "DOWN"
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.dir = "RIGHT"

        if self.isAlive == False:
            if keys[pygame.K_SPACE]:
                self.isAlive = True
                self.snakeLength = 0
            
        
         
        if self.dir == "UP":
            movX = 0
            movY = -(self.speed)
        if self.dir == "DOWN":
            movX = 0 
            movY = (self.speed)
        if self.dir == "LEFT":
            movX = -(self.speed)
            movY = 0
        if self.dir == "RIGHT":
            movX = (self.speed) 
            movY = 0
          
        if not self.body or self.body[-1] != (self.rect.x,self.rect.y):
            self.body.append((self.rect.x, self.rect.y))    

        if len(self.body) > self.snakeLength:
            del self.body[0]

        for part in self.body:
            screen.fill('white', rect=[part[0],part[1], 20, 20])

        self.rect.x += movX
        self.rect.y += movY
      
    def collision(self):
        if pygame.sprite.spritecollide(self,food,True):
            food.add(Food())
            self.snakeLength += 1          

        if len(self.body) > 2:
            for part in self.body[:-1]:
                if self.rect.x == part[0] and self.rect.y == part[1]:
                    self.isAlive = False              
                    self.reset()
               
    def calcScore(self):
        score = textFont.render(str(self.snakeLength), False, 'white' )
        score_rect = score.get_rect(center=(640,100))
        screen.blit(score, score_rect)
    
    def reset(self):

        self.body.clear()
        self.rect.x , self.rect.y = random.randint(100,1000), random.randint(200,600)
        food.remove(Food())
        food.add(Food())       
        self.dir = None

    def update(self):
        self.playerMovement()
        self.collision()
        if gameStarted and self.isAlive:
            self.calcScore()

        if not self.isAlive:
            finalScore = self.snakeLength

            gameOver = textFont.render('Game Over!', True, 'white')
            gameOver_rect = gameOver.get_rect(center=(640,100))

            finalScoreText = textFont.render(f'Final score: {self.snakeLength}', True, 'white')
            finalScoreText_rect = finalScoreText.get_rect(center=(640,140))

            gameOversub = subtextFont.render('Press Space to continue', True, 'white')
            gameOversub_rect = gameOversub.get_rect(center=(640,175))

            screen.blit(gameOver, gameOver_rect)
            screen.blit(finalScoreText,finalScoreText_rect)
            screen.blit(gameOversub, gameOversub_rect)



       

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=(random.randint(100,1000),random.randint(200,600)))

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
gameStarted = False

textFont = pygame.font.Font('graphics/retro.ttf', 50)
subtextFont = pygame.font.Font('graphics/retro.ttf', 25)
title = textFont.render('Snake', True, 'White')
titleRect = title.get_rect(center=(640,100))
subtitle = subtextFont.render('Use WASD or Arrow Keys to move', True, 'white')
subtitle_rect = subtitle.get_rect(center=(640,650))
displayTitle = pygame.display.set_caption('Snake')

snake = pygame.sprite.GroupSingle()
snake.add(Snake())

food = pygame.sprite.GroupSingle()
food.add(Food())


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            gameStarted = True
        
    screen.fill("black")
    snake.draw(screen)
  
    if not gameStarted:
        screen.blit(title, titleRect)
        screen.blit(subtitle, subtitle_rect)       
    else:
        food.draw(screen)

    snake.update()
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()