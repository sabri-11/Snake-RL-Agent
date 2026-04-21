from snake import *
import random


class Agent:
    def __init__(self):
        self.Q_table = {}
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.8
        self.alpha = 0.1

    def get_action(self, etat_liste):
        etat = tuple(etat_liste)

        if etat not in self.Q_table:
            self.Q_table[etat] = [0.0, 0.0, 0.0]
        
        rand = random.uniform(0, 1)
        if rand <= self.epsilon:
            return random.randint(0, 2)
        else:
            scores = self.Q_table[etat]
            return scores.index(max(scores))
        

    def update_Q_table(self, S_l, action, rwd, new_S_l, go):

        S = tuple(S_l)
        new_S = tuple(new_S_l)
        if S not in self.Q_table:
            self.Q_table[S] = [0.0, 0.0, 0.0]
        if new_S not in self.Q_table:
            self.Q_table[new_S] = [0.0, 0.0, 0.0]

        old_scores = self.Q_table[S]
        old_score = old_scores[action]

        if go:
            max_new_score = 0.0
        else:
            max_new_scores = self.Q_table[new_S] 
            max_new_score = max(max_new_scores)
            
        score_corr = old_score + self.alpha*(rwd + self.gamma*max_new_score - old_score)
        self.Q_table[S][action] = score_corr
        




if __name__ == "__main__":
    agent = Agent()
    jeu = SnakeGame()
    running = True
    action=0
    nb_parties = 10000
        
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
            if partie > 5000:
                fps = 60
                jeu.render()
                jeu.clock.tick(fps)
            

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay
        

        print(f"Partie {partie + 1}/{nb_parties} | Score : {jeu.score} | Taille Mémoire : {len(agent.Q_table)}")

    pygame.quit()

    


