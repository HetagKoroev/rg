import math

import pygame

from entities.weapons import MachineGun, Pistol, Shotgun, Weapon


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]
    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()

    def __init__(self, screen_size):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill(pygame.Color('green'))
        self.rect = self.image.get_rect(
            x=screen_size[0] // 2,
            y=screen_size[1] // 2
        )

        self.pos = [screen_size[0] // 2, screen_size[1] // 2]
        self.health = 3
        self.alive = True
        self.movement_vector = [0, 0]
        self.movement_speed = 3
        self.available_weapons: list[Weapon] = [
            Pistol(cooldown=250),
            Shotgun(),
            MachineGun()
        ]
        self.equipped_weapon = self.available_weapons[0]

    def move(self, screen_size, t_delta):
        self.movement_vector = normalize_vector(self.movement_vector)
        new_position = (self.pos[0] + self.movement_vector[0] * self.movement_speed * t_delta,
                        self.pos[1] + self.movement_vector[1] * self.movement_speed * t_delta)
        if new_position[0] < 0:
            self.pos[0] = 0
        elif new_position[0] > screen_size[0] - self.rect.width:
            self.pos[0] = screen_size[0] - self.rect.width
        else:
            self.pos[0] = new_position[0]

        if new_position[1] < 0:
            self.pos[1] = 0
        elif new_position[1] > screen_size[1] - self.rect.height:
            self.pos[1] = screen_size[1] - self.rect.width
        else:
            self.pos[1] = new_position[1]

        self.rect.topleft = self.pos
        self.movement_vector = [0, 0]

    def shoot(self, mouse_coordinates):
        self.equipped_weapon.shoot(self, mouse_coordinates)

    def render(self, surface):
        surface.blit(self.image, self.pos)
