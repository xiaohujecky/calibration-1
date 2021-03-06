import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
from util import *

DEFAULT_PATH = "myplot.png"

def make_axes3d(size):
    figure = pyplot.figure(figsize=(10, 6.5))
    axes3d = figure.add_subplot(111, projection="3d")
    axes3d.autoscale(False)
    axes3d.set_xlabel('X')
    axes3d.set_ylabel('Z')
    axes3d.set_zlabel('Y')
    axes3d.set_xlim3d(-size - 2, size + 2)
    axes3d.set_ylim3d(size + 2, -size - 2)
    axes3d.set_zlim3d(0, 2 * size)
    return axes3d

def plot_points(axes3d, points):
    for i in range(points.shape[1]):
        axes3d.scatter(
            points[0, i] / points[3, i],
            points[2, i] / points[3, i],
            points[1, i] / points[3, i])

def plot_camera(axes3d, camera):
    def quiver(axes3d, p, d, **kwargs):
        axes3d.quiver(
            p[0], p[2], p[1],
            d[0], d[2], d[1],
            pivot = 'tail',
            length = norm(d),
            **kwargs)

    K, R, T = decompose(camera[0])

    # print("K:\n", K)
    # print("R:\n", R)
    # print("T:\n", T)

    quiver(axes3d, T, R[0] * 2, colors=[(1, 0, 0, 1)])
    quiver(axes3d, T, R[1] * 2, colors=[(0, 1, 0, 1)])
    quiver(axes3d, T, R[2] * 2, colors=[(0, 0, 1, 1)])

    return K, R, T

def plot_scene(points, cameras, size = 10, path = "scene.png"):
    axes3d = make_axes3d(size)
    plot_points(axes3d, points)

    if isinstance(cameras, ndarray):
        m = cameras.shape[0] // 3

        for i in range(m):
            camera = (cameras[i * 3 + 0: i * 3 + 3, :], (100, 100))
            plot_camera(axes3d, camera)
    else:
        for i, camera in enumerate(cameras):
            K, R, T = plot_camera(axes3d, camera)

            print("Camera #", i)
            print("K:")
            print(K)
            print("R:")
            print(R)
            print("T:")
            print(T.ravel())
            print("", flush = True)

    pyplot.savefig(path)

def plot_view(points, camera, path = "view.png"):
    points2D = project(points, camera[0])

    pyplot.figure()
    pyplot.plot(
        points2D[0] / points2D[2],
        points2D[1] / points2D[2],
        'o')

    width, height = camera[1]
    w = width / 2
    h = height / 2

    pyplot.axis('scaled')
    pyplot.axis([-w, w, -h, h])
    pyplot.savefig(path)




