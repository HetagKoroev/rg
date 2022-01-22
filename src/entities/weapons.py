import math
import random
from abc import ABC, abstractmethod

import pygame

from entities.projectile import Projectile


class Weapon(ABC):
    def __init__(self):
        self.last_shot = 0

    @abstractmethod
    def shoot(self, user, mouse_coordinates):
        ...

    @staticmethod
    def normalize_vector(vector):
        if vector == [0, 0]:
            return [0, 0]

        pythagoras = math.sqrt(
            vector[0] * vector[0]
            + vector[1] * vector[1]
        )
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
        if current_time - self.last_shot > self.cooldown:
            direction = (mouse_coordinates[0] - user.pos[0], mouse_coordinates[1] - user.pos[1]) \
                if mouse_coordinates != user.pos else (1, 1)
            self.last_shot = current_time
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
        self.weapon_cooldown = 750
        self.spread_arc = 90
        self.projectiles_count = 7

    def shoot(self, user, mouse_coordinates):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (mouse_coordinates[0] - user.pos[0], mouse_coordinates[1] - user.pos[1]) \
                if mouse_coordinates != user.pos else (1, 1)
            self.last_shot = current_time
            arc_difference = self.spread_arc / (self.projectiles_count - 1)
            for proj in range(self.projectiles_count):
                theta = math.radians(arc_difference * proj - self.spread_arc / 2)
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
        self.weapon_cooldown = 100
        self.spread_arc = 25

    def shoot(self, user, mouse_coordinates):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (
                (mouse_coordinates[0] - user.pos[0], mouse_coordinates[1] - user.pos[1])
                if mouse_coordinates != user.pos else (1, 1)
            )
            self.last_shot = current_time
            theta = math.radians(random.random() * self.spread_arc - self.spread_arc / 2)
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
