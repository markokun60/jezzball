import  pygame
from os.path import join 
  
from utils import load_images
from settings import *

class AnimatedObject:
    IMAGES = None
    ASSET_FOLDER = ''

    def __init__(self,images):
        if Heart.IMAGES is None:
            path = join(AnimatedObject.ASSET_FOLDER, FOLDER_IMAGES,  'heart')
            Heart.IMAGES = load_images(path, sizes=None, clr_key=None)
        self.index = 0
        self.active = False
        self.images = images
        self.is_looping = False
    
    def end_of_loop(self):
        pass

    def draw(self, screen:pygame.Surface,x:int,y:int):
        if not self.active: return
        screen.blit(self.images[self.index], (x, y)) 
        x += self.images[self.index].get_width()
        self.index += 1
        if self.index >= len(self.images):
            if self.is_looping:
                 self.index = 0
            else:
                self.index = self.index - 1
                self.active = False        
                self.end_of_loop()                
        return x
    
class Heart(AnimatedObject):
    IMAGES = None
    def __init__(self):
        if Heart.IMAGES is None:
            path = join(AnimatedObject.ASSET_FOLDER, FOLDER_IMAGES,  'heart')
            Heart.IMAGES = load_images(path, sizes=None, clr_key=None)

        super().__init__(Heart.IMAGES)
        self.active = True
        self.is_looping = True
     

class Explosion(AnimatedObject):
    IMAGES = None
    def __init__(self):
        if Explosion.IMAGES is None:
            path = join(AnimatedObject.ASSET_FOLDER, FOLDER_IMAGES,  'explosion')
            Explosion.IMAGES = load_images(path, sizes=None, clr_key=None)

        super().__init__(Explosion.IMAGES)

    def end_of_loop(self):
        self.active = False
        self.func()

    def set_position(self, pos:tuple,func):
        self.x = pos[0] - self.images[0].get_width()//2
        self.y = pos[1] - self.images[0].get_height()//2
        self.func = func
        self.active = True
        self.index = 0

    def draw(self, screen:pygame.Surface):
        if self.active:
            super().draw(screen,self.x,self.y)



