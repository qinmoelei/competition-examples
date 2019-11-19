from sklearn.cluster import MiniBatchKMeans


class Model:
    def __init__(self):
        self.kmeans = MiniBatchKMeans(n_clusters=3)

    def partial_fit(self, X, y):
        self.kmeans.partial_fit(X=X, y=y)

    def predict(self, X):
        return self.kmeans.predict(X)
