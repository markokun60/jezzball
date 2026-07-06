import pygame

class Timer:
    timers = []
    def __init__(self, duration, func = None, repeat = None, autostart:bool = False,on_update=None):
        self.duration = duration
        self.start_time = 0
        self.active     = False
        self.func       = func
        self.repeat     = repeat
        self.on_update  = on_update

        if autostart:
            self.activate()
        Timer.timers.append(self)

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:            
            self.activate()

    def get_run_time(self):
        return pygame.time.get_ticks() - self.start_time
    
    def get_time_left(self):
        return self.duration - self.get_run_time()        

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                if self.func and self.start_time != 0:
                    self.func()
                self.deactivate()
                return True
            elif self.on_update is not None:
                self.on_update()
                
        return False