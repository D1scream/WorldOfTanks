
import math
import time
from pygame import Vector2
from client.Projectile import Projectile

class Tank():
    def __init__(self, rotate=Vector2(0, 0), x=0, y=0):
        self.speed: float = 10
        self.position: Vector2 = Vector2(x,y)
        self.rotate: Vector2 = rotate
        self.last_shoot_time = 0
        
    def shoot(self):
        if(time.time() - self.last_shoot_time == 0):
            self.last_shoot_time +=60
            angle = math.atan2(self.rotate.y, self.rotate.x)
            distance = 20
            offset_x = math.cos(angle) * distance
            offset_y = math.sin(angle) * distance

            projectile_position = self.position + Vector2(offset_x, offset_y)

            projectile = Projectile(x=projectile_position.x, y=projectile_position.y, rotate=self.rotate)
            return projectile
        return None
        
    def move(self):
        direction = self.controller.get_moving_vector()
        if direction.x: 
            self.rotate = self.rotate.rotate(direction.x * self.rotation_speed)
            direction.x = 0  
        
        direction = self.rotate * self.speed * direction.y * -1
        self.position += direction 
        
    def update(self):
        self.move()
        self.last_shoot_time -= 1
        return self.check_shoot()
    
        
     