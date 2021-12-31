import pygame.font
class Button:
    def __init__(self, ai_game, msg):
        #initialize button attribute
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #dimensions of button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48) #none argument tells pygame to use default font and 48 specifies size of text

        #build button's rect object and centre it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center #set buttons center attribute to match that of screen

        #button message needs to be prepared only once
        self._prep_msg(msg) #pygame works with text by rendering string to display an image.We call  _prep_msg() to handle this


    def _prep_msg(self, msg):#turns msg into rendered image and center text on button
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self): #draw blank button and then draw message
        self.screen.fill(self.button_color,self.rect) #draw rectangular portion of button
        self.screen.blit(self.msg_image, self.msg_image_rect) #draw text image to screen










