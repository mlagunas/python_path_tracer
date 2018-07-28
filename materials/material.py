class Material(object):
    def scatter(self, ray_in, hit_record):
        raise NotImplementedError()
