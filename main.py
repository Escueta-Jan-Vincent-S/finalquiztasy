import os
import pygame
import sys
import cv2
import numpy as np

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Final Quiztasy")

class MenuBackground:
    def __init__(self, file_path, speed=0.5):
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            sys.exit()
        self.speed = speed
        self.frame_counter = 0

    def get_frame(self):
        self.frame_counter += self.speed
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_counter)

        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.frame_counter = 0
            ret, frame = self.cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        return pygame.surfarray.make_surface(frame)

    def close(self):
        self.cap.release()

background_video = MenuBackground(os.path.join('images', 'background', 'backgroundMenu.mp4'), speed=0.3)

class Button():
    def __init__(self, x, y, idle_img, hover_img, action=None, scale=1.0):
        self.idle_img = pygame.image.load(idle_img).convert_alpha()
        self.hover_img = pygame.image.load(hover_img).convert_alpha()

        self.idle_img = pygame.transform.scale(self.idle_img, (
        int(self.idle_img.get_width() * scale), int(self.idle_img.get_height() * scale)))
        self.hover_img = pygame.transform.scale(self.hover_img, (
        int(self.hover_img.get_width() * scale), int(self.hover_img.get_height() * scale)))

        self.image = self.idle_img
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def update(self):
        if self.visible:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.image = self.hover_img
            else:
                self.image = self.idle_img

    def check_click(self):
        if self.visible:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                if self.action:
                    self.action()


class FinalQuiztasy:
    def __init__(self):
        self.screen = screen
        self.click_sound = pygame.mixer.Sound(os.path.join('audio', 'click_sound_button.mp3'))  # Load the click sound

        self.main_buttons = [
            Button(610, 450, os.path.join('images', 'button', 'play_btn.png'),
                   os.path.join('images', 'button', 'play_btn_hover.png'), self.show_game_modes, scale=0.35),
            Button(610, 510, os.path.join('images', 'button', 'option_btn.png'),
                   os.path.join('images', 'button', 'option_btn_hover.png'), self.open_options, scale=0.35),
            Button(610, 570, os.path.join('images', 'button', 'credits_btn.png'),
                   os.path.join('images', 'button', 'credits_btn_hover.png'), self.show_credits, scale=0.35),
            Button(610, 630, os.path.join('images', 'button', 'quit_btn.png'),
                   os.path.join('images', 'button', 'quit_btn_hover.png'), self.exit_game, scale=0.35)
        ]

        self.game_mode_buttons = [
            Button(640, 180, os.path.join('images', 'button', 'sp_btn.png'),
                   os.path.join('images', 'button', 'sp_btn_hover.png'), self.single_player, scale=0.70),
            Button(320, 540, os.path.join('images', 'button', 'pvp_btn.png'),
                   os.path.join('images', 'button', 'pvp_btn_hover.png'), self.pvp_mode, scale=0.70),
            Button(960, 540, os.path.join('images', 'button', 'custom_btn.png'),
                   os.path.join('images', 'button', 'custom_btn_hover.png'), self.custom_mode, scale=0.70)
        ]

        """
        self.back_button = [
            Button(300, 300, os.path.join('images', 'button', 'back_btn.png'), os.path.join('images', 'button', 'back_btn_hover.png'), self.back_button, scale=0.50),
        ]
        """

    def show_menu(self):
        pygame.mixer.music.load(os.path.join('audio', 'menuOst.mp3'))
        pygame.mixer.music.play(-1)
        self.set_main_buttons_visibility(True)
        self.set_game_mode_buttons_visibility(False)

    def set_main_buttons_visibility(self, visible):
        for button in self.main_buttons:
            button.visible = visible

    def set_game_mode_buttons_visibility(self, visible):
        for button in self.game_mode_buttons:
            button.visible = visible

    def show_game_modes(self):
        self.set_main_buttons_visibility(False)
        self.set_game_mode_buttons_visibility(True)
        self.click_sound.play()

    def play_game(self):
        print("Play Button Clicked")

    def open_options(self):
        print("Options Button Clicked")
        self.click_sound.play()

    def show_credits(self):
        print("Credits Button Clicked")
        self.click_sound.play()

    def exit_game(self):
        print("Exit Button Clicked")
        self.click_sound.play()
        pygame.quit()
        exit()

    def single_player(self):
        print("Single Player Mode Selected")
        self.click_sound.play()

    def pvp_mode(self):
        print("PvP Mode Selected")
        self.click_sound.play()

    def custom_mode(self):
        print("Custom Mode Selected")
        self.click_sound.play()

    def update(self):
        for button in self.main_buttons + self.game_mode_buttons:
            button.update()
            button.draw(self.screen)

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.main_buttons + self.game_mode_buttons:
                button.check_click()

    def main(self):
        self.show_menu()
        run = True
        while run:
            frame_surface = background_video.get_frame()
            frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(frame_surface, (0, 0))
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                self.check_events(event)
            pygame.display.update()
            clock.tick(60)
        background_video.close()
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    game = FinalQuiztasy()
    game.main()