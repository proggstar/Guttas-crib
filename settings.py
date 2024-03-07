# Konstanter
WINDOW_WIDTH = 1000  # Bredden til vinduet
WINDOW_HEIGHT = 700 # Høyden til vinduet

# Størrelsen til vinduet
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

SIZE_BG = (WINDOW_WIDTH, WINDOW_HEIGHT - 60)

# Frames Per Second (bilder per sekund)
FPS = 60

# Farger (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (100, 100, 255)
GREY = (142, 142, 142)
LIGHTRED = (255, 100, 100)
YELLOW = (255, 255, 0)

FREEZONE_UP = 60
FREEZONE_DOWN = WINDOW_HEIGHT - FREEZONE_UP


# Innstillinger til spilleren
PLAYER_WIDTH = 36
PLAYER_HEIGHT = 76
START_X_PLAYER = WINDOW_WIDTH * 0.2
START_Y_PLAYER = FREEZONE_DOWN - PLAYER_HEIGHT

max_fuel = 100
fuel = 20
ratio = fuel / max_fuel

timer = 0
scroll_x = 0

# Innstillinger for Powerups
POWERUP_WIDTH = 40
POWERUP_HEIGHT = 40

SCROLL_SPEED = 4