import pygame
import logging

class DrawHTML:
    def __init__(self,source:str,fnt:pygame.font.Font, color:tuple,images:dict):
        self.source = source.strip().replace('\n','<hr>')
        self.images = images
        self.text = []
        self.font = fnt
        self.line_dx = 3
        self.color = color
        t = self._parse(self.source)
        while t is not None:
            t = self._parse(t)
        #print(self.text)
        self.width, self.height = self.draw(None,(0,0))

    def _parse(self,source):
        i0 = source.find('<')
        if i0 == -1:
            self.text.append(('','',source))
            return None
        i1 = source.find('>',i0)
        if i1 == -1:
            logging.error('Invalid HTML: missing ">"')
        s   = source[:i0]        
        self.text.append(('',s))
        tag = source[i0+1:i1] 
        i0 = tag.find(' ')
        attributes = None
        if i0 > 0:
            tag_name   = tag[:i0].strip()
            parameters = tag[i0:]
            attributes = []
            pa = parameters.split()
            for p in pa:
                i0 = p.find('=')
                if i0 < 0:
                    attributes.append((p,None))
                else:
                    v = p[i0+1:].strip()
                    n = p[:i0].strip()
                    attributes.append((n,v))        
            
            #print(tag_name,attributes)
        else:
            tag_name = tag
        self.text.append(('T',tag_name,attributes))
        return source[i1+1:]

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def draw(self,surface:pygame.Surface,position:tuple):
        pos_start = position
        text_surf = None
        width = 0
        for t in self.text:
            type = t[0]
            if type == 'T':
                tag  = t[1]
                attr = t[2]
                if tag == 'b':
                    self.font.set_bold(True)
                elif tag == '/b':
                    self.font.set_bold(False)
                elif tag == 'i':
                    self.font.set_italic(True)
                elif tag == '/i':
                    self.font.set_italic(False)
                elif tag == 'u':
                    self.font.set_underline(True)
                elif tag == '/u':
                    self.font.set_underline(False)
                elif tag == 'hr':
                    if text_surf is not None:
                        position = (pos_start[0],position[1]+ text_surf.get_height()+self.line_dx) 
                elif tag == 'img':
                    position = self._draw_image(surface,position,attr)
            else:
                s = t[1]
                text_surf = self.font.render(s,1,self.color)
                if surface != None:

                    surface.blit(text_surf,position)
                position = (position[0]+text_surf.get_width(),position[1])
                if width < position[0]  - pos_start[0]:
                    width = position[0] - pos_start[0]
                   
        return width,position[1] - pos_start[1] + text_surf.get_height() if text_surf is not None else 0
    
    def _draw_image(self,surface:pygame.Surface,pos:tuple,attributes:dict):
        img = None
        width  = 0
        height = 0
        for (n,v) in attributes:
            if n == 'src':                
                img = self.images[v]
            elif n == 'width':
                width = int(v)
            elif n == 'height':
                height = int(v)

        if img == None:
            logging.error("image is missing in img tag")
            return pos
        elif surface != None:        
            if width > 0 and height > 0:
                img = pygame.transform.scale(img,(width,height))
            surface.blit(img,pos)
        x = pos[0] + img.get_width()
        return (x,pos[1])


        





