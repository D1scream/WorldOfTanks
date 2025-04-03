from pygame import Vector2
import pygame
from Tank.Control import Control
from Tank.Tank import Tank


class ControlledTank(Tank):
    def __init__(self, controller: Control, rotate=Vector2(0, 1), x=0, y=0):
        super().__init__(rotate, x, y)
        self.controller: Control = controller
        self.rotation_speed: float = 10

    def move(self):
        direction = self.controller.get_moving_vector()
        if direction.x: 
            self.rotate = self.rotate.rotate(direction.x * self.rotation_speed)
            direction.x = 0  
        
        direction = self.rotate * self.speed * direction.y * -1
        self.position += direction 
    
    def check_shoot(self):
        keys = pygame.key.get_pressed()
        if(self.controller.get_shoot(keys)):
            return self.shoot()
        else:
            return None
        
    def update(self):
        self.move()
        return self.check_shoot()
        
    
    
        
     