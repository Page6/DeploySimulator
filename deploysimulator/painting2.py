#!/usr/bin/env python3

import math as ma
import random as rnd

from PyQt5.QtCore import (QPointF, QPoint, QRect, QRectF, Qt, QSize, pyqtSignal, 
        QTime)
from PyQt5.QtGui import QPainter, QRadialGradient, QFontMetrics, QImage
from PyQt5.QtWidgets import QWidget, QOpenGLWidget
from PyQt5.QtGui import QBrush, QColor, QFont, QLinearGradient, QPen
from PyQt5.QtCore import QTimer

#from Sympy import Point3D

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

class Sensor(object):
    
    def __init__(self, position, radius, velocity):
        
        self.position = position
        self.vel = velocity
        self.radius = radius
        self.color = self.randomColor()
        
    def drawSensor(self):
        
        gl.glPushMatrix()
        gl.glTranslatef(rx[i],ry[i],rz[i])
        gl.glColor3f(colr[i],colg[i],colb[i])
        glut.glutSolidSphere(rad[i],20,20)
        gl.glPopMatrix()
    
    def randomColor(self):
        red = random.randrange(205, 256)
        green = random.randrange(205, 256)
        blue = random.randrange(205, 256)
        alpha = random.randrange(91, 192)

        return QColor(red, green, blue, alpha)

