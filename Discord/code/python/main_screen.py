# Python libraries
import pygame, pygame_gui, time

# Custom-made libraries
from settings import SIZE_C
from main_screen_interface import *

class MainScreen:
    def __init__(self, manager: pygame_gui.ui_manager.UIManager) -> None:
        # Pygame setup
        self.display_surface = pygame.display.get_surface()
        self.manager = manager

        # General setup
        self.screen_size = self.WIDTH, self.HEIGHT = (SIZE_C["width"], SIZE_C["height"])
        self.picture_path = "assets/graphics/icon.png"

        self.message_list = []
        self.object_ids = ["main"]

        self.texts = []
        self.create_text_input()

        self.username = ""

    def redraw_messagebox(self, update_message_time: int) -> None:
        """redraw all of the messagebox when switching to the main screen.


        Args:
            update_message_time (int): whenever the function is called this variable starts with zero
        """
        if self.message_list and not update_message_time:
            update_message_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - update_message_time <= 10:
                self.draw(True)
    
    def make_new_message_box(self, text: str) -> None:
        """
        Makes a new messagebox whenever a message is sent.

        Get the current time, and empty the messagebox for new text input.

        Args:
            event (class): An event class that is usually found on the for event loop
        """
        # Get current time
        current_time = time.time()
        local_time = time.localtime(current_time)
        formatted_current_time = time.strftime("%H:%M:%S", local_time)

        max_character = self.text_input.rect.size[0]//15
        if len(text) < max_character:
            pass
        else:
            text = text[:max_character]

        if len(text) > 0:
            self.texts.insert(0, (text, formatted_current_time))

            # Empty the text entry line
            self.text_input.kill()
            self.create_text_input()
            self.text_input.focus()
    
    def update_manager(self, manager: pygame_gui.ui_manager.UIManager) -> None:
        self.manager = manager
    
    def create_text_input(self) -> None:
        """
        Creates a new text input whenever a text is sent.
        """
        self.text_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, self.HEIGHT-60, self.WIDTH-20, 50),
            placeholder_text="Message...",
            manager=self.manager,
            object_id=f"#{self.object_ids[0]}_text_entry"
            )

    def arrange_and_create_messages(self) -> None:
        """
        Arrange messages while also creating message_boxes.
        
        
        Note:
            - This func arranges messages from old to recent.
        """
        if self.texts:
            for i, text in enumerate(self.texts):
                self.message_list.append(MessageBox(
                   pos=(75, self.HEIGHT-65*(i+2)),
                   size=(self.WIDTH-85, 60), 
                   picture_path=self.picture_path,
                   name=self.username, 
                   text=text[0],
                   time_sent_at=text[1]))

    def update(self, draw: bool) -> None:
        if draw:
            self.arrange_and_create_messages()

    def draw(self, draw: bool) -> None:
        if draw:
            for message_box in self.message_list:
                message_box.draw()
