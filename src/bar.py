import pygame
from settings import *
from themes import Theme

class Bar:
    SIZE = CELL_SIZE 

    def __init__(self):
        self.direction = 'H'
        self.start_position = (0, 0)
        self.position = (0, 0)
        self.speed = 80  # pixels per second
        self.direction_value = 0
        self.active = False
        self.direction_value = 0

    def start(self,pos:tuple,direction:str,direction_value:int):
        self.direction = direction
        if direction_value == 0:
            print("Error: direction_value cannot be 0")  
        elif self.direction == HORIZONTAL:
            if direction_value < 0:
                pos = (pos[0]+CELL_SIZE2, pos[1]-CELL_SIZE2)
            else:
                pos = (pos[0]-CELL_SIZE2, pos[1]-CELL_SIZE2)
        else:
            if direction_value < 0:
                pos = (pos[0]-CELL_SIZE2, pos[1]+CELL_SIZE2)
            else:   
                pos = (pos[0]-CELL_SIZE2, pos[1]-CELL_SIZE2)

        self.position = pos
        self.start_position = pos
        self.direction_value = direction_value
        i = 0 if self.direction_value < 0 else 1
        self.color = Theme.Current.bar_colors[i]        
        self.active = True

    def get_rect(self) -> pygame.FRect:
        (x,y) = self.start_position
      
        if self.direction == HORIZONTAL:
            if self.direction_value < 0: # to left bar
                w = x - self.position[0]
                x -= w
            else: # to right bar
                w = self.position[0] - x
            rect = pygame.FRect(x,y, w, Bar.SIZE)

        else:
            if self.direction_value < 0:
                h = y - self.position[1]
                y -= h
            else:
                h = self.position[1] - y

            rect = pygame.FRect(x,y, Bar.SIZE, h)
        return rect
        
    def draw(self, screen:pygame.Surface):
        if self.active == False: return
        rect = self.get_rect()
        pygame.draw.rect(screen, self.color, rect)
        #print(f"Bar position: {self.position}, direction: {self.direction}:{self.direction_value}")

    def move(self,dt,field):
        rect= field.get_rect()
        d = self.speed * dt * self.direction_value 
        (x,y) = self.position

        if self.direction == HORIZONTAL:            
            x += d
            if x < rect.left or x > rect.right:
                self.active = False
        else:
            y += d
            if y < rect.top or y > rect.bottom:
                self.active = False

        self.position = (x,y)
        p = field.get_cell((x,y))   
        if p is None:
            self.active = False
        else:
            (col,row)  = p
            if field.cells[col][row] == BAR:
                self.active = False

    def set_cells_not_use(self,field,value):
        (col0,row0) = field.get_cell((self.position[0],self.start_position[1])) 
        (col1,row1) = field.get_cell((self.position[0],self.position[1])) 
        if row0 == row1:
            if col0 < col1:
                for c in range(col0,col1+1):
                    field.cells[c][row0] = value
            else: 
                for c in range(col1,col0+1):
                    field.cells[c][row0] = value
        else:
            if row0 < row1:
                for r in range(row0,row1+1):
                    field.cells[col0][r] = value
            else:
                for r in range(row1,row0+1):
                    field.cells[col0][r] = value


    def update(self,dt,field) ->bool:
        if self.active:
            self.move(dt,field)
            if not self.active:
                field.set_bar(self.get_rect(),self.direction)
                return True
        return False
        
  
