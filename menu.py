import pygame, sys

class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.offset = -100

    def blit_screen(self):
        self.game.screen.blit(self.game.menu_display, (0, 0))
        pygame.display.update()
        self.clock.tick(60)
    
    def blit_pause_screen(self):
        self.game.screen.blit(self.game.pause_display, (0, 0))
        pygame.display.update()
        self.clock.tick(60)

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.click = False
        self.run_display = True
        self.startx, self.starty = self.mid_w + 220, self.mid_h + 80
    
    def display_menu(self):
        self.run_display = True
        self.play_text = 'Play'
        self.option_text = 'Options'
        self.exit_text = 'Exit'
        while self.run_display:
            # Tracking mouse events
            mx, my = pygame.mouse.get_pos()

            play_rect = self.game.draw_text(self.play_text, 50, self.WHITE, self.game.menu_display, self.startx, self.starty)
            options_rect = self.game.draw_text(self.option_text, 30, self.WHITE, self.game.menu_display, self.startx, self.starty + 50)
            exit_rect = self.game.draw_text(self.exit_text, 30, self.WHITE, self.game.menu_display, self.startx, self.starty + 100)
            
            # Execute Actions
            if play_rect.collidepoint((mx, my)):
                if self.click:
                    self.click = False
                    break
            
            if options_rect.collidepoint((mx, my)):
                if self.click:
                    pass
            
            if exit_rect.collidepoint((mx, my)):
                if self.click:
                    # self.game.running= False
                    self.run_display = False
                    pygame.quit()
                    sys.exit()

            self.click = False            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.game.running = False
                    self.run_display = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            self.blit_screen()
        self.game.run()

class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.startx, self.starty = self.mid_w, self.mid_h + 70
        self.click = False
        self.run_pause_display = True
    
    def display_menu(self):
        self.resume_text = 'Resume'
        self.options_text = 'Options'
        self.exit_text = 'Exit to Main Menu'

        while self.run_pause_display:
            # Tracking mouse events
            mx, my = pygame.mouse.get_pos()

            resume_rect = self.game.draw_text(self.resume_text, 50, self.WHITE, self.game.pause_display, self.startx, self.starty - 50)
            options_rect = self.game.draw_text(self.options_text, 30, self.WHITE, self.game.pause_display, self.startx, self.starty + 50)
            exit_rect = self.game.draw_text(self.exit_text, 30, self.WHITE, self.game.pause_display, self.startx, self.starty + 100)
            
            # Execute Actions
            if resume_rect.collidepoint((mx, my)):
                if self.click:
                    self.run_pause_display = False
            
            if exit_rect.collidepoint((mx, my)):
                if self.click:
                    # self.game.running = False
                    self.run_pause_display = False
                    pygame.mixer.music.stop()
                    # pygame.mixer.Sound.stop()
                    self.game.setCurrMenu(MainMenu)

            self.click = False            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.game.running = False
                    self.run_pause_display = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run_pause_display = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            self.blit_pause_screen()

class OptionsMenu(Menu):
    pass
