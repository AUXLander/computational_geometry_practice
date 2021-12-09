from __future__ import print_function
from CGAL.CGAL_Kernel import Point_2
from CGAL import CGAL_Convex_hull_2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQGLViewer import QGLViewer
from typing import Collection, Dict
from numpy import NaN, int32, unsignedinteger
from dataclasses import dataclass
import random
import math

class Viewer(QGLViewer):

    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.is_points_generated = False
        self.is_hull_generated = False
        self.points = []
        self.convex_hull = []
        
    def generate_points(self):
        points_count = 33
        for i in range(points_count):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            self.points.append(Point_2(x, y))
            
        self.is_points_generated = True
           
    def draw_points(self):
        if (not self.is_points_generated):
            self.generate_points()
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex2f(float(point.x()), float(point.y()))
        glEnd()
        
    def create_convex_hull(self):
        self.convex_hull.clear()
        CGAL_Convex_hull_2.convex_hull_2(self.points, self.convex_hull)
        self.is_hull_generated = False
        
    def draw_convex_hull(self):
        if (not self.is_hull_generated):
            self.create_convex_hull()
            
        glBegin(GL_LINES)
        for i in range(len(self.convex_hull) - 1):
            glVertex2f(self.convex_hull[i].x(), self.convex_hull[i].y())
            glVertex2f(self.convex_hull[i + 1].x(), self.convex_hull[i + 1].y())
        glVertex2f(self.convex_hull[0].x(), self.convex_hull[0].y())
        glVertex2f(self.convex_hull[len(self.convex_hull) - 1].x(), self.convex_hull[len(self.convex_hull) - 1].y())
        glEnd()
    
    def draw(self):
        glPointSize(4)
        self.draw_points()
        self.draw_convex_hull()
             
                
                                
                
		
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_G):
            self.is_points_generated = False
            self.points.clear()
        self.updateGL()

def print_2d_points(points):

    for point in points:
        print(f"({point})", end = " ")

    print()
 
L = []
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