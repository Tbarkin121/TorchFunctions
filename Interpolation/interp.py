# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:21:25 2023

@author: MiloPC
"""

import torch

# 2D bilinear interpolation 

# Inputs : 
# Z = Z(x,y) : Evenly spaced data to be interpolated
# xe = X evaluation point
# ye = Y evaluation point
# min_x = min X value 
# max_x 
def interp2(Z,xe,ye,min_x,max_x,min_y,max_y):

    x0 = (xe - min_x)/(max_x - min_x)*(nx-1)
    y0 = (ye - min_y)/(max_y - min_y)*(ny-1)

    x_floor = torch.clamp(torch.floor(x0).long(),0,nx-1)
    x_ceil = torch.clamp(x_floor + 1,0,nx-1)
    y_floor = torch.clamp(torch.floor(y0).long(),0,nx-1)
    y_ceil = torch.clamp(y_floor + 1,0,nx-1)

    z11 = Z[x_floor,y_floor]
    z12 = Z[x_floor,y_ceil]
    z21 = Z[x_ceil,y_floor]
    z22 = Z[x_ceil,y_ceil]

    x_frac = x_ceil - x0
    y_frac = y_ceil - y0

    z1 = z11*(1-x_frac) + z12*x_frac
    z2 = z21*(1-x_frac) + z22*x_frac
    ze = z1*(1-y_frac) + z2*y_frac
    
    return ze

# Example Usage
pi = torch.tensor(torch.pi)
nx = 50
ny = 100

x = torch.linspace(-pi,pi,nx)
y = torch.linspace(-pi,pi,ny)

X,Y = torch.meshgrid(x,y)

Z = torch.sin(X)*torch.cos(Y)

xe = pi*(2*torch.rand([10,])-1.0)
ye = pi*(2*torch.rand([10,])-1.0)

min_x = torch.min(x)
max_x = torch.max(x)
min_y = torch.min(y)
max_y = torch.max(y)

ze = interp2(Z,xe,ye,min_x,max_x,min_y,max_y)