
import math
import time
from pygame import Vector2
from server.Projectile import Projectile

class Tank():
    def __init__(self, id, rotate=Vector2(0, 1), x=100, y=100):
        self.speed: float = 2
        self.position: Vector2 = Vector2(x,y)
        self.rotate: Vector2 = rotate
        self.rotation_speed = 1
        self.last_shoot_time = 0
        self.id = id
        self.shoot_flag = False
        self.direction = Vector2(0,0)
        self.collision_radius = 10
        
    def shoot(self):
        self.last_shoot_time = max(0,self.last_shoot_time-1)
        if self.shoot_flag:
            self.shoot_flag = False
            if(self.last_shoot_time == 0):
                self.last_shoot_time += 60
                angle = math.atan2(self.rotate.y, self.rotate.x)
                distance = 20
                offset_x = math.cos(angle) * distance
                offset_y = math.sin(angle) * distance

                projectile_position = self.position + Vector2(offset_x, offset_y)

                projectile = Projectile(x=projectile_position.x, y=projectile_position.y, rotate=self.rotate)
                return projectile
        
        return None
        
    def move(self):
        direction = self.direction
        if direction.x: 
            self.rotate = self.rotate.rotate(direction.x * self.rotation_speed) 
        dm = self.rotate * self.speed * direction.y * -1
        self.position += dm
        
    def update(self):
        self.move()
        
        self.last_shoot_time -= 1
        return self.shoot()
    
    @property
    def __dict__(self):
        return {
            "position": {"x": self.position.x, "y": self.position.y},
            "rotate": {"x": self.rotate.x, "y": self.rotate.y},
            "id": self.id,
            "direction": {"x": self.direction.x, "y": self.direction.y}
        }
        
    
        
     