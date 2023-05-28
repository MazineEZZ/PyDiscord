# Python libraries
import pygame
import pygame_gui
import json
from typing import Sequence, List

# Custom-made libraries
from app_engine.settings import *


class LogInScreen:
    def __init__(self, manager: pygame_gui.ui_manager.UIManager, background_path: str):
        # Pygame setup
        self.display_surface = pygame.display.get_surface()

        self.fonts = {font_name: pygame.font.SysFont(
            FONT_NAME, size) for font_name, size in FONT_SIZES.items()}

        # General setup
        self.screen_size = self.WIDTH, self.HEIGHT = (
            SIZE_L["width"], SIZE_L["height"])
        self.dimensions = (400, self.HEIGHT-240)
        self.main_box_position = (self.WIDTH//2-self.dimensions[0]//2, 110)
        self.manager = manager

        self.animated_bg = pygame.image.load(background_path).convert_alpha()
        self.animated_bg = pygame.transform.smoothscale(
            self.animated_bg, pygame.math.Vector2(self.animated_bg.get_size())*0.35)
        self.animated_bg_rect = self.animated_bg.get_rect(
            center=(self.WIDTH/2, self.HEIGHT/2 + 70))

        # Create text input
        self.text_inputs = []
        self.object_ids = ["username", "password"]

        self.texts = [["Welcome Back!", "B", (self.WIDTH//2, self.main_box_position[1] + 20)],
                      [self.object_ids[0].upper(), "S", (self.main_box_position[0] +
                                                         50, self.main_box_position[1] + 165/2)],
                      [self.object_ids[1].upper(), "S", (self.main_box_position[0] + 50, self.main_box_position[1] + 182)],]
        self.text_list = [(self.fonts["big"].render(text[0], True, WHITE), text[2]) if text[1] == "B" else
                          (self.fonts["normal"].render(text[0], True, WHITE), text[2]) if text[1] == "N" else
                          (self.fonts["small"].render(text[0], True,
                           GRAY), text[2]) if text[1] == "S" else 0
                          for text in self.texts]

        # Submit button
        submit_btn_offset = 10
        self.submit_btn_info: List[tuple[int]] = [(self.main_box_position[0] + submit_btn_offset,
                                                   self.main_box_position[1] + self.dimensions[1] - 70), (self.dimensions[0] - submit_btn_offset*2, 50)]
        self.submit_btn_rect = pygame.Rect(
            self.submit_btn_info[0], self.submit_btn_info[1])
        self.submit_btn_txt_surf = self.fonts["intermediate"].render(
            "Log in", True, WHITE)
        self.submit_btn_hovered = False
        self.submit_btn_pressed = False
        self.submit_btn_can_press = True

        # Checkbox
        self.checkbox_rect = pygame.Rect(0, 0, 0, 0)
        self.checkbox_clicked: int = 0

        # * Backend setup
        self.username = ""
        self.password = ""
        self.unidentified_user = False
        self.incorrect_password = False

        # * json file setup
        try:
            with open("code/json_files/users.json") as users_file:
                self.users = json.load(users_file)["users"]
        except:
            with open("code/json_files/users.json", "w") as users_file:
                pass

    def check_users(self) -> None:
        requirements = [False, False]

        for user in self.users:
            if user[0].lower() == self.username.lower():
                # Normalize username format if different
                self.username = user[0]
                requirements[0] = True
            if user[1] == self.password:
                requirements[1] = True

        if all(requirements):
            self.unidentified_user = False
        else:
            self.unidentified_user = True

    def create_all_text_inputs(self) -> None:
        self.text_inputs = [self.create_text_input(
                            pos=(
                                self.main_box_position[0] + 10, ((i * 100) + self.main_box_position[1]) + 100),
                            size=(self.WIDTH -
                                  self.main_box_position[0]*2 - 20, 50),
                            message=f"Type your {object_id}",
                            object_id=f"#{object_id}_text_entry")

                            for i, object_id in enumerate(self.object_ids)]

    def animate_the_background(self) -> None:
        """Smoothly animates the background."""
        # Get mouse main_box_position
        animated_bg_pos = (pygame.mouse.get_pos()[0]/self.WIDTH,
                           pygame.mouse.get_pos()[1]/self.HEIGHT)

        self.display_surface.blit(self.animated_bg, (self.animated_bg_rect.x +
                                  animated_bg_pos[0]*10, self.animated_bg_rect.y + animated_bg_pos[1]*10))

    def create_text_input(self, pos: Sequence[int], size: Sequence[int], message: str, object_id: str) -> pygame_gui.elements.ui_text_entry_line.UITextEntryLine:
        """
        Creates a new text input whenever a text is sent.

        Args:
            pos (tuple/list): A List or a tuple containing the x and y main_box_positions (x, y).
            size (tuple/list): A List or a tuple containing the width and the height (width, height).
            message (str): A string message.
            object_id (str): The id of the specified object.
        """
        return pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(pos, size),
            placeholder_text=message,
            manager=self.manager,
            object_id=object_id
        )

    def create_submit_button(self) -> None:
        """Creates the submit button of the log-in's screen.

        """
        # Button
        submit_btn_rect = (self.submit_btn_rect.x,
                           self.submit_btn_info[0][1]+5)
        pygame.draw.rect(self.display_surface, DARKER_BLUISH, [
                         submit_btn_rect, self.submit_btn_rect.size], 0, 5)

        if self.submit_btn_hovered:
            pygame.draw.rect(self.display_surface, DARK_BLUE,
                             self.submit_btn_rect, 0, 5)
        else:
            pygame.draw.rect(self.display_surface, BLUISH,
                             self.submit_btn_rect, 0, 5)

        # Text
        text_offset = 5
        self.display_surface.blit(self.submit_btn_txt_surf, (self.submit_btn_rect.x + self.submit_btn_rect.w//2 - self.submit_btn_txt_surf.get_width(
        )/2, self.submit_btn_rect.y + self.submit_btn_rect.h//2 - self.submit_btn_txt_surf.get_height()/2 + text_offset))

    def draws_the_output_text(self) -> None:
        """Draws the wrong input text.

        """
        requirements = [self.unidentified_user,
                        self.incorrect_password, (not self.checkbox_clicked % 2)]
        offset = 20

        if any(requirements):
            color = RED

            if not self.checkbox_clicked % 2:
                text_color_info = (
                    "Before proceeding, please ensure your human\nauthenticity by selecting the designated checkbox above.",
                    color
                )
                offset = 40
            elif self.unidentified_user and self.incorrect_password:
                text_color_info = (
                    "Incorrect username or password. Your password must\nbe at least 6 characters.",
                    color
                )
                offset = 40
            elif self.unidentified_user:
                text_color_info = ("Incorrect username or password.", color)
            elif self.incorrect_password:
                text_color_info = (
                    "Your password must be at least 6 characters.",
                    color
                )

        else:
            text_color_info = ("Everything is looking good.", GREEN)

        output_text = self.fonts["small"].render(
            text_color_info[0], True, text_color_info[1])

        self.display_surface.blit(
            output_text, (self.main_box_position[0] + 15, self.main_box_position[1] + self.dimensions[1]/1.2 - offset))

    def create_check_box(self) -> None:
        checkbox_text = self.fonts["medium"].render(
            "Please confirm your human identity.", True, WHITISH)

        self.checkbox_rect = pygame.Rect(
            (self.main_box_position[0] + 15,
             self.main_box_position[1] + self.dimensions[1]/1.45 - 30),
            (20, 20))

        self.display_surface.blit(
            checkbox_text, (self.checkbox_rect.x + 30, self.checkbox_rect.y))

        if self.checkbox_clicked % 2:
            pygame.draw.rect(self.display_surface, DARK_BLUE,
                             self.checkbox_rect, 0, 2)
        pygame.draw.rect(self.display_surface, WHITE, self.checkbox_rect, 2, 2)

    def update_manager(self, manager: pygame_gui.ui_manager.UIManager) -> None:
        self.manager = manager

    def draw_password_hider(self, hide: bool = False) -> None:
        # Text
        asterics_text = '*' * len(self.password)
        if len(asterics_text) >= 33:
            asterics_text = asterics_text[:34]
        asterics_text_rendered = self.fonts["intermediate"].render(
            asterics_text, True, WHITISH)

        # Rect
        rect_offset = 5
        rect = pygame.Rect(self.text_inputs[1].rect.x+rect_offset/2,
                           self.text_inputs[1].rect.y+rect_offset/2,
                           self.text_inputs[1].rect.w - rect_offset,
                           self.text_inputs[1].rect.h-rect_offset)

        # Draw
        if self.password and not hide:
            pygame.draw.rect(self.display_surface, DARKER_GRAY, rect=rect)
            self.display_surface.blit(
                asterics_text_rendered, (rect.x + 2, rect.y + asterics_text_rendered.get_height()//2))

    def draw(self) -> None:
        # * Background
        pygame.draw.rect(self.display_surface, DARKER_GRAY_BG, [
                         self.main_box_position, self.dimensions], 0, 7)

        # * Text
        for text in self.text_list:
            self.display_surface.blit(
                text[0], (text[1][0] - text[0].get_width()//2, text[1][1]))

        # * Submit Button
        self.create_submit_button()

        # * Wrong input text
        self.draws_the_output_text()

        # * checkbox
        self.create_check_box()

    def update(self) -> None:
        self.animate_the_background()
