# Python Libraries
import pygame
import pygame_gui

# System Libraries
import sys
import ctypes

# Custom-made libraries
from app_engine.settings import *


class HandleEvents():
    def __init__(self, manager, current_screen, hwnd, object_ids, title_bar, log_in_screen, chat_screen) -> None:
        # General setu
        self.display_surface = pygame.display.get_surface()

        self.manager = manager
        self.current_screen = current_screen
        self.hwnd = hwnd
        self.object_ids = object_ids
        self.title_bar = title_bar
        self.log_in_screen = log_in_screen
        self.chat_screen = chat_screen

        self.title_bar_is_dragging = False
        self.switch_focus = 1

    def handle_event(self, event: pygame.event.Event, app) -> None:
        self.app = app

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)
        self.handle_pygame_guis_event(event)

        self.manager.process_events(event)

    def handle_mouse_button_down(self, event) -> None:
        # Checks if the title bar buttons are being pressed
        for rect in self.title_bar.window_control_rects:
            if rect[0].collidepoint(event.pos):
                if rect[2] == "x":
                    pygame.quit()
                    sys.exit()
                if rect[2] == "-":
                    pygame.display.iconify()

        # Checks if we are title_bar_is_dragging the title bar's bar
        if event.button == 1:
            if self.title_bar.title_bar_rect.collidepoint(event.pos):
                self.title_bar_is_dragging = True
            if self.log_in_screen.submit_btn_rect.collidepoint(event.pos) and self.log_in_screen.submit_btn_can_press:
                self.log_in_screen.submit_btn_rect.y = self.log_in_screen.submit_btn_info[
                    0][1] + 5
                self.log_in_screen.submit_btn_pressed = True

        # Chekcs if the checkbox is clicked
        if self.log_in_screen.checkbox_rect.collidepoint(event.pos):
            self.log_in_screen.checkbox_clicked += 1
            if self.log_in_screen.unidentified_user:
                self.log_in_screen.unidentified_user = False

        # Handles scrolling
        if event.button == 5 and self.chat_screen.all_collided_messageboxes:
            if self.chat_screen.screen_offset >= 0:
                self.chat_screen.screen_offset -= self.chat_screen.scrolling_speed
            else:
                self.chat_screen.screen_offset = -self.chat_screen.scrolling_speed

        elif event.button == 4 and self.chat_screen.all_collided_messageboxes:
            num = 0
            for _ in range(len(self.chat_screen.all_collided_messageboxes)):
                num += 60
            num -= self.chat_screen.screen_offset/self.chat_screen.scrolling_speed

            if self.chat_screen.screen_offset <= num:
                self.chat_screen.screen_offset += self.chat_screen.scrolling_speed
            else:
                self.chat_screen.screen_offset = num + self.chat_screen.scrolling_speed

    def handle_mouse_button_up(self, event) -> None:
        if event.button == 1:
            self.title_bar_is_dragging = False

            if self.log_in_screen.submit_btn_pressed:
                self.log_in_screen.submit_btn_pressed = False
                self.log_in_screen.submit_btn_rect.y = self.log_in_screen.submit_btn_info[0][1]

                if self.log_in_screen.username and self.log_in_screen.password and self.current_screen == "log_in_screen":
                    self.log_in_screen.check_users()

                    if not self.log_in_screen.unidentified_user and self.log_in_screen.checkbox_clicked % 2:
                        self.log_in_screen.submit_btn_can_press = False
                        self.chat_screen.username = self.log_in_screen.username
                        self.app.change_screen("chat_screen")

                else:
                    self.log_in_screen.unidentified_user = True

    def handle_mouse_motion(self, event) -> None:
        self.title_bar.update(True)

        if self.title_bar_is_dragging:
            # Move the window with the mouse pos
            ctypes.windll.user32.ReleaseCapture()
            ctypes.windll.user32.SendMessageW(self.hwnd, 0xA1, 0x2, 0)

        self.log_in_screen.submit_btn_hovered = True if self.log_in_screen.submit_btn_rect.collidepoint(
            event.pos) else False

    def handle_key_down(self, event) -> None:
        if event.key == pygame.K_TAB and self.current_screen == "chat_screen":
            self.manager.set_focus_set(self.chat_screen.text_input)

        if event.key == pygame.K_TAB and self.current_screen == "log_in_screen":
            self.switch_focus = (self.switch_focus + 1) % 2
            self.manager.set_focus_set(
                self.log_in_screen.text_inputs[self.switch_focus])

    def handle_pygame_guis_event(self, event) -> None:
        for object_id in self.object_ids:
            if self.current_screen == "chat_screen":
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == f"#{object_id}_text_entry":
                    self.chat_screen.message_count += 1
                    self.chat_screen.make_new_message_box(event.text)
            if self.current_screen == "log_in_screen":
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == f"#{object_id}_text_entry":
                    self.handle_ui_text_entry_changed_log_in_screen(
                        object_id, event)

    def handle_ui_text_entry_changed_log_in_screen(self, object_id, event) -> None:
        if self.log_in_screen.unidentified_user:
            self.log_in_screen.unidentified_user = False

        if object_id == "username":
            self.log_in_screen.username = event.text

        elif object_id == "password":
            self.log_in_screen.password = event.text

            if len(self.log_in_screen.password) < 6:
                self.log_in_screen.incorrect_password = True
            else:
                self.log_in_screen.incorrect_password = False
