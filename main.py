# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys
import config
import random

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    return screen

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True

def draw_rect(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))

def draw_text(screen, text, color, location, font_name='FreeMono.ttf', font_size=30, bold=False, italic=False):
    font = pygame.font.Font(font_name, font_size)
    font.set_bold(bold)
    font.set_italic(italic)

    text = font.render(text, True, color)
    screen.blit(text, location)

def draw_player(screen, playerlength):
    for player_chunk in playerlength:
        if player_chunk['type'] == 'head':
            part_color = (0, 100, 0)
        else:
            part_color = config.GREEN
        draw_rect(screen, part_color, player_chunk['x']*config.GAME_SCALE + config.GAME_SCALE*1/10, player_chunk['y']*config.GAME_SCALE + config.GAME_SCALE*1/10, config.GAME_SCALE*4/5, config.GAME_SCALE*4/5)

def move_player(playerlength, direction):
    # Move body
    this_chunk = len(playerlength) - 1
    while this_chunk != 0:
        playerlength[this_chunk]['x'] = playerlength[this_chunk-1]['x']
        playerlength[this_chunk]['y'] = playerlength[this_chunk-1]['y']
        this_chunk -= 1
    # Move head
    if direction == 'w':
        playerlength[0]['y'] -= 1
    if direction == 's':
        playerlength[0]['y'] += 1
    if direction == 'a':
        playerlength[0]['x'] -= 1
    if direction == 'd':
        playerlength[0]['x'] += 1
    return playerlength

def main():
    screen = init_game()
    clock = pygame.time.Clock()
    running = True
    player_data = [
        {'type' : 'head', 'x' : 5, 'y' : 4},
        {'type' : 'body', 'x' : 4, 'y' : 4},
        {'type' : 'body', 'x' : 3, 'y' : 4}
    ]
    apple = {'x' : 5, 'y' : 6}
    count_to_keyframe = 0
    movement = 'd'
    game_over = False
    while running:
        running = handle_events()
        screen.fill(config.GREEN)
        draw_rect(screen, config.BLACK, config.GAME_SCALE, config.GAME_SCALE, config.WINDOW_WIDTH - (config.GAME_SCALE*2), config.WINDOW_HEIGHT - (config.GAME_SCALE*2))
        
        if game_over == False:
            # Get player Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                movement = 'w'
            if keys[pygame.K_s]:
                movement = 's'
            if keys[pygame.K_a]:
                movement = 'a'
            if keys[pygame.K_d]:
                movement = 'd'

            count_to_keyframe += 1
            if count_to_keyframe == config.FPS/2:
                count_to_keyframe = 0
                player_data = move_player(player_data, movement)

            # apple
            draw_rect(screen, config.RED, apple['x']*config.GAME_SCALE + config.GAME_SCALE*1/10, apple['y']*config.GAME_SCALE + config.GAME_SCALE*1/10, config.GAME_SCALE*4/5, config.GAME_SCALE*4/5)
            draw_player(screen, player_data)

            # collision
            print(player_data[0])
            if player_data[0]['x'] == apple['x'] and player_data[0]['y'] == apple['y']:
                player_data.append({'type' : 'body', 'x' : 0, 'y' : 0})
                looping = True
                while looping:
                    flag = False
                    apple = {'x' : random.randint(1, 14), 'y' : random.randint(1, 10)}
                    for chunk in player_data:
                        if chunk['x'] == apple['x'] and chunk['y'] == apple['y']:
                            flag = True
                    if flag == False:
                        looping = False



            for chunk in player_data:
                if chunk != player_data[0]:
                    if player_data[0]['x'] == chunk['x'] and player_data[0]['y'] == chunk['y']:
                        game_over = True
            
            if not((0 < player_data[0]['x'] < 15) and (0 < player_data[0]['y'] < 10)):
                game_over = True
        else:
            draw_text(screen, 'Game Over', config.GREEN, [400, 300])
        pygame.display.flip()
        # Limit clock to FPS
        clock.tick(config.FPS)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()