import matplotlib.pyplot as plt


class LDRfilm(object):

    def save_image(self, img, path):
        plt.figure()
        plt.axis('equal')
        plt.imshow(img, origin='lower')
        plt.axis('off')
        plt.show()
        plt.imsave('images/' + out_name + '.png', multithread.out_img, origin='lower')

    def show_img(self):
