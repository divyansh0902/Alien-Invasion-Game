import pygame
from pygame.sprite import Sprite
class Ship(Sprite):

    #class to manage ship


    def __init__(self, ai_game):
        #initialize ship and set its starting position
        super().__init__()
        
        self.screen = ai_game.screen #assign screen to an attribute of ship
        self.settings = ai_game.settings #setting attribute for ship so we can use it in update()
        self.screen_rect = ai_game.screen.get_rect() #access screen's rect attribute using get_rect()method and assign it to self.screen_rect

        #load ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp') #To load the image we call pygame.image.load() and give it location of ship image
        self.rect = self.image.get_rect() #when image loaded, we call get_rect() to access ship surface's rect attribute so we can later use it to replace ship

        #start new ship at bottom centre of screen
        self.rect.midbottom = self.screen_rect.midbottom #position ship at bottom centre of screen

        self.x = float(self.rect.x) #store decimal value for ship's horizontal position

        self.moving_right = False #added a self.moving_right attribute and set it to false initialy
        self.moving_left = False

    def update(self): #moves the ship right if flag is true and left if its true. manages ship position.
        #update ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed #value of self.x adjusted by amount stored in settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #update rect object from self.x
        self.rect.x = self.x #controls position of the ship

    def blitme(self):
        #draws ship at position specified by self.rect
        self.screen.blit(self.image, self.rect)

    def center_ship(self): #center the ship on screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)





