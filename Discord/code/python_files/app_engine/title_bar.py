# Python libraries
import pygame
from typing import Sequence

# Custom-made libraries
from app_engine.settings import *

class TitleBar:
    def __init__(self, size: Sequence[int], text: str, icon: pygame.surface.Surface) -> None:
        # Pygame setup
        self.display_surface = pygame.display.get_surface()
        self.size = size
        self.normal_font = pygame.font.SysFont("bahnschrift", 25)
        self.small_font = pygame.font.SysFont("Segoe UI", 20)

        # window controls setup
        self.win_ctrl_icons = ["x", "-"]
        self.window_controls()

        # Title bar text setup
        self.text = self.small_font.render(text, True, WHITE)

        # Title bar icon setup
        self.icon = icon

        # Hovering state variables
        self.hovering = False
        self.hover_start_time = 0.0
        self.fade_out_start_time = 0.0
    
    def window_controls(self) -> None:
        """Initialize the window's controls.
        """
        title_bar_size = (self.size["width"] - len(self.win_ctrl_icons) * 40, 40)

        self.window_control_rects = [
            [pygame.Rect((self.size["width"] - (1+i) * title_bar_size[1]), 0, 40, title_bar_size[1]), False, icon]
            for i, icon in enumerate(self.win_ctrl_icons)]
        
        self.window_control_buttons = [
            self.normal_font.render(button, True, WHITE)
            for button in self.win_ctrl_icons]
        
        self.title_bar_rect = pygame.Rect((0, 0), title_bar_size)
    
    def handling_hovering(self, rect: pygame.rect.Rect, current_time: float, DEFAULT_COLOR: tuple[int, int, int], HOVER_COLOR: tuple[int, int, int]) -> None:
        """Handles title bar's buttons hovering animation.

        Args:
            rect (pygame.rect.Rect): The rect of the button.
            current_time (float): The run time of the app diveded by 1000 in seconds.
            DEFAULT_COLOR (tuple[int, int, int]): The Default color of the button
            HOVER_COLOR (tuple[int, int, int]): The Hovered color of the button
        """

        if self.hovering:
            elapsed_time = current_time - self.hover_start_time
            hover_progress = min(elapsed_time / TRANSITION_DURATION, 1.0)

            # Interpolate colors
            r = int((1 - hover_progress) * DEFAULT_COLOR[0] + hover_progress * HOVER_COLOR[0])
            g = int((1 - hover_progress) * DEFAULT_COLOR[1] + hover_progress * HOVER_COLOR[1])
            b = int((1 - hover_progress) * DEFAULT_COLOR[2] + hover_progress * HOVER_COLOR[2])

            pygame.draw.rect(self.display_surface, (r, g, b), rect)
            
        else:
            if self.fade_out_start_time > 0:
                elapsed_time = current_time - self.fade_out_start_time
                fade_out_progress = min(elapsed_time / TRANSITION_DURATION, 1.0)  # Clamp progress to 1.0 at maximum

                # Interpolate colors
                r = int((1 - fade_out_progress) * HOVER_COLOR[0] + fade_out_progress * DEFAULT_COLOR[0])
                g = int((1 - fade_out_progress) * HOVER_COLOR[1] + fade_out_progress * DEFAULT_COLOR[1])
                b = int((1 - fade_out_progress) * HOVER_COLOR[2] + fade_out_progress * DEFAULT_COLOR[2])

                pygame.draw.rect(self.display_surface, (r, g, b), rect)
            else:
                pygame.draw.rect(self.display_surface, DEFAULT_COLOR, rect)

    def update_hovering_state(self, mouse_pos: tuple[int, int]) -> None: 
        """Updates the hovering state based on the mouse position.

        Args:
            mouse_pos (tuple[int, int]): Mouse position.
        """
        is_hovering = False
        for rect in self.window_control_rects:
            if rect[0].collidepoint(mouse_pos):
                rect[1] = True
                is_hovering = True
            else:
                rect[1] = False

        if is_hovering != self.hovering:
            self.hovering = is_hovering
            if self.hovering:
                self.hover_start_time = pygame.time.get_ticks() / 1000.0
            else:
                self.fade_out_start_time = pygame.time.get_ticks() / 1000.0

    def draw(self) -> None:
        """Draws the title bar's components (Bar, Text, Icon, Buttons)
        """
        # Title bar
        pygame.draw.rect(self.display_surface, DARKER_GRAY, self.title_bar_rect)

        # Title bar's buttons
        for i, rect in enumerate(self.window_control_rects):
            if rect[2] == "x":
                DEFAULT_COLOR = (169, 15, 15)
                HOVER_COLOR = (206, 32, 32)
            else:
                DEFAULT_COLOR = (35, 37, 41)
                HOVER_COLOR = (54, 57, 63)

            pygame.draw.rect(self.display_surface, DARKER_GRAY, rect[0])
            if rect[1]:
                self.handling_hovering(rect[0], pygame.time.get_ticks()/1000, DEFAULT_COLOR, HOVER_COLOR)
            self.display_surface.blit(self.window_control_buttons[i], (self.size["width"] - (40 * (i+1) - self.window_control_buttons[i].get_width() - 1), 21 - self.window_control_buttons[i].get_height()/2))

        # Title bar text
        self.display_surface.blit(self.text, (self.title_bar_rect.x + 10 + self.icon.get_width(), - 2 + self.title_bar_rect.y + self.title_bar_rect.h//2 - self.text.get_height()//2))

        # Title bar icon
        title_bar_icon_offset = 5
        self.display_surface.blit(self.icon, (self.title_bar_rect.x + title_bar_icon_offset, self.title_bar_rect.y + title_bar_icon_offset))

    def update(self, hovering: bool) -> None:
        if hovering:
            self.update_hovering_state(pygame.mouse.get_pos())
