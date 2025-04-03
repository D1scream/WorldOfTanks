
import math
from pygame import Vector2
import pygame
from client.Projectile import Projectile


class Tank():
    def __init__(self, rotate=Vector2(0, 0), x=0, y=0):
        self.speed: float = 10
        self.position: Vector2 = Vector2(x,y)
        self.rotate: Vector2 = rotate
    
    def shoot(self):
        # Вычисляем смещение по направлению поворота
        angle = math.atan2(self.rotate.y, self.rotate.x)
        distance = 20
        offset_x = math.cos(angle) * distance
        offset_y = math.sin(angle) * distance

        # Новая позиция снаряда
        projectile_position = self.position + Vector2(offset_x, offset_y)

        # Создаем снаряд
        projectile = Projectile(x=projectile_position.x, y=projectile_position.y, rotate=self.rotate)
        return projectile
        
    def move(self):
        self.position += self.position + self.rotate.normalize()*self.speed
        
    def update(self):
        pass
    
    def draw(self, screen):

        angle = math.degrees(math.atan2(self.rotate.y, self.rotate.x))  

        half_width = 20 // 2
        half_height = 20 // 2
        rect_points = [
            pygame.math.Vector2(-half_width, -half_height),
            pygame.math.Vector2(half_width, -half_height),
            pygame.math.Vector2(half_width, half_height),
            pygame.math.Vector2(-half_width, half_height)
        ]

        rotated_points = [point.rotate(angle) + self.position for point in rect_points]

        pygame.draw.polygon(screen, (0, 233, 0), rotated_points)
        
        line_length = 20 
        direction_end = self.position + self.rotate.normalize() * line_length

        pygame.draw.line(screen, (255, 0, 0), self.position, direction_end, 2) 
        
    
        
     