import json
import time
from pygame import Vector2
import pygame

from client.Tank.Control import Control
from client.Tank.Tank import Tank


class ControlledTank(Tank):
    def __init__(self, controller: Control, wsHandler, position=Vector2(0,0), rotate=Vector2(0, 1), direction=None):
        super().__init__(rotate, position=position)
        self.controller: Control = controller
        self.rotation_speed: float = 1
        self.rotate = rotate
        from Client import WSHandler
        self.wsHandler: WSHandler  = wsHandler
        self.last_shoot_time = time.time()
        self.direction = direction

    def move(self):
        direction = self.controller.get_moving_vector()
        new_direction = direction.copy()
        if direction.x: 
            self.rotate = self.rotate.rotate(direction.x * self.rotation_speed)
            direction.x = 0  
        
        direction = self.rotate * self.speed * direction.y * -1
        self.position += direction 
        return new_direction
    
    def check_shoot(self):
        keys = pygame.key.get_pressed()
        if(self.controller.get_shoot(keys)):
            return True
        else:
            return False
        
    async def update(self):
        dir = self.move()
        await self.wsHandler.send_message(json.dumps({'direction': [dir.x, dir.y], 'shoot': self.check_shoot()}))
    
    def draw(self, screen):
        pass
        
        
    
    
        
     