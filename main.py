import random

import pygame

from Enemy import Enemy
from Player import Player

pygame.init()
SCREEN_SIZE = (800, 600)
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


def game_loop():
    done = False
    hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    enemies = pygame.sprite.Group()
    last_enemy = pygame.time.get_ticks()
    score = 0

    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        screen.fill(pygame.Color('white'))

        process_keys(keys, hero)
        process_mouse(mouse, hero)

        # Enemy spawning process
        if last_enemy < current_time - 200 and len(enemies) < 50:
            spawn_side = random.random()
            if spawn_side < 0.25:
                enemies.add(Enemy((0, random.randint(0, SCREEN_SIZE[1]))))
            elif spawn_side < 0.5:
                enemies.add(Enemy((SCREEN_SIZE[0], random.randint(0, SCREEN_SIZE[1]))))
            elif spawn_side < 0.75:
                enemies.add(Enemy((random.randint(0, SCREEN_SIZE[0]), 0)))
            else:
                enemies.add(Enemy((random.randint(0, SCREEN_SIZE[0]), SCREEN_SIZE[1])))
            last_enemy = current_time

        score += move_entities(hero, enemies, clock.get_time() / 17)
        render_entities(hero, enemies)

        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(health_render, (15 + hp * 35, 0))
        score_render = score_font.render(str(score), True, pygame.Color('black'))
        score_rect = score_render.get_rect()
        score_rect.right = SCREEN_SIZE[0] - 20
        score_rect.top = 20
        screen.blit(score_render, score_rect)

        pygame.display.flip()
        clock.tick(120)


done = game_loop()
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if keys[pygame.K_r]:
        done = game_loop()
pygame.quit()
