#!/usr/bin/env python

import sys
from geant4_pybind import *
import math 

class X5DetectorConstruction(G4VUserDetectorConstruction):
   """
   Simple model: a sphere with water in the box with air.
   """
 
   def __init__(self):
     super().__init__()
     self.fScoringVolume = None
 
   def Construct(self):
     nist = G4NistManager.Instance()
 
     envelop_x = 10*cm
     envelop_y = 10*cm
     envelop_z = 10*cm
 
     envelop_mat = nist.FindOrBuildMaterial("G4_AIR")

#....Box
     box_x = 1*envelop_x 
     box_y = 1*envelop_y 
     box_z = 1*envelop_z      

#....Skull
     mat1 = nist.FindOrBuildMaterial("G4_B-100_BONE")

#....Water orb

     mat2 = nist.FindOrBuildMaterial("G4_WATER")

#....Mozg
     xSemiAxis1 = 1.2*cm 
     ySemiAxis1 = 1.2*cm 
     zSemiAxis1 = 1*cm 
     mat3 = nist.FindOrBuildMaterial("G4_Benzene")

     zTrans = G4Transform3D(G4RotationMatrix(), G4ThreeVector(-0.24*envelop_x, -0.1*envelop_y, 0))
     
     xSemiAxis2 = 2.5*cm 
     ySemiAxis2 = 3.5*cm 
     zSemiAxis2 = 2.5*cm 
     mat4 = nist.FindOrBuildMaterial("G4_Acetone")

#....Check for Overlaps
     checkOverlaps = True
 
#....World creating 
     world_x = 1.5*envelop_x
     world_y = 1.5*envelop_y
     world_z = 1.5*envelop_z

     sWorld = G4Box("World", 0.5*world_x, 0.5*world_y,
                    0.5*world_z)
 
     lWorld = G4LogicalVolume(sWorld, envelop_mat, "World")
 
     pWorld = G4PVPlacement(None, G4ThreeVector(),
                            lWorld, "World", None, False,
                            0, checkOverlaps)
#....Room
     sBox = G4Box("Box", 0.5*box_x, 0.5*box_y, 0.5*box_z)
     lBox = G4LogicalVolume(sBox, envelop_mat, "Box")
     G4PVPlacement(None, G4ThreeVector(), lBox, "Box", lWorld, False, 0, checkOverlaps)

#....Geometry volume creating 
     sSphere = G4Sphere("Skull", 0.45*envelop_x, 0.5*envelop_x, 2*math.pi, 2*math.pi, 0, 2*math.pi)
     sOrb = G4Orb("Blood", 0.45*envelop_x)
     sBrain1 = G4Ellipsoid("Brain1", xSemiAxis1, ySemiAxis1, zSemiAxis1, 0, 0)
     sBrain2 = G4Ellipsoid("Brain2", xSemiAxis2, ySemiAxis2, zSemiAxis2, 0, 0)

     sCutOrb = G4SubtractionSolid("Mozg", sBrain2, sBrain1, zTrans)

#....Logical volume creating
     lSphere = G4LogicalVolume(sSphere, mat1, "Skull")
     lOrb = G4LogicalVolume(sOrb, mat2, "Blood")
     lBrain1 = G4LogicalVolume(sBrain1, mat3, "Brain1")
     lBrain2 = G4LogicalVolume(sCutOrb, mat4, "Brain2")

#....Physical volume creating
     G4PVPlacement(None, G4ThreeVector(), lSphere,
                   "Skull", lBox, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(), lOrb,
                   "Blood", lSphere, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(-0.12*envelop_x, -0.1*envelop_y, 0), lBrain1,
                   "Brain1", lOrb, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(0.12*envelop_x, 0*envelop_y, 0), lBrain2, 
                   "Brain2", lOrb, True, 0, checkOverlaps)

     self.fScoringVolume = lSphere
 

     return pWorld


ui = None
if len(sys.argv) == 1:
  ui = G4UIExecutive(len(sys.argv), sys.argv)

# Optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

runManager.SetUserInitialization(X5DetectorConstruction())

# Physics list
physicsList = QBBC()
physicsList.SetVerboseLevel(1)

runManager.SetUserInitialization(physicsList)

# User action initialization
#runManager.SetUserInitialization(X5ActionInitialization())

visManager = G4VisExecutive()
# G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
# visManager = G4VisExecutive("Quiet")
visManager.Initialize()

# Get the User Interface manager
UImanager = G4UImanager.GetUIpointer()

# # Process macro or start UI session
if ui == None:
  # batch mode
  command = "/control/execute "
  fileName = sys.argv[1]
  UImanager.ApplyCommand(command + fileName)
else:
  # interactive mode
  UImanager.ApplyCommand("/control/execute init_vis.mac")
  ui.SessionStart()
