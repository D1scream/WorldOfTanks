import json

from server.Projectile import Projectile
from server.Tank import Tank

class ProjectileListModel:
    def __init__(self, projectile_list: list[Projectile]):
        self.projectile_list = projectile_list
        
    def to_json(self):
        return json.dumps([projectile.__dict__ for projectile in self.projectile_list])

    @classmethod
    def from_json(cls, json_str: str, projectile_class):
        data = json.loads(json_str)
        projectiles = []
        for projectile_data in data:
            projectiles.append(projectile_class(**projectile_data))
        return cls(projectiles)

class TanksListModel:
    def __init__(self, tanks_list: list[Tank]):
        self.tanks_list = tanks_list

    def to_json(self):
        return json.dumps([tank.__dict__ for tank in self.tanks_list])

    @classmethod
    def from_json(cls, json_str: str, tank_class):
        data = json.loads(json_str)
        tanks = []
        for tank_data in data:
            tanks.append(tank_class(**tank_data))
        return cls(tanks)
    
class User:
    def __init__(self, nickname):
        self.nickname = nickname
        self.connection = None

    def serialize(self):
        return json.dumps({"nickname": self.nickname})

    @classmethod
    def deserialize(cls, json_data: str):
        data = json.loads(json_data)
        return cls(nickname=data["nickname"])