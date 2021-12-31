import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
    def __init__(self, ai_game):
        #initializing scoreboard attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font setting
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)


        #prepare initial score image
        self.prep_score() 
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self): #turn score into rendered image
        rounded_score = round(self.stats.score, -1) # tells python to round the value of stats.score to nearest 10 ans store it in rounded_score #format the score to include comma seprators in large numbers
        score_str = "{:,}".format(rounded_score) #turn numerical value into string and insert commas
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color ) #pass the string to render() which creates image

        #display score at top right of screen
        self.score_rect = self.score_image.get_rect() #to make sure score always lines up with right side of screen we create a rect called score_rect and set its right edge 20 pixels from right edge of screen
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 #place top edge 20 pixcels down from top of screen

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1) # tells python to round the value of stats.score to nearest 10 ans store it in rounded_score #format the score to include comma seprators in large numbers
        high_score_str = "{:,}".format(high_score) #turn numerical value into string and insert commas
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color ) #pass the string to render() which creates image

        #display high score at top of screen
        self.high_score_rect = self.high_score_image.get_rect() #to make sure score always lines up with right side of screen we create a rect called score_rect and set its right edge 20 pixels from right edge of screen
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def show_score(self): #this method draws score, high score,level images onscreen at location score_rect , high_score_rect , level_rect specifies
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen) #draws the ship


    def check_high_score(self): #checks current score against high score. if current score greater than high score, we update value of high score and call prep_high_score()
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self): #creates an image from value stored in stats.level
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right #sets image's right attribute to match score's right attribute
        self.level_rect.top = self.score_rect.bottom + 10 #sets top attribute 10 pixels beneth bottom of score image


    def prep_ships(self):
        self.ships = Group() #creates empty group to hold ship instances
        for ship_number in range(self.stats.ship_left): #to fill this group, loop runs once for every ship the player has left
            ship = Ship(self.ai_game) #create a new ship and set each ship's x coordinate value so the ships appear next to each other with 10 pixel margin on left side of group of ships
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10 #y coordinate value 10 pixel down from top of screen
            self.ships.add(ship) #we add each new ship tp group ship