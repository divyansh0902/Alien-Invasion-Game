import pygame
from pygame.sprite import Sprite #when use sprite ,we can group related elements in game and act on all the grouped elements at once

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__() #to inherit property from sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0,0 , self.settings.bullet_width, self.settings.bullet_height) #bullet rect attribute
        self.rect.midtop = ai_game.ship.rect.midtop #we set bullet's midtop attribute to match ship's midtop attribute

        self.y = float(self.rect.y) #we can store decimal value for y coordinate of bullet

    def update(self): #manages bullet position
        self.y -= self.settings.bullet_speed #when bullet fired it moves up the screen which correspondes to decreasing y-coordinate.
        #to update position we subtract amount stored in settings.bullet_speed from self.y
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect) #draw.rect()func fills part of screen defined by bullet's rect with color stored in self.color 


















