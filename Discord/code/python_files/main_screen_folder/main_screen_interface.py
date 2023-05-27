# Python libraries
import pygame
from PIL import Image
from typing import Sequence

# Custom-made libraries
from app_engine.settings import *

class MessageBox:
    def __init__(self, pos: Sequence[int], size: Sequence[int], picture_path: str, name: str, text: str, time_sent_at: str) -> None:
        # Pygame Setup
        self.display_surface = pygame.display.get_surface()

        font_name = "bahnschrift"
        self.big_font = pygame.font.SysFont(font_name, 25)
        self.medium_font = pygame.font.SysFont(font_name, 20)
        self.small_font = pygame.font.SysFont(font_name, 15)

        # General setup
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        
        self.name = self.big_font.render(name, True, WHITE)
        self.text = self.medium_font.render(text, True, WHITISH)
        self.time_text = self.small_font.render(f"sent at {time_sent_at}", True, LIGHT_GRAY)

        # Profile picture setup
        pfp_size = (60, 60)
        picture_path = self.resize_picture(pfp_size, picture_path)
        self.make_pfp_round(pfp_size, picture_path)

    def resize_picture(self, size: Sequence[int], picture_path: str) -> pygame.surface.Surface:
        """Resize the given picture.
        
        using the PIL library.


        Args:
            picture_path (str): the path of the picture.
            size (Sequence[int]) : the new size of the picture.

        Returns:
            pygame.surface.Surface: image surface.
        """
        original_image = Image.open(picture_path)
        resized_image = original_image.resize(size)
        resized_image = resized_image.convert("RGBA")
        return pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode)

    def make_pfp_round(self, size: Sequence[int], pfp) -> None:
        """Transform any image into a circular image.
        
        Note:
            - The transformed image's width and height is always 60.
        """
    
        # Create circular surface with the same size as the image
        mask = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(
            surface=mask, 
            color=(255, 255, 255),
            center=(int(size[0]/2), int(size[1]/2)),
            radius=int(size[0]/2))
    
        # Resize the profile picture using smoothscale for anti-aliasing
        pfp_smooth = pygame.transform.smoothscale(pfp, (size[0], size[1]))
    
        # Blit the smoothed profile picture onto the circular surface
        self.masked_img = pygame.Surface(size, pygame.SRCALPHA)
        self.masked_img.blit(pfp_smooth, (0, 0))
        self.masked_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def draw(self) -> None:
        # Create a nice outline at the bottom of each messagebox
        pygame.draw.rect(self.display_surface, DARKER_GRAY, [
                        self.rect.x, self.rect.y, self.rect.w, self.rect.h+2], 0, 5)
        pygame.draw.rect(self.display_surface, DARK_GRAY, [
                        self.rect.x, self.rect.y, self.rect.w, self.rect.h-2], 0, 5)

        # * Bliting onto the screen
        self.display_surface.blit(self.masked_img, (self.rect.x - 65, self.rect.y))

        # Blit the name
        self.display_surface.blit(self.name, (self.rect.x + 5, self.rect.y + 7.5))

        # Blit the text
        self.display_surface.blit(self.text, (self.rect.x+5, self.rect.y+30))

        # Blit the time that the message was sent at
        self.display_surface.blit(
            self.time_text,
            (self.rect.w - self.time_text.get_width()/2 + 15, self.rect.y + self.time_text.get_height()/2 + 12))
