#import asyncio

import pygame
import time 
import sys 
from   configparser import ConfigParser
from enum       import Enum
from os         import makedirs
from os.path    import join,abspath ,isfile,isdir
from typing     import Final
from utils      import *

from ball       import Ball
from bar        import Bar 
from settings   import *
from colors     import *
from field      import Field
from animated_object import Explosion, Heart,AnimatedObject
from themes     import set_theme,create_themes,Theme
from main_form  import MainForm,MenuMode
from controls.controls   import Control,init_controls
from timer      import Timer

class GameMode(Enum):
    WELCOME   = 1
    PRE_LEVEL = 2
    PLAY_MODE = 3
    POST_LEVEL= 4
    LOST      = 5

class Game:
    PROGRESS_BAR_WIDTH = 80
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init() 
        #
        base_path = getattr(sys, '_MEIPASS', abspath("."))
        self.resources = join(base_path,FOLDER_ASSETS)
        Ball.asset_folder = self.resources
        AnimatedObject.ASSET_FOLDER = self.resources

        #
        self.theme_name = CLASSIC
        self.player_name =''
        self.is_sound = False
        #
        self.high_score  = 0
        self.high_level  = 0
        self.total_games = 0
        self.avg_level   = 0
        #
        self.speed      = 1
        self.field = Field()
        self.read_config()
        self.set_sizes(self.field.cols,self.field.rows)
        self.imgJezzball  = pygame.image.load(join(self.resources, FOLDER_IMAGES, 'jezzball.png'))
        #
        self.screen = pygame.display.set_mode((self.field.window_width, self.field.window_height))
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(self.imgJezzball)
        self.imgJezzball =  self.imgJezzball.convert_alpha()
        #self.imgBackground = pygame.image.load(join(self.resources, FOLDER_IMAGES, 'background','space','1.jpg'))
        #
        self.clock = pygame.time.Clock()
        self.running = False
        
        self.score = 0
        self.start_time = time.time()        
        self.game_duration = 60  # Game lasts for 60 seconds
        self.direction = HORIZONTAL
        self.total_balls = 1
        self.balls = []
        # 
        self.bars = []
        self.bars.append(Bar())
        self.bars.append(Bar())
        #
        self.explosion = Explosion()
        #
        self.hearts = []
        self.mouse_pos = (0,0)
        self.cursor_iamges = []
        self.cursor_base_iamges = load_images(join(self.resources, FOLDER_IMAGES, 'bar'), clr_key=(255,255,255))
        self.level = 0
        self.total_lives = 0
     
        self.is_paused = False
  
        self.message  = None
        self.mode = GameMode.WELCOME
        self.target_cells = self.field.rows * self.field.cols * TARGET_PERCENT // 100
        create_themes()
        self._load_sounds()
        #
        init_controls()
        self.font      = pygame.font.SysFont(Control.FONT, 36,bold=True)
        self.font_info = pygame.font.SysFont(Control.FONT, 16)
        self.main_form = MainForm(self)
        self.select_theme(self.theme_name)
        self.timer_lost = Timer(duration=5000,func=self.to_welcome , on_update=self.on_update_lost_timer)
        self.timer_pass_level = Timer(2000,func=self.start_mode_new_level)
    
    def _load_sounds(self):
        path = join(self.resources,FOLDER_SOUNDS)
        self.start_sound     = pygame.mixer.Sound(join(path,"start.ogg"))    
        self.click_sound     = pygame.mixer.Sound(join(path,"click.ogg"))    
        self.explosion_sound = pygame.mixer.Sound(join(path,"explode.wav"))    
        self.loss_sound      = pygame.mixer.Sound(join(path,"loss.ogg"))    
        self.new_level_sound = pygame.mixer.Sound(join(path,"new_level.ogg"))    
    
    def set_default(self):
        self.is_sound = True
        self.speed    = 1
        set_theme(CLASSIC)
        self.field.set_cols_rows(COLS,ROWS)
        self.field.is_grid = True

    def select_theme(self,name:str):
        set_theme(name)
        self.cursor_iamges.clear()
        for ci in self.cursor_base_iamges:
            im = swap_color(ci,BLACK,Theme.Current.cursor_color).convert()
            im.set_colorkey(WHITE)
            self.cursor_iamges.append(im)
        self.set_cursor()

    def set_cursor(self):
        if self.mode == GameMode.PLAY_MODE:
            i = 0 if self.direction == HORIZONTAL else 1
            cursor_image = self.cursor_iamges[i] 
            w = cursor_image.get_width()
            h = cursor_image.get_height() 
            cursor = pygame.cursors.Cursor((w//2, h//2), cursor_image)
            pygame.mouse.set_cursor(cursor) 
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

    def create_bars(self, pos:tuple):
        i = -1
        for bar in self.bars:
            p = self.field.get_cell(self.mouse_pos)
            if p is None:
                if not self.is_paused:
                    self.pause(True)
                return
            (col,row) = p            
            if i > 0:
                if self.direction==HORIZONTAL:
                    col += 1
                else:                
                    row += 1   

            pos = cell_to_xy((col, row ))
            #print(f"{(row, col)}, bar pos: {pos}, direction: {self.direction} {i}")
            bar.start(pos,self.direction,i)
            i = 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.mode == GameMode.WELCOME:
                #
                self.main_form.handle_controls_events(event)
                if self.main_form.status == MenuMode.EXIT:
                    self.running = False
                elif self.main_form.status == MenuMode.START:
                    self.main_form.close()
                    self.start()
            elif self.mode == GameMode.PRE_LEVEL:
                break            
            elif event.type == pygame.KEYDOWN:
                if self.is_paused:
                    self.pause(False)
                elif event.key == pygame.K_ESCAPE:
                    self.pause(True)
            elif event.type == pygame.MOUSEMOTION:                
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_sound:
                    self.click_sound.play()
                if self.is_paused:
                    self.pause(False)
                elif event.button == 3:  # Right click to change direction
                    self.direction = VERTICAL if self.direction == HORIZONTAL else HORIZONTAL
                    self.set_cursor()
                else:
                    self.mouse_pos = event.pos   
                    self.create_bars(self.mouse_pos)
                    
        return self.running
    
    def draw_lives(self):
        x = LEFT + 10
        y = 0
        i = 0
        for heart in self.hearts:
            x = heart.draw(self.screen,x,y)
            x += 5
            i += 1
            if i >= self.total_lives:
                break;

    def _draw_game_msg(self,txt:str):
        return draw_message(self.screen, txt,-1,-1,self.font,Theme.Current.text_color_field,self.field.window_width,self.field.window_height)

    def _draw_info_msg(self,txt:str,x:int,y:int,color:tuple[int,int,int]):
        return draw_message(self.screen,txt,x,y,self.font_info,color,self.field.window_width,self.field.window_height   )

    def draw_level_messge(self):
        text = f"Level: {self.level+1}"
        self._draw_game_msg(text)

    def get_progress_value(self) -> int: 
        total_cells = self.field.rows * self.field.cols
        n = self.done_cells * 100
        n /= total_cells
        return int(n)

    def draw_center_info_messages(self):          
        messages = Messages()
        messages.add("Level:",str(self.level))
        messages.add("Lives:",str(self.total_lives))
        messages.generate(self.font_info,Theme.Current.text_color_info)

        x = self.field.window_width //2 - messages.width // 2
        y = self.field.window_height - 2 * CELL_SIZE

        messages.draw(self.screen,x,y)

    def draw_right_info_messages(self):   
        messages = Messages()
        messages.add("Score:",str(self.score),"123456789")
        messages.add("Game Time:",str(self.game_time))
        messages.generate(self.font_info,Theme.Current.text_color_info)

        rect = self.field.get_rect()
        #x = rect.right - messages.width
        x = self.field.window_width - messages.width - 10
        y = self.field.window_height - 2 * CELL_SIZE

        messages.draw(self.screen,x,y)

    def draw_left_info_messages(self):
        n = self.get_progress_value()
        elapsed_time = self.get_elapsed_time()
        time_left = self.game_duration  - elapsed_time  
      
        messages = Messages()
        messages.add(f"{n}%"        ,'','100')
        messages.add("Time Left:"   ,str(time_left),'xxx')
        messages.generate(self.font_info,Theme.Current.text_color_info)

        x = 10
        y = self.field.window_height - 2 * CELL_SIZE

        messages.draw(self.screen,x,y)
        x += messages.width
        x += 4
        draw_h_pregress_bar(self.screen, x,y,self.done_cells,self.target_cells,Game.PROGRESS_BAR_WIDTH)
        y += CELL_SIZE
        draw_h_pregress_bar(self.screen, x,y,elapsed_time,self.game_duration,Game.PROGRESS_BAR_WIDTH)
        
       
    def draw(self):
        self.screen.fill(Theme.Current.background_color)

        if self.mode == GameMode.WELCOME:
            self.main_form.draw(self.screen)
        elif self.mode == GameMode.PRE_LEVEL:
            self.explosion.draw(self.screen)
            self.draw_level_messge()    
        else:
            #jself.screen.blit(self.imgBackground,(LEFT,TOP))
            self.draw_lives()
            self.draw_left_info_messages()
            self.draw_center_info_messages()
            self.draw_right_info_messages()

            self.field.draw(self.screen)

        if self.mode != GameMode.WELCOME:            
            for ball in self.balls:
                ball.draw(self.screen)

            for bar in self.bars:
                bar.draw(self.screen)
        
        if self.message is not None:
            self._draw_game_msg(self.message)

        pygame.display.update()

    def pause(self,f:bool):
        if f:            
            if not self.is_paused:
                self.is_paused = True
                self.message =  "Paused. \n Click any key to resume"
                self.pause_started = time.time()
        elif self.is_paused:
            self.is_paused = False
            self.pause_time += (time.time() - self.pause_started)
            self.message = None


    def set_sizes(self,c:int,r:int):
        #if  c != self.field.cols or r != self.field.rows:
        self.field.set_cols_rows(cols=c,rows=r)
        self.screen = pygame.display.set_mode((self.field.window_width, self.field.window_height))

    def to_welcome(self):

        self.message = None
        self.set_cursor()
        self.mode = GameMode.WELCOME

    def start(self):
        Ball.images = None
        if self.is_sound:
            self.start_sound.play()
        self.level = 0
        self.score = 0
        self.pause_time = 0
        self.game_time = 0
        self.direction = VERTICAL
        self.message = None
        self.start_mode_new_level()
        #

    def start_mode_new_level(self):   
        self.message = None
        if self.is_sound:
            self.new_level_sound.play()            
        self.mode = GameMode.PRE_LEVEL
        self.balls.clear()
        self.field.reset()
        for b in self.bars:
            b.active = False
        #
        y = TOP + (self.field.rows - 3) * CELL_SIZE
        for i in range(2):
            x = LEFT if i == 0 else self.field.window_width - RIGHT_EDGE
            ball = Ball(x, y)
            ball.direction.y = 0
            ball.direction.x = 1 if i == 0 else -1
            self.balls.append(ball)            
        Ball.balls = self.balls    
        #     

    def start_new_level(self):
        self.mode = GameMode.PLAY_MODE
        self.set_cursor()
        if self.level == 0:
            self.game_time = 0
        else:
            self.game_time += self.get_elapsed_time()    

        self.game_duration = 60  # Game lasts for 60 seconds
        self.game_duration += (self.level * 10)
        self.level += 1 
        self.total_lives = self.level
        self.total_balls =  self.level
        if self.total_balls > MAX_BALLS:
            self.total_balls = MAX_BALLS

        self.hearts.clear()
        for i in range(self.total_lives):
            self.hearts.append(Heart())
        #
        self.balls.clear()
        self.field.mark_random(self.total_balls)
        for c in range(self.field.cols):
            for r in range(self.field.rows):
                if self.field.cells[c][r] == MARKED:
                    p = cell_to_xy((c,r))
                    b = Ball(p[0],p[1])
                    self.balls.append(b)
        #    
        Ball.balls = self.balls           
        self.field.reset()
        self.start_time = time.time()
        self.pause_time = 0
        self.done_cells = 0

    def on_update_lost_timer(self):            
        n = self.timer_lost.get_time_left()
        if n >= 0:
            sec = n // 1000
            self.message = f"{sec}\n{self.lost_message}"

    def lost(self,msg:str) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
        if self.level > self.high_level:
            self.high_level  = self.level
        avg_levels = self.avg_level * self.total_games
        avg_levels += self.level
        self.total_games += 1
        self.avg_level = avg_levels / self.total_games
        #      
        if self.is_sound:
            self.loss_sound.play()
        self.lost_message = msg

        self.mode = GameMode.LOST
        self.timer_lost.activate()

    def ball_bar_collision(self, ball:Ball, bar:Bar) -> bool:
        if bar.active == False: return False
        (x,y) = ball.position
        bar_rect = bar.get_rect()
        if bar.direction == HORIZONTAL:
            if abs(y - bar_rect.centery) < ball.radius + Bar.SIZE/2 and bar_rect.left < x < bar_rect.right:
                return True
        else:
            if abs(x - bar_rect.centerx) < ball.radius + Bar.SIZE/2 and bar_rect.top < y < bar_rect.bottom:
                return True
        return False
    
    def get_free_cells(self) -> None:
        for ball in self.balls:
            (col,row) = self.field.get_cell_in_field(ball.position)
            self.field.marked_cells(col,row)

        self.field.change_marked_cells(FREE, BAR)     
        self.field.change_marked_cells(MARKED, FREE)
        #self.field.print_cells()

    def update_for_newlevel(self, dt:int) -> None:
        if self.explosion.active:
            return
        for ball in self.balls:
            ball.move(dt) 
            ball.update_draw_index()
            if self.balls_collision():   
                y = ball.position.y
                rect = self.field.get_rect()
                x = rect = rect.centerx
                self.explosion.set_position((x,y),self.start_new_level)
                if self.is_sound:
                    self.explosion_sound.play()
                break
                   

    def get_elapsed_time(self) -> int:
        if self.is_paused:
            elapsed_time = self.pause_started - self.start_time - self.pause_time  
        else:  
            elapsed_time = time.time() - self.start_time - self.pause_time
        return int(elapsed_time)

    def balls_collision(self):
        res = False
        for a in self.balls:
            a.tag = 0 

        for a in self.balls:
            if a.tag == 0:
                for b in self.balls: 
                    if a == b: continue
                    if a.meet_ball(b):
                        a.tag = 1
                        b.tag = 1
                        res = True
                        #print(f"meet ball {self.position}")
        return res

    def balls_bars_collision(self,dt:int):
        for ball in self.balls:
            ball.update(dt,self.field)
            for bar in self.bars:
                if bar.active:
                    if self.ball_bar_collision(ball, bar):
                        self.total_lives -= 1
                        bar.active = False
                        print(f"Lost a life! {self.total_lives}. Score: {self.score}")
                        if self.total_lives <= 0:
                            self.lost("No more lives")        

    def update(self,dt:int) -> None:
        old_done = self.done_cells
        b = False
        for bar in self.bars:
            if bar.update(dt,self.field):
                b = True
        if b:
            self.get_free_cells()
            
        self.done_cells = self.field.count(BAR)

        if self.done_cells != old_done:
            score = (self.done_cells -  old_done) * SCORE_PER_CELL
            if self.direction == HORIZONTAL:
                score += SCORE_H_CELL
            else:
                score += SCORE_V_CELL
            #      
            self.score +=  score
    
        if self.done_cells >= self.target_cells:
            percent = self.get_progress_value() - TARGET_PERCENT
            print(f"Level {self.level} completed! Score: {self.score} Done: {self.done_cells}: {percent}% . Target:{self.target_cells}")

            if percent >= 90:      
                self.score += (self.get_progress_value() - TARGET_PERCENT) * SCORE_BONUS_80
            elif percent >= 80:      
                self.score += (self.get_progress_value() - TARGET_PERCENT) * SCORE_BONUS_90
            self.mode = GameMode.POST_LEVEL
            self.timer_pass_level.activate()
            self.message = "You pass the level"
        else:
            self.balls_collision()
            self.balls_bars_collision(dt)
            if self.mode == GameMode.PLAY_MODE:
                if self.get_elapsed_time() >= self.game_duration:
                    self.lost("No more time")

    def run(self):
        self.running = True        
        while self.running:
            fps = 10 + self.speed * 10
            dt = self.clock.tick(fps)/1000
            if not self.handle_events(): break
            #
            if self.mode == GameMode.PRE_LEVEL:
                self.update_for_newlevel(dt)
            elif self.mode == GameMode.LOST:
                self.timer_lost.update()
            elif self.mode == GameMode.POST_LEVEL:
                self.timer_pass_level.update()
            elif self.mode == GameMode.PLAY_MODE:
                if not self.is_paused:
                    self.update(dt)
            self.draw()
        self.save_config()
        pygame.quit()
        sys.exit()        
            
    def save_settings(self):
        x = {
            KEY_SOUND : self.is_sound,
            KEY_PLAYER: self.player_name,
            KEY_THEME : self.theme_name,
            KEY_SPEED : self.speed,
            KEY_ROWS  : self.field.rows,
            KEY_COLS  : self.field.cols,
            KEY_GRID  : self.field.is_grid  
        }
        return x

    def restore_settings(self,x:list):
        self.is_sound      = x[KEY_SOUND]
        self.player_name   = x[KEY_PLAYER]
        self.theme_name    = x[KEY_THEME]
        self.speed         = x[KEY_SPEED]
        self.field.rows    = x[KEY_ROWS]
        self.field.cols    = x[KEY_COLS]
        self.field.is_grid = x[KEY_GRID]    

    def save_config(self):
        file_path = join(FOLDER_DATA,SETTINGS_FILE)
        config =  ConfigParser()
        config[SECTION_GENERAL] = self.save_settings()   
        config[SECTION_SUMMARY] = {
            KEY_SCORE: self.high_score,
            KEY_LEVEL: self.high_level,
            KEY_GAMES_COUNT: self.total_games,
            KEY_AVG_LEVEL:self.avg_level

        }
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    def read_config(self):
        file_path = join(FOLDER_DATA,SETTINGS_FILE)
        if not isfile(file_path):
            self.save_config()
            return
        config = ConfigParser()
        config.read(file_path)

        section = SECTION_GENERAL
        self.is_sound    = config.getboolean(section, KEY_SOUND )
        self.player_name = config.get       (section, KEY_PLAYER)
        self.theme_name  = config.get       (section, KEY_THEME)
        if config.has_option(section,KEY_SPEED):
            self.speed  = config.getint(section,KEY_SPEED)

        if config.has_option(section,KEY_GRID):
            self.field.is_grid = config.getboolean(section,KEY_GRID)

        if config.has_option(section,KEY_ROWS) and config.has_option(section,KEY_COLS):
            self.field.rows = config.getint(section,KEY_ROWS) 
            self.field.cols = config.getint(section,KEY_COLS)     
        #
        if config.has_section(SECTION_SUMMARY):
            section = SECTION_SUMMARY
            if config.has_option(section,KEY_SCORE):
                self.high_score = config.getfloat(section,KEY_SCORE)
            if config.has_option(section,KEY_LEVEL):
                self.high_level = config.getint  (section,KEY_LEVEL)
            if config.has_option(section,KEY_GAMES_COUNT):
                self.total_games = config.getint  (section,KEY_GAMES_COUNT)
            if config.has_option(section,KEY_AVG_LEVEL):
                self.avg_level= config.getfloat(section,KEY_AVG_LEVEL)
        



#async def main():
#    game = Game()
#    game.run()
#    pygame.quit()  

#asyncio.run(main())             

if __name__=="__main__":
    if not isdir(FOLDER_DATA):
        makedirs(FOLDER_DATA)
    game = Game()
    game.run()
    pygame.quit()            
