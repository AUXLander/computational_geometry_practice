from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from PyQGLViewer import QGLViewer
from typing import Collection, Dict
from numpy import NaN

class fPoint:
    def __init__(self, x : float, y  : float, z : float):
        self.x : float = x
        self.y : float = y
        self.z : float = z
    
    def __getitem__(self, key):
        if (key == 0):
            return self.x
        
        if (key == 1):
            return self.y

        if (key == 2):
            return self.z

        return NaN

    def __setitem__(self, key, value):
        if (key == 0):
            self.x = value
            return self.x
        
        if (key == 1):
            self.y = value
            return self.y

        if (key == 2):
            self.z = value
            return self.z

    def glVertex(self):
        glVertex3f(self.x, self.y, self.z)

    def point(self):
        return self



class fColor:
    def __init__(self, r : float, g : float, b : float):
        self.r = r
        self.g = g
        self.b = b

    def glColor(self):
        glColor3f(self.r, self.g, self.b)



class fVertex:
    def __init__(self, point : fPoint, color : fColor):
        self.point : fPoint = point
        self.color : fColor = color

    def glVertex(self):
        self.point.glVertex()
        self.color.glVertex()

    def build(self):
        self.glVertex()



class VertexList:
    def __init__(self, vlist : list[fVertex] = list()):
        self.vlist : list[fVertex] = vlist

    def push(self, vertex):
        self.vlist.append(vertex)

    def empty(self) -> bool:
        return len(self.vlist) == 0



class Cube:
    def __init__(self, position : fPoint, size : float, color : fColor):
        [cx, cy, cz] = [1.0 - 0.5, 1.0 - 0.5, 1.0 - 0.5]

        x = position.x
        y = position.y
        z = position.z

        self.color = color
        self.points : list[fPoint] = [
            fPoint(-cx*size + x, -cy*size + y, -cz*size + z), #0
            fPoint(-cx*size + x, +cy*size + y, -cz*size + z), #1
            fPoint(+cx*size + x, +cy*size + y, -cz*size + z), #2
            fPoint(+cx*size + x, -cy*size + y, -cz*size + z), #3

            fPoint(-cx*size + x, -cy*size + y, +cz*size + z), #4
            fPoint(-cx*size + x, +cy*size + y, +cz*size + z), #5
            fPoint(+cx*size + x, +cy*size + y, +cz*size + z), #6
            fPoint(+cx*size + x, -cy*size + y, +cz*size + z), #7
        ]

    def draw(self):
        self.color.glColor()
        
        glBegin(GL_POLYGON)
        for idx in [0,1,2,3]: #1234
            self.points[idx].glVertex()
        glEnd()
        
        glBegin(GL_POLYGON)
        for idx in [4,5,6,7]: #5678
            self.points[idx].glVertex()
        glEnd()

        glBegin(GL_POLYGON)
        for idx in [0,1,5,4]: #1265
            self.points[idx].glVertex()
        glEnd()

        glBegin(GL_POLYGON)
        for idx in [2,3,7,6]: #3487
            self.points[idx].glVertex()
        glEnd()

        glBegin(GL_POLYGON)
        for idx in [1,2,6,5]: #2376
            self.points[idx].glVertex()
        glEnd()

        glBegin(GL_POLYGON)
        for idx in [0,3,7,4]: #1485
            self.points[idx].glVertex()
        glEnd()
        
        
        
class Task:
    def __init__(self, name : str, descr : str):
        self.name = name
        self.descr = descr

    def main(self):
        pass

    def run(self):
        print("Task: ", self.name, "\n\n", self.descr, "\n\nPresent result")
        self.main()
            
        

class TaskTest(Task):
    def __init__(self, name : str = "", descr : str = ""):
        Task.__init__(self, name, descr)

    def main(self):
        print("Hello, World!")
        


class Viewer(QGLViewer):
    def __init__(self, parent = None):
        QGLViewer.__init__(self, parent)
        self.cube = Cube(fPoint(0,0,0), 1.0, fColor(0.0, 1.0, 0.0))

    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (e.nativeVirtualKey()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        self.updateGL()

    def draw(self):
        # glBegin(GL_TRIANGLES)
        # self.vlist.build()
        # glEnd()

        self.cube.draw()


 
def main():
    qapp = QApplication([])

    viewer = Viewer()
    viewer.show()

    qapp.exec_()

if __name__ == '__main__':
    main()
