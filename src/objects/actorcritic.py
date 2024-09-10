from typing import Tuple
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.python.ops.gen_nn_ops import data_format_dim_map


class ActorCritic(tf.keras.Model):
    """Combined actor-critic network."""

    def __init__(
        self,
        num_actions: int,
    ):
        """Initialize."""
        super().__init__()
        # Couches convolutionnelles pour traiter des grilles de tailles variables
        self.conv1 = layers.Conv2D(32,
                                   kernel_size=(3, 3),
                                   activation="relu")
        self.conv2 = layers.Conv2D(64, kernel_size=(3, 3), activation="relu")
        self.conv3 = layers.Conv2D(128, kernel_size=(3, 3), activation="relu")

        # Pooling global pour réduire la sortie de taille variable à un vecteur fixe
        self.global_pool = layers.GlobalAveragePooling2D()

        self.common = layers.Dense(128, activation="relu")
        self.actor = layers.Dense(num_actions, activation="softmax")
        self.critic = layers.Dense(1)

    def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.global_pool(x)
        x = self.common(x)

        return self.actor(x), self.critic(x)
