import geoplotlib
from geoplotlib.utils import read_csv, BoundingBox, DataAccessObject
from matplotlib import pylab
from pylab import *
from geoplotlib.colors import create_set_cmap
import pyglet
from sklearn.cluster import KMeans
import geoplotlib
from geoplotlib.layers import BaseLayer
from geoplotlib.core import BatchPainter
from geoplotlib.utils import BoundingBox
import numpy as np
import inspect
import matplotlib.pyplot as plt


class KMeansLayer(BaseLayer):

    def __init__(self, data):
        self.data = data
        self.k = 6

    def invalidate(self, proj):
        self.painter = BatchPainter()
        x, y = proj.lonlat_to_screen(self.data['lon'], self.data['lat'])

        k_means = KMeans(n_clusters=self.k)
        k_means.fit(np.vstack([x, y]).T)
        labels = k_means.labels_

        self.cmap = create_set_cmap(set(labels), 'hsv')
        for l in set(labels):
            self.painter.set_color(self.cmap[l])
            self.painter.convexhull(x[labels == l], y[labels == l])
            self.painter.points(x[labels == l], y[labels == l], 2)

    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        ui_manager.info('Use left and right to increase/decrease the number of clusters. k = %d' % self.k)
        self.painter.batch_draw()

    def on_key_release(self, key, modifiers):
        if key == pyglet.window.key.LEFT:
            self.k = max(2, self.k - 1)
            return True
        elif key == pyglet.window.key.RIGHT:
            self.k = self.k + 1
            return True
        return False

    def kvalue(self, data):
        wcss = []

        for i in range(1, 11):
            #x, y = proj.lonlat_to_screen(self.data['lon'], self.data['lat'])
            x = data['lon']
            y = data['lat']
            k_means = KMeans(n_clusters=i)
            k_means.fit(np.vstack([x, y]).T)
            wcss.append(k_means.inertia_)


        plt.plot(range(1, 11), wcss)
        plt.title('The elbow method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')  # within cluster sum of squares
        plt.show()
print(inspect.getfile(geoplotlib.utils.BoundingBox))

BoundingBox.JEJU = BoundingBox(north=33.641010, west=125.993352, south=33.134193, east=127.119451)

data = geoplotlib.utils.read_csv('nodis.csv')
geoplotlib.kde(data, bw=8, cmap='terrain', cut_below=1e-4, scaling='lin')

#kmeans k num
#gildong = KMeansLayer(data)
#gildong.kvalue(data)


geoplotlib.add_layer(KMeansLayer(data))
geoplotlib.set_smoothing(True)
geoplotlib.set_bbox(geoplotlib.utils.BoundingBox.JEJU)
geoplotlib.show()
