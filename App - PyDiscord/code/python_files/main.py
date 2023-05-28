# Python libraries
import pygame, pygame_gui
from typing import Sequence
from pygame.locals import *

# System libraries
import sys, os, ctypes, subprocess

# Custom-made libraries
from pygame_gui.elements import UITextEntryLine

from app_engine.settings import *
from app_engine.handle_events import HandleEvents
from app_engine.title_bar import TitleBar

from log_in_screen_folder.log_in_screen import LogIn
from main_screen_folder.main_screen import MainScreen


class App():
    def __init__(self) -> None:
        pygame.init()

        # Screen properties
        pygame.display.set_caption("Discord")
        self.icon = pygame.image.load("assets/graphics/icon.png")
        pygame.display.set_icon(self.icon)
        self.screen_flag = pygame.NOFRAME
        self.screen_size = SIZE_L

        self.vsync = 1 if VSYNC_ENABLED else 0

        self.screens = ["log_in_screen", "main_screen"]
        self.count = 0
        self.current_screen = self.screens[0]

        self.update_message_time = 0

        self.hovering = False
        self.hover_start_time = 0.0
        self.fade_out_start_time = 0.0

        self.change_screen_info()

    def change_window_position(self, window_size: Sequence[int]) -> None:
        """
        Centers the game window on the display screen.

        This method automatically detects the operating system (Linux or Windows) and adjusts the window position accordingly.
        
        Args:
            window_size (dict): A dictionary containing the width and height of the game window.

        Note:
            - On Windows, the window position is centered based on the screen resolution.
            - On Linux, this method requires the necessary dependencies to be installed for the 'xdotool' command to work.

        """
        
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        window_x = (screen_width - window_size["width"]) // 2
        window_y = (screen_height - window_size["height"]) // 2

        self.hwnd = pygame.display.get_wm_info()['window']

        if os.name == 'nt':  # ! Windows
            ctypes.windll.user32.SetWindowPos(
                self.hwnd, 0, window_x, window_y - 25, 0, 0, SWP_NOSIZE | SWP_SHOWWINDOW)

        elif os.name == 'posix': # ! Linux
            subprocess.run(['xdotool', 'windowmove',
                str(self.hwnd), str(window_x), str(window_y)])

    def change_window_info(self, window_size: Sequence[int]) -> None:
        """
        Changes the window size
        
        it utilizes the 'change_window_postion' to center the new window
        
        Args:
            window_size (dict): A dictionary containing the width and height of the game window.
            
        """
        self.screen = pygame.display.set_mode((window_size["width"], window_size["height"]), flags=self.screen_flag, vsync=self.vsync)
        self.change_window_position(window_size)

    def change_screen(self, screen_name: str) -> None:
        self.count += 1
        self.current_screen = screen_name
        self.change_screen_info()
    
    def change_screen_info(self) -> None:
        """Change the screen information to adapt with the new settings.

        """
        pygame.display.set_caption("Discord")
        
        # * General screen setup
        # Screen setup
        self.screen_size = SIZE_L if self.current_screen == "log_in_screen" else SIZE_C
        self.change_window_info(self.screen_size)
        self.clock = pygame.time.Clock()

        # Screen's title bar setup
        title_bar_icon_path = "assets/graphics/title_bar_icon.png"
        title_bar_text = "Log in to Discord" if  self.current_screen == "log_in_screen" else "Discord"
        self.title_bar = TitleBar(
            self.screen_size,
            text=title_bar_text,
            icon=pygame.image.load(title_bar_icon_path).convert_alpha())

        # Manager setup (pygame_gui)
        manager_theme_path = "code/json_files/theme.json"
        self.manager = pygame_gui.UIManager((self.screen_size["width"], self.screen_size["height"]))
        self.manager.get_theme().load_theme(manager_theme_path)

        # * Screens setup
        if self.count == 0:
            background = "assets/graphics/background.png"
            self.log_in_screen = LogIn(self.manager, background)
            self.main_screen = MainScreen(self.manager)
        else:
            self.log_in_screen.update_manager(self.manager)
            self.main_screen.update_manager(self.manager)

        self.screen.fill(DARKER_GRAY_BG)
        
        if self.current_screen == "main_screen":
            self.object_ids = [object_id for object_id in self.main_screen.object_ids]

            # Delete the log-in screen text inputs
            for i in range(len(self.log_in_screen.text_inputs)):
                self.log_in_screen.text_inputs[i].kill()
            self.log_in_screen.text_inputs.clear()

            self.main_screen.create_text_input()

        elif self.current_screen == "log_in_screen":
            self.object_ids = [object_id for object_id in self.log_in_screen.object_ids]

            self.main_screen.text_input.kill()
            self.log_in_screen.create_all_text_inputs() 

        # Initialize the event handler module
        self.handle_events = HandleEvents(self.manager, self.current_screen, self.hwnd, self.object_ids, self.title_bar, self.log_in_screen, self.main_screen)

    def update_gui(self, dt: float):
        self.manager.update(dt)
        self.manager.draw_ui(self.screen)

    def main(self, app) -> None:
        while True:
            dt = self.clock.tick(FPS)/1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Event handler module
                self.handle_events.handle_event(event, app)
            # * App logic
            if self.current_screen == "main_screen":
                self.screen.fill(DARKER_GRAY_BG)

                # Updating section
                self.main_screen.update()

                # Drawing section
                self.main_screen.draw()

                self.update_gui(dt)

            elif self.current_screen == "log_in_screen":
                # Updating section
                self.log_in_screen.update()

                # Drawing section
                self.log_in_screen.draw()

                self.update_gui(dt)

            # External section
            self.title_bar.draw()

            pygame.display.update()

if __name__ == '__main__':
    app = App()
    app.main(app)
