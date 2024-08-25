# Add background image and music

import pygame, sys
from pygame.locals import *
import time
import random
from button import Button

pygame.init()

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

gameleveldata = [0.1, 0.05, 0.01]
backgroundlv = ["resources/Backgroundlv1.png", "resources/Backgroundlv2.png", "resources/Backgroundlv3.png"]
bgmlv = ["resources/bgmlv1.mp3", "resources/bgmlv2.mp3", "resources/bgmlv3.mp3"]

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/strippe.ttf", size)


class GameSpeed:
    def __init__(self, speed):
        self.speed = speed

gamelv = GameSpeed(1)

def lvconfigure():
    gamelv.speed += 1
    if gamelv.speed > 3:
        gamelv.speed = 1


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(f"resources/victim{gamelv.speed}.png")
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 31) * SIZE
        self.y = random.randint(1, 17) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(f"resources/snake texture{gamelv.speed}.png")
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GROUP 1 Snake Game Comp Prog Project")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1280, 720))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load(f'resources/bgmlv{gamelv.speed}.ogg')
        pygame.mixer.music.play(loops=-1)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound(f"resources/bite{gamelv.speed}.mp3")

        pygame.mixer.Sound.play(sound)
        # pygame.mixer.music.stop()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load(backgroundlv[gamelv.speed - 1])
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1240 and 0 <= self.snake.y[0] <= 680):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.Font('resources/strippe.ttf', 40)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (1020, 55))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.Font('resources/strippe.ttf', 35)
        line1 = font.render(f"Your End Has Come! Your score is {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (350, 300))
        line2 = font.render(f"To play again press Enter. To go back to main menu, press Esc!", True, (255, 255, 255))
        self.surface.blit(line2, (130, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.music.pause()
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(gameleveldata[gamelv.speed - 1])

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=None, pos=(630, 375),
                             text_input="PLAY", font=get_font(64), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(630, 500),
                                text_input=f"Level: {gamelv.speed}", font=get_font(64), base_color="#d7fcd4",
                                hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(630, 615),
                             text_input="QUIT", font=get_font(64), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    startgame = Game()
                    startgame.run()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lvconfigure()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == '__main__':
    main_menu()


