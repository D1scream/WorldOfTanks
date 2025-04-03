import pygame
from pygame.math import Vector2

class Projectile():
    def __init__(self, rotate=Vector2(0, 0), x=0, y=0):
        self.speed: float = 10
        self.position: Vector2 = Vector2(x,y)
        self.rotate: Vector2 = rotate
    
    def _hit(self, tank):
        pass
    
    def move(self):
        self.position += self.rotate.normalize()*self.speed
        
    def update(self):
        self.move()
        
    def draw(self, screen):
        radius = 3
        pygame.draw.circle(screen, (0, 0, 255), self.position, radius)
        
    
    