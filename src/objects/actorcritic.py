from typing import Tuple
import tensorflow as tf
from tensorflow.keras import layers


class ActorCritic(tf.keras.Model):
    """Combined actor-critic network."""

    def __init__(
        self,
        num_actions: int,
    ):
        """Initialize."""
        super().__init__()

        self.common = layers.Dense(128, activation="relu")
        self.actor = layers.Dense(num_actions, activation="softmax")
        self.critic = layers.Dense(1)

    def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        x = self.common(inputs)

        return self.actor(x), self.critic(x)
