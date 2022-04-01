import math
import numpy as np

# Om = R * Or + Pr
def Object_To_World(a,Omx,Omy,Orx,Ory):      # Angle en degré
    alpha = math.radians(a)                         # Conversion en rad
    Om = np.array([Omx,Omy])                     # Position Robot dans le repère Monde
    Or = np.array([Orx,Ory])                     # Position objet dans le repère Robot
    R = np.array([[math.cos(alpha), math.sin(-alpha)],[math.sin(alpha), math.cos(alpha)]])
    return R @ Or + Om  

def Robot_in_world(a,Orx,Ory,Omx,Omy):            # Angle en degré
    alpha = math.radians(a)                         # Conversion en rad
    Or = np.array([Orx,Ory])                      # Position objet Robot
    Om = np.array([Omx,Omy])                        # Position objet Monde 
    R = np.array([[math.cos(alpha), math.sin(-alpha)],[math.sin(alpha), math.cos(alpha)]])
    return Om - (R @ Or)              
    
def Object_To_Robot(Xpm,Ypm,Xrm,Yrm,Xrm_2,Yrm_2):
    a = Xrm_2 - Xrm
    b = Yrm_2 - Yrm
    alpha = math.atan2(b,a)                         # Conversion en rad
    Pr = np.array([Xrm_2,Yrm_2])                    # Position Robot Monde
    Om = np.array([Xpm,Ypm])                        # Position objet Monde 
    R = np.array([[math.cos(alpha), math.sin(-alpha)],[math.sin(alpha), math.cos(alpha)]])
    return R.T @ (Om - Pr)                           # Calcul
