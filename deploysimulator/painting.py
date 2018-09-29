#!/usr/bin/env python3

import math as ma
import random as rnd
import numpy as np

from PyQt5.QtCore import (QPointF, QPoint, QRect, QRectF, Qt, QSize, pyqtSignal, 
        QTime)
from PyQt5.QtGui import QPainter, QRadialGradient, QFontMetrics, QImage
from PyQt5.QtWidgets import QWidget, QOpenGLWidget
from PyQt5.QtGui import QBrush, QColor, QFont, QLinearGradient, QPen
from PyQt5.QtCore import QTimer

import OpenGL.GL as gl
import OpenGL.GLU as glu

class Point3f:
    
    x = 0.0
    y = 0.0
    z = 0.0
    
    def __init__(self,x,y,z):
        
        self.x = x
        self.y = y
        self.z = z

class PWidgetGL(QOpenGLWidget):
    
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        
        super(PWidgetGL, self).__init__(parent)

        self.object = 0
        self.xRot = 500
        self.yRot = 500
        self.zRot = 0
        self.coordLength = 3.0
        self.lastPos = QPoint()
        
        self.rn = 0.0
        self.Trn = 0.0

        self.trolltechBlue = QColor.fromCmykF(1.0, 0.40, 0.0, 0.0)
        self.trolltechRed = QColor.fromCmykF(0.0, 1.0, 0.40, 0.0)
        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechBlack = QColor.fromCmykF(0.0, 0.0, 0.0, 1.0)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.inited = False
        
        self.rcount = 0
        self.tcount = 0
        self.vcount = 0.0
        
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
    
        #self.object = self.makeObject()

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
        
    def initialization(self, radDown, radUp, angDown, angUp, num, TradDown, TradUp, Tnum):
        
        # initialize values
        
        self.rn = num
        self.Trn = Tnum
        self.dt = 0.1
        
        self.rcount = 0
        self.tcount = 0
        self.vcount = 0.0
        
        self.rad = np.zeros(self.rn+1, float)
        self.Trad = np.zeros(self.Trn+1, float)
        
        self.ang = np.zeros(self.rn+1, int)
        
        self.colr = np.zeros(self.rn+1, float)
        self.colg = np.zeros(self.rn+1, float)
        self.colb = np.zeros(self.rn+1, float)
        self.Tcolr = np.zeros(self.Trn+1, float)
        self.Tcolg = np.zeros(self.Trn+1, float)
        self.Tcolb = np.zeros(self.Trn+1, float)
        
        self.rx = np.zeros(self.rn+1, float)
        self.ry = np.zeros(self.rn+1, float)
        self.rz = np.zeros(self.rn+1, float)
        self.Trx = np.zeros(self.Trn+1, float)
        self.Try = np.zeros(self.Trn+1, float)
        self.Trz = np.zeros(self.Trn+1, float)
        
        self.vx = np.zeros(self.rn+1, float)
        self.vy = np.zeros(self.rn+1, float)
        self.vz = np.zeros(self.rn+1, float)
        self.Tvx = np.zeros(self.Trn+1, float)
        self.Tvy = np.zeros(self.Trn+1, float)
        self.Tvz = np.zeros(self.Trn+1, float)
        
        self.dx  = np.zeros(self.rn+1, float)
        self.dy = np.zeros(self.rn+1, float)
        self.dz = np.zeros(self.rn+1, float)
        
        # create random sets
        
        for i in range(1,self.rn+1):
            
            self.rad[i] = rnd.uniform(radDown,radUp)
            #print('rad[%.0f]=%f' %(i,self.rad[i]))
            
            self.ang[i] = rnd.randint(angDown,angUp)
            
            self.colr[i] = abs(ma.sin(self.rad[i]*100))
            self.colg[i] = abs(ma.cos(self.rad[i]*100))
            self.colb[i] = ma.sqrt(abs(ma.sin(self.rad[i]*100)*ma.cos(self.rad[i]*100)))
            #print('colr[%.0f]=%f,colg[%.0f]=%f,colb[%.0f]=%f' %(i,self.colr[i],i,self.colg[i],i,self.colb[i]))
            
            self.rx[i] = rnd.uniform(-self.coordLength,self.coordLength)
            self.ry[i] = rnd.uniform(-self.coordLength,self.coordLength)
            self.rz[i] = rnd.uniform(-self.coordLength,self.coordLength)
            #self.rx[i] = rnd.uniform(-0.9,-1.2)
            #self.ry[i] = rnd.uniform(-0.9,-1.2)
            #self.rz[i] = rnd.uniform(-0.9,-1.2)
            #print('rx[%.0f]=%f,ry[%.0f]=%f,rz[%.0f]=%f' %(i,self.rx[i],i,self.ry[i],i,self.rz[i]))
            
            self.vx[i] = 0.0
            self.vy[i] = 0.0
            self.vz[i] = 0.0
            
            self.dx[i] = 0.0#ma.sin(5.0*rnd.random() + 1.0)*100#math.sin(rnd.uniform(0.5,2.0))
            self.dy[i] = 0.0#ma.cos(5.0*rnd.random() + 1.0)*100
            self.dz[i] = 0.0#ma.sin(5.0*rnd.random() + 1.0) * ma.cos(5.0*rnd.random() + 1.0)*100
            #print('dx[%.0f]=%f,dy[%.0f]=%f,dz[%.0f]=%f' %(i,self.dx[i],i,self.dy[i],i,self.dz[i]))
            
        for i in range(1,self.Trn+1):
            
            self.Trad[i] = rnd.uniform(TradDown,TradUp)
            #print('Trad[%.0f]=%f' %(i,self.Trad[i]))
            self.Tcolr[i] = 0.0
            self.Tcolg[i] = 0.0
            self.Tcolb[i] = 0.0

            self.Trx[i] = rnd.uniform(-1.0,1.0)
            self.Try[i] = rnd.uniform(-1.0,1.0)
            self.Trz[i] = rnd.uniform(-1.0,1.0)
            #print('Trx[%.0f]=%f,Try[%.0f]=%f,Trz[%.0f]=%f\n' %(i,self.Trx[i],i,self.Try[i],i,self.Trz[i]))
            
            self.Tvx[i] = 0.0
            self.Tvy[i] = 0.0
            self.Tvz[i] = 0.0
        
        self.animate()
        self.inited = True
        
    def showEvent(self, event):
        
        #self.initialization(0.01, 0.25, 30, 90, 2, 0.5, 1.0, 1)
        
        #print('showEvent')
        pass
    
    def paintEvent(self, event):
        
        self.makeCurrent()
        
        # Set the color of background
        
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        
        # Enable depth testing for true 3D effects
        
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        # Add lighting and shading effects
        
        gl.glShadeModel(gl.GL_SMOOTH)
        lightdiffuse = [1.0, 1.0, 1.0, 1.0]
        lightposition = [1.0, 1.0, 1.0, 0.0]
        lightambient = [0.0, 0.0, 0.0, 1.0]
        lightspecular = [1.0, 1.0, 1.0, 1.0]
        
        # Turn on the light
        
        gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, lightdiffuse)
        gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, lightposition)
        gl.glLightfv(gl.GL_LIGHT1, gl.GL_AMBIENT, lightambient)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, lightdiffuse)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, lightspecular)
        #gl.glEnable(gl.GL_LIGHT1)
        #gl.glEnable(gl.GL_LIGHTING)
        #gl.glEnable(gl.GL_COLOR_MATERIAL)
        
        gl.glClear(
                gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        
        if self.inited:
            gl.glCallList(self.object)
        
        #print('paintEvent')

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
        
        genList = gl.glGenLists(4+self.rn+self.Trn)  # the number of objects 
        
        gl.glNewList(genList, gl.GL_COMPILE)

        # object : the coordiante
        self.drawCoordinate()
        
        # object : targets
        
        for i in range(1,self.Trn+1):
            
            gl.glPushMatrix()
            gl.glTranslatef(self.Trx[i],self.Try[i],self.Trz[i])
            #print('Trx[%.0f]=%f,Trx[%.0f]=%f,Trx[%.0f]=%f\n' %(i,self.Trx[i],i,self.Trx[i],i,self.Trx[i]))
            gl.glColor3f(self.Tcolr[i],self.Tcolg[i],self.Tcolb[i])
            self.drawTarget(Point3f(self.Trx[i],self.Try[i],self.Trz[i]),self.Trad[i])
            gl.glPopMatrix()
        
            # object : sensors
            
            for j in range(1,self.rn+1):
                
                gl.glPushMatrix()
                gl.glColor3f(self.colr[j],self.colg[j],self.colb[j])
                self.drawSensor(Point3f(self.rx[j],self.ry[j],self.rz[j]),
                                Point3f(self.Trx[i],self.Try[i],self.Trz[i]),
                                self.rad[j],self.ang[j])
                gl.glPopMatrix()
        
        gl.glEndList()

        return genList

    def drawCoordinate(self):
        
        gl.glBegin(gl.GL_LINES)
        gl.glColor3ub(255,0,0)
        gl.glVertex3f(-self.coordLength,0.0,0.0)
        gl.glVertex3f(self.coordLength,0.0,0.0)
        gl.glColor3ub(0,255,0)
        gl.glVertex3f(0.0,-self.coordLength,0.0)
        gl.glVertex3f(0.0,self.coordLength,0.0)
        gl.glColor3ub(0,0,255)
        gl.glVertex3f(0.0,0.0,-self.coordLength)
        gl.glVertex3f(0.0,0.0,self.coordLength)
        gl.glEnd()
        
    def drawSensor(self,o,t,rad,theta):
        
        R = (3.0 * (theta/180.0*ma.pi) * rad) / (4.0 * ma.sin((theta/2.0)/180.0*ma.pi))
        r = R * ma.sin((theta/2.0)/180.0*ma.pi)
        h = R * ma.cos((theta/2.0)/180.0*ma.pi)
        #print('R=%.4f,r=%.4f,h=%.4f' %(R,r,h))
        
        #print('ox=%.4f,oy=%.4f,oz=%.4f' %(o.x,o.y,o.z))
        #print('tx=%.4f,ty=%.4f,tz=%.4f' %(t.x,t.y,t.z))
        x = o.x - t.x
        y = o.y - t.y
        z = o.z - t.z
        
        Dxy = ma.sqrt(x**2 + y**2)
        Dxz = ma.sqrt(x**2 + z**2)
        Dyz = ma.sqrt(y**2 + z**2)
        
        dx1 = o.x * (Dxy-h) / (Dxy+0.00001) + t.x * h / Dxy
        dy1 = o.y * (Dxy-h) / (Dxy+0.00001) + t.y * h / Dxy
        dx2 = o.x * (Dxz-h) / (Dxz+0.00001) + t.x * h / Dxz
        dz1 = o.z * (Dxz-h) / (Dxz+0.00001) + t.z * h / Dxz
        dy2 = o.y * (Dyz-h) / (Dyz+0.00001) + t.y * h / Dyz
        dz2 = o.z * (Dyz-h) / (Dyz+0.00001) + t.z * h / Dyz
        dx = (dx1+dx2) / 2.0
        dy = (dy1+dy2) / 2.0
        dz = (dz1+dz2) / 2.0
        #print('dx1=%.4f,dy1=%.4f,dz1=%.4f' %(dx1,dy1,dz1))
        #print('dx2=%.4f,dy2=%.4f,dz2=%.4f' %(dx2,dy2,dz2))
        self.drawCone(Point3f(dx,dy,dz),
                      Point3f(o.x,o.y,o.z),
                      r,20)
        
    def drawCone(self,c,v,r,n):
        
        c0 = np.array([c.x,c.y,c.z])
        v0 = np.array([v.x,v.y,v.z])
        
        # calculate the distance for the height
        
        h = ma.sqrt(np.sum((c0-v0) * (c0-v0)))
        alpha = ma.acos(np.dot(np.array([0.0,0.0,1.0]),v0-c0) / (h+0.00001))
        
        if v0[0]-c0[0] == 0 and v0[1]-c0[1] == 0:
            dx = 0
            dy = 0
        elif v0[0]-c0[0] == 0:
            dx = -(v0[1]-c0[1])
            dy = 0
        elif v0[1]-c0[1] == 0:
            dx = 0
            dy = v0[0]-c0[0]
        else:
            k = (v0[1]-c0[1]) / (v0[0]-c0[0])
            l = -1.0/k
            
            if l > 0.0:
                dx = v0[0] - c0[0]
            else:
                dx = -(v0[0] - c0[0])
            
            dy = dx * l
        
        zdir = np.array([dx+c0[0], dy+c0[1], c0[2]])
        t = np.linspace(0, ma.pi*2, n)
        tx = t.copy()
        ty = t.copy()
        
        for i in range(0,n):
            tx[i] = r * ma.cos(t[i]) + c0[0]
            ty[i] = r * ma.sin(t[i]) + c0[1]
        #print(tx)
        
        vert = np.array([tx-c0[0],ty-c0[1],c0[2]*np.linspace(1.0,1.0,n)-c0[2]]).T

        if zdir[0] != c0[0] and zdir[1] != c0[1]:
            vert = self.rot3d(vert, np.array([0.0,0.0,0.0]), zdir-c0, alpha)
        vert = vert + c0
        #print(vert)
        
        # reference points
        
        gl.glBegin(gl.GL_LINES)
        #gl.glVertex3f(c0[0],c0[1],c0[2])
        #gl.glVertex3f(v0[0],v0[1],v0[2])
        #gl.glVertex3f(c0[0],c0[1],c0[2])
        #gl.glVertex3f(zdir[0],zdir[1],zdir[2])
        #gl.glVertex3f(v0[0],v0[1],v0[2])
        #gl.glVertex3f(self.Trx[1],self.Try[1],self.Trz[1])

        for i in range(0,n):
            gl.glVertex3f(v0[0],v0[1],v0[2])
            gl.glVertex3f(vert[i][0], vert[i][1], vert[i][2])
        gl.glEnd()
        
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(0,n):
            gl.glVertex3f(vert[i][0], vert[i][1], vert[i][2])
        gl.glEnd()
        
    def rot3d(self,p,origin,dirct,theta):
        
        T_dirct = np.array([dirct]).T
        dirct = T_dirct / np.linalg.norm(dirct)
        
        A_hat = np.dot(dirct, dirct.T)
        
        A_star = np.array([[0.0,-dirct[2],dirct[1]],
                           [dirct[2],0.0,-dirct[0]],
                           [-dirct[1],dirct[0],0.0]])
        I = np.eye(3)
        M = A_hat + np.cos(theta) * (I - A_hat) + np.sin(theta) * A_star
        origin = np.tile(origin,(np.size(p,0),1))
        pr = np.dot(p-origin,M.T) + origin
        
        return pr
        
    def drawTarget(self,t,r):
        
        rc = r
        
        p1 = Point3f(rc,rc,rc)
        p2 = Point3f(rc,rc,-rc)
        p3 = Point3f(rc,-rc,-rc)
        p4 = Point3f(rc,-rc,rc)
        p5 = Point3f(-rc,rc,rc)
        p6 = Point3f(-rc,rc,-rc)
        p7 = Point3f(-rc,-rc,-rc)
        p8 = Point3f(-rc,-rc,rc)
        
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex3f(p1.x,p1.y,p1.z)
        gl.glVertex3f(p2.x,p2.y,p2.z)
        gl.glVertex3f(p3.x,p3.y,p3.z)
        gl.glVertex3f(p4.x,p4.y,p4.z)
        gl.glEnd()
        
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex3f(p5.x,p5.y,p5.z)
        gl.glVertex3f(p6.x,p6.y,p6.z)
        gl.glVertex3f(p7.x,p7.y,p7.z)
        gl.glVertex3f(p8.x,p8.y,p8.z)
        gl.glEnd()
        
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(p1.x,p1.y,p1.z)
        gl.glVertex3f(p5.x,p5.y,p5.z)
        gl.glVertex3f(p2.x,p2.y,p2.z)
        gl.glVertex3f(p6.x,p6.y,p6.z)
        gl.glVertex3f(p3.x,p3.y,p3.z)
        gl.glVertex3f(p7.x,p7.y,p7.z)
        gl.glVertex3f(p4.x,p4.y,p4.z)
        gl.glVertex3f(p8.x,p8.y,p8.z)
        gl.glEnd()
        
        circle = np.linspace(0, ma.pi*2, 50)
        R = r * ma.sqrt(2)
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(1,50):
            gl.glVertex3f(R*ma.cos(circle[i]), 0.0, R*ma.sin(circle[i]))
        gl.glEnd()
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(1,50):
            gl.glVertex3f(0.0, R*ma.cos(circle[i]), R*ma.sin(circle[i]))
        gl.glEnd()
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(1,50):
            gl.glVertex3f(R*ma.cos(circle[i]), R*ma.sin(circle[i]), 0.0)
        gl.glEnd()
        
    def moveSensors(self):
        
        self.tcount += 1
        if self.tcount % 10 == 0:
            pass
            #print('coverage = %.4f' %(self.rcount * 1.0 / self.rn))
            #print('%.4f' %(self.rcount * 1.0 / self.rn))
            print('%.4f' %(self.vcount / self.rn))
            #print('coverage = %f / %f' %(self.rcount,self.rn))
        
        #print('rx[1]=%f' %(self.rx[1]))
        self.rcount = 0
        for i in range(1,self.rn+1):
            
            self.rx[i] += self.vx[i] * self.dt
            self.ry[i] += self.vy[i] * self.dt
            self.rz[i] += self.vz[i] * self.dt
            #print('rx[%.0f]=%f,ry[%.0f]=%f,rz[%.0f]=%f' %(i,self.rx[i],i,self.ry[i],i,self.rz[i]))
            #print('vx[%.0f]=%f,vy[%.0f]=%f,vz[%.0f]=%f' %(i,self.vx[i],i,self.vy[i],i,self.vz[i]))
            self.vcount += abs(self.vx[i] * self.dt) + abs(self.vy[i] * self.dt) + abs(self.vz[i] * self.dt)
            
            for j in range(1,self.Trn+1):
                
                r2 = (self.rx[i]-self.Trx[j]) * (self.rx[i]-self.Trx[j])
                r2 += (self.ry[i]-self.Try[j]) * (self.ry[i]-self.Try[j])
                r2 += (self.rz[i]-self.Trz[j]) *(self.rz[i]-self.Trz[j])
                
                r3 = ma.sqrt(r2)
                
                if r3 < self.Trad[j] * 2.0:
                    self.rcount += 1
                
                r4 = self.sigmoid(r3,self.Trad[j]*0.9,1) # test use 3
                #print('Tr3[%.0f]=%f' %(j,r3))
                
                self.vx[i] = -(self.rx[i]-self.Trx[j]) / r3 * r4
                self.vy[i] = -(self.ry[i]-self.Try[j]) / r3 * r4
                self.vz[i] = -(self.rz[i]-self.Trz[j]) / r3 * r4
                
                #if abs(self.rx[i]-self.Trx[j]) > self.Trad[j] * 2.0:
                #    self.vx[i] = -(self.rx[i]-self.Trx[j]) / r3 * 0.05
                #if abs(self.ry[i]-self.Try[j]) > self.Trad[j] * 2.0:
                #    self.vy[i] = -(self.ry[i]-self.Try[j]) / r3 * 0.05
                #if abs(self.rz[i]-self.Trz[j]) > self.Trad[j] * 2.0:
                #    self.vz[i] = -(self.rz[i]-self.Trz[j]) / r3 * 0.05
                
            for j in range(1,self.rn+1):
                
                if j != i:
                    
                    r2 = (self.rx[i]-self.rx[j]) ** 2
                    
                    r2 += (self.ry[i]-self.ry[j]) * (self.ry[i]-self.ry[j])
                    r2 += (self.rz[i]-self.rz[j]) *(self.rz[i]-self.rz[j])
                    
                    r3 = ma.sqrt(r2)
                    
                    r4 = self.sigmoid(r3,self.rad[i],2)
                    #print('r3[%.0f,%.0f]=%f' %(i,j,r3))
                    
                    self.vx[i] += -(self.rx[i]-self.rx[j]) / r3 * r4
                    self.vy[i] += -(self.ry[i]-self.ry[j]) / r3 * r4
                    self.vz[i] += -(self.rz[i]-self.rz[j]) / r3 * r4
                    
                    #if abs(self.rx[i]-self.rx[j]) > self.rad[i] + self.rad[j]:
                    #self.vx[i] += -(self.rx[i]-self.rx[j]) / r3 * 0.001
                    #if abs(self.ry[i]-self.ry[j]) > self.rad[i] + self.rad[j]:
                    #self.vy[i] += -(self.ry[i]-self.ry[j]) / r3 * 0.001
                    #if abs(self.rz[i]-self.rz[j]) > self.rad[i] + self.rad[j]:
                    #self.vz[i] += -(self.rz[i]-self.rz[j]) / r3 * 0.001
    
    def moveTargets(self):
        
        for i in range(1,self.Trn+1):
            
            if self.Trx[i] > 0.02:
               self.Trx[i] += -0.01
            elif self.Trx[i] < 0.02:
                self.Trx[i] += 0.01
            else:
                pass
            
            if self.Try[i] > 0.02:
               self.Try[i] += -0.01
            elif self.Try[i] < 0.02:
                self.Try[i] += 0.01
            else:
                pass
            
            if self.Trz[i] > 0.02:
               self.Trz[i] += -0.01
            elif self.Trz[i] < 0.02:
                self.Trz[i] += 0.01
            else:
                pass
            
            #print('Trx[%.0f]=%f,Try[%.0f]=%f,Trz[%.0f]=%f' %(i,self.Trx[i],i,self.Try[i],i,self.Trz[i]))
                
    def sigmoid(self,x,rad,useState):
    
        if useState == 1:
            return 1.0 / (1.0+np.exp(-float(x-rad*2.0))) - 0.5
        elif useState == 2:
            if x < rad*2.0:
                return -rad#*0.1
            else:
                return 0.0
        elif useState == 3:
            if x < rad*2.0:
                return -rad*0.1
            else:
                return rad*0.1
        else:
            return x

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
        
        self.moveSensors()
        self.moveTargets()
        self.object = self.makeObject()
        
        self.update()
        
    def setAnimating(self, animating):
        
        if animating:
            self.timer.start(100)
            self.inited = True
        else:
            self.timer.stop()
    
    def setTime(self, time):
        
        self.dt = time * 0.01
        
