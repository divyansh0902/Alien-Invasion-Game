class GameStats:

    def __init__(self, ai_game):
        #initialize stats
        self.setting = ai_game.settings
        self.reset_stats() #we can call this method from __init__ so statistics are set properly when GameStat instance is first created

        self.game_active = False #start alien invasion in an inactive state

        #high score should never reset
        self.high_score = 0

        self.level = 1

    def reset_stats(self):
        #initialize stats that can change during game
        self.ship_left = self.setting.ship_limit
        self.score = 0