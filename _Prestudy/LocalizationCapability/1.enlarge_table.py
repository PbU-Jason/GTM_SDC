#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### package ###
import math
import numpy as np
import pandas as pd 
import scipy.interpolate
#====================

### selection ###
filename = 'typical1_response' # middle energy
# filename = 'typical2_response' # hard energy
# filename = 'typical3_response' # soft energy
#====================

### function ###
def Polar2Cartesian(ThetaDegree, PhiDegree):
    ThetaRadian = ThetaDegree * np.pi/180
    PhiRadian   = PhiDegree * np.pi/180
    X = -np.sin(ThetaRadian) * np.cos(PhiRadian) # NSPO define +x to -x
    Y = np.sin(ThetaRadian) * np.sin(PhiRadian)
    Z = -np.cos(ThetaRadian)                     # NSPO define +z to -z
    return np.array([X, Y, Z])

def Fibonacci_Sphere(Skypoint):
    PointsList = []
    Phi = math.pi * (3. - math.sqrt(5.))    # golden angle in radians
    for i in range(Skypoint):
        Z = 1 - (i/float(Skypoint - 1)) * 2 # Z goes from 1 to -1
        Radius = math.sqrt(1 - Z * Z)       # radius at Z
        Theta  = Phi * i                    # golden angle increment!
        X = math.cos(Theta) * Radius
        Y = math.sin(Theta) * Radius
        PointsList.append([X, Y, Z])
    return np.array(PointsList).T
#====================

### fixed variables ###
total_skypoints = 41168 # number of total sky points to make angle between 2 points is ~ 1 degree
sensor_name_list = ['NN','NP','NT','NB','PN','PP','PT','PB']
#====================

### main code ###
# load data
df = pd.read_csv('./1.table/' + filename + '.csv')

# transfer polar angle to x, y & z
xyz = Polar2Cartesian(df['theta'], df['phi'])
x, y, z = xyz

# use Fibonacci sphere to create more skypoints
points_list = Fibonacci_Sphere(total_skypoints)
X, Y, Z = points_list

# collect X, Y & Z of big table
big_table = np.array([X,Y,Z]).T

# interpolate
for i in range(8):
    interpolate_ref = df[sensor_name_list[i]]
    interpolator = scipy.interpolate.Rbf(x, y, z, interpolate_ref)
    interpolate_result = np.array([interpolator(X, Y, Z)]).T
    big_table = np.hstack((big_table, interpolate_result))
   
# output big table
# np.savetxt('./1.table/big_' + filename + '.csv', big_table, 
#            delimiter=',', header='X, Y, Z, NN, NP, NT, NB, PN, PP, PT, PB')
#====================