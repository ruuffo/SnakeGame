from typing import List
from PyQt5.QtCore import Qt
import tensorflow as tf
import numpy as np
from src.objects.grid import Grid
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.objects.actorcritic import ActorCritic


class ActorCriticAlgorithm(PathfindingAlgorithm):

    def __init__(self, model: ActorCritic) -> None:
        self.model = model
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.1)
        self.ACTION_MAP = {
            0: Qt.Key_Up,
            1: Qt.Key_Down,
            2: Qt.Key_Left,
            3: Qt.Key_Right,
        }
        self.REVERSE_ACTION_MAP = {v: k for k, v in self.ACTION_MAP.items()}

    def define_new_directions(self, grid: Grid, snake: Snake,
                              rabbits: List[Rabbit]) -> List[Qt.Key]:
        state = self.get_state(grid=grid, snake=snake, rabbits=rabbits)
        state_tensor = tf.convert_to_tensor(state, dtype=tf.float32)
        state_tensor = tf.expand_dims(state_tensor,
                                      0)  # Ajouter une dimension batch

        # Utiliser le modèle Actor-Critic pour prédire la probabilité des actions
        action_probs, _ = self.model(state_tensor)

        # Afficher la forme de la sortie
        print("Shape of action_probs before squeeze:", action_probs.shape)

        # Convertir en tableau numpy et squeezer pour obtenir un tableau 1D
        action_probs = np.squeeze(action_probs.numpy())

        # Afficher la forme après le squeeze
        print("Shape of action_probs after squeeze:", action_probs.shape)

        # Vérifier les valeurs des probabilités
        print("Action probabilities:", action_probs)

        action = np.random.choice(len(action_probs), p=action_probs)

        return [self.ACTION_MAP[action]]

    def get_state(self, grid: Grid, snake: Snake, rabbits: List[Rabbit]):
        state = [
            grid.width, grid.height, self.REVERSE_ACTION_MAP[snake.direction]
        ]
        for bodypart in snake.body:
            state.append(bodypart[0])
            state.append(bodypart[1])
        for rabbit_ in rabbits:
            state.append(rabbit_.x)
            state.append(rabbit_.y)
        return np.array(state)

    def train_step(self, state_tensor, action, reward, next_state_tensor, done):
        with tf.GradientTape() as tape:


            action_probs, value = self.model(state_tensor)
            _, next_value = self.model(next_state_tensor)

            # Calculer l'avantage
            advantage = reward + (1 - done) * next_value - value

            # Calculer la perte Critic (Mean Squared Error)
            critic_loss = advantage**2

            # Calculer la perte Actor (Policy Gradient Loss)
            action_one_hot = tf.one_hot(action, len(action_probs[0]))
            actor_loss = (
                -tf.math.log(tf.reduce_sum(action_probs * action_one_hot)) *
                advantage)

            # Perte totale
            loss = actor_loss + critic_loss

        # Appliquer les gradients pour mettre à jour le modèle
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(
            zip(grads, self.model.trainable_variables))
        return loss
