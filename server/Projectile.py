import pygame
from pygame.math import Vector2

class Projectile():
    def __init__(self, rotate=Vector2(0, 0), x=0, y=0):
        self.speed: float = 3
        self.position: Vector2 = Vector2(x,y)
        self.rotate: Vector2 = rotate
        self.collision_radius = 10
    
    def _hit(self, tank):
        pass
    
    def move(self):
        self.position += self.rotate.normalize()*self.speed
        
    def update(self):
        self.move()
        
    def draw(self, screen):
        radius = 3
        pygame.draw.circle(screen, (0, 0, 255), self.position, radius)
        
    @property
    def __dict__(self):
        return {
            "position": {"x": self.position.x, "y": self.position.y},
            "rotate": {"x": self.rotate.x, "y": self.rotate.y},
        }
        
    