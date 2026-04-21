from snake import SnakeGame
from agent import Agent
import pygame


if __name__ == "__main__":
    agent = Agent()
    jeu = SnakeGame()
    running = True
    action=0
    nb_parties = 1000
        
    for partie in range(nb_parties):
        jeu.reset()
        etat0 = jeu._get_state()
        tours_sans_manger=0
        go = False
        while not go:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            action = agent.get_action(etat0)
            etat, rwd, go = jeu.step(action)
            if rwd == 10:
                tours_sans_manger = 0
            else:
                tours_sans_manger += 1

            if tours_sans_manger > 500:
                go = True
                rwd = -5
            
            agent.update_Q_table(etat0, action, rwd, etat, go)
            etat0 = etat.copy()
            if partie > nb_parties-10:
                fps = 180
                jeu.render()
                jeu.clock.tick(fps)
            

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay
        

        print(f"Partie {partie + 1}/{nb_parties} | Score : {jeu.score} | Taille Mémoire : {len(agent.Q_table)}")

    pygame.quit()