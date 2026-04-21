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
        
