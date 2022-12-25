import pygame
import random


# Game state

class Timer:
    def __init__(self):
        self.count = 0
        self.update = True
        self.TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMEREVENT, 1400)

    def increment(self):
        self.count += 1


class GameState:
    def __init__(self):
        self.timer = Timer()
        self.size = self.width, self.height = 640, 580
        self.truth_center = (self.width / 2, self.height / 2)

    def update(self):
        if self.timer.update:
            self.timer.increment()


# Layers

class TimerLayer:
    def __init__(self, timer):
        self.font = pygame.font.SysFont("muktamahee", 20)
        self.timer = timer

    def render(self, surface):
        timer_surface = self.font.render(str(self.timer.count), True, "white", (0, 0, 0))
        timer_rect = timer_surface.get_rect()
        timer_rect.center = (surface.get_width() / 2, surface.get_height() - 20)
        surface.blit(timer_surface, timer_rect)


class TitleLayer:
    def __init__(self):
        self.font = pygame.font.SysFont("muktamahee", 30)
        self.surface = self.font.render("Grasp the Truth", True, "white", (0, 0, 0))
        self.rect = self.surface.get_rect()

    def render(self, surface):
        self.rect.center = (surface.get_width() / 2, 30)
        surface.blit(self.surface, self.rect)


class PeopleLayer:
    def __init__(self):
        pass

    def render(self, surface):
        pass


class TruthLayer:
    def __init__(self, game_state):
        self.game_state = game_state
        self.truth_center = game_state.truth_center
        self.font = pygame.font.SysFont("muktamahee", 40)
        self.surface = self.font.render("the Truth", True, "white", (0, 0, 0))
        self.rect = self.surface.get_rect()

    def render(self, surface):
        self.rect.center = self.game_state.truth_center
        surface.blit(self.surface, self.rect)


# Main game

class UI:
    def __init__(self):
        pygame.init()
        self.running = True
        self.game_state = GameState()
        self.size = self.width, self.height = self.game_state.size
        self.window = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption("The Truth")

        self.clock = pygame.time.Clock()

        self.timer = self.game_state.timer
        self.TIMEREVENT = self.timer.TIMEREVENT
        self.layers = [TimerLayer(self.timer), TitleLayer(), PeopleLayer(), TruthLayer(self.game_state)]

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.TIMEREVENT:
                self.timer.update = True

        mouse_pos = pygame.mouse.get_pos()
        truth_x, truth_y = self.game_state.truth_center
        truth_buff_x, t_buff_y = 100, 50
        x, y = [truth_x - truth_buff_x, truth_x + truth_buff_x], [truth_y - t_buff_y, truth_y + t_buff_y]
        if x[0] < mouse_pos[0] < x[1] and y[0] < mouse_pos[1] < y[1]:
            self.game_state.truth_center = (random.randrange(100, 550), random.randrange(80, 500))

    def update(self):
        self.game_state.update()

    def render(self):
        if self.timer.update:
            self.timer.update = False

        self.window.fill((0, 0, 0))
        for layer in self.layers[0:3]:
            layer.render(self.window)

        self.layers[3].render(self.window)

        pygame.display.update()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = UI()
    game.run()
