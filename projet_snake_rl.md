# Projet Machine Learning — Snake RL Agent

> **Niveau :** 2ème année école d'ingénieur (informatique générale)  
> **Langage :** Python  
> **Durée estimée :** 2 à 3 semaines  
> **Domaine :** Apprentissage par renforcement (Reinforcement Learning)

---

## 🎯 Objectif

L'objectif de ce projet est de créer un **agent intelligent** capable d'apprendre à jouer au jeu **Snake** de façon totalement autonome, sans aucune règle codée explicitement. L'agent apprend uniquement par **essais et erreurs**, en maximisant une récompense numérique au fil des parties.

Le projet est divisé en deux grandes approches :

1. **Q-Learning tabulaire** — méthode classique et fondatrice de l'apprentissage par renforcement
2. **Deep Q-Network (DQN)** — version avancée utilisant un réseau de neurones

---

## 🐍 Le jeu Snake

Snake est un jeu simple où :
- Un serpent se déplace dans une grille de taille fixe
- Il doit manger des pommes qui apparaissent aléatoirement
- Il meurt s'il touche un mur ou son propre corps
- Son score correspond au nombre de pommes mangées

C'est un environnement idéal pour l'apprentissage par renforcement : les règles sont simples, la progression est visible, et la complexité est modulable.

---

## 📚 Bibliothèques utilisées

| Bibliothèque | Rôle dans le projet |
|---|---|
| `pygame` | Affichage graphique du jeu Snake |
| `numpy` | Calculs matriciels, représentation de la Q-table |
| `torch` (PyTorch) | Construction et entraînement du réseau de neurones (DQN) |
| `matplotlib` | Tracé des courbes d'apprentissage et de score |
| `collections` | Implémentation de la Replay Memory (`deque`) |

> ℹ️ L'environnement du jeu est codé **from scratch** sans bibliothèque dédiée comme `gymnasium`. C'est un choix pédagogique pour mieux comprendre les mécanismes internes.

---

## 📋 Structure du projet

```
snake_rl/
│
├── game.py          # Environnement Snake (Pygame)
├── agent_qlearning.py   # Agent Q-Learning tabulaire
├── agent_dqn.py         # Agent Deep Q-Network
├── model.py             # Architecture du réseau de neurones
├── memory.py            # Replay Memory
├── train.py             # Boucle d'entraînement principale
├── plot.py              # Visualisation des résultats
└── README.md
```

---

## 🔧 Partie 1 — Environnement de jeu

**Durée estimée : 2 à 3 jours**

La première étape consiste à implémenter le jeu Snake sous forme d'un **environnement interactif** compatible avec un agent RL.

### Interface à implémenter

La classe `SnakeGame` doit exposer les méthodes suivantes :

- `reset()` → remet le jeu à zéro et retourne l'état initial
- `step(action)` → applique une action et retourne `(état, récompense, game_over)`
- `render()` → affiche le jeu avec Pygame

### Actions possibles

L'agent dispose de **3 actions** à chaque pas de temps :

| Action | Signification |
|---|---|
| `0` | Continuer tout droit |
| `1` | Tourner à droite |
| `2` | Tourner à gauche |

### Système de récompenses

| Événement | Récompense |
|---|---|
| Manger une pomme | `+10` |
| Mourir (mur ou soi-même) | `−10` |
| Chaque pas sans événement | `0` ou petit malus |

---

## 🧠 Partie 2 — Q-Learning tabulaire

**Durée estimée : 2 à 3 jours**

### Principe

Le Q-Learning est un algorithme d'apprentissage par renforcement **sans modèle** (*model-free*). Il maintient une table `Q(s, a)` associant à chaque paire (état, action) une valeur estimée de récompense future.

### Équation de mise à jour (Bellman)

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \cdot \max_{a'} Q(s', a') - Q(s, a) \right]$$

| Symbole | Signification |
|---|---|
| `α` (alpha) | Taux d'apprentissage |
| `γ` (gamma) | Facteur de discount (importance du futur) |
| `r` | Récompense immédiate |
| `s'` | État suivant |

### Représentation de l'état

Pour que la Q-table reste de taille raisonnable, l'état est encodé sous forme d'un **vecteur binaire de 11 dimensions** :

- Danger devant / à droite / à gauche (3 bits)
- Direction actuelle : haut / bas / gauche / droite (4 bits)
- Position relative de la pomme : haut / bas / gauche / droite (4 bits)

### Politique ε-greedy

Pour équilibrer **exploration** et **exploitation** :

- Avec probabilité `ε` : action aléatoire (exploration)
- Avec probabilité `1 − ε` : meilleure action connue (exploitation)

`ε` diminue progressivement au fil de l'entraînement.

---

## 🤖 Partie 3 — Deep Q-Network (DQN)

**Durée estimée : 3 à 5 jours**

### Motivation

La Q-table devient impraticable quand l'espace d'états est grand. Le DQN remplace la table par un **réseau de neurones** qui approxime la fonction `Q(s, a)`.

### Architecture du réseau

```
Input Layer  (11 neurones  — vecteur d'état)
     ↓
Hidden Layer (256 neurones — activation ReLU)
     ↓
Hidden Layer (256 neurones — activation ReLU)
     ↓
Output Layer (3 neurones   — une valeur Q par action)
```

### Techniques de stabilisation

Deux mécanismes essentiels rendent l'entraînement du DQN stable :

**1. Replay Memory**  
Les transitions `(s, a, r, s', done)` sont stockées dans un buffer. À chaque étape, un mini-batch est tiré **aléatoirement** pour briser les corrélations temporelles.

**2. Target Network**  
Un second réseau (identique mais mis à jour moins fréquemment) est utilisé pour calculer les cibles. Cela évite que la cible change à chaque pas et déstabilise l'apprentissage.

### Paramètres d'entraînement conseillés

| Hyperparamètre | Valeur suggérée |
|---|---|
| Taille du buffer | 100 000 |
| Taille du batch | 1 000 |
| Taux d'apprentissage | `0.001` |
| Gamma (discount) | `0.9` |
| Fréquence mise à jour target | tous les 100 pas |

---

## 📊 Partie 4 — Analyse et rapport

**Durée estimée : 1 à 2 jours**

- Comparer les courbes d'apprentissage du Q-Learning et du DQN
- Analyser l'impact des hyperparamètres (α, γ, ε, taille du réseau)
- Rédiger un court rapport expliquant les choix techniques et les résultats

---

## ✅ Critères de réussite

| Objectif | Indicateur |
|---|---|
| Agent Q-Learning opérationnel | Score moyen > 5 après entraînement |
| Agent DQN opérationnel | Score moyen > 20 après entraînement |
| Compréhension | Savoir expliquer pourquoi le DQN surpasse le Q-Learning |
| Analyse | Courbes de convergence commentées |

---

## 📖 Ressources recommandées

- [Cours de David Silver sur le RL (DeepMind)](https://www.davidsilver.uk/teaching/) — référence académique
- [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) — article original DQN (DeepMind, 2013)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [Pygame Documentation](https://www.pygame.org/docs/)
- Chaîne YouTube **Patrick Loeber** (*Python Engineer*) — tutoriel Snake RL très accessible

---

*Projet réalisé dans le cadre d'un apprentissage personnel du Machine Learning — Apprentissage par Renforcement.*
