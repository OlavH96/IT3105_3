import numpy as np
import kerasnn.KerasNN as KerasNN
import kerasnn.KerasConfig as KerasConfig

if __name__ == '__main__':
    X = np.array([(1, 0), (0, 1), (1, 1)])
    Y = np.array([0, 0, 1])

    config = KerasConfig.KerasConfig(ndim=[2, 3, 1], haf="relu", oaf="relu")
    nn = KerasNN.KerasNN(config)
    model = nn.build()

    #model.fit(X, Y, epochs=10)
    # evaluate the model
    #scores = model.evaluate(X, Y)
    #print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    nn.print()
    print(model.predict([[X[0]]]))
    # model.save("model.h5")
    # keras.models.load_model
