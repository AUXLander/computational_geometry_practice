from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0 , 0.0)
        glVertex3f(-0.7, 0.0, 0.0)
        glColor3f(0.0, 1.0 , 0.0)
        glVertex3f(0.7, 0.0, 0.0)
        glColor3f(0.0, 0.0 , 1.0)
        glVertex3f(0.0, 1.0, 0.0)
        glEnd()
        pass
 
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
