from keras import optimizers


class KerasConfig:

    def __init__(self, lr=0.01, ndim=None, haf="sigmoid", oaf="sigmoid", optimizer="adam"):
        if ndim is None or len(ndim) < 2: raise Exception("NDIM must be specified and len > 1, ndim is:", ndim)
        self.lr: float = lr
        self.ndim: [int] = ndim
        self.haf: str = self.parseAF(haf)
        self.oaf: str = self.parseAF(oaf)
        self.optimizer: str = self.parseOptimizer(optimizer)

    def parseAF(self, haf):
        options = {
            "sigmoid": "sigmoid",
            "tanh": "tanh",
            "relu": "relu",
            "softmax":"softmax"
        }
        return options[haf] or options["sigmoid"]

    def parseOptimizer(self, optimizer):
        options = {
            "gradientdescent": "sgd",
            "adam": "adam",
            "rmsprop": "rmsprop",
            "adagrad": "adagrad"
        }
        return options[optimizer] or options["gradientdescent"]
