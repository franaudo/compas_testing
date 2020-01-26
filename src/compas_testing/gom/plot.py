from compas.datastructures import Mesh
from compas.geometry import pointcloud_xy
from compas.geometry import delaunay_from_points_numpy
from compas_plotters import MeshPlotter

points = pointcloud_xy(20, (0, 50))
print(points[0])
faces = delaunay_from_points_numpy(points)
print(faces[0])

delaunay = Mesh.from_vertices_and_faces(points, faces)
#
# plotter = MeshPlotter(delaunay)
# plotter.draw_vertices(radius=0.1)
# plotter.draw_faces()
# plotter.show()
