from __future__ import print_function
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
import numpy  as np

class fColor:
    def __init__(self, r : float, g : float, b : float):
        self.r = r
        self.g = g
        self.b = b

    def glColor(self):
        glColor3f(self.r, self.g, self.b)

def clamp(value, minval, maxval):
    return max(minval, min(value, maxval))

class BSplineBase:
    def __init__(self, reference_points, discrete_num = 10, closed = False):
        self.points = reference_points
        self.d_num = int(discrete_num)
        self.closed = closed

        self.point_index = 0
        
        # Генерация коэффициентов для сгенеренных вершин B-сплайна 3 порядка
        self.coefs = []
        for i in range(self.d_num):
            spline_segm_coef = self.calc_spline_coef(i/self.d_num)
            self.coefs.append(spline_segm_coef)

    def calc_spline_coef(self, t):
        return (t, t, t)

    def select_next_point(self):
        self.point_index = (self.point_index + 1) % len(self.points)
        print(self.point_index)

    def keyPressEvent(self,e):
        modifiers = e.modifiers()

        if (e.nativeVirtualKey() == Qt.Key_M):
            self.select_next_point()

        if (e.nativeVirtualKey() == Qt.Key_D):
            [x,y,z] = self.points[self.point_index]
            self.points[self.point_index] = (x + 0.1, y, z)

        if (e.nativeVirtualKey() == Qt.Key_A):
            [x,y,z] = self.points[self.point_index]
            self.points[self.point_index] = (x - 0.1, y, z)

        if (e.nativeVirtualKey() == Qt.Key_W):
            [x,y,z] = self.points[self.point_index]
            self.points[self.point_index] = (x, y + 0.1, z)

        if (e.nativeVirtualKey() == Qt.Key_S):
            [x,y,z] = self.points[self.point_index]
            self.points[self.point_index] = (x, y - 0.1, z)

    def draw_spline_curve(self, color : fColor):
        glPointSize(5)
        
        glColor3f(1.0,0.0,0.0)
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex(point)
        glEnd()

        glColor4f(0.0,0.0,1.0, 0.5)
        glBegin(GL_LINE_LOOP)
        for point in self.points:
            glVertex(point)
        glEnd()

        if not self.closed:     
            segmentsCount = len(self.points) - 1
            glBegin(GL_LINE_STRIP)
        else:
            segmentsCount = len(self.points) #Сегмент между первой и последней вершиной
            glBegin(GL_LINE_LOOP)

        color.glColor()

        for i in range(segmentsCount):
            self.draw_glvertex_for_one_segment_of_spline(i)
        glEnd()

    def draw_glvertex_for_one_segment_of_spline(self, segment_id):
        pNum = len(self.points)
        cNum = len(self.coefs[0])

        f1 = lambda index : (segment_id + index - 1 + pNum) % pNum
        f2 = lambda index : clamp(segment_id + index - 1, 0, pNum - 1)

        f = f2 if not self.closed else f1

        p = [0,0,0,0]
        for idx in range(cNum):
            # Вычисление номеров вершин в списке вершин для построения сплайна
            p[idx] = f(idx)
        
        for i in range(self.d_num):
            x = + self.coefs[i][0] * self.points[p[0]][0] \
                + self.coefs[i][1] * self.points[p[1]][0] \
                + self.coefs[i][2] * self.points[p[2]][0] \
                + self.coefs[i][3] * self.points[p[3]][0] 

            y = + self.coefs[i][0] * self.points[p[0]][1] \
                + self.coefs[i][1] * self.points[p[1]][1] \
                + self.coefs[i][2] * self.points[p[2]][1] \
                + self.coefs[i][3] * self.points[p[3]][1] 

            z = + self.coefs[i][0] * self.points[p[0]][2] \
                + self.coefs[i][1] * self.points[p[1]][2] \
                + self.coefs[i][2] * self.points[p[2]][2] \
                + self.coefs[i][3] * self.points[p[3]][2]
 
            glVertex3f(x, y, z)

class BSpline_3(BSplineBase):
    def __init__(self, reference_points, discrete_num = 10, closed = False):
        BSplineBase.__init__(self, reference_points, discrete_num, closed)
    
    def calc_spline_coef(self, t):
        return (
            (1.0-t) * (1.0-t) * (1.0-t) / 6.0,
            (3.0*t*t*t - 6.0*t*t + 4) / 6.0,
            (-3.0*t*t*t + 3*t*t + 3*t+1) / 6.0,
            t*t*t / 6.0
        )

class BSpline_2(BSplineBase):
    def __init__(self, reference_points, discrete_num = 10, closed = False):
        BSplineBase.__init__(self, reference_points, discrete_num, closed)
    
    def calc_spline_coef(self, t):
        return (
            (1.0 - t)*(1.0 - t) / 2.0,
            (-2*t*t + 2*t + 1) / 2.0,
            t*t /2.0,
            0
        )

# Make spline
points = [(0,0,0),(0,3,0),(1,3,0),(1,1,0),(2,1,0),(3,2,0),(3,0,0)]
spline2 =  BSpline_2(points, 100, True)
spline3 =  BSpline_3(points, 100, True)

green = fColor(0.0, 1.0, 0.0)
yello = fColor(1.0, 1.0, 0.0)

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        
    def draw(self):
        spline2.draw_spline_curve(green)
        spline3.draw_spline_curve(yello)

    def keyPressEvent(self,e):
        spline2.keyPressEvent(e)
        spline3.keyPressEvent(e)
        self.updateGL()
        
  
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
