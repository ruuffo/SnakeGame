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
        # Couches convolutionnelles pour traiter des grilles de tailles variables
        # self.conv1 = layers.Conv2D(32, kernel_size=(7, 7), activation="relu")
        # self.conv2 = layers.Conv2D(64, kernel_size=(5, 5), activation="relu")
        # self.conv3 = layers.Conv2D(128, kernel_size=(3, 3), activation="relu")

        # self.flatten = layers.Flatten()

        self.fully_connected = layers.Dense(128, activation="relu")
        self.actor = layers.Dense(num_actions, activation="softmax")
        self.critic = layers.Dense(1)

    def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        # x = self.conv1(inputs)
        # x = self.conv2(x)
        # x = self.conv3(inputs)
        # x = self.flatten(inputs)
        x = self.fully_connected(inputs)

        return self.actor(x), self.critic(x)
