class Material(object):
    def scatter(self, ray_in):
        raise NotImplementedError()

    @staticmethod
    def reflect(vector, normal):
        raise NotImplementedError()
