from __future__ import print_function
from CGAL.CGAL_Kernel import Point_2
from CGAL import CGAL_Convex_hull_2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQGLViewer import QGLViewer
from dataclasses import dataclass
import random

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.points = []
        self.convex_hull = []

        self.emplace(50)
        self.create_convex_hull()
        
    def emplace(self, points_count):
        for i in range(points_count):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)

            self.points.append(Point_2(x, y))
           
    def draw_points(self):
        glBegin(GL_POINTS)
        glColor3f(0.0, 1.0, 0.0)

        for point in self.points:
            glVertex2f(point.x(), point.y())

        glEnd()
        
    def create_convex_hull(self):
        self.convex_hull.clear()
        CGAL_Convex_hull_2.convex_hull_2(self.points, self.convex_hull)
        
    def draw_convex_hull(self):
        glBegin(GL_LINES)

        cnv_first = self.convex_hull[0]
        cnv_prev = cnv_first

        for cnv_next in self.convex_hull:
            glVertex2f(cnv_prev.x(), cnv_prev.y())
            glVertex2f(cnv_next.x(), cnv_next.y())
            cnv_prev = cnv_next
        
        glVertex2f(cnv_first.x(), cnv_first.y())
        glVertex2f(cnv_prev.x(), cnv_prev.y())
        
        glEnd()
    
    def draw(self):
        glPointSize(4)
        self.draw_points()
        self.draw_convex_hull()

def print_2d_points(points : list[Point_2]):
    for point in points:
        print(f"({point})", end = " ")

    print()
 
L : list[Point_2] = []
L.append(Point_2(0, 0))
L.append(Point_2(1, 0))
L.append(Point_2(0, 1))
L.append(Point_2(1, 1))

L.append(Point_2(0.5, 0.5))
L.append(Point_2(0.25, 0.25))

result = []
CGAL_Convex_hull_2.convex_hull_2(L, result)
print_2d_points(L)
print_2d_points(result)


def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()