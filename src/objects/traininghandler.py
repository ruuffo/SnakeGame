from typing import List
import numpy as np
import tensorflow as tf
from numpy import int16
from src.objects.actorcritic import ActorCritic


class TrainingHandler:

    def __init__(self) -> None:
        self.num_actions = 4  # Haut, Bas, Gauche, Droite
        self.num_hidden_units = 128
        self.model = ActorCritic(num_actions=self.num_actions,
                                 num_hidden_units=self.num_hidden_units)

    def select_action(self, intial_state: np.ndarray) -> None:
        state = tf.convert_to_tensor(intial_state, dtype=tf.int8)
        state = tf.expand_dims(state, 0)

        action_logits_t, value = self.model(state)

        action = tf.random.categorical(action_logits_t, 1)[0, 0]
        return action
