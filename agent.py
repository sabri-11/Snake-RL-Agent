import snake
import random


class Agent(self):
    def __init__(self):
        self.Q_table = {}
        self.epsilon = 0.1
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
            max = self.Q_table.get(etat)[0]
            index=0
            for v in self.Q_table.values(): 
                for j in range(0, 3):
                    if v[j] > max:
                        v = max
                        index=j

            return index



if __name__ == "__main__":
    q_learn = Agent()
    etat,_,_ = jeu.step(0)
    action = q_learn.get_action(etat)
    print(action)


