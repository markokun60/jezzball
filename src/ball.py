import  pygame
from os.path import join 

from random import choice

from pygame.math import Vector2     
from utils       import load_images
from settings    import *
from colors      import *
from utils       import swap_color  
from themes      import Theme

class Ball:
    RIGHT = 0
    LEFT  = 1
    DOWN  = 2
    UP    = 3  
    #
    images = None
    asset_folder = ''

    def __init__(self, x, y, radius=7):
        self.position = Vector2(x, y)
        self.radius = radius
        self.rect = pygame.FRect(0,0,self.radius*2,self.radius *2)
        x = choice([-1, 1])
        y = choice([-1, 1])
        self.direction = Vector2(x, y)
        #
        if Ball.images is None:
            self.generate_images()
        #
        self.index = 0
        self.speed = 100
        self.velocity = Vector2(1, 1).normalize_ip()
        self.old_position = self.position.copy()
        self.tag = 0

    def generate_images(self):
        path = join(Ball.asset_folder, FOLDER_IMAGES,  Theme.Current.ball_path)
        Ball.images = load_images(path, sizes=(self.radius*2, self.radius*2))#, clr_key=(0,0,0))
        self.index = 0

    def get_edge_points(self):
        return [
            self.position + Vector2( self.radius, 0),  # Right
            self.position + Vector2(-self.radius, 0),  # Left
            self.position + Vector2(0,  self.radius),  # Down
            self.position + Vector2(0, -self.radius)   # Up
        ]

    def move(self,dt:int):
        self.position += self.direction * dt * self.speed   

    def check_border_collision_not_use(self,field:pygame.FRect):     
        rect = field.get_rect()
        if self.position.x - self.radius < rect.left:
            self.position.x = LEFT + self.radius
            self.direction.x *= -1

        elif self.position.x + self.radius > rect.right:
            self.position.x = rect.right - self.radius
            self.direction.x *= -1
        
        if self.position.y - self.radius < rect.top:
            self.position.y = rect.top + self.radius
            self.direction.y *= -1

        elif self.position.y + self.radius > rect.bottom:
            self.position.y = rect.bottom - self.radius
            self.direction.y *= -1
            
        else:
            return False
        self.position = self.old_position     
   

        #print(f"Ball position: {self.position}, direction: {self.direction}")   
        return True

    def get_rect(self):
        self.rect.center = self.position
        return self.rect

    def meet_ball(self,ball:Ball):
        res = False
        rect = ball.get_rect()
        positions = self.get_edge_points()
        if self.direction.x > 0:
            point = positions[Ball.RIGHT]
        else:
            point = positions[Ball.LEFT]
        if rect.collidepoint((point.x,point.y)):            
            self.direction.x  *= -1
            ball.direction.x  *= -1
            res = True

        if self.direction.y < 0:
            point = positions[Ball.UP]
        else:
            point = positions[Ball.DOWN]

        if rect.collidepoint((point.x,point.y)):            
            self.direction.y *= -1
            ball.direction.y *= -1
            res = True

        #print(f"a={self.direction} b={ball.direction} {i}")
        return res

    def check_field_collision(self, field):
        res = False
        points = self.get_edge_points()
        if self.direction.x > 0:
            point = points[Ball.RIGHT]
        else:
            point = points[Ball.LEFT]            

        p = field.get_cell([point.x, point.y])            
        if p is None:
            self.direction.x *= -1
            res = True
        else:
            (col,row) = p
            if field.cells[col][row] == BAR:
                self.direction.x *= -1
                res = True

        if self.direction.y < 0:
            point = points[Ball.UP]
        else:
            point = points[Ball.DOWN]      

        p = field.get_cell([point.x, point.y])            
        if p is None:
            self.direction.y *= -1
            res = True
        else:
            (col,row) = p
            if field.cells[col][row] == BAR:
                self.direction.y *= -1
                res = True

        #print(f"{point} {p} {self.direction.y}")

        if res:
            self.position = self.old_position
                      
    def draw(self, screen:pygame.Surface):
        x = int(self.position.x - self.radius)
        y = int(self.position.y - self.radius)          
        screen.blit(Ball.images[self.index], (x, y))
        pygame.draw.circle(screen,(0,0,0),(self.position.x,self.position.y),self.radius,1)
        
    def update(self, dt:int,field):
        self.old_position = self.position.copy()
        self.move(dt) 
        #self.check_border_collision(field)
        self.check_field_collision(field)
        self.update_draw_index()

    def update_draw_index(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0   
        