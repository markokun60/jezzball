import pygame
from  os.path import join

from controls.form       import Form
from controls.button     import Button
from controls.checkbox   import Checkbox
from controls.combobox   import Combobox 
from controls.textBox    import InputBox 
from controls.label      import Label 
from controls.controls   import *

from settings import *
from menu_mode          import MenuMode
from themes             import Theme,set_theme

class Form_Options(Form):

   def __init__(self,parent,game,images):
      super().__init__()
      self.parent = parent
      self.game = game
      self.images = images
      self._create_images()
      Control.form = self
      self._create_controls()
      Control.form = parent


   def open(self):
      self.old_controls_settings = save_controls_settings()
      self.old_game_settings     = self.game.save_settings()
      self._update_controls()

   def _create_images(self):
        root = join(self.game.resources,FOLDER_IMAGES)
        self.imgUndo    = pygame.image.load(join(root,'undo.png')).convert_alpha()
        self.imgDefault = pygame.image.load(join(root,'default.png')).convert_alpha()
      
   def create_themes_box(self,x,y):
      i = 0
      theme_index = 0
      themes  = []
      for theme_name in Theme.Themes.keys():
         if theme_name == Theme.CurrentName:
               theme_index = i
         themes.append(theme_name)
         i += 1
      cboThemes = Combobox('cboThemes',position=(x,y),width=40,values=themes,index=theme_index,func=self.theme) 
      return cboThemes 

   def create_size_box(self,x:int,y:int):
      sizes = []
      index = 0
      i = 0
      for (c,r) in SIZES:
         s = f"{c} x {r}"
         sizes.append(s) 
         if r == self.game.field.rows and c == self.game.field.cols:
            index = i
         i += 1

      cboSizes = Combobox('cboSizes',position=(x,y),width=40,values=sizes,index=index,func=self.sizes) 
      return cboSizes       

   def _create_controls(self):
      big_font_size = Control.FONT_SIZE + 4
      x = W_BUTTON // 2 + 24
      y = self.parent.yButton 
      DY = 25

      imgBack = self.images['back']
      btnBack = Button('btnBackOptions',position=(x, y),  size=(W_BUTTON, H_BUTTON),  func=self.back, text='Back',image= imgBack)
      btnBack.hint  = "Back to main menu" 
      btnBack.key   = pygame.K_ESCAPE 

      (xLeft,y) = self.next_right(40)

      btnUndo = Button('btnUndo',position=(x ,btnBack.rect.bottom + H_BUTTON/2 + DY), font_name=Control.FONT_DEFAULT , size=(W_BUTTON, H_BUTTON),  
                       func=self.undo, text='Undo',image=self.imgUndo) 
      btnUndo.hint = "Restore old settings"
      
      btnDefault = Button('btnDefalt',position=(x ,btnUndo.rect.bottom + H_BUTTON/2 + DY), font_name=Control.FONT_DEFAULT , size=(W_BUTTON, H_BUTTON), 
                          func=self.set_default, text='Default',image=self.imgDefault ) 
      btnDefault.hint = "Set default settings"

      DX = 4
      DY = 12
     
      Label('lblSettings',position=(xLeft, y),text='Game settings',font_size=big_font_size)
      (x,y) = self.next_down(DY)
     
      lblUserName = Label('lblUser',position=(x, y),  text='Player name:')
      (xv,y) = self.next_right(DX)
      self.txtUserName = InputBox('txtUser',position=(xv,y),width=120,text=self.game.player_name,func = self.player_name)
      self.txtUserName.add_linked_controls(lblUserName)
      #
      (x,y) = self.next_down(DY,lblUserName)
      self.chkSound = Checkbox('chkSounds',position=(x,y),text='Sounds',checked= self.game.is_sound,func=self.sound)
      #      
      (x,y) = self.next_down(DY,self.chkSound)
      self.chkGrid = Checkbox('chkGrid',position=(x,y),text='Grid',checked= self.game.field.is_grid,func=self.grid)
      #      
      (x,y) = self.next_down(DY,self.chkGrid )
      self.chkTimeLimit = Checkbox('chkTimeLimmit',position=(x,y),text='Time Limit',checked= self.game.is_time_limit,func=self.time_limit)
      #
      (x,y) = self.next_down(DY)
      lblTheme =  Label('lblTheme',position=(xLeft ,y),text='Theme:') 
      self.cboThemes = self.create_themes_box(xv,y)
      self.cboThemes.add_linked_controls(lblTheme)

      (x,y) = self.next_down(DY)
      lblSpeed =  Label('lblSpeed',position=(xLeft ,y),text='Speed:') 
      speeds = ['Slow','Regular','Fast']
      self.cboSpeed = Combobox('cboSpeed',position=(x,y),width=40,values=speeds,index=self.game.speed,func=self.speed) 
      self.cboSpeed.add_linked_controls(lblSpeed)
      
      (x,y) = self.next_down(DY)
      lblSizes =  Label('lblSize',position=(xLeft ,y),text='Size:') 
      self.cboSizes = self.create_size_box(x,y)
      self.cboSizes.add_linked_controls(lblSizes)
   
   def back(self):
      #self.parent.hide_show()
      self.parent.status = MenuMode.WELCOME
      self.game.save_config()
   
   def player_name(self,value):
      self.game.player_name = value

   def sound(self,value):
      self.game.is_sound = value
 
   def grid(self,value):
      self.game.field.is_grid = value

   def time_limit(self,value):
      self.game.is_time_limit = value

   def theme(self,value,index):
      self.game.theme_name = value
      set_theme(value)

   def speed(self,value,index):
      self.game.speed = index

   def sizes(self,value,index):
      (c,r) = SIZES[index]
      self.game.set_sizes(c,r)
 
   def set_default(self):
      default_contols_setings()
      self.game.set_default()
      self._update_controls()

   def undo(self):
       restore_controls_settings( self.old_controls_settings)
       self.game.restore_settings(self.old_game_settings)
       self._update_controls()
   
   def _update_controls(self):
      self.cboThemes.setValue(Theme.CurrentName)
      self.chkSound.checked = self.game.is_sound
      self.chkGrid.checked  = self.game.field.is_grid 
      self.txtUserName.set_text(self.game.player_name)
      self.cboSpeed.setIndex(self.game.speed)
      self.chkTimeLimit.checked = self.game.is_time_limit
          