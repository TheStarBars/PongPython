import pygame
from pygame import mixer
from pygame.locals import *
import random

pygame.init()
mixer.init()

# Définir la taille de la fenêtre
largeur_fenetre = 1600
hauteur_fenetre = 1000
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

# Charger les fichiers audio
audio_start_path = "audioStart.mp3"
audio_game_path = "audiogame.mp3"
audio_victory_path = "audioVictoire.mp3"

# Charger les images
fond_menu = pygame.image.load("backgroundMenu.jpg").convert()
fond_jeu = pygame.image.load("background.png").convert()
fond_victoire = pygame.image.load("fondVictoire.jpg").convert()
perso1 = pygame.image.load("player1.png").convert_alpha()
perso2 = pygame.image.load("player2.png").convert_alpha()

# Positions initiales des personnages
perso1_x, perso1_y = 100, 500
perso2_x, perso2_y = 1300, 500

# Taille des personnages
perso_width, perso_height = 180, 180

# Vitesse de déplacement
vitesse = 6

class Ball:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.sprites = [pygame.image.load("goompa.png").convert_alpha(),
                        pygame.image.load("pokeball.png").convert_alpha(),
                        pygame.image.load("spaceInvader.png").convert_alpha(),
                        pygame.image.load("Dk.png").convert_alpha(),
                        pygame.image.load("pacMan.png").convert_alpha()]
        self.current_sprite = 0

    def update(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

        # Vérifier les collisions avec les bords de l'écran
        if self.x <= 0:
            self.direction[0] = 1
            self.reset()
            return "Player 2"
        elif self.x >= 1600 - self.sprites[self.current_sprite].get_width():
            self.direction[0] = -1
            self.reset()
            return "Player 1"

        if self.y <= 0 or self.y >= 1000 - self.sprites[self.current_sprite].get_height():
            self.direction[1] *= -1
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)

        # Vérifier les collisions avec les joueurs
        if (perso1_x <= self.x <= perso1_x + perso_width and
                perso1_y <= self.y <= perso1_y + perso_height) or \
                (perso2_x <= self.x <= perso2_x + perso_width and
                 perso2_y <= self.y <= perso2_y + perso_height):
            self.direction[0] *= -1
            self.x += self.speed * self.direction[0]

    def reset(self):
        self.x = 800
        self.y = 600
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def draw(self, fenetre):
        fenetre.blit(self.sprites[self.current_sprite], (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surf = pygame.font.Font(None, font_size).render(text, True, (255, 255, 255))

    def draw(self, fenetre):
        pygame.draw.rect(fenetre, (0, 0, 0), self.rect)
        fenetre.blit(self.text_surf, (self.rect.centerx - self.text_surf.get_width() // 2,
                                      self.rect.centery - self.text_surf.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Création de la balle
ball = Ball(800, 600, 6)

# Création des boutons
jouer_button = Button(800, 300, 200, 50, "Jouer")
quitter_button = Button(800, 400, 200, 50, "Quitter")
pause_button = Button(800, 500, 200, 50, "Pause")

# Gestion du temps
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks() // 1000
temps_ecoule = 0

# Variables de score
score_player1 = 0
score_player2 = 0

# Menu de démarrage
en_menu = True
while en_menu:
    start_sound = mixer.Sound(audio_start_path)
    start_sound.play()
    for event in pygame.event.get():
        if event.type == QUIT:
            start_sound.stop()
            en_menu = False
        elif event.type == MOUSEBUTTONDOWN:
            if jouer_button.is_clicked(pygame.mouse.get_pos()):
                start_sound.stop()
                en_menu = False
            elif quitter_button.is_clicked(pygame.mouse.get_pos()):
                start_sound.stop()
                en_menu = False

    fenetre.blit(fond_menu, (0, 0))

    font_title = pygame.font.Font(None, 72)
    title_text = font_title.render("Pong Retro", True, (255, 255, 255))
    fenetre.blit(title_text, (680, 200))

    jouer_button.draw(fenetre)
    quitter_button.draw(fenetre)
    pygame.display.flip()
    clock.tick(60)

mixer.music.load(audio_game_path)# Boucle principale du jeu
continuer = True
victoire = False
defaite = False
gagnant_nom = None
perdant_nom = None
pause = False
mixer.music.play()

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            mixer.music.stop()
            continuer = False
        elif event.type == MOUSEBUTTONDOWN:
            if defaite:
                if jouer_button.is_clicked(pygame.mouse.get_pos()):
                    defaite = False
                    ball.reset()
                    start_time = pygame.time.get_ticks() // 1000
                    score_player1 = 0
                    score_player2 = 0
                    en_menu = True
                elif quitter_button.is_clicked(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    continuer = False
            elif victoire:
                if jouer_button.is_clicked(pygame.mouse.get_pos()):
                    victoire = False
                    ball.reset()
                    start_time = pygame.time.get_ticks() // 1000
                    score_player1 = 0
                    score_player2 = 0
                    en_menu = True
                elif quitter_button.is_clicked(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    continuer = False
            elif victoire:
                if jouer_button.is_clicked(pygame.mouse.get_pos()):
                    victoire = False
                    ball.reset()
                    start_time = pygame.time.get_ticks() // 1000
                    score_player1 = 0
                    score_player2 = 0
                    en_menu = True
                elif quitter_button.is_clicked(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    continuer = False
            elif not pause and pause_button.is_clicked(pygame.mouse.get_pos()):
                pause = True
            elif pause and pause_button.is_clicked(pygame.mouse.get_pos()):
                pause = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                pause = not pause
            elif event.key == K_m and pause:
                en_menu = True

    if en_menu:
        score_player1 = 0
        score_player2 = 0
        pause = False
        fenetre.blit(fond_menu, (0, 0))
        font_title = pygame.font.Font(None, 72)
        title_text = font_title.render("Pong Retro", True, (255, 255, 255))
        fenetre.blit(title_text, (680, 200))
        jouer_button.draw(fenetre)
        quitter_button.draw(fenetre)
        pygame.display.flip()
        continue

    if not victoire and not defaite and not pause:
        touches = pygame.key.get_pressed()
        if touches[K_UP]:
            perso2_y -= vitesse
        elif touches[K_DOWN]:
            perso2_y += vitesse

        if touches[K_z]:
            perso1_y -= vitesse
        elif touches[K_s]:
            perso1_y += vitesse

        perso1_y = max(0, min(perso1_y, 1000 - perso_height))
        perso2_y = max(0, min(perso2_y, 1000 - perso_height))

        temps_ecoule = (pygame.time.get_ticks() // 1000) - start_time

        gagnant = ball.update()
        if gagnant:
            if gagnant == "Player 1":
                score_player1 += 1
            else:
                score_player2 += 1

            if score_player1 == 10:
                gagnant_nom = "Player 1"
                perdant_nom = "Player 2"
                fond = fond_victoire
                victoire = True
                fin_jeu_sound = mixer.Sound(audio_victory_path)
                fin_jeu_sound.play()
            elif score_player2 == 10:
                gagnant_nom = "Player 2"
                perdant_nom = "Player 1"
                fond = fond_victoire
                victoire = True
                fin_jeu_sound = mixer.Sound(audio_victory_path)
                fin_jeu_sound.play()

    if not victoire and not defaite and not pause:
        fenetre.blit(fond_jeu, (0, 0))
        fenetre.blit(perso1, (perso1_x, perso1_y))
        fenetre.blit(perso2, (perso2_x, perso2_y))
        ball.draw(fenetre)

        font_score = pygame.font.Font(None, 36)
        score_text_player1 = font_score.render(f"Player 1: {score_player1}", True, (255, 255, 255))
        score_text_player2 = font_score.render(f"Player 2: {score_player2}", True, (255, 255, 255))
        fenetre.blit(score_text_player1, (50, 50))
        fenetre.blit(score_text_player2, (1400, 50))

    elif victoire or defaite:
        fenetre.blit(fond, (0, 0))
        if victoire:
            jouer_button.draw(fenetre)
            quitter_button.draw(fenetre)
        elif defaite:
            jouer_button.draw(fenetre)
            quitter_button.draw(fenetre)
        font = pygame.font.Font(None, 36)
        gagnant_texte = font.render(f"{gagnant_nom} gagne !", True, (255, 255, 255))
        fenetre.blit(gagnant_texte, (600, 300))
        perdant_texte = font.render(f"{perdant_nom} a perdu...", True, (255, 255, 255))
        fenetre.blit(perdant_texte, (600, 350))
        if temps_ecoule > 0:
            temps_texte = font.render(f"Temps écoulé: {temps_ecoule} secondes", True, (255, 255, 255))
            fenetre.blit(temps_texte, (600, 400))

        score_text_player1_victoire = font.render(f"Player 1: {score_player1}", True, (255, 255, 255))
        score_text_player2_victoire = font.render(f"Player 2: {score_player2}", True, (255, 255, 255))
        fenetre.blit(score_text_player1_victoire, (600, 450))
        fenetre.blit(score_text_player2_victoire, (600, 500))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
