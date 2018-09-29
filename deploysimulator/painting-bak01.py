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
        
        self.rn = 50
        self.Trn = 1
        self.dt = 0.1
        
        self.rad = np.zeros(self.rn+1, float)
        self.Trad = np.zeros(self.Trn+1, float)
        
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
    
        self.object = self.makeObject()

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
        
        # create random sets
        
        for i in range(1,self.rn+1):
            
            self.rad[i] = 0.05*rnd.random()*5.0 + 0.01#rnd.uniform(0.01,0.05)
            #print('rad[%.0f]=%f' %(i,self.rad[i]))
            self.colr[i] = abs(ma.sin(self.rad[i]*100))
            self.colg[i] = abs(ma.cos(self.rad[i]*100))
            self.colb[i] = ma.sqrt(abs(ma.sin(self.rad[i]*100)*ma.cos(self.rad[i]*100)))
            #print('colr[%.0f]=%f,colg[%.0f]=%f,colb[%.0f]=%f' %(i,self.colr[i],i,self.colg[i],i,self.colb[i]))
            
            self.rx[i] = ma.sin(5.0*rnd.random() + 1.0)#math.sin(rnd.uniform(0.5,2.0))
            self.ry[i] = ma.cos(5.0*rnd.random() + 1.0)
            self.rz[i] = ma.sin(5.0*rnd.random() + 1.0) * ma.cos(5.0*rnd.random() + 1.0)
            #print('rx[%.0f]=%f,ry[%.0f]=%f,rz[%.0f]=%f' %(i,self.rx[i],i,self.ry[i],i,self.rz[i]))
            
            self.vx[i] = 0.0
            self.vy[i] = 0.0
            self.vz[i] = 0.0
            
            self.dx[i] = 0.0#ma.sin(5.0*rnd.random() + 1.0)*100#math.sin(rnd.uniform(0.5,2.0))
            self.dy[i] = 0.0#ma.cos(5.0*rnd.random() + 1.0)*100
            self.dz[i] = 0.0#ma.sin(5.0*rnd.random() + 1.0) * ma.cos(5.0*rnd.random() + 1.0)*100
            #print('dx[%.0f]=%f,dy[%.0f]=%f,dz[%.0f]=%f' %(i,self.dx[i],i,self.dy[i],i,self.dz[i]))
            
        for i in range(1,self.Trn+1):
            
            self.Trad[i] = 0.3#0.3*rnd.random() + 0.01
            #print('Trad[%.0f]=%f' %(i,self.Trad[i]))
            self.Tcolr[i] = 1.0
            self.Tcolg[i] = 1.0
            self.Tcolb[i] = 1.0
            
            #self.Trx[1] = 1.0 #math.sin(rnd.uniform(0,0.5))
            #self.Trx[i] = 0.0 #math.cos(rnd.uniform(0,0.5))
            #self.Trx[i] = 0.0 #math.sin(rnd.uniform(0,0.5)) * math.cos(rnd.uniform(0,0.5))
            self.Trx[i] = 0.0#ma.sin(5.0*rnd.random() + 1.0)#math.sin(rnd.uniform(0.5,2.0))
            self.Try[i] = 0.0#ma.cos(5.0*rnd.random() + 1.0)
            self.Trz[i] = 0.0#ma.sin(5.0*rnd.random() + 1.0) * ma.cos(5.0*rnd.random() + 1.0)
            #print('Trx[%.0f]=%f,Try[%.0f]=%f,Trz[%.0f]=%f\n' %(i,self.Trx[i],i,self.Try[i],i,self.Trz[i]))
            
            self.Tvx[i] = 0.0
            self.Tvy[i] = 0.0
            self.Tvz[i] = 0.0
        
        #print('showEvent')
    
    def paintEvent(self, event):
        
        self.makeCurrent()
        
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
        
        # object : the target
        
        #gl.glPushMatrix()
        #gl.glTranslatef(1.0,ma.sqrt(3.0),1.0)
        #ax,az = self.rotateDirect(1.0,ma.sqrt(3.0),1.0)
        #gl.glRotatef(ax,1.0,0.0,0.0)
        #gl.glRotatef(0.0,0.0,1.0,0.0)
        #gl.glRotatef(az,0.0,0.0,1.0)
        #self.drawCone(Point3f(0.0,0.0,0.0), 
        #                Point3f(1.0,1.0,1.0), 
        #                1.0, 20)
        #self.drawSensor(Point3f(1.0,1.5,-1.5), 
        #                Point3f(0.0,0.0,0.0), 
        #                1.0, 1.0471975511965976)
        #gl.glPopMatrix()
        
        #gl.glPushMatrix()
        #self.drawSensor(Point3f(-2.0,-1.5,2.0), 
        #                Point3f(0.0,0.0,0.0), 
        #                0.5, 60)
        #gl.glPopMatrix()
        #gl.glPushMatrix()
        #self.drawSensor(Point3f(1.0,1.0,-2.0), 
        #                Point3f(0.0,0.0,0.0), 
        #                1.0, 60)
        #gl.glPopMatrix()
        
        # Plot targets
        
        for i in range(1,self.Trn+1):
            
            gl.glPushMatrix()
            gl.glTranslatef(self.Trx[i],self.Try[i],self.Trz[i])
            #print('Trx[%.0f]=%f,Trx[%.0f]=%f,Trx[%.0f]=%f\n' %(i,self.Trx[i],i,self.Trx[i],i,self.Trx[i]))
            gl.glColor3f(self.Tcolr[i],self.Tcolg[i],self.Tcolb[i])
            self.drawTarget(self.Trad[i])
            gl.glPopMatrix()
        
        # Plot sensors
        
        for i in range(1,self.rn+1):
            
            gl.glPushMatrix()
            #gl.glTranslatef(self.rx[i],self.ry[i],self.rz[i])
            #print('rx[%.0f]=%f,ry[%.0f]=%f,rz[%.0f]=%f' %(i,self.rx[i],i,self.ry[i],i,self.rz[i]))
            #gl.glRotatef(self.dx[i],1.0,0.0,0.0)
            #gl.glRotatef(self.dy[i],0.0,1.0,0.0)
            #gl.glRotatef(self.dz[i],0.0,0.0,1.0)
            gl.glColor3f(self.colr[i],self.colg[i],self.colb[i])
            #self.drawSensor(self.rad[i])
            self.drawSensor(Point3f(self.rx[i],self.ry[i],self.rz[i]),
                            Point3f(self.Trx[1],self.Try[1],self.Trz[1]),
                            self.rad[i],60)
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
        
    def drawSensor1(self,r):
        
        circle = np.linspace(0, ma.pi*2, 50)
        #point = Point3f(0.0,0.0,0.0)
        #print(r)
        
        gl.glBegin(gl.GL_LINES)
        #gl.glVertex3f(point.x, point.y, point.z)
        for i in range(1,50):
            gl.glVertex3f(0.0, 0.0, 0.0)
            gl.glVertex3f(r*ma.cos(circle[i]), -r, r*ma.sin(circle[i]))
        gl.glEnd()
        
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(1,50):
            gl.glVertex3f(r*ma.cos(circle[i]), -r, r*ma.sin(circle[i]))
        gl.glEnd()
        
    def drawSensor(self,o,t,rad,theta):
        
        R = (3.0 * (theta/180.0*ma.pi) * rad) / (4.0 * ma.sin((theta/2.0)/180.0*ma.pi))
        r = R * ma.sin((theta/2.0)/180.0*ma.pi)
        h = R * ma.cos((theta/2.0)/180.0*ma.pi)
        #print('R=%.4f,r=%.4f,h=%.4f' %(R,r,h))
        
        x = o.x - t.x
        y = o.y - t.y
        z = o.z - t.z
        
        Dxy = ma.sqrt(x**2 + y**2)
        Dxz = ma.sqrt(x**2 + z**2)
        Dyz = ma.sqrt(y**2 + z**2)
        
        dx1 = x * (Dxy-h) / Dxy
        dy1 = y * (Dxy-h) / Dxy
        dx2 = x * (Dxz-h) / Dxz
        dz1 = z * (Dxz-h) / Dxz
        dy2 = y * (Dyz-h) / Dyz
        dz2 = z * (Dyz-h) / Dyz
        dx = (dx1+dx2) / 2.0
        dy = (dy1+dy2) / 2.0
        dz = (dz1+dz2) / 2.0
        #print('dx1=%.4f,dy1=%.4f,dz1=%.4f' %(dx1,dy1,dz1))
        #print('dx2=%.4f,dy2=%.4f,dz2=%.4f' %(dx2,dy2,dz2))
        
        #px = h * x/y * ma.sin(ma.atan(x/y))
        #py = h * x/y * ma.cos(ma.atan(x/y))
        #pz = h * x/z * ma.sin(ma.atan(z/x))
        #print('px=%.4f,py=%.4f,pz=%.4f' %(px,py,pz))

        #dx = rad * ma.sin(ma.atan(x/y))
        #dy = rad * ma.cos(ma.atan(x/y))
        #dz = rad * ma.sin(ma.atan(z/x))
        
        #if np.sign(x) == np.sign(px):
        #    qx = x - px
        #else:
        #    qx = x + px
        #    
        #if np.sign(y) == np.sign(py):
        #    qy = y - py
        #else:
        #    qy = y + py
        #    
        #if np.sign(z) == np.sign(pz):
        #    qz = z - pz
        #else:
        #    qz = z + pz
        #print((x-qx)*(x-qx) + (y-qy)*(y-qy))
        #qz = z - ma.sqrt(h*h - (x-qx)*(x-qx) - (y-qy)*(y-qy))
        #qz = t.z
        #print(qx)
        #print(qy)
        #print(qz)
        #print('qx=%.4f,qy=%.4f,qz=%.4f' %(qx+t.x,qy+t.y,qz+t.z))
        #print('ox=%.4f,oy=%.4f,oz=%.4f' %(o.x+t.x,o.y+t.y,o.z+t.z))
        #print('r=%.4f' %(r))
        #gl.glBegin(gl.GL_LINES)
        #gl.glVertex3f(o.x,o.y,o.z)
        #gl.glVertex3f(t.x,t.y,t.z)
        #gl.glVertex3f(o.x,o.y,o.z)
        #gl.glVertex3f(dx1,dy1,dz1)
        #gl.glVertex3f(o.x,o.y,o.z)
        #gl.glVertex3f(dx2,dy2,dz2)
        #gl.glVertex3f(o.x,o.y,o.z)
        #gl.glVertex3f(qx,qy,qz)
        
        #gl.glVertex3f(v0[0]+c0[0]*2,v0[0]+c0[1]*2,v0[0]+c0[2]*2)
        #gl.glVertex3f(v0[0],v0[1],v0[2])
        #for i in range(0,n):
        #    gl.glVertex3f(v0[0],v0[1],v0[2])
        #    gl.glVertex3f(vert[i][0], vert[i][1], vert[i][2])
        #gl.glEnd()
        #self.drawCone(Point3f(qx+t.x,qy+t.y,qz+t.z),
        #              Point3f(o.x+t.x,o.y+t.y,o.z+t.z),
        #              r,20)
        self.drawCone(Point3f(dx,dy,dz),
                      Point3f(o.x,o.y,o.z),
                      r,20)
        
    def drawCone(self,c,v,r,n):
        
        c0 = np.array([c.x,c.y,c.z])
        #print(c0)
        v0 = np.array([v.x,v.y,v.z])
        
        # calculate the distance for the height
        h = ma.sqrt(np.sum((c0-v0) * (c0-v0)))
        alpha = ma.acos(np.dot(np.array([0.0,0.0,1.0]),v0-c0) / h)
        #alpha = ma.degrees(alpha)
        
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
            #print(t[i])
            #print(tx[i])
            #print(ty[i])
            #print()
        #print(tx)
        
        vert = np.array([tx-c0[0],ty-c0[1],c0[2]*np.linspace(1.0,1.0,n)-c0[2]]).T
        #print(vert)
        #print('zdx=%.4f,zdy=%.4f,zdz=%.4f' %(zdir[0]-c0[0],zdir[1]-c0[1],zdir[2]-c0[2]))
        #print('alpha=%.4f' %(alpha))
        if zdir[0] != c0[0] and zdir[1] != c0[1]:
            vert = self.rot3d(vert, np.array([0.0,0.0,0.0]), zdir-c0, alpha)
            #print(vert)
        vert = vert + c0
        #print(vert)
        
        # reference points
        gl.glBegin(gl.GL_LINES)
        #gl.glVertex3f(c0[0],c0[1],c0[2])
        #gl.glVertex3f(v0[0],v0[1],v0[2])
        #gl.glVertex3f(c0[0],c0[1],c0[2])
        #gl.glVertex3f(zdir[0],zdir[1],zdir[2])
        #gl.glVertex3f(v0[0],v0[1],v0[2])
        #gl.glVertex3f(0.0,0.0,0.0)
        #gl.glVertex3f(v0[0]+c0[0]*2,v0[0]+c0[1]*2,v0[0]+c0[2]*2)
        #gl.glVertex3f(v0[0],v0[1],v0[2])
        for i in range(0,n):
            gl.glVertex3f(v0[0],v0[1],v0[2])
            gl.glVertex3f(vert[i][0], vert[i][1], vert[i][2])
        gl.glEnd()
        
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(0,n):
            #pass
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
        #print(M)
        origin = np.tile(origin,(np.size(p,0),1))
        #print(origin)
        pr = np.dot(p-origin,M.T) + origin
        #print(pr)
        
        return pr
        
    def drawTarget(self,r):
        
        p1 = Point3f(r,r,r)
        p2 = Point3f(r,r,-r)
        p3 = Point3f(r,-r,-r)
        p4 = Point3f(r,-r,r)
        p5 = Point3f(-r,r,r)
        p6 = Point3f(-r,r,-r)
        p7 = Point3f(-r,-r,-r)
        p8 = Point3f(-r,-r,r)
        
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
        
    def moveSensors(self):
        #print('rx[1]=%f' %(self.rx[1]))
        for i in range(1,self.rn+1):
            
            self.rx[i] += self.vx[i] * self.dt
            self.ry[i] += self.vy[i] * self.dt
            self.rz[i] += self.vz[i] * self.dt
            #print('rx[%.0f]=%f,ry[%.0f]=%f,rz[%.0f]=%f' %(i,self.rx[i],i,self.ry[i],i,self.rz[i]))
            
            for j in range(1,self.Trn+1):
                
                r2 = (self.rx[i]-self.Trx[j]) * (self.rx[i]-self.Trx[j])
                r2 += (self.ry[i]-self.Try[j]) * (self.ry[i]-self.Try[j])
                r2 += (self.rz[i]-self.Trz[j]) *(self.rz[i]-self.Trz[j])
                
                r3 = ma.sqrt(r2)
                
                r4 = self.sigmoid(r3,self.Trad[j]*1.5,1)
                #print('Tr3[%.0f]=%f' %(j,r3))
                
                self.vx[i] = -(self.rx[i]-self.Trx[j]) / r3 * r4
                self.vy[i] = -(self.ry[i]-self.Try[j]) / r3 * r4
                self.vz[i] = -(self.rz[i]-self.Trz[j]) / r3 * r4
                
                #print('dx=%f,dy=%f,dz=%f' %(self.dx[i]-self.Trx[j],self.dy[i]-self.Try[j],self.dz[i]-self.Trz[j]))
                self.dx[i],self.dz[i] = self.rotateDirect(self.rx[i]-self.Trx[j], self.ry[i]-self.Try[j], self.rz[i]-self.Trz[j])
                self.dy[i] = 0.0#self.rotateDirectZ(self.rx[i],self.rz[i])
                #self.dz[i] = 0.0#self.rotateDirectZ(self.rx[i],self.ry[i])
                
            for j in range(1,self.rn+1):
                
                if j != i:
                    
                    r2 = (self.rx[i]-self.rx[j]) * (self.rx[i]-self.rx[j])
                    r2 += (self.ry[i]-self.ry[j]) * (self.ry[i]-self.ry[j])
                    r2 += (self.rz[i]-self.rz[j]) *(self.rz[i]-self.rz[j])
                    
                    r3 = ma.sqrt(r2)
                    
                    r4 = self.sigmoid(r3,self.rad[i],2)
                    #print('r3[%.0f,%.0f]=%f' %(i,j,r3))
                    
                    self.vx[i] += -(self.rx[i]-self.rx[j]) / r3 * r4
                    self.vy[i] += -(self.ry[i]-self.ry[j]) / r3 * r4
                    self.vz[i] += -(self.rz[i]-self.rz[j]) / r3 * r4
                
    def sigmoid(self,x,rad,useState):
    
        if useState == 1:
            return 1.0 / (1.0+np.exp(-float(x-rad*2.0))) - 0.5
        elif useState == 2:
            if x < rad*2.0:
                return -rad
            else:
                return 0.0
        else:
            return x
        
    def rotateDirect(self,x,y,z):
        
        # consider about zero
        #if x == 0.0 and y == 0.0:
        #    return 0.0
        #elif x == 0.0:
        #    return 0.0 if y > 0.0 else 180.0
        #elif y == 0.0:
        #    return 90.0 if x > 0.0 else 270.0
        
        # calculate the angle of arctan
        ranX = ma.atan2(z,y)
        ranZ = ma.atan2(x,y)
        angX = ma.degrees(ranX)
        angZ = ma.degrees(ranZ)
        #print('radianX = %f.angleX = %f' %(ranX,angX))
        #print('radianZ = %f.angleZ = %f' %(ranZ,angZ))
        
        # calculate the angle of limits
        if y > 0.0:
            if x > 0.0:
                angZ = -angZ
            else:
                angZ += 90.0
        else:
            if x < 0.0:
                angZ += 180.0
                    
        #print('angleX = %f.angleZ = %f' %(angX,angZ))
        
        return angX,angZ

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
        self.object = self.makeObject()
        #print('animating')
        
        self.update()
        
    def setAnimating(self, animating):
        
        if animating:
            self.timer.start(100)
        else:
            self.timer.stop()
        
