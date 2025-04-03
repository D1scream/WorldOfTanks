import pygame

class Keyset():
    def __init__(self, key_up, key_down, key_left, key_right, key_division):
        self.action_up = key_up
        self.action_down = key_down
        self.action_left = key_left
        self.action_right = key_right
        self.action_division = key_division

class Control:
    def __init__(self, keyset: Keyset):
        self.keyset = keyset

    def get_moving_vector(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)
        if keys[self.keyset.action_up]: direction.y = -1
        if keys[self.keyset.action_down]: direction.y = 1
        if keys[self.keyset.action_left]: direction.x = -1
        if keys[self.keyset.action_right]: direction.x = 1
        return direction
    
    def get_shoot(self, keys):
        return keys[self.keyset.action_division]