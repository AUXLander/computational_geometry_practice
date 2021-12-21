from __future__ import print_function
import CGAL
from CGAL import CGAL_Polyhedron_3
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Plane_3
from CGAL import CGAL_Convex_hull_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQGLViewer import QGLViewer
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
        
        self.recreate_points()
        #self.create_intersection()

        for vertice in self.vertices:
            print(vertice)

    def recreate_points(self, points_count = 100):
        self.points.clear()
        for i in range(points_count):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            z = random.uniform(0.0, 1.0)

            self.points.append(Point_3(x, y, z))
        
        self.create_convex_hull()

    def keyPressEvent(self,e):
        if (e.nativeVirtualKey() == Qt.Key_G):
            self.recreate_points()

        self.updateGL()

    def create_convex_hull(self):
        self.convex_hull.clear()
        CGAL_Convex_hull_3.convex_hull_3(self.points, self.convex_hull)
        self.vertices = self.convex_hull.points()

    def create_intersection(self):
        self.convex_hull.clear()
        CGAL_Convex_hull_3.halfspace_intersection_3(self.planes, self.convex_hull)
        self.vertices = self.convex_hull.vertices()

    def draw(self):
        glPointSize(5)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_POINTS)
        glColor3f(1.0, 0.0, 0.0)

        for point in self.points:
            glVertex3f(point.x(), point.y(), point.z())

        glEnd()
       
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 1.0, 0.0)

        for face in self.convex_hull.facets():
            p1 = face.halfedge()
            p2 = p1.next()
            p3 = p2.next()

            glVertex3f(p1.vertex().point().x(), p1.vertex().point().y(), p1.vertex().point().z())
            glVertex3f(p2.vertex().point().x(), p2.vertex().point().y(), p2.vertex().point().z())
            glVertex3f(p3.vertex().point().x(), p3.vertex().point().y(), p3.vertex().point().z())

        glEnd()

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()