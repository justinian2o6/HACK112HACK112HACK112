from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3
from panda3d.core import *

from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.interval.MetaInterval import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
import sys

TRACK_SEGMENT_LENGTH = 15
TRACK_TIME = 2

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
 
        # Disable the camera track controls.
        #self.disableMouse()
 
        # Load the environment model.
        '''self.scene = self.loader.loadModel("environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)'''

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(1, 1, 1, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)
        '''self.track=loader.loadModel("H2.egg")
        self.track.reparentTo(render)
        # Create Ambient Light
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(1, 1, 1, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)

    
         
        ambient = AmbientLight('ambient')
        ambient.setColor(Vec4(0.5, 1, 0.5, 1))
        ambientNP = self.track.attachNewNode(ambient)
        self.track.setLightOff()
        self.track.setLight(ambientNP)'''

        self.initTrack()
        self.contTrack()

    def initTrack(self):
        self.trackList = [None] * 4

        for x in range(4):
            # Load a copy of the track
            self.trackList[x] = loader.loadModel("H2.egg")
            self.trackList[x].reparentTo(render)
            # Create Ambient Light

            ambient = AmbientLight('ambient')
            ambient.setColor(Vec4(0.5, 1, 0.5, 1))
            ambientNP = self.trackList[x].attachNewNode(ambient)
            self.trackList[x].setLightOff()
            self.trackList[x].setLight(ambientNP)
            # The front segment needs to be attached to render
            if x == 0:
                self.trackList[x].reparentTo(render)
            # The rest of the segments parent to the previous one, so that by moving
            # the front segement, the entire track is moved
            else:
                self.trackList[x].reparentTo(self.trackList[x - 1])
            # We have to offset each segment by its length so that they stack onto
            # each other. Otherwise, they would all occupy the same space.
            self.trackList[x].setPos(0, 0, -TRACK_SEGMENT_LENGTH)
            # Now we have a track consisting of 4 repeating segments with a
            # hierarchy like this:
            # render<-track[0]<-track[1]<-track[2]<-track[3]

    # This function is called to snap the front of the track to the back
    # to simulate traveling through it
    def contTrack(self):
        # This line uses slices to take the front of the list and put it on the
        # back. For more information on slices check the Python manual
        self.trackList = self.trackList[1:] + self.trackList[0:1]
        # Set the front segment (which was at track_SEGMENT_LENGTH) to 0, which
        # is where the previous segment started
        self.trackList[0].setZ(0)
        # Reparent the front to render to preserve the hierarchy outlined above
        self.trackList[0].reparentTo(render)
        # Set the scale to be apropriate (since attributes like scale are
        # inherited, the rest of the segments have a scale of 1)
        self.trackList[0].setScale(.155, .155, .305)
        # Set the new back to the values that the rest of teh segments have
        self.trackList[3].reparentTo(self.trackList[2])
        self.trackList[3].setY(-TRACK_SEGMENT_LENGTH)
        self.trackList[3].setScale(1)

        # Set up the track to move one segment and then call conttrack again
        # to make the track move infinitely
        self.trackMove = Sequence(
            LerpFunc(self.trackList[0].setY,
                     duration=TRACK_TIME,
                     fromData=0,
                     toData=TRACK_SEGMENT_LENGTH * .305),
            Func(self.contTrack)
        )
        self.trackMove.start()
app = MyApp()
app.run()