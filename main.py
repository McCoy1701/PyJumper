from re import T
import pygame, random, asyncio, time
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        playerWalk0 = pygame.image.load('graphics/player/running0.png').convert_alpha()
        playerWalk1 = pygame.image.load('graphics/player/running1.png').convert_alpha()
        self.playerWalking = [playerWalk0, playerWalk1]
        self.playerIndex = 0
        self.playerJump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.playerWalking[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (100, 200))
        self.gravity = 0
        self.jumpSound = pygame.mixer.Sound('audio/jump.ogg')
        self.jumpSound.set_volume(0.01)

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jumpSound.play()
            self.gravity = -20
    
    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 305: self.rect.bottom = 305
    
    def animate(self):
        if self.rect.bottom < 305:
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalking): self.playerIndex = 0
            self.image = self.playerWalking[int(self.playerIndex)]

    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'flyer':
            flyerF0 = pygame.image.load('graphics/flyer/Flyer0.png').convert_alpha()
            flyerF1 = pygame.image.load('graphics/flyer/Flyer1.png').convert_alpha()
            self.frames = [flyerF0, flyerF1]
            yPos = 210
        else:
            slimerF0 = pygame.image.load('graphics/pooper/slimer0.png').convert_alpha()
            slimerF1 = pygame.image.load('graphics/pooper/slimer1.png').convert_alpha()
            self.frames = [slimerF0, slimerF1]
            yPos = 300
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (random.randint(600, 700), yPos))
    
    def animate(self):
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]
    
    def update(self):
        self.animate()
        self.rect.x -= 5
        self.destory()
    
    def destory(self):
        if self.rect.x <= -50:
            self.kill()

def displayScore():
    current_time = ((pygame.time.get_ticks()- startTime) / 1000)
    scoreSf = font.render(f'Score: {int(current_time)}', False, ('black'))
    scoreRect = scoreSf.get_rect(center=(320, 100))
    screen.blit(scoreSf, scoreRect)
    return current_time

def spriteCollisions(player, obstacleGroup):
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    else: return True

def tester(obstacle_Timer):
    timer = obstacle_Timer
    timerSF = font.render(f'Timer: {int(timer)}', False, ('black'))
    timerRect = timerSF.get_rect(center = (320, 200))
    screen.blit(timerSF, timerRect)

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('PyJumper')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
gameActive = False
startTime = 0
score = 0
bgMusic = pygame.mixer.Sound('audio/fa.ogg')
bgMusic.set_volume(0.2)
bgMusic.play(loops = -1)

#intro screen
playerStand = pygame.image.load('graphics/player/down.png').convert_alpha()
playerStand = pygame.transform.scale(playerStand, (90, 180))
playerStandRect = playerStand.get_rect(center = (320, 180))

gameOverSf = font.render('YOU NEED TO WIPE!!!', False, ('black'))
gameOverRect = gameOverSf.get_rect(center = (320, 70))

startScreenSf = font.render("DON'T POOP YOUR PANTS", False, ('black'))
startScreenRect = startScreenSf.get_rect(center = (320, 300))

returnButtonSf = font.render("Enter To Start", False, ('black'))
returnButtonRect = returnButtonSf.get_rect(center = (320, 330))

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacleGroup = pygame.sprite.Group()


async def main():
    
    global gameActive, startTime, score, font, clock, screen, bgMusic
    global playerStand, playerStandRect, gameOverSf, gameOverRect, startScreenSf
    global player, obstacleGroup, startScreenRect, returnButtonRect, returnButtonSf
    x = 0
    y = 0
    test = False
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not gameActive:
                    gameActive = True
                    test = True
                    startTime = pygame.time.get_ticks()

        if gameActive:
            if test:
                x += 0.015
                if x > 1:
                    obstacleGroup.add(Obstacle(random.choice(['flyer', 'slimer', 'slimer', 'slimer', 'flyer'])))
                    y += 1
                    x = 0

        if gameActive:
            screen.blit(pygame.image.load('graphics/Sky.png').convert_alpha(), (0, 0))
            screen.blit(pygame.image.load('graphics/ground.png').convert_alpha(), (0, 300))
            score = displayScore()

            #Player
            player.draw(screen)
            player.update()

            #Obstacles
            obstacleGroup.draw(screen)
            obstacleGroup.update()

            #Collision
            gameActive = spriteCollisions(player, obstacleGroup)

        else:
            screen.fill('cyan')
            scoreMessage = font.render(f'Score: {int(score)}', False, 'black')
            scoreMessageRect = scoreMessage.get_rect(center = (320, 300))
            if score == 0:
                screen.blit(startScreenSf, startScreenRect)
                screen.blit(returnButtonSf, returnButtonRect)
                screen.blit(playerStand, playerStandRect)
            else:
                screen.blit(scoreMessage, scoreMessageRect)
                screen.blit(gameOverSf, gameOverRect)
                screen.blit(playerStand, playerStandRect)

        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
