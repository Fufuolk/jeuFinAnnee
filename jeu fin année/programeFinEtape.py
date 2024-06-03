
from datetime import time
from multiprocessing.connection import wait
from secrets import choice
from pynput.keyboard import Key, Controller
import pygame
import random
import keyboard
# Initialisation de Pygame
pygame.init()

# Paramètres de l'écran
screen_width = 258
screen_height = 344
screen = pygame.display.set_mode((screen_width, screen_height))
roadTexture= pygame.image.load("road.png.jpg")

# colors
black = (0,0,0)
white = (255,255,255)
grey = (200, 200, 200)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

# Paramètres du joueur
player_width = 35
player_height = 50
player_x = 25
player_y = screen_height - player_height - 10
player_velocity = 5

#music
def load_sound(File):
    return pygame.mixer.Sound(File)

#parametre random
policespawnrate = 0
score = 0
music = load_sound("sound.mp3")

#score display
font= pygame.font.Font(None, 36)


# Liste des obstacles
obstacles = []
popolice = []

#gestion des voie de la route
voie1 = (25)
voie2 = (85)
voie3 = (145)
voie4 = (205)

# Fonction pour ajouter un nouvel obstacle
def add_obstacle():
    obstacle_width = 50
    obstacle_height = 50
    obstacle_x = choice(range(25, 206, 60))
    obstacle_y = -obstacle_height
    obstacle_speed = 6  # Vitesse variable
    obstacles.append({"x": obstacle_x, "y": obstacle_y, "speed": obstacle_speed})

#fonction police
def add_police():
    police_width = 50
    police_height = 50
    police_x = choice(range(25, 206, 60))
    police_y = -police_height
    police_speed = 7  # Vitesse variable
    popolice.append({"x": police_x, "y": police_y, "speed": police_speed})

# Fonction pour dessiner le joueur
def draw_player(x, y):
    pygame.draw.rect(screen, yellow, [x, y, player_width, player_height])

# Fonction pour dessiner les obstacles
def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, blue, [obstacle["x"], obstacle["y"], 35, 50])

# dessiner police
def draw_police():
    for police in popolice:
        pygame.draw.rect(screen, white, [police["x"], police["y"], 35, 50 ])
        pygame.draw.rect(screen, blue,[police["x"], police["y"] + 17, 18, 15 ])
        pygame.draw.rect(screen, red, [police["x"] + 17, police["y"] + 17, 18, 15])

# Boucle principale du jeu
running = True
frame_count = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ajout d'un nouvel obstacle toutes les 50 frames
    if frame_count % 50 == 0:
        policespawnrate = random.randint(1,10)
        if policespawnrate <= 9:
            add_obstacle()
            score += 1
        if policespawnrate == 10:
            add_police()
            score += 5
    frame_count += 1


    # Gestion des touches
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT] and player_x != 25:
        if frame_count % 5 == 0:
            player_x -= 60
    if keys[pygame.K_RIGHT] and player_x != 205:
        if frame_count % 5 == 0:
            player_x += 60

    # Mise à jour de la position des obstacles
    for obstacle in obstacles:
        obstacle["y"] += obstacle["speed"]
        # Vérification de la collision
        if player_y < obstacle["y"] + 35 and player_y + player_height > obstacle["y"] and player_x < obstacle["x"] + 50 and player_x + player_width > obstacle["x"]:
            running = False

    # Mise à jour de la position des police
    for police in popolice:
        police["y"] += police["speed"]
        # Vérification de la collision
        if player_y < police["y"] + 35 and player_y + player_height > police["y"] and player_x < police["x"] + 50 and player_x + player_width > police["x"]:
            running = False

    # Suppression des obstacles qui ont quitté l'écran
    i = 0
    while i < len(obstacles):
        if obstacles[i]["y"] >= screen_height:
            obstacles.pop(i)
        else:
            i += 1

    o = 0
    while o < len(popolice):
        if popolice[o]["y"] >= screen_height:
            popolice.pop(o)
        else:
            o += 1

    #score
    text = font.render(f'Score: {score}', True, grey)

#musique
    music.play()

    # Mise à jour de l'écran
    screen.fill(black)
    screen.blit(roadTexture, (0, 0) )
    screen.blit(text, (20, 10))
    draw_player(player_x, player_y)
    draw_obstacles()
    draw_police()
    pygame.display.flip()

    # Contrôle de la fréquence de rafraîchissement
    pygame.time.Clock().tick(60)

pygame.quit()