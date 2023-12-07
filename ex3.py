#!/usr/bin/env python

import sys
from geant4_pybind import *

class X2DetectorConstruction(G4VUserDetectorConstruction):
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
 
     sphere_rad = 7*cm
     sOrb1 = 2*cm
     sOrb2 = 4*cm

     mat = nist.FindOrBuildMaterial("G4_WATER")
     mat1 = nist.FindOrBuildMaterial("G4_Fe")
     mat2 = nist.FindOrBuildMaterial("G4_C")
#     mat3 = nist.FindOrBuildMaterial("G4_WATER")
     checkOverlaps = True
 
     world_x = 2.2*envelop_x
     world_y = 2.2*envelop_y
     world_z = 2.2*envelop_z

     sWorld = G4Box("World", 0.5*world_x, 0.5*world_y, 0.5*world_z)
     lWorld = G4LogicalVolume(sWorld, envelop_mat, "World")
     pWorld = G4PVPlacement(None, G4ThreeVector(), lWorld, "World", None, False,0, checkOverlaps)

     box_x = 1.8*envelop_x
     box_y = 1.8*envelop_y
     box_z = 1.8*envelop_z

     sBox = G4Box("Box", 0.5*box_x, 0.5*box_y, 0.5*box_z)
     lBox = G4LogicalVolume(sBox, envelop_mat, "Box")
     G4PVPlacement(None, G4ThreeVector(), lBox, "Box", lWorld, False, 0, checkOverlaps)
 
     sSphere = G4Orb("Head", sphere_rad)
     sOrb1 = G4Orb("Bullit", sOrb1)
     sOrb2 = G4Orb("Coal", sOrb2)

     lSphere = G4LogicalVolume(sSphere, mat, "Head")
     lOrb1 = G4LogicalVolume(sOrb1, mat1, "Bullit")
     lOrb2 = G4LogicalVolume(sOrb2, mat2, "Coal")

     G4PVPlacement(None, G4ThreeVector(), lSphere, "Head", lWorld, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(0, 0, -0.2*sphere_rad), lOrb1, "Bullit", lSphere, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(0, 0, 0.4*sphere_rad), lOrb2, "Coal", lSphere, True, 0, checkOverlaps)
 
     self.fScoringVolume = lSphere
 
     return pWorld


ui = None
if len(sys.argv) == 1:
  ui = G4UIExecutive(len(sys.argv), sys.argv)

# Optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

runManager.SetUserInitialization(X2DetectorConstruction())

# Physics list
physicsList = QBBC()
physicsList.SetVerboseLevel(1)

runManager.SetUserInitialization(physicsList)

# User action initialization
#runManager.SetUserInitialization(X2ActionInitialization())

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
