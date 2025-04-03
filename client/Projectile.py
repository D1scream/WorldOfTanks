import pygame
from pygame.math import Vector2

class Projectile():
    def __init__(self, rotate=Vector2(0, 1), position=Vector2(0,0)):
        self.position: Vector2 = position
        self.rotate: Vector2 = rotate
        
    def draw(self, screen):
        radius = 3
        pygame.draw.circle(screen, (0, 0, 255), (self.position.x, self.position.y), radius)
        
    
    