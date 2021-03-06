import random
import sys

import pygame

from entities.characters.enemies import Enemy
from entities.characters.player import Player
from settings import HEIGHT, SCREEN_SIZE, WIDTH, FPS

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
score_font = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
health_font = pygame.font.Font("fonts/OmnicSans.ttf", 50)
health_render = health_font.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down")

clock = pygame.time.Clock()


def move_entities(hero, enemies, time_delta):
    score = 0
    hero.sprite.move(screen.get_size(), time_delta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.topleft, time_delta)
        enemy.shoot(hero.sprite.rect.topleft)
    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), time_delta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0:
                hero.sprite.alive = False
    for proj in Player.projectiles:
        proj.move(screen.get_size(), time_delta)
        enemies_hit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemies_hit:
            proj.kill()
            score += len(enemies_hit)
    return score


def render_entities(hero, enemies):
    hero.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)


def process_keys(keys, hero):
    if keys[pygame.K_w]:
        hero.sprite.movement_vector[1] -= 1
    if keys[pygame.K_a]:
        hero.sprite.movement_vector[0] -= 1
    if keys[pygame.K_s]:
        hero.sprite.movement_vector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movement_vector[0] += 1
    if keys[pygame.K_1]:
        hero.sprite.equipped_weapon = hero.sprite.available_weapons[0]
    if keys[pygame.K_2]:
        hero.sprite.equipped_weapon = hero.sprite.available_weapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equipped_weapon = hero.sprite.available_weapons[2]


def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())


def run_game():
    hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    enemies = pygame.sprite.Group()
    last_enemy = pygame.time.get_ticks()
    score = 0

    while True:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or not hero.sprite.alive:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color('white'))

        process_keys(keys, hero)
        process_mouse(mouse, hero)

        # Enemy spawning process
        if last_enemy < current_time - 200 and len(enemies) < 50:
            spawn_side = random.random()
            if spawn_side < 0.25:
                enemies.add(Enemy((0, random.randint(0, HEIGHT))))
            elif spawn_side < 0.5:
                enemies.add(Enemy((WIDTH, random.randint(0, HEIGHT))))
            elif spawn_side < 0.75:
                enemies.add(Enemy((random.randint(0, WIDTH), 0)))
            else:
                enemies.add(Enemy((random.randint(0, WIDTH), HEIGHT)))
            last_enemy = current_time

        score += move_entities(hero, enemies, clock.get_time() / 17)
        render_entities(hero, enemies)

        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(health_render, (15 + hp * 35, 0))
        score_render = score_font.render(
            str(score),
            True,
            pygame.Color('black')
        )
        score_rect = score_render.get_rect()
        score_rect.right = WIDTH - 20
        score_rect.top = 20
        screen.blit(score_render, score_rect)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    run_game()
