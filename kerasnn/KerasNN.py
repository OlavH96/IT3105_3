import kerasnn.KerasConfig as KerasConfig
from keras.models import Sequential
from keras.layers import Dense


class KerasNN:

    def __init__(self, keras_config: KerasConfig):
        self.config: KerasConfig = keras_config

    def build(self):
        layers: [int] = self.config.ndim
        num_layers = len(layers)
        input_layer_size: int = layers[0]

        model = Sequential()
        model.add(Dense(layers[1], input_dim=input_layer_size, activation=self.config.haf))

        for i in range(1, num_layers - 1):
            next_layer_size = layers[i + 1]
            print("Adding layer", next_layer_size)
            print()
            model.add(Dense(next_layer_size, activation=self.config.haf if i != (num_layers - 2) else self.config.oaf))

        # model.add(Dense(layers[-1], activation=self.config.oaf))
        model.compile(loss='binary_crossentropy', optimizer=self.config.optimizer, metrics=['accuracy'])

        return model
