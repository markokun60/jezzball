from colors     import *
from settings   import *
from controls.controls import *

class Theme:
    Themes:dict = {}
    CurrentName:str = ''
    Current:Theme = None
    def __init__(self,
                 bkg_color          :tuple[int,int,int],
                 bar_colors         :tuple[tuple[int,int,int],tuple[int,int,int]],
                 grid_color         :tuple[int,int,int],
                 closed_cell_color  :tuple[int,int,int],
                 open_cell_color    :tuple[int,int,int],
                 text_color_info    :tuple[int,int,int],
                 text_color_field   :tuple[int,int,int],
                 control_mode:int
        ):
        self.background_color   = bkg_color
        self.bar_colors         = bar_colors
        self.grid_color         = grid_color
        self.closed_cell_color  = closed_cell_color
        self.open_cell_color    = open_cell_color
        self.text_color_info    = text_color_info,
        self.text_color_field   = text_color_field,
        self.control_mode       = control_mode   
        self.progress_bars      = [BLUE,RED]   
        self.cursor_color       = RED
        self.ball_path          = "ball"

class ClassicTheme(Theme):   
    def __init__(self): 
            super().__init__(
                bkg_color           =  BLACK,                
                bar_colors          = (RED, BLUE),
                grid_color          = GRAY,
                closed_cell_color   = LIGHT_GRAY,
                open_cell_color     = BLACK,
                text_color_info     = WHITE,
                text_color_field    = WHITE,
                control_mode=Control.NIGHT_MODE   
            )  


class DesertTheme(Theme):   
     def __init__(self): 
            super().__init__(
                bkg_color        =  ORANGE,                
                bar_colors       = (RED, BLUE),
                grid_color       = LIGHT_GRAY,
                closed_cell_color= YELLOW,
                open_cell_color  = LIGHT_GRAY,
                text_color_info  = BLACK,
                text_color_field = BLACK,
                control_mode = Control.DESERT_MODE
            )  
            #self.ball_path = "ball_monster"        

class GreenTheme(Theme):   
     def __init__(self): 
            super().__init__(
                bkg_color        =  DARK_GREEN,                
                bar_colors       = (RED, BLUE),
                grid_color       = LIGHT_GRAY,
                closed_cell_color= GREEN,
                open_cell_color  = AQUA,
                text_color_info  = YELLOW,
                text_color_field = BLACK,
                control_mode = Control.GREEN_MODE
            )          

class SnowTheme(Theme):   
     def __init__(self): 
            super().__init__(
                bkg_color=  WHITE,                
                bar_colors= (RED, BLUE),
                grid_color       = AQUA,
                closed_cell_color= WHITE_DARK  ,
                open_cell_color  = PURPL_LIGHT,
                text_color_info  = BLACK,
                text_color_field = BLACK,
                control_mode = Control.DAY_MODE      
            )   

class MarsTheme(Theme):   
     def __init__(self): 
            super().__init__(
                bkg_color=  RED,                
                bar_colors= (GREEN, BLUE),
                grid_color=LIGHT_GRAY,
                closed_cell_color= ORANGE,
                open_cell_color  = RED_DARK ,
                text_color_info  = WHITE,
                text_color_field = WHITE,
                control_mode = Control.RED_MODE      
            )  
            self.progress_bars = [GREEN,BLUE]   
            self.cursor_color  = AQUA

def create_themes() -> dict[str, Theme]:
    themes = {
        CLASSIC: ClassicTheme(),
        DESERT : DesertTheme(),
        FOREST : GreenTheme(),
        SNOW   : SnowTheme(),
        MARS   : MarsTheme()
    }
    Theme.Themes = themes


def set_theme(theme_name:str=CLASSIC):
    Theme.CurrentName = theme_name
    if theme_name in Theme.Themes:
        Theme.Current = Theme.Themes[theme_name]
    else:
        print(f"Theme '{theme_name}' not found. Using default theme.")
        Theme.Current = Theme.Themes[CLASSIC]
    set_contols_mode(Theme.Current.control_mode)
    reset_all_controls()  
    #reset_all_groups() 
