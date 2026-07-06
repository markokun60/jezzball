import pygame
from os import walk,listdir
from os.path import join
from settings import *
from colors   import *
from themes   import Theme

def load_images(path:str,sizes = None,clr_key = None,scale:float = None):
    images = []
    for img_name in sorted(listdir(path)):
        if img_name[0] == '.': continue
        if not '.png' in img_name: continue
        if clr_key == None:
            img = pygame.image.load(join(path,img_name)).convert_alpha()
        else:
            img = pygame.image.load(join(path,img_name)).convert()
            img.set_colorkey(clr_key)
             
        if sizes != None:
            img = pygame.transform.smoothscale(img,sizes)
        if scale != None:
            img = pygame.transform.scale_by(img,scale)

        #pygame.draw.rect(img,(255,0,0),(0,0,img.get_width(),img.get_height()),1)            
        images.append(img)
    return images

def cell_to_xy(cell:tuple) -> tuple:
    (col, row) = cell
    x = LEFT + col * CELL_SIZE + CELL_SIZE // 2
    y = TOP  + row * CELL_SIZE + CELL_SIZE // 2
    return (x, y)


def swap_color(image:pygame.Surface, old_color:tuple[int,int,int], new_color:tuple[int,int,int]):
    # Create a copy and fill it with the new color
    new_surface = pygame.Surface(image.get_size())
    new_surface.fill(new_color)

    # Make the old color transparent in the original image
    image.set_colorkey(old_color)

    # Blit original onto the new color; only non-old-color parts show
    new_surface.blit(image, (0, 0))
    return new_surface

def draw_message(screen:pygame.Surface,txt:str,x:int,y:int,font:pygame.Font,color:tuple[int,int,int],w_width,w_height):
    messages = txt.split('\n')
    msg_surf_list = []
    width  = 0
    height = 0
    for msg in messages:
        surf = font.render(msg, True, color)    
        w = surf.get_width()
        if w > width: width = w
        height += surf.get_height()
        msg_surf_list.append(surf)

    if y < 0:
        y = w_height // 2 - height // 2

    for m in msg_surf_list:
        xm = x
        if x < 0:
            xm = w_width // 2 - m.get_width() // 2
        screen.blit(m, (xm,y))   
        y += m.get_height()

    return (width,height)  



def draw_h_pregress_bar(screen:pygame.Surface,x:int,y:int,value:int,max_value:int,width:int):
    h = CELL_SIZE2
    p = value /max_value
    w = width * p
    rect = pygame.Rect(x,y,int(w),h)
    pygame.draw.rect(screen,Theme.Current.progress_bars[0],rect)

    x += w
    w = width - w
    rect = pygame.Rect(x,y,int(w),h)
    pygame.draw.rect(screen,Theme.Current.progress_bars[1],rect)

class Messages:
    DX:Final[int] = 5
    def __init__(self):
        self.width      = 0
        self.width_label= 0
        self.surfs      = []
        self.messages   = []

    def add(self,label,value,value1=''):
        self.messages.append((label,value,value1))

    def generate(self,font:pygame.Font,color:tuple[int,int,int]):     
        for (label,value,value1) in self.messages:

            font.set_italic(False)
            surf_label = font.render(label,True,color)

            if value is not None:
                font.set_italic(True)
                surf_value = font.render(value,True,color)
                if value1 == '':
                    surf_value1 = None
                else:
                    surf_value1 = font.render(value1,True,color)
            else:
                surf_value = None

            self.surfs.append((surf_label,surf_value))
            
            w_item = surf_label.get_width()
            if w_item > self.width_label:
                self.width_label= w_item

            if surf_value1 is not None:
                w_item += surf_value1.get_width()
                w_item += Messages.DX
            elif surf_value is not None:
                w_item += surf_value.get_width()
                w_item += Messages.DX
          
            if w_item > self.width:
                self.width= w_item   


    def draw(self,screen:pygame.Surface,x:int,y:int):
        for (sl,sv) in self.surfs:
            screen.blit(sl,(x,y))
            if sv is not None:
                screen.blit(sv,(x+self.width_label+Messages.DX,y))
            y += CELL_SIZE
   