class PWidgetGL3(QOpenGLWidget):
    
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        
        super(PWidgetGL3, self).__init__(parent)

        self.object = 0
        self.xRot = 500
        self.yRot = 500
        self.zRot = 0
        self.coordLength = 3.0
        self.lastPos = QPoint()
        
        self.sensors = []
        self.targets = []

        self.trolltechBlue = QColor.fromCmykF(1.0, 0.40, 0.0, 0.0)
        self.trolltechRed = QColor.fromCmykF(0.0, 1.0, 0.40, 0.0)
        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechBlack = QColor.fromCmykF(0.0, 0.0, 0.0, 1.0)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        
    def getOpenglInfo(self):
        
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
            """.format(gl.glGetString(gl.GL_VENDOR), 
                            gl.glGetString(gl.GL_RENDERER), 
                            gl.glGetString(gl.GL_VERSION), 
                            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION))
        
        return info

    def minimumSizeHint(self):
        
        return QSize(400, 400)

    def sizeHint(self):
        
        return QSize(600, 600)

    def setXRotation(self, angle):
        
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        
        print(self.getOpenglInfo())

        self.setClearColor(self.trolltechBlack.darker())
        self.object = self.makeObject()
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        
        gl.glClear(
                gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        
        # To insure we don't have a zero height
    
        if height == 0:
            height = 1
            
        # Fill the entire graphics window!
        
        gl.glViewport(0, 0, width, height)
        
        # Set the projection matrix... our "view"
        
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Set how we view the world and position our eyeball
        
        glu.gluPerspective(45.0, 1.0, 1.0, 100.0)
    
        # Set the matrix for the object we are drawing
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        # Place the camera position, the direction of view
        # and which axis is up
        
        glu.gluLookAt(self.coordLength, self.coordLength, self.coordLength, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        
    def showEvent(self, event):
        
        pass

    def mousePressEvent(self, event):
        
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        gl.glBegin(gl.GL_LINES)

        self.createCoordinate()

        gl.glEnd()
        gl.glEndList()

        return genList

    def createCoordinate(self):
        
        gl.glColor3ub(255,0,0)
        gl.glVertex3f(-self.coordLength,0.0,0.0)
        gl.glVertex3f(self.coordLength,0.0,0.0)
        gl.glColor3ub(0,255,0)
        gl.glVertex3f(0.0,-self.coordLength,0.0)
        gl.glVertex3f(0.0,self.coordLength,0.0)
        gl.glColor3ub(0,0,255)
        gl.glVertex3f(0.0,0.0,-self.coordLength)
        gl.glVertex3f(0.0,0.0,self.coordLength)
        
    def createSensors(self, number):
        
        for i in range(1,number+1):
            
            position = point3d(self.width()*(0.1 + 0.8*random.random()),
                               self.height()*(0.1 + 0.8*random.random()))
            radius = min(self.width(), self.height())*(0.0125 + 0.0875*random.random())
            velocity = QPointF(self.width()*0.0125*(-0.5 + random.random()),
                               self.height()*0.0125*(-0.5 + random.random()))

            self.bubbles.append(Bubble(position, radius, velocity))

    def normalizeAngle(self, angle):
        
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())
        
    def animate(self):
        
        self.update()
        
    def setAnimating(self, animating):
        
        self.m_animating = animating
        
        if animating:
            self.timer.start(50)
        

class Bubble(object):
    def __init__(self, position, radius, velocity):
        self.position = position
        self.vel = velocity
        self.radius = radius

        self.innerColor = self.randomColor()
        self.outerColor = self.randomColor()
        self.updateBrush()

    def updateBrush(self):
        gradient = QRadialGradient(QPointF(self.radius, self.radius),
                self.radius, QPointF(self.radius*0.5, self.radius*0.5))

        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(0.25, self.innerColor)
        gradient.setColorAt(1, self.outerColor)
        self.brush = QBrush(gradient)

    def drawBubble(self, painter):
        painter.save()
        painter.translate(self.position.x() - self.radius,
                self.position.y() - self.radius)
        painter.setBrush(self.brush)
        painter.drawEllipse(0, 0, int(2*self.radius), int(2*self.radius))
        painter.restore()

    def randomColor(self):
        red = random.randrange(205, 256)
        green = random.randrange(205, 256)
        blue = random.randrange(205, 256)
        alpha = random.randrange(91, 192)

        return QColor(red, green, blue, alpha)

    def move(self, bbox):
        self.position += self.vel
        leftOverflow = self.position.x() - self.radius - bbox.left()
        rightOverflow = self.position.x() + self.radius - bbox.right()
        topOverflow = self.position.y() - self.radius - bbox.top()
        bottomOverflow = self.position.y() + self.radius - bbox.bottom()

        if leftOverflow < 0.0:
            self.position.setX(self.position.x() - 2 * leftOverflow)
            self.vel.setX(-self.vel.x())
        elif rightOverflow > 0.0:
            self.position.setX(self.position.x() - 2 * rightOverflow)
            self.vel.setX(-self.vel.x())

        if topOverflow < 0.0:
            self.position.setY(self.position.y() - 2 * topOverflow)
            self.vel.setY(-self.vel.y())
        elif bottomOverflow > 0.0:
            self.position.setY(self.position.y() - 2 * bottomOverflow)
            self.vel.setY(-self.vel.y())

    def rect(self):
        return QRectF(self.position.x() - self.radius,
                self.position.y() - self.radius, 2 * self.radius,
                2 * self.radius)
                
class PWidgetGL2(QOpenGLWidget):
    def __init__(self, parent=None):
        super(PWidgetGL2, self).__init__(parent)

        midnight = QTime(0, 0, 0)
        random.seed(midnight.secsTo(QTime.currentTime()))

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.image = QImage()
        self.bubbles = []
        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.animationTimer = QTimer()
        self.animationTimer.setSingleShot(False)
        self.animationTimer.timeout.connect(self.animate)
        self.animationTimer.start(25)

        self.setAutoFillBackground(False)
        self.setMinimumSize(400, 400)
        #self.setWindowTitle("Overpainting a Scene")

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle

    def initializeGL(self):
        self.object = self.makeObject()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def paintEvent(self, event):
        self.makeCurrent()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()

        self.setClearColor(self.trolltechPurple.darker())
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_DEPTH_TEST)
        #self.gl.glEnable(self.gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_MULTISAMPLE)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,
                (0.5, 5.0, 7.0, 1.0))

        self.setupViewport(self.width(), self.height())

        gl.glClear(
                gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for bubble in self.bubbles:
            if bubble.rect().intersects(QRectF(event.rect())):
                bubble.drawBubble(painter)

        #self.drawInstructions(painter)
        painter.end()

    def resizeGL(self, width, height):
        self.setupViewport(width, height)

    def showEvent(self, event):
        self.createBubbles(20 - len(self.bubbles))

    def sizeHint(self):
        return QSize(600, 600)

    def makeObject(self):
        list = gl.glGenLists(1)
        gl.glNewList(list, gl.GL_COMPILE)

        gl.glEnable(gl.GL_NORMALIZE)
        gl.glBegin(gl.GL_QUADS)

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,
                (self.trolltechGreen.red()/255.0,
                 self.trolltechGreen.green()/255.0,
                 self.trolltechGreen.blue()/255.0, 1.0))

        """
        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)
        
        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)
            """

        gl.glEnd()

        gl.glEndList()
        return list

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        gl.glNormal3d(0.0, 0.0, -1.0)
        gl.glVertex3d(x1, y1, -0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x3, y3, -0.05)
        gl.glVertex3d(x4, y4, -0.05)

        gl.glNormal3d(0.0, 0.0, 1.0)
        gl.glVertex3d(x4, y4, +0.05)
        gl.glVertex3d(x3, y3, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        gl.glNormal3d((x1 + x2)/2.0, (y1 + y2)/2.0, 0.0)
        gl.glVertex3d(x1, y1, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def createBubbles(self, number):
        for i in range(number):
            position = QPointF(self.width()*(0.1 + 0.8*random.random()),
                               self.height()*(0.1 + 0.8*random.random()))
            radius = min(self.width(), self.height())*(0.0125 + 0.0875*random.random())
            velocity = QPointF(self.width()*0.0125*(-0.5 + random.random()),
                               self.height()*0.0125*(-0.5 + random.random()))

            self.bubbles.append(Bubble(position, radius, velocity))

    def animate(self):
        for bubble in self.bubbles:
            bubble.move(self.rect())

        self.update()

    def setupViewport(self, width, height):
        side = min(width, height)
        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def drawInstructions(self, painter):
        text = "Click and drag with the left mouse button to rotate the Qt " \
                "logo."
        metrics = QFontMetrics(self.font())
        border = max(4, metrics.leading())

        rect = metrics.boundingRect(0, 0, self.width() - 2*border,
                int(self.height()*0.125), Qt.AlignCenter | Qt.TextWordWrap,
                text)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.fillRect(QRect(0, 0, self.width(), rect.height() + 2*border),
                QColor(0, 0, 0, 127))
        painter.setPen(Qt.white)
        painter.fillRect(QRect(0, 0, self.width(), rect.height() + 2*border),
                QColor(0, 0, 0, 127))
        painter.drawText((self.width() - rect.width())/2, border, rect.width(),
                rect.height(), Qt.AlignCenter | Qt.TextWordWrap, text)

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

class PWidgetGL(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(PWidgetGL, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        
    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
            """.format(gl.glGetString(gl.GL_VENDOR), 
                            gl.glGetString(gl.GL_RENDERER), 
                            gl.glGetString(gl.GL_VERSION), 
                            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION))
        
        return info

    def minimumSizeHint(self):
        return QSize(400, 400)

    def sizeHint(self):
        return QSize(600, 600)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        self.setClearColor(self.trolltechPurple.darker())
        self.object = self.makeObject()
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        gl.glClear(
                gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        gl.glBegin(gl.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        gl.glEnd()
        gl.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.setColor(self.trolltechGreen)

        gl.glVertex3d(x1, y1, -0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x3, y3, -0.05)
        gl.glVertex3d(x4, y4, -0.05)

        gl.glVertex3d(x4, y4, +0.05)
        gl.glVertex3d(x3, y3, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        gl.glVertex3d(x1, y1, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())
        
    def setAnimating(self, animating):
        pass

class PWidget2D(QWidget):
    def __init__(self, parent):
        super(PWidget2D, self).__init__(parent)

        self.painting = Painting2D()
        self.elapsed = 0
        self.setFixedSize(800, 600)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()
        
    def setAnimating(self, animating):
        self.m_animating = animating
        
        if animating:
            self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.painting.paint(painter, event, self.elapsed)
        painter.end()

class Painting2D(object):
    def __init__(self):
        gradient = QLinearGradient(QPointF(50, -20), QPointF(80, 20))
        gradient.setColorAt(0.0, Qt.white)
        gradient.setColorAt(1.0, QColor(0xa6, 0xce, 0x39))

        self.background = QBrush(QColor(64, 32, 64))
        self.circleBrush = QBrush(gradient)
        self.circlePen = QPen(Qt.black)
        self.circlePen.setWidth(1)
        self.textPen = QPen(Qt.white)
        self.textFont = QFont()
        self.textFont.setPixelSize(50)
        
    def paint(self, painter, event, elapsed):
        painter.fillRect(event.rect(), self.background)
        painter.translate(400, 300)

        painter.save()
        painter.setBrush(self.circleBrush)
        painter.setPen(self.circlePen)
        painter.rotate(elapsed * 0.030)

        r = elapsed / 1000.0
        n = 30
        for i in range(n):
            painter.rotate(30)
            radius = 0 + 120.0*((i+r)/n)
            circleRadius = 1 + ((i+r)/n)*20
            painter.drawEllipse(QRectF(radius, -circleRadius,
                    circleRadius*2, circleRadius*2))

        painter.restore()

        painter.setPen(self.textPen)
        painter.setFont(self.textFont)
        painter.drawText(QRect(-200, -150, 400, 300), Qt.AlignCenter, "Qt")
