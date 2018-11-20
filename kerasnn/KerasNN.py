import kerasnn.KerasConfig as KerasConfig
from keras.models import Sequential
from keras.layers import Dense
from keras.models import Model


class KerasNN:

    def __init__(self, keras_config: KerasConfig):
        self.config: KerasConfig = keras_config

    def build(self) -> Model:
        layers: [int] = self.config.ndim
        num_layers = len(layers)
        input_layer_size: int = int(layers[0])

        model = Sequential()
        model.add(Dense(int(layers[1]), input_dim=input_layer_size, activation=self.config.haf))

        for i in range(1, num_layers - 1):
            next_layer_size = int(layers[i + 1])
            model.add(Dense(next_layer_size, activation=self.config.haf if i != (num_layers - 2) else self.config.oaf))

        # model.add(Dense(layers[-1], activation=self.config.oaf))
        model.compile(loss='binary_crossentropy', optimizer=self.config.optimizer   , metrics=['accuracy'])
        self.model = model
        return model

    def print(self):

        print("KerasNN")
        print(self.model.layers)
        for l in self.model.layers:
            print(l.input)
            print(l.output)
            print()
