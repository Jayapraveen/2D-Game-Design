"""
2D Game Design Project 1
Title : Earth Crusaders
Author: Jayapraveen Arcot Ravikumar
Version: 1.0
Date: 09/23/2021

#controls
UP, Down, Left, Right = Movement
space = fire repulsor beams

#Running the game
use python to run the main.py file
"""

import arcade
import pathlib
from enum import auto, Enum

# Game Window
window_width, window_height = 1280, 720
window_x, window_y = 100, 200
background_image = pathlib.Path.cwd() / "assets" / "images" / "background.png"
game_title = "Earth crusaders"

# Load sounds. Sounds from kenney.nl
repulsor_beam_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
repulsor_beam_image = ":resources:images/space_shooter/laserBlue01.png"

# Sprite Information
spaceship_image = pathlib.Path.cwd() / "assets" / "images" / "spaceship.png"
sprite_scaling_laser = 0.8
bullet_speed = 10


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SPACE = auto()


class Spaceshipsprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed: int, game_window):
        super().__init__(ship_path, 0.10)
        self.speed = speed
        self.game = game_window

    def move(self, direction: MoveEnum):
        if (
            direction == MoveEnum.UP
            and self.center_y + self.height / 2 < self.game.height
        ):
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN and self.center_y - self.height / 2 > 0:
            self.center_y -= self.speed
        elif direction == MoveEnum.LEFT and self.center_x - self.width / 2 > 0:
            self.center_x -= self.speed
        elif (
            direction == MoveEnum.RIGHT
            and self.center_x + self.height / 2 < self.game.width
        ):
            self.center_x += self.speed
        else:  # should be MoveEnum.NONE
            pass


class Game(arcade.Window):
    def __init__(self, title: str):
        super().__init__(window_width, window_height, title)
        self.set_location(window_x, window_y)
        self.background = arcade.load_texture(background_image)
        self.bg_scroll_count = window_width
        self.bg1_scroll_count = 0
        self.pict = None
        self.direction = MoveEnum.NONE
        # hold sprite lists
        self.main_sprite_list = None
        self.bullet_list = arcade.SpriteList()

    def update_background(self, delta_time: float):
        if self.bg_scroll_count <= 0:
            self.bg_scroll_count = window_width
        if self.bg1_scroll_count <= -window_width:
            self.bg1_scroll_count = 0

        self.bg1_scroll_count = self.bg1_scroll_count - window_width / 10
        self.bg_scroll_count = self.bg_scroll_count - window_width / 10

    def spaceship_setup(self):
        self.pict = Spaceshipsprite(str(spaceship_image), speed=3, game_window=self)
        self.pict.center_x = 500
        self.pict.center_y = 500
        self.main_sprite_list = arcade.SpriteList()
        self.main_sprite_list.append(self.pict)

    def on_update(self, delta_time: float):
        self.pict.move(self.direction)

        # Call update on bullet sprites
        self.bullet_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:
            # If the bullet flies off-screen, remove it.
            if bullet.bottom > window_width:
                bullet.remove_from_sprite_lists()

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            self.bg_scroll_count, 0, window_width, window_height, self.background
        )
        arcade.draw_lrwh_rectangle_textured(
            self.bg1_scroll_count, 0, window_width, window_height, self.background
        )
        self.main_sprite_list.draw()
        self.bullet_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.direction = MoveEnum.LEFT
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.direction = MoveEnum.RIGHT
        elif key == arcade.key.SPACE:
            self.fire_bullet()

    def fire_bullet(self):
        arcade.play_sound(repulsor_beam_sound)
        # Create a bullet
        bullet = arcade.Sprite(repulsor_beam_image, sprite_scaling_laser)

        # Give the bullet a speed
        bullet.change_x = bullet_speed

        # Position the bullet
        bullet.center_x = self.pict.center_x + self.pict.width / 2
        bullet.bottom = self.pict.center_y

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (
            key == arcade.key.UP or key == arcade.key.W
        ) and self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (
            key == arcade.key.DOWN or key == arcade.key.S
        ) and self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE


def main():
    window = Game(game_title)
    window.spaceship_setup()
    arcade.schedule(window.update_background, 0.10)
    arcade.run()


if __name__ == "__main__":
    main()
