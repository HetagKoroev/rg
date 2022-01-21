import math

import pygame

from projectile import Projectile


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]
    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class Enemy(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.radius = self.rect.width / 2

        self.pos = list(pos)
        self.movement_vector = [0, 0]
        self.movementSpeed = 1.5
        self.last_shot = pygame.time.get_ticks()
        self.weapon_cooldown = 1500

    def move(self, enemies, player_coordinates, t_delta):
        self.movement_vector = (player_coordinates[0] - self.pos[0],
                                player_coordinates[1] - self.pos[1])
        self.movement_vector = normalize_vector(self.movement_vector)
        self.pos[0] += self.movement_vector[0] * self.movementSpeed * t_delta
        self.pos[1] += self.movement_vector[1] * self.movementSpeed * t_delta

        # Collision test with other enemies
        self.movement_vector = [0, 0]
        for sprite in enemies:
            if sprite is self:
                continue
            if pygame.sprite.collide_circle(self, sprite):
                self.movement_vector[0] += self.pos[0] - sprite.pos[0]
                self.movement_vector[1] += self.pos[1] - sprite.pos[1]

        self.movement_vector = normalize_vector(self.movement_vector)
        self.pos[0] += self.movement_vector[0] * 0.5  # The constant is how far the sprite will be
        self.pos[1] += self.movement_vector[1] * 0.5  # dragged from the sprite it collided with

        self.rect.topleft = self.pos

    def shoot(self, player_coordinates):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (player_coordinates[0] - self.pos[0], player_coordinates[1] - self.pos[1])
            self.last_shot = current_time
            self.projectiles.add(
                Projectile(
                    self.pos,
                    normalize_vector(direction),
                    3,
                    500,
                    (255, 0, 0)
                )
            )

    def render(self, surface):
        surface.blit(self.image, self.pos)
