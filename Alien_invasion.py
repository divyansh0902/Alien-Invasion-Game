import sys  # use sys to exit the game when player quits
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    # overall calss to manage game assets and behavior
    def __init__(self):
        # initialize the game, and create game resources

        pygame.init()  # initializes background setting
        self.settings = Settings()  # create instance of setting and assign it to self.settings

        # this tells pygame to figure out a window size that will fill the screen
        self.screen = pygame.display.set_mode((0, 0),  pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) #assign this display window to attribute self.screen, so it is available in all methods in class

        # self.screen = pygame.display.set_mode((1200,800)) #pygame.display.set_mode((1200,800)) creates a display window of size 1200X800 and we have assined it to attribute self.screen
        # object assigned to self.screen is called a surface which is a part of screen where game elements can be displayed

        pygame.display.set_caption("Alien Invasion")

        #create instance to store game statistics
        self.stats = GameStats(self)

        self.sb = Scoreboard(self) #creates a scoreboard

        # make an instance of ship. Self argument here refers to current instance of AlienInvasion
        self.ship = Ship(self)
        # storing all the live bullets so we can manage bullets that already been fired
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() #creat a group to hold fleet of aliens

        self._create_fleet()

        self.play_button = Button(self, "PLAY") #make play button

        # set background color
        self.bg_color = (230, 230, 230)

    def run_game(self):  # game controlled by run_dame()method
        # start main loop for game

        while True:  # this while loop contains an event loop and code that manages screen updates
            self._check_events()  # we call method from inside the while loop in run_game() #always need to call check_event() even if game is inactive and rest function call only need to happen when game is active
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens() #call to update position of each alien
            self._update_screen()

    def _update_bullets(self):  # refactoring run_game
        # when we call update() on a group, group automatically calls update() for each sprite in the group
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self): #refactoring _update_bullet() #check collision  and take appropriate action
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions: #update the scoreeach time an alien is shot down

            #if 2 bullets collide with an alien during the same pass through the loop or if we make extra wide bullet, the player will only receive points for hitting one alien. To fix this we redefine the way bullet and alien collision is detected
            for aliens in collisions.values(): #we loop through all values in dictionary. Each value is a list of aliens hit by single bullet.
                self.stats.score += self.settings.alien_points * len(aliens) #we multiply value of each alien by number of aliens in each list and add this to current score
            self.sb.prep_score() #preps scoreboard with a 0 score.
            self.sb.check_high_score()

        if not self.aliens: #check whether aliens group is empty
            self.bullets.empty() #we get rid of any existing bullets
            self._create_fleet() #fills screen with aliens again
            self.settings.increase_speed() #increase game tempo

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self): #check if fleet is at the edge, then update position of all aliens in fleet
        self._check_fleet_edges()
        self.aliens.update()


        #look for alien ship collision
        if pygame.sprite.spritecollideany(self.ship , self.aliens): #if no collision occur, it would return none and the if block won't execute
            self._ship_hit()

        #look for aliens hitting bottom of screen
        self._check_aliens_bottom()

    def _ship_hit(self): #response when alien hits the ship
        if self.stats.ship_left > 0:
            #decrement ships_left
            self.stats.ship_left -= 1
            self.sb.prep_ships() #updates display of ship images when player loses a ship
    
            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
    
            #create new fleet and centrs the ship
            self._create_fleet()
            self.ship.center_ship()
    
            #pause for 0.5sec
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #check whether any aliens have reached the bottom of screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this same as if ship got hit
                self._ship_hit()
                break

    def _check_events(self):  # helps in refactoring. Made new method and moved lines that check whether player clicked to close window into this new method
        for event in pygame.event.get():  # event loop is an action that user performs while playing game. To make our program respond to events we write this event loop to listen for events and perform tasks
            # to access events that pygame detects we use pygame.event.get()func

            if event.type == pygame.QUIT:  # when player clicks game window close buttona pygame.QUIT event is detected and we call sys.exit() to exit the game
                sys.exit()

            elif event.type == pygame.KEYDOWN:  # each keypress is registered as a KEYDOWN event
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # responds to keyup events. when player releases right arrow we set moving_right to false
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN: #detect mousebutton down
                mouse_pos = pygame.mouse.get_pos() #returns a tuple containing coordinated of mouse cursor when mouse button is clicked 
                self._check_play_button(mouse_pos) #we send these values to new method

    def _check_play_button(self, mouse_pos): #starts new game when player clicks play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) #stores a true or false value 
        if button_clicked and not self.stats.game_active: # game will restart only if play is clicked and game is not currently active
            self.settings.initialize_dynamic_settings() #reset game settings
            self.stats.reset_stats() #restart game statistics
            self.stats.game_active = True
            self.sb.prep_score() #we call prep_score() after resetting game stats when starting a new game.
            self.sb.prep_level() #we call prep_level() after resetting game stats when starting a new game.
            self.sb.prep_ships() #to show player how many ships they have to start with

            self.aliens.empty() #get rid of any remaining aliens and bullets
            self.bullets.empty()

            self._create_fleet() #creates fleet and center the ship
            self.ship.center_ship()

            pygame.mouse.set_visible(False) #hides mouse cursor

    def _check_keydown_events(self, event):  # refactoring def _check_events
        if event.key == pygame.K_RIGHT:  # moves ship to the right
            # modify how game responds when player presses right arrow key. Insted of changing ship's position directly we merely set moving_right to true
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # if keydown occur for K_LEFT, we set moving_left to true
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # ends the game when player presses Q
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # we call _fire_bullet() when the spacebar is pressed

    def _check_keyup_events(self, event):  # refactoring def _check_events
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:  # if keyup occur for K_LEFT, we set moving_left to false
            self.ship.moving_left = False

    def _fire_bullet(self):  # create a new bullet and add it to bullets group
        # if len(self.bullets) is less than 3, we create new bullet. if 3 bullets already active,nothing happens when spacebar pressed
        if len(self.bullets) < self.settings.bullets_allowed:
            # we make an instance of Bullet and call it new_bullet
            new_bullet = Bullet(self)
            # we then add it to group bullets using add() method
            self.bullets.add(new_bullet)

    def _create_fleet(self):  # new helper method
        # instance of alien and adding it to group that will hold the fleet
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size #we need width and height if alien, we use attribute size which contains a tuple with width and height of a rect object
        # we get alien's width from its rect attribute and store this value in alien_width so we dont have to keep working through rect attribute
        # we calculate horizontal space available for aliens and number of aliens that can fit into that space
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)


        #determine number of ows of aliens that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        #create full fleet of aliens
        for row_number in range(number_rows): #we use 2 nested loops # outer loop counts from 0 to numbers of aliens we need to make
            for alien_number in range(number_aliens_x):  #inner loop creates aliens in one row
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number): #helper method which is being called from _create_fleet()
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            #alien_width = alien.rect.width
            # create a new alien and set its x coordinate value to place it in the row
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number #we change alien's y coordinate when it's not in first row by starting with one alien's height to create empty space at top of screen
            self.aliens.add(alien)
 
    #respond appropriately if ant aliens have reached an edge
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites(): #loop through fleet and call check_edges() on each alien
            if alien.check_edges(): #if check_edge() returns true we know an alien is at edge and whole fleet needs to change direction so we call _change_fleet_direction() and break out of loop
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites(): #loop through all the aliens and drop each one using setting fleet_drop_speed than we change the fleetb_direction by multiplying its current value by -1
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):  # helps in refactoring. We moved code that draws background and ship and flips screen to _update_screen() #redraw screen during each pass through the loop
        self.screen.fill(self.bg_color)

        # we draw ship on screen by calling ship.blitme(). blit() copies content of one surface to another.
        self.ship.blitme()
        for bullet in self.bullets.sprites():  # returns a list of all sprites in the group bullets
            # to draw all fired bullets to the screen, we loop through the sprites in bullets and call draw_bullet()
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # to make alien appear

        self.sb.show_score() #draw score info

        if not self.stats.game_active: #draw the play button if game is inactive
            self.play_button.draw_button()

        # make most recently drawn screen visible
        pygame.display.flip()  # tells pygame to make the most recently drawn screen visible. it simply draws an empty screen on each pass through the while loop, erasing old screen so only new screen is visible


if __name__ == "__main__":  # we palce run_game() in an if block that only run if the file is called directly
    # make game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
