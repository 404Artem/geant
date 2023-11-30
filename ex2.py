#!/usr/bin/env python

import sys
from geant4_pybind import *

class XXDetectorConstruction(G4VUserDetectorConstruction):
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
     sphere_rad2 = 2*cm     
     sphere_rad3 = 4*cm

     mat3 = nist.FindOrBuildMaterial("G4_C")
     mat = nist.FindOrBuildMaterial("G4_WATER")
     mat2 = nist.FindOrBuildMaterial("G4_Fe")
 
     checkOverlaps = True
 
     world_x = 1.4*envelop_x
     world_y = 1.4*envelop_y
     world_z = 1.4*envelop_z
 
     sWorld = G4Box("World", 0.5*world_x, 0.5*world_y,
                    0.5*world_z)
 
     lWorld = G4LogicalVolume(sWorld, envelop_mat, "World")
 
     pWorld = G4PVPlacement(None, G4ThreeVector(),
                            lWorld, "World", None, False,
                            0, checkOverlaps)
 
     sSphere = G4Orb("Head", sphere_rad)
     sSphere2 = G4Orb("Bullit", sphere_rad2)
     sSphere3 = G4Orb("Coal", sphere_rad3)

     lSphere = G4LogicalVolume(sSphere, mat, "Head")
     lSphere2 = G4LogicalVolume(sSphere2, mat2, "Bullit")
     lSphere3 = G4LogicalVolume(sSphere3, mat3, "Coal")

     G4PVPlacement(None, G4ThreeVector(), lSphere,
                   "Head", lWorld, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(0, 0, -0.5*sphere_rad), lSphere2,
                   "Billit", lSphere, True, 0, checkOverlaps)
     G4PVPlacement(None, G4ThreeVector(0, 0, 0.45*sphere_rad), lSphere3,
                   "Coal", lSphere, True, 0, checkOverlaps)


     self.fScoringVolume = lSphere
 

     return pWorld


ui = None
if len(sys.argv) == 1:
  ui = G4UIExecutive(len(sys.argv), sys.argv)

# Optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

runManager.SetUserInitialization(XXDetectorConstruction())

# Physics list
physicsList = QBBC()
physicsList.SetVerboseLevel(1)

runManager.SetUserInitialization(physicsList)

# User action initialization
#runManager.SetUserInitialization(XXActionInitialization())

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
