import pygame
import sys

pygame.init()

l, L = (800, 600)
n=5
tailleBoule = (l+L) * 0.4/100
screen = pygame.display.set_mode((l, L))
pygame.display.set_caption("Snake RL")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fond noir
    screen.fill((0, 0, 0))

    # centre de la fenêtre

    # dessiner la boule
    for i in range(0, n-1):
        pygame.draw.circle(screen, (255, 255, 255), (l//2+i*tailleBoule, L//2), tailleBoule)


    # afficher
    pygame.display.flip()

pygame.quit()
sys.exit()