import pygame
import random


BACKGROUND = (10, 90, 50) # vert / bleu
SERPENT = (255, 255, 255)  # blanc
POMME = (255, 50, 0)   # rouge
TIGE = (0, 255, 0)    # vert
NOIR = (0, 0, 0)

DROITE = 0
HAUT = 1
GAUCHE = 2
BAS = 3

AC = 0
AG = 2
AD = 1


class SnakeGame:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        # self.l = info.current_w
        # self.h = info.current_h

        ### Tests ###
        self.l = 1200
        self.h = 800

        self.xt = self.l*10/100     # x haut gauche limites
        self.yt = self.h*10/100     # y haut gauche limites

        # self.xt = self.l*35/100     # x haut gauche limites
        # self.yt = self.h*35/100  


        self.t_boule = int(1.5*(self.l+self.h) * 0.3/100)
        self.longeur_jeu = self.l*80/100
        self.hauteur_jeu = self.h*80/100

        # self.longeur_jeu = self.l*30/100
        # self.hauteur_jeu = self.h*30/100

        self.nb_cases_x = int(self.longeur_jeu/self.t_boule)
        self.nb_cases_y = int(self.hauteur_jeu/self.t_boule)

        # self.screen = pygame.display.set_mode((self.l, self.h), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.l, self.h))
        pygame.display.set_caption("Snake RL")
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.score = 0
        self.dir = DROITE
        
        self.case_milieu_x = self.nb_cases_x // 2
        self.case_milieu_y = self.nb_cases_y // 2

        self.x_init = self.xt + self.case_milieu_x*self.t_boule
        self.y_init = self.yt + self.case_milieu_y*self.t_boule

        self.serpent = [
            (self.x_init, self.y_init)
        ]
        self.placer_pomme()

    def placer_pomme(self):
        
        x_pomme, y_pomme = self.serpent[0]
        
        while (x_pomme, y_pomme) in self.serpent:
            case_random = (random.randint(0, self.nb_cases_x-1), random.randint(0, self.nb_cases_y-1))     # peut être mettre -2 au lieu de -1 ! 2 au début pour pas avoir boule sur ligne noire

            x_pomme = self.xt + case_random[0]*self.t_boule

            y_pomme = self.yt + case_random[1]*self.t_boule
            self.coord_pomme = (x_pomme, y_pomme)


    def render(self):
        self.screen.fill(BACKGROUND) 
        pygame.draw.rect(self.screen, NOIR, (self.xt, self.yt, self.longeur_jeu, self.hauteur_jeu), self.t_boule)  # limites de 10 à 90% de l'écran
        for b in self.serpent: 
            pygame.draw.circle(self.screen, SERPENT, b, self.t_boule)

        pygame.draw.circle(self.screen, POMME, self.coord_pomme, self.t_boule)

        debut_tige = (self.coord_pomme[0], self.coord_pomme[1]-(self.t_boule/2))
        fin_tige = ((self.coord_pomme[0]+self.t_boule/2, self.coord_pomme[1]-(1.25*self.t_boule)))  

        pygame.draw.line(self.screen, TIGE, debut_tige, fin_tige, self.t_boule//2)
        
        pygame.display.flip()



    def step(self, action):     # actions : AC : continuer, AD : tourner à droite, AG : tourner à gauche
        
        go = False
        reward = 0
        if action == AC:
            pass
        elif action == AD:
            self.dir = (self.dir-1)%4
        elif action == AG:
            self.dir = (self.dir+1)%4
        
        
        x, y = self.serpent[0]
        
        if self.dir == DROITE:
            n_tete = (x+self.t_boule, y)
        elif self.dir == HAUT:
            n_tete = (x, y-self.t_boule)

        elif self.dir == GAUCHE:
            n_tete = (x-self.t_boule, y)

        elif self.dir == BAS:
            n_tete = (x, y+self.t_boule)


        go = self.danger(n_tete)
        
        if go:
            reward = -10
            return self._get_state(), reward, go

        if n_tete == self.coord_pomme:
            reward = 10
            self.score += 1
            self.serpent.insert(0, n_tete)
            self.placer_pomme()
        else:   
            reward = -0.1
            self.serpent.insert(0, n_tete)
            self.serpent.pop()
        
        return self._get_state(), reward, go
        

    def _get_state(self):

        dir_d = self.dir == DROITE
        dir_h = self.dir == HAUT
        dir_g = self.dir == GAUCHE
        dir_b = self.dir == BAS

        p_tete = self.serpent[0]

        pomme_d = p_tete[0] < self.coord_pomme[0]
        pomme_h = p_tete[1] > self.coord_pomme[1]
        pomme_g = p_tete[0] > self.coord_pomme[0]
        pomme_b = p_tete[1] < self.coord_pomme[1]

        pt_d = (p_tete[0] + self.t_boule, p_tete[1])
        pt_h = (p_tete[0], p_tete[1] - self.t_boule)
        pt_g = (p_tete[0] - self.t_boule, p_tete[1])
        pt_b = (p_tete[0], p_tete[1] + self.t_boule)
        
        danger_d = self.danger(pt_d)
        danger_h = self.danger(pt_h)
        danger_g = self.danger(pt_g)
        danger_b = self.danger(pt_b)

        # danger continuer, tourner gauche et tourner droite : 
        danger_c = (dir_d and danger_d) or (dir_h and danger_h) or (dir_g and danger_g) or (dir_b and danger_b)
        danger_tg = (dir_d and danger_h) or (dir_h and danger_g) or (dir_g and danger_b) or (dir_b and danger_d)
        danger_td = (dir_d and danger_b) or (dir_h and danger_d) or (dir_g and danger_h) or (dir_b and danger_g)

        return [danger_c, danger_td, danger_tg, dir_d, dir_h, dir_g, dir_b, pomme_d, pomme_h, pomme_g, pomme_b]
    
    def danger(self, pt):

        # Mur Gauche
        if pt[0] < self.xt:
            return True
        # Mur Droite
        elif pt[0] >= self.xt + (self.nb_cases_x * self.t_boule):
            return True
        # Mur Haut
        elif pt[1] < self.yt:
            return True
        # Mur Bas
        elif pt[1] >= self.yt + (self.nb_cases_y * self.t_boule):
            return True
        # Corps
        elif pt in self.serpent:
            return True
        else:
            return False
        

        




if __name__ == "__main__":
    jeu = SnakeGame()
    
    running = True
    while running:
        # 1. On écoute le système (évite que la fenêtre "plante")
        for event in pygame.event.get():
            # Permet de fermer la fenêtre avec la croix (si on n'est pas en plein écran)
            if event.type == pygame.QUIT:
                running = False
            # ASTUCE : Permet de quitter le plein écran en appuyant sur Échap !
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        # 2. On dessine l'écran en continu
        jeu.render()
        #etat, _, _ = jeu.step(0)
        #print(etat)
        
        # 3. On limite la vitesse (15 images par seconde par exemple)
        jeu.clock.tick(15)

    pygame.quit()