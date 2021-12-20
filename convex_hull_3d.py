from __future__ import print_function
import CGAL
from CGAL import CGAL_Polyhedron_3
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Plane_3
from CGAL import CGAL_Convex_hull_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3

from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Vertex_handle

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQGLViewer import QGLViewer
from dataclasses import dataclass
import random

pts : list[Point_3] = []
pts.append(Point_3(0, 0, 0))
pts.append(Point_3(0, 1, 0))
pts.append(Point_3(1, 1, 0))
pts.append(Point_3(1, 0, 0))
pts.append(Point_3(0, 0, 1))
pts.append(Point_3(0, 1, 1))
pts.append(Point_3(1, 1, 1))
pts.append(Point_3(1, 0, 1))

res = Polyhedron_3()

CGAL_Convex_hull_3.convex_hull_3(pts, res)

print("convex hull has ", res.size_of_vertices(), " vertices")
print("is strongly convex: ", CGAL_Convex_hull_3.is_strongly_convex_3(res))


planes : list[Point_3] = []
planes.append(Plane_3(-1, 0, 0, 0))
planes.append(Plane_3(1, 0, 0, -1))
planes.append(Plane_3(0, -1, 0, 0))
planes.append(Plane_3(0, 1, 0, -1))
planes.append(Plane_3(0, 0, -1, 0))
planes.append(Plane_3(0, 0, 1, -1))

res.clear()
CGAL_Convex_hull_3.halfspace_intersection_3(planes, res)
print("halfspace intersection has ", res.size_of_vertices(), " vertices")

class Viewer(QGLViewer):
    def __init__(self, parent = None):
        QGLViewer.__init__(self, parent)
        self.points : list[Point_3] = []
        self.planes : list[Plane_3] = []
        self.convex_hull = Polyhedron_3()
        self.vertices = []
        
        self.create_points()
        self.create_convex_hull()
        #self.create_intersection()

        # self.vertices = [Point_3(1, 0, 0),
        #                  Point_3(1, 1, 0),
        #                  Point_3(1, 0, 1),
        #                  Point_3(0, 0, 0),
        #                  Point_3(0, 1, 1),
        #                  Point_3(0, 1, 0),
        #                  Point_3(0, 0, 1),
        #                  Point_3(1, 1, 1)]

        for vertice in self.vertices:
            print(vertice)

    def create_points(self):
        self.points.append(Point_3(0, 0, 0))
        self.points.append(Point_3(0, 1, 0))
        self.points.append(Point_3(1, 1, 0))
        self.points.append(Point_3(1, 0, 0))
        self.points.append(Point_3(0, 0, 1))
        self.points.append(Point_3(0, 1, 1))
        self.points.append(Point_3(1, 1, 1))
        self.points.append(Point_3(1, 0, 1))

    def create_planes(self):
        self.planes.append(Plane_3(-1, 0, 0, 0))
        self.planes.append(Plane_3(1, 0, 0, -1))
        self.planes.append(Plane_3(0, -1, 0, 0))
        self.planes.append(Plane_3(0, 1, 0, -1))
        self.planes.append(Plane_3(0, 0, -1, 0))
        self.planes.append(Plane_3(0, 0, 1, -1))

    def create_convex_hull(self):
        self.convex_hull.clear()
        CGAL_Convex_hull_3.convex_hull_3(self.points, self.convex_hull)
        self.vertices = self.convex_hull.points()

    def create_intersection(self):
        self.convex_hull.clear()
        CGAL_Convex_hull_3.halfspace_intersection_3(self.planes, self.convex_hull)
        self.vertices = self.convex_hull.vertices()
        
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (e.nativeVirtualKey()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        self.updateGL()


    def draw(self):
        glPointSize(4)
        
        glBegin(GL_POINTS)

        for point in self.points:
            glVertex3f(point.x() * 0.9, point.y() * 0.9, point.z() * 0.9)

        glEnd()

        # glBegin(GL_POLYGON)
        glBegin(GL_LINE_STRIP)

        for vertice in self.vertices:
            glVertex3f(vertice.x(), vertice.y(), vertice.z())

        glEnd()

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()