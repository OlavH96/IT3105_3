class TrainingCase:

    def __init__(self, feature_set: [float], target_distribution: [float], PID: int):
        self.feature_set: [float] = feature_set
        self.target_distribution: [float] = target_distribution
        self.PID: int = PID

    def F(self) -> [float]:
        return self.feature_set + [float(self.PID)]

    def D(self) -> [float]:
        return self.target_distribution
