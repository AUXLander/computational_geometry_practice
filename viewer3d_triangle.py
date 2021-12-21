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

@dataclass
class Size:
    x: float
    y: float
    z: float

def frange(x : float, y : float, step : float = 1.0):
    while x < y:
        yield x
        x += step



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

class Figure:
    def draw():
        pass

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
        

class Task(QGLViewer):
    def __init__(self, name : str, descr : str, parent = None):
        QGLViewer.__init__(self, parent)
        
        self.name = name
        self.descr = descr
        
    def resize(self, width, height):
        side = min(width, height)
        glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (e.nativeVirtualKey()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        self.updateGL()

    def draw(self):
        pass

    def run(self):
        print("Task: ", self.name, "\n\n", self.descr, "\n\nPresent result")
            

class CubeTask(Task):
    def __init__(self):
        Task.__init__(self, "Cube", "Draw cube")

        self.cube = Cube(fPoint(0,0,0), 1.0, fColor(0.0, 1.0, 0.0))

    def draw(self):
        self.cube.draw()


class CubesGrid:
    def __init__(self, count : int):
        self.count : int = count
        self.cubes : list[Cube] = []

        self.emplace()

    def emplace(self):
        pass

    def draw(self):
        glDisable(GL_DEPTH_TEST)

        for cube in self.cubes:
            cube.draw()

class CubesOnSphereGrid(CubesGrid, Task):
    size : float
    radius : float
    position : fPoint


    def __init__(self, size : float, position : fPoint, radius : float, count : int):
        Task.__init__(self, "Cube Grid", "Draw cube grid")

        self.radius = radius
        self.position = position
        self.size = size

        CubesGrid.__init__(self, count)

    def emplace(self):
        r = self.radius
        origin = Size(0,0,0)

        self.cubes.clear()
        for idx in range(0, self.count):

            phi = random.uniform(0, 360.0)
            psi = random.uniform(0, 180.0)

            origin.x = r * math.sin(psi) * math.cos(phi)
            origin.y = r * math.sin(psi) * math.sin(phi)

            origin.z = r * math.cos(psi) + random.uniform(.0, .25)

            x = self.position.x + origin.x
            y = self.position.y + origin.y
            z = self.position.z + origin.z
            
            color = fColor(.1, .8, .2)
            self.cubes.append(Cube(fPoint(x,y,z), self.size, color))

    def keyPressEvent(self,e):
        if (e.nativeVirtualKey()==Qt.Key_G):
            self.emplace()
            self.updateGL()

class CubesInSphereGrid(CubesGrid, Task):
    size : float
    radius : float
    position : fPoint


    def __init__(self, size : float, position : fPoint, radius : float, count : int):
        Task.__init__(self, "Cube Grid", "Draw cube grid")

        self.radius = radius
        self.position = position
        self.size = size

        CubesGrid.__init__(self, count)

    def emplace(self):
        r = self.radius
        origin = Size(0,0,0)

        self.cubes.clear()
        for idx in range(0, self.count):

            phi = random.uniform(0, 360.0)
            psi = random.uniform(0, 180.0)

            origin.x = r * math.sin(psi) * math.cos(phi)
            origin.y = r * math.sin(psi) * math.sin(phi)

            origin.z = r * math.cos(psi) * random.uniform(0, 1.0)

            x = self.position.x + origin.x
            y = self.position.y + origin.y
            z = self.position.z + origin.z
            
            color = fColor(.1, .8, .2)
            self.cubes.append(Cube(fPoint(x,y,z), self.size, color))

    def keyPressEvent(self,e):
        if (e.nativeVirtualKey()==Qt.Key_G):
            self.emplace()
            self.updateGL()


class CubesInCubeGrid(CubesGrid, Task):
    grid : Size
    size : float
    position : fPoint


    def __init__(self, width: float, height : float, depth : float, position : fPoint, size : float, count : int):
        Task.__init__(self, "Cube Grid", "Draw cube grid")

        self.size = size / 2
        self.position = position
        self.grid = Size(width, height, depth)

        CubesGrid.__init__(self, count)

    def emplace(self):
        self.cubes.clear()

        for idx in range(0, self.count):
            x = self.position.x + random.uniform(-1.0, 1.0) * self.grid.x
            y = self.position.y + random.uniform(-1.0, 1.0) * self.grid.y
            z = self.position.z + random.uniform(-1.0, 1.0) * self.grid.z

            color = fColor(.1, .8, .2)
            self.cubes.append(Cube(fPoint(x,y,z), self.size, color))
    
    def keyPressEvent(self,e):
        if (e.nativeVirtualKey()==Qt.Key_G):
            self.emplace()
            self.updateGL()

        


class CubesOnGrid(CubesGrid, Task):
    dim  : Size
    size : Size
    step : Size

    def __init__(self, width: float, height : float, depth : float, dimX : int, dimY : int, dimZ : int):
        Task.__init__(self, "Cube Grid", "Draw cube grid")

        self.dim = Size(dimX, dimY, dimZ)
        self.size = Size(width, height, depth)
        self.step = Size(width, height, depth)
        
        self.step.x = self.size.x / float(self.dim.x)
        self.step.y = self.size.y / float(self.dim.y)
        self.step.z = self.size.z / float(self.dim.z)

        CubesGrid.__init__(self, dimX * dimY)

    def emplace(self):
        for z in frange(0, self.size.z, self.step.z):
            for x in frange(0, self.size.x, self.step.x):
                for y in frange(0, self.size.y, self.step.y):
                    point = fPoint(x,y,z)
                    color = fColor(.1, .8, .2)
                    self.cubes.append(Cube(point, .01, color))


 
def main():
    qapp = QApplication([])

    viewers = [
        CubesOnGrid(1, 1, 1, 5, 5, 5),
        CubesInCubeGrid(0.5, 0.5, 0.5, fPoint(0,0,0), 0.01, 350),
        CubesInSphereGrid(0.01, fPoint(0,0,0), 1.0, 900),
        CubesOnSphereGrid(0.01, fPoint(0,0,0), 1.0, 900)
    ]

    viewers[0].show()
    viewers[1].show()
    viewers[2].show()
    viewers[3].show()

    qapp.exec_()

if __name__ == '__main__':
    main()
