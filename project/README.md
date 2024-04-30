# Asteroid

A simple space shooter game written in Lua using the Love2D framework.

Game not using sprites, every object is geometry drawed by love2d

Asteroid game belongs to the endless runner game genre

## Requirements

- Windows 10
- Lua 5.4.2
- Love2D 11.4
- lunajson 1.2.3-1

## Installation

1. Download the [installer](https://github.com/NguyenNguyen0/asteroid-lua-game.git).

## How to play

1. Start the game.
2. Use the up arrow key, w letter, kp8 to move your spaceship forward.
3. Use the right, left arrow key, a letter, d letter , kp4, kp6 to rotate your spaceship
4. Press the **Space** bar to shoot laser.

## Controls

- **Arrow keys:** Move the spaceship.
- **Space bar:** Shoot bullets.
- **Esc:** Pause game play

## Goals

- Survive as long as possible by shooting asteroids.
- Earn points by destroying asteroids.

## Credits

- Developed by NguyenNguyen0

## File Hierarchy

The following is a breakdown of the file hierarchy for the Asteroid game project:

- main.lua - Entry point, initializes core game systems.
- globals.lua - Holds global variables and functions accessible throughout the program.
- conf.lua - Defines configurable settings (window title, size of window).

- states/ - Game state scripts:

  - Game.lua - Handles gameplay logic:
    + spawning asteroids: spawning the asteroids when game is playing.
    + progression: the game progression when player pause the game, select setting option, quit the game, start new game handling.
    + game level: when player finhish a level, the Game.lua will level up the game and more difficulty for player.
  - Menu.lua - Manages home menu options:
    + start: starting a new game level.
    + settings: go to the game setting options.
    + quit: quit the game.
  - Pause.lua - Handles pause state when playing:
    + resume: resume the playing game.
    + home menu: exit the playing game and go back to home menu.
    + settings: setting menu opstions.
  - Setting.lua - Controls settings menu:
    + sound: sound volume setting
    + music: music volume setting
    + reset high score: reset high score to 0.

- src/ - Resource folders:

  - sounds/ - Game sound effects and background music.
  - data/ - High score data file.

- objects/ - Script files for game objects:

  - Asteroid.lua - Defines asteroid behavior and characteristics.
  - Player.lua - Controls player ship movement, firing, collision detection.
  - Laser.lua - Manages player laser projectiles.

  All objects has draw function to draw

- components/ - Reusable UI components:
  - Button.lua - Defines interactive buttons with visuals and button event handling.
  - Label.lua - Creates dynamic text labels displayed on screen.
  - Text.lua - Renders dynamic text elements on screen.
  - SFX.lua - Handles all sound effects playback and music management.
