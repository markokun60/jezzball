import  pygame
from    importlib.resources import files
from    os.path import join
from    typing  import Final

from controls.form       import Form
from controls.button     import Button
from controls.controls   import Control,init_controls
from settings            import *
from colors              import *
from codecs              import *
from draw_html           import DrawHTML
from form_options        import Form_Options
from menu_mode           import MenuMode
from themes              import Theme

class MainForm(Form):
    DX:Final[int] = 10
    
    def __init__(self,game):
        super().__init__()
        Control.form = self
        self.game = game
        init_controls()

        self.yButton  = H_BUTTON 
        self.xButtton = (WINDOW_WIDTH - 5 * W_BUTTON - 4 * MainForm.DX)//2+ W_BUTTON/ 2
        
        self._create_images()
        self._create_buttons()
        self._get_images_to_show()
        
        self.form_options = Form_Options(self,self.game, self.images)
        self.status = MenuMode.WELCOME
        self.draw_sources = {}
        self.font = pygame.font.SysFont(Control.FONT, 16,bold=True)

    def close(self):
        self.status = MenuMode.WELCOME

    def _create_images(self):
        root = join(self.game.resources,FOLDER_IMAGES)
        self.imgJezzball= pygame.transform.smoothscale(self.game.imgJezzball,(24,24))
        self.imgStart   = pygame.image.load(join(root,'start.png')).convert_alpha()
        self.imgHelp    = pygame.image.load(join(root,'help.png')).convert_alpha()
        self.imgOptions = pygame.image.load(join(root,'options.png')).convert_alpha()
        self.imgBack    = pygame.image.load(join(root,'cancel.png')).convert_alpha()
        self.imgExit    = pygame.image.load(join(root,'exit.png')).convert_alpha()

        self.images = {
            'back': self.imgBack
        }


    def _get_images_to_show(self):
        self.images['appl'] = self.imgJezzball

    def _draw_text_resource(self,surface,key):
        macros = {
            "{APP_NAME}"  : TITLE,
            "{VERSION}"   : VERSION,
            "{AUTHOR}"    : AUTHOR,
            "{USER_NAME}" : self.game.player_name,
            "{SCORE}"     : str(self.game.high_score),
            "{LEVEL}"     : str(self.game.high_level) ,
            "{AVG_LEVEL}" : str(round(self.game.avg_level,3)) ,
            "{GAME_COUNT}": str(self.game.total_games)
        }

        if not key in self.draw_sources.keys():
            source = f"{key}.txt"
            source  = files(RESOURCES).joinpath(source).read_text(encoding='utf-8')             
            for key in macros.keys():
                source = source.replace(key,macros[key])
                
            self.draw_sources[key] = DrawHTML(source=source,fnt=self.font,color=Theme.Current.text_color_info,images=self.images)

        dh = self.draw_sources[key] 
        x = (self.game.field.window_width  - dh.get_width())//2
        y = (self.game.field.window_height - dh.get_height() - H_BUTTON)//2 + H_BUTTON 
        dh.draw(surface,(x,y))

    def _create_buttons(self):
        x = self.xButtton
        y = self.yButton 
     
        btnBack = Button('btnBack',position=(W_BUTTON // 2+12, y),  size=(W_BUTTON, H_BUTTON),  func=self.back, text='Back',image=self.imgBack)
        btnBack.hide  = True
        btnBack.hint  = "Back to main menu" 
        btnBack.key   = pygame.K_ESCAPE

        self.btnStart = Button('btnStart',position=(x, y), size=(W_BUTTON, H_BUTTON), func= self.start, text='Start',image = self.imgStart)    
        self.btnStart.key = pygame.K_SPACE

        x += W_BUTTON
        x += MainForm.DX
        btnAbout = Button('btnAbout',position=(x, y), size=(W_BUTTON, H_BUTTON),  func=self.about, text='About',image=self.imgJezzball)
        btnAbout.hint  = "Show about information"

        x += W_BUTTON
        x += MainForm.DX
        btnHelp = Button('btnHelp',position=(x, y), size=(W_BUTTON, H_BUTTON),  func=self.help, text='Help',image=self.imgHelp)
        btnHelp.hint  = "Show how to play"
  
        x += W_BUTTON
        x += MainForm.DX
        btnOptions = Button('btnOptions',position=(x, y), size=(W_BUTTON, H_BUTTON),  func=self.menu_settings, text='Options',image=self.imgOptions)
        btnOptions.hint  = "Change settings"

        x += W_BUTTON
        x += MainForm.DX
        btnExit = Button('btnExit',position=(x, y), size=(W_BUTTON, H_BUTTON), func=self.exit_game, text='Exit',image=self.imgExit)
        btnExit.hint  = "Exit the game"      

    def back(self):
        self.hide_show()
        self.status = MenuMode.WELCOME

    def start(self):    
        self.status =  MenuMode.START

    def about(self):
        self.hide_show()
        self.status =  MenuMode.ABOUT

    def help(self):
        self.hide_show()
        self.status =  MenuMode.HELP

    def exit_game(self):
        self.status =  MenuMode.EXIT

    def menu_settings(self):
        self.status = MenuMode.OPTIONS
        self.form_options.open()

    def draw(self,surface:pygame.Surface):
        super().draw(surface)       

    def draw(self,surface:pygame.Surface):
        if self.status == MenuMode.OPTIONS:
            self.form_options.draw(surface)
            return        
        super().draw(surface)       
        if self.status == MenuMode.HELP:
            self._draw_text_resource(surface,'help')
        elif self.status == MenuMode.ABOUT:
            self._draw_text_resource(surface,'about')
        elif self.status == MenuMode.WELCOME:
            self._draw_text_resource(surface,'welcome')    

    def handle_controls_events(self,event):
        if self.status == MenuMode.OPTIONS:
            self.form_options.handle_controls_events(event)
        else:
            super().handle_controls_events(event)
          
    