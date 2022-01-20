import math
import random
from abc import abstractmethod, ABC

import pygame

from Projectile import Projectile


class Weapon(ABC):
    def __init__(self):
        self.lastShot = 0

    @abstractmethod
    def shoot(self, user, mouse_coordinates):
        ...

    @staticmethod
    def normalize_vector(vector):
        if vector == [0, 0]:
            return [0, 0]
        pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
        return vector[0] / pythagoras, vector[1] / pythagoras

    @staticmethod
    def rotate_vector(vector, theta):
        return (vector[0] * math.cos(theta)
                - vector[1] * math.sin(theta),
                vector[0] * math.sin(theta)
                + vector[1] * math.cos(theta))


class Pistol(Weapon):
    def __init__(self, cooldown):
        super().__init__()
        self.cooldown = cooldown

    def shoot(self, user, mouse_coordinates):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastShot > self.cooldown:
            direction = (mouse_coordinates[0] - user.pos[0], mouse_coordinates[1] - user.pos[1]) \
                if mouse_coordinates != user.pos else (1, 1)
            self.lastShot = current_time
            user.projectiles.add(
                Projectile(
                    user.pos,
                    super().normalize_vector(direction),
                    5,
                    2000,
                    (0, 0, 255)
                )
            )


class Shotgun(Weapon):
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 750
        self.spreadArc = 90
        self.projectilesCount = 7

    def shoot(self, user, mouse_coordinates):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastShot > self.weaponCooldown:
            direction = (mouse_coordinates[0] - user.pos[0], mouse_coordinates[1] - user.pos[1]) \
                if mouse_coordinates != user.pos else (1, 1)
            self.lastShot = current_time
            arc_difference = self.spreadArc / (self.projectilesCount - 1)
            for proj in range(self.projectilesCount):
                theta = math.radians(arc_difference * proj - self.spreadArc/2)
                proj_dir = super().rotate_vector(direction, theta)
                user.projectiles.add(
                    Projectile(
                        user.pos,
                        super().normalize_vector(proj_dir),
                        7,
                        500,
                        (232, 144, 42)
                    )
                )


class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 100
        self.spreadArc = 25

    def shoot(self, user, mouse_coordinates):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastShot > self.weaponCooldown:
            direction = (mouse_coordinates[0] - user.pos[0], mouse_coordinates[1] - user.pos[1]) \
                if mouse_coordinates != user.pos else (1, 1)
            self.lastShot = current_time
            theta = math.radians(random.random()*self.spreadArc - self.spreadArc/2)
            proj_dir = super().rotate_vector(direction, theta)
            user.projectiles.add(
                Projectile(
                    user.pos,
                    super().normalize_vector(proj_dir),
                    6,
                    1000,
                    (194, 54, 16)
                )
            )
