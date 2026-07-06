from typing import Final

AUTHOR :Final[str] = "Mark"
VERSION:Final[str] = "1.0.0"
TITLE:Final[str]  = 'Jezzball'

CELL_SIZE :Final[int]  = 16
CELL_SIZE2 :Final[int] = CELL_SIZE // 2

LEFT :Final[int] = 48
TOP  :Final[int] = 48
RIGHT_EDGE  :Final[int] = 32
BOTTOM_EDGE :Final[int] = 48

ROWS :Final[int] = 20
COLS :Final[int] = 28

SIZES = [
    (28,20),  
    (35,25),
    {35,30}
]

WINDOW_WIDTH :Final[int] = LEFT + COLS * CELL_SIZE + RIGHT_EDGE 
WINDOW_HEIGHT:Final[int] = TOP  + ROWS * CELL_SIZE + BOTTOM_EDGE

#RIGHT :Final[int]  = WINDOW_WIDTH  - RIGHT_EDGE
#BOTTOM :Final[int] = WINDOW_HEIGHT - BOTTOM_EDGE

FOLDER_ASSETS:Final[str] = 'assets'
FOLDER_SOUNDS:Final[str] = 'sounds'
FOLDER_IMAGES:Final[str] = 'images'
FOLDER_DATA  :Final[str] = 'data'
RESOURCES    :Final[str] = 'resources'

SETTINGS_FILE  :Final[str] = 'jezzball.ini'
#
SECTION_GENERAL:Final[str] = "General"
KEY_SOUND      :Final[str] = "sound"
KEY_GRID       :Final[str] = "grid"
KEY_PLAYER     :Final[str] = "player"
KEY_THEME      :Final[str] = "theme"
KEY_SPEED      :Final[str] = 'speed'
SECTION_SUMMARY:Final[str] = "Summary"
KEY_SCORE      :Final[str] = "score"
KEY_LEVEL      :Final[str] = "level"
KEY_ROWS       :Final[str] = "rows"
KEY_COLS       :Final[str] = "cols"
KEY_GAMES_COUNT:Final[str] = "total_games"
KEY_AVG_LEVEL  :Final[str] = "avg_level"
#
# Themes
#
CLASSIC:Final[str] = 'classic'
DESERT :Final[str] = 'desert'
FOREST :Final[str] = 'forest'
SNOW   :Final[str] = "snow"
MARS   :Final[str] = "mars"
#
VERTICAL  :Final[str] = 'V'
HORIZONTAL:Final[str] = 'H'	

FREE:Final[int]   = 0
BAR:Final[int] 	  = 1
MARKED:Final[int] = 2

#
W_BUTTON :Final[int] = 90
H_BUTTON :Final[int] = 40
#
SCORE_PER_CELL = 3.5
SCORE_V_CELL   = 70
SCORE_H_CELL   = 98
#
SCORE_BONUS_80 = 10  
SCORE_BONUS_90 = 10    
#
TARGET_PERCENT = 75
MAX_BALLS      = 50
#
#


