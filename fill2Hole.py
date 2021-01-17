# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:33:58 2020
This code: 
    - Calculates the probability to fill tile holes in Knotris.  
@author: Kelemua Tesfaye
"""
#only concered with connection points (CPs) of tiles so we can reduce the 11 knot mosaic tiles to 7 tiles
#tile is a tuple of tuples that outlines the 7 knot mosaic tiles 
    #each tuple within tile has 2 elements, where the first element is the tile name and the 2nd is the boundary condition for the tile
    #tile BCs consist of 0s and 1s coresponding to edges of the tile (Left, Top, Right, Bottom)
    #where 0 means there isn't a CP along the edge and 1 indicates there is a CP along the edge    
tile = (('blank', (0,0,0,0)), 
        ('elbow bottom left', (1,0,0,1)), 
        ('elbow bottom right', (0,0,1,1)),
        ('elbow top left', (1,1,0,0)),
        ('elbow top right', (0,1,1,0)),
        ('horizontal', (1,0,1,0)),
        ('vertical', (0,1,0,1)),
        ('crossing', (1,1,1,1)))

#dictionary defining probability assumed for picking each tile 
probs = {(0,0,0,0):1/7, #blank
         (1,0,0,1):2/7, #elbowBL
         (0,0,1,1):2/7, #elbowBR
         (1,1,0,0):2/7, #elbowTL
         (0,1,1,0):2/7, #elbowTR
         (1,0,1,0):2/7, #horizontal
         (0,1,0,1):2/7, #vertical
         (1,1,1,1):2/7} #crossing

#elbows and lines equivalence classes defined as lists 
elbows = [tile[1], tile[2], tile[3], tile[4]]
lines = [tile[5], tile[6]]

#Makes list of possible boundary conditions (BCs) of a row. The number of elements in 
    #possBoundary can be adjusted to reflect all possible BCs of a hole
pickCP = [0, 1]
possBoundary = [pickCP, pickCP, pickCP, pickCP, pickCP, pickCP]
from itertools import product
boundaries = list(product(*possBoundary))
boundaryCount = {}
for i in range(len(boundaries)):
    boundaryCount[boundaries[i]] = 0
#prints the boundary conditions 
doprint = 'no'
if doprint == 'yes':
    for i in boundaryCount:          
        print(i)  
    
#functions that begin with 'which' return the tuples of the tiles that can satisfy the BC
        #these functions concern only 1 tile holes
def whichTile3(boundary):                         #working
    """
    given 3 tuple boundary as argument 
    returns the tuple of the unique tile that will satisfy the boundary condition
    """
    global tile
    keep = ()       #for some reason requires this for twoTileH3Det
    for t in tile:
        if t[1][0] == boundary[0]:
            if t[1][3] == boundary[1]:
                if t[1][2] == boundary[2]:
                    keep = t[1]
                    break
    return keep

def whichTile2(boundary):                       #working
    """
    given 2 tuple boundary as argument
    returns a list of 2 tuples of the tiles can satisfy the BC         
    """
    global tile
    
    if boundary[0] == boundary[1] == 0:
        keep = [tile[0][1], tile[4][1]]
    elif boundary[0] == boundary[1] == 1:
        keep = [tile[1][1], tile[7][1]]
    elif boundary[0] == 0 and boundary[1] ==1:
        keep = [tile[2][1], tile[6][1]]
    else:
        keep = [tile[3][1], tile[5][1]]
    return keep

def whichTile2From(boundary, tileList, face):      #working
    """ 
    boundary is a 2 tuple, tileList is list of tiles from which to check SC 
    tiles, and face can be 'L' 'l' or 'R' 'r'
    returns the tile that satisfy BC
    """
    keep = ()
    if face == 'L' or face == 'l':
        for tile in tileList:
            if tile[1][0] == boundary[0] and tile[1][3] == boundary[1]:
                keep = tile[1]
                break   
    if face == 'R' or face == 'r':
        for tile in tileList:
            if tile[1][3] == boundary[0] and tile[1][2] == boundary[1]:
                keep = tile[1]
                break
    return keep

def whichTile1From(boundary, tileList):         #working 
    """
    boundary is a 1 tuple, titleList is a list of tiles from which to 
    check SC 
    returns the tuples of the tiles that satisfies BC  
    """    
    global tile
    if tileList == tile or tileList == elbows:
        keep = []
        for t in tileList:
            if (t[1][3],) == boundary:
                keep.append(t[1])
    else: 
        keep = ()
        for t in tileList: 
            if (t[1][3],) == boundary:             
                keep = t[1]
                break
    return keep

#functions that end in 'Det' (follor form zzzTilezDet) return the probability of filling a hole 

def oneTile3Det(boundary):                      #working 
    """
    takes boundary condition a 3-element tuple as a parameter which describes
    a 1x1 hole with 3 determined edges returns the probability to 
    fill the hole 
    """
    global probs
    
    keep = whichTile3(boundary)
    probability = probs[keep]
    return probability

def oneTile2Det(boundary):                      #working
    """
    takes boundary condition a 2-element tuple as a parameter which describes
    a 1x1 hole with 1 free & 2 determined edges 
    returns the probability to fill the hole 
    """
    global probs
    
    keep = whichTile2(boundary)
    probability = 0
    for tile in keep:
        probability += probs[tile]
    return probability

def twoTileV5Det(boundary):                     #working
    """
    2 tile vertical hole
    5 element tuple as parameter
    return probability to fill hole
    only one such configuration can fill this hole
    """
    global tile
    
    first = (boundary[1], boundary[2], boundary[3])
    det1st = whichTile3(first)
    probability = probs[det1st]
    
    second = (boundary[0], det1st[1], boundary[4])
    det2nd = whichTile3(second)
    probability *= probs[det2nd]
    return probability 
 
def threeTileV7Det(boundary):                   #working
    """
    3 tile vertical hole
    7 element tuple as parameter
    returns probability to fill hole
    only one such configuration can fill this hole 
    """
    global tile
    
    first = (boundary[2], boundary[3], boundary[4])
    det1st = whichTile3(first)
    probability = probs[det1st]
    
    second = (boundary[1], det1st[1], boundary[5])
    det2nd = whichTile3(second)
    probability *= probs[det2nd]
    
    third = (boundary[0], det2nd[1], boundary[6])
    det3rd = whichTile3(third)
    probability *= probs[det3rd]
    return probability 

def twoTileH4Det(boundary):                     #working  
    """
    accepts 4-element tuple as boundary
    return probability 
    """
    global probs
    global tile
    global elbows
    global lines
    
    probability = 0
    smartProbability = 0
    placeL = (boundary[0], boundary[1])
    placeR = (boundary[2], boundary[3])  
     
    #elbow branch
    a = b = 0
    keepEL = whichTile2From(placeL, elbows, 'L') 
    if keepEL != ():
        secondERBoundary = (keepEL[2], boundary[2], boundary[3])
        keepELR = whichTile3(secondERBoundary)
    keepER = whichTile2From(placeR, elbows, 'R')   
    if keepER != ():
        secondELBoundary = (boundary[0], boundary[1], keepER[0])
        keepERL = whichTile3(secondELBoundary)
    choice = (len(keepEL) + len(keepER)) / 4
    if keepEL != ():
        a = (1 / choice) * probs[keepEL] * probs[keepELR]
        probability += a
    if keepER != ():
        b = (1 / choice) * probs[keepER] * probs[keepERL]
        probability += b
    if a == b:
        smartProbability += a + b
    elif a > b: 
        smartProbability += a
    elif a < b:
        smartProbability += b
    #print('elbow', a+b)
    #line branch  
    c = d = 0
    keepLL = whichTile2From(placeL, lines,'L')
    if keepLL != ():
        secondLRBoundary = (keepLL[2], boundary[2], boundary[3])
        keepLLR = whichTile3(secondLRBoundary)  
    keepLR = whichTile2From(placeR, lines, 'R')
    if keepLR != ():
        secondLLBoundary = (boundary[0], boundary[1], keepLR[0])
        keepLRL = whichTile3(secondLLBoundary)
    choice = (len(keepLL) + len(keepLR)) / 4
    if keepLL != ():
        c = (1 / choice) * probs[keepLL] * probs[keepLLR]
        probability += c
    if keepLR != ():
        d = (1 / choice) * probs[keepLR] * probs[keepLRL]
        probability += d
    if c == d:
        smartProbability += c + d
    elif c > d:
        smartProbability += c
    elif d > c: 
        smartProbability += d
    #print('line', c+d)    
    #blank branch
    e = f = 0
    keepBL = whichTile2From(placeL, [tile[0]], 'L')
    if keepBL != ():
        secondBRBoundary = (keepBL[2], boundary[2], boundary[3])
        keepBLR = whichTile3(secondBRBoundary)
    keepBR = whichTile2From(placeR, [tile[0]], 'R')
    if keepBR != ():
        secondBLBoundary = (boundary[0], boundary[1], keepBR[0])
        keepBRL = whichTile3(secondBLBoundary)
    choice = (len(keepBL) + len(keepBR)) / 4 
    if keepBL != ():
        e = (1 / choice) * probs[keepBL] * probs[keepBLR]
        probability += e
    if keepBR != ():
        f = (1 / choice) * probs[keepBR] * probs[keepBRL]
        probability += f
    if e == f:
        smartProbability += e + f
    elif e > f: 
        smartProbability += e
    elif f > e: 
        smartProbability += f
    #print('blank', e + f)
    #crossing branch
    g = h = 0
    keepCL = whichTile2From(placeL, [tile[7]], 'L')
    if keepCL != ():
        secondCRBoundary = (keepCL[2], boundary[2], boundary[3])
        keepCLR = whichTile3(secondCRBoundary)
    keepCR = whichTile2From(placeR, [tile[7]], 'R')
    if keepCR != ():
        secondCLBoundary = (boundary[0], boundary[1], keepCR[0])
        keepCRL = whichTile3(secondCLBoundary)
    choice = (len(keepCL) + len(keepCR)) / 4
    if keepCL != ():
        g = (1 / choice) * probs[keepCL] * probs[keepCLR]
        probability += g
    if keepCR != ():
        h = (1 / choice) * probs[keepCR] * probs[keepCRL]
        probability += h
    if g == h:
        smartProbability += g + h
    elif g > h:
        smartProbability += g
    elif h > g:
        smartProbability += h        
    #print('crossing', g+h)
    return probability 

def threeTileH5Det(boundary):                   #working
    """
    accepts 5 tuple BC as an argument 
    returns probability of filling a 1x3 (three tile horizontal) hole 
    """
    global tile
    global probs
    global elbows
    global lines
    
    probability = 0
    smartProb = 0
    placeL = (boundary[0], boundary[1])
    placeC = (boundary[2],)
    placeR = (boundary[3], boundary[4])

    #blank branch
    choice1st = 0
    keepBL = whichTile2From(placeL, [tile[0]], 'L')
    if keepBL != ():
        keepBL2R = (keepBL[2], boundary[2], boundary[3], boundary[4])
        probBL2R = twoTileH4Det(keepBL2R)
        choice1st += 1
    keepBC = whichTile1From(placeC, [tile[0]])
    if keepBC !=():
        keepBCL = (boundary[0], boundary[1], keepBC[0])
        probBCL = oneTile3Det(keepBCL)
        keepBCR = (keepBC[2], boundary[3], boundary[4]) 
        probBCR = oneTile3Det(keepBCR)
        choice1st += 1
    keepBR = whichTile2From(placeR, [tile[0]], 'R')
    if keepBR != ():
        keepBR2L = (boundary[0], boundary[1], boundary[2], keepBR[0])
        probBR2L = twoTileH4Det(keepBR2L)
        choice1st += 1
   
    if keepBL != ():
        a = (1 / choice1st) * probs[keepBL] * probBL2R
        probability += a
    if keepBC != ():
        b = (1 / choice1st) * probs[keepBC] * probBCL * probBCR
        probability += b
    if keepBR != ():
        c = (1 / choice1st) * probs[keepBR] * probBR2L
        probability += c
    
#    if probBL2R == probBCR == probBR2L:
#        smartProbability = probability 
#    else: 
#        max 

    #crossing branch
    choice1st = 0
    keepCL = whichTile2From(placeL, [tile[7]], 'L')
    if keepCL != ():
        keepCL2R = (keepCL[2], boundary[2], boundary[3], boundary[4])
        probCL2R = twoTileH4Det(keepCL2R)
        choice1st += 1
    keepCC = whichTile1From(placeC, [tile[7]])
    if keepCC !=():
        keepCCL = (boundary[0], boundary[1], keepCC[0])
        probCCL = oneTile3Det(keepCCL)
        keepCCR = (keepCC[2], boundary[3], boundary[4]) 
        probCCR = oneTile3Det(keepCCR)
        choice1st += 1
    keepCR = whichTile2From(placeR, [tile[7]], 'R')
    if keepCR != ():
        keepCR2L = (boundary[0], boundary[1], boundary[2], keepCR[0])
        probCR2L = twoTileH4Det(keepCR2L)
        choice1st += 1
   
    if keepCL != ():
        d = (1 / choice1st) * probs[keepCL] * probCL2R
        probability += d
    if keepCC != ():
        e = (1 / choice1st) * probs[keepCC] * probCCL * probCCR
        probability += e
    if keepCR != ():
        f = (1 / choice1st) * probs[keepCR] * probCR2L
        probability += f 
    
    #line branch
    keepLL = whichTile2From(placeL, lines, 'L')
    if keepLL != ():
        keepLL2R = (keepLL[2], boundary[2], boundary[3], boundary[4])
        probLL2R = twoTileH4Det(keepLL2R)
        choice1st += 1
    keepLC = whichTile1From(placeC, lines)
    if keepLC !=():
        keepLCL = (boundary[0], boundary[1], keepLC[0])
        probLCL = oneTile3Det(keepLCL)
        keepLCR = (keepLC[2], boundary[3], boundary[4]) 
        probLCR = oneTile3Det(keepLCR)
        choice1st += 1
    keepLR = whichTile2From(placeR, lines, 'R')
    if keepLR != ():
        keepLR2L = (boundary[0], boundary[1], boundary[2], keepLR[0])
        probLR2L = twoTileH4Det(keepLR2L)
        choice1st += 1
   
    if keepLL != ():
        g = (1 / choice1st) * probs[keepLL] * probLL2R
        probability += g
    if keepLC != ():
        h = (1 / choice1st) * probs[keepLC] * probLCL * probLCR
        probability += h
    if keepLR != ():
        l = (1 / choice1st) * probs[keepLR] * probLR2L
        probability += l
    
    #elbow branch
    keepEL = whichTile2From(placeL, elbows, 'L')
    keepEL2R =  (keepEL[2], boundary[2], boundary[3], boundary[4])
    probEL2R = twoTileH4Det(keepEL2R)
    
    keepEC = whichTile1From(placeC, elbows) #2 tiles
    keepECL1 = (boundary[0], boundary[1], keepEC[0][0])
    probECL1 = oneTile3Det(keepECL1)
    keepECR1 = (keepEC[0][2], boundary[3], boundary[4])
    probECR1 = oneTile3Det(keepECR1)
    
    keepECL2 = (boundary[0], boundary[1], keepEC[1][0])
    probECL2 = oneTile3Det(keepECL2)
    keepECR2 = (keepEC[1][2], boundary[3], boundary[4])
    probECR2 = oneTile3Det(keepECR2)
    
    keepER = whichTile2From(placeR, elbows, 'R')
    keepER2L = (boundary[0], boundary[1], boundary[2], keepER[0])
    probER2L = twoTileH4Det(keepER2L)
    choice1st = 4
    
    m = (1 / choice1st) * probs[keepEL] * probEL2R
    probability += m
    n = (1 / choice1st) * probs[keepEC[0]] * probECL1 * probECR1
    probability += n
    o = (1 / choice1st) * probs[keepEC[1]] * probECL2 * probECR2
    probability += o
    p = (1 / choice1st) * probs[keepER] * probER2L
    probability += p
    return probability

def twoTileH3Det(boundary, freeEdge):           #working
    """
    freeEdge is which face the free edge is on left/right
    returns probability
    """
    if freeEdge == 'L' or 'l':
        probability = twoTileH3DetR(boundary)
    elif freeEdge == 'R' or 'r':
        flipBoundary = (boundary[2], boundary[1], boundary[0]) 
        probability = twoTileH3DetR(flipBoundary)
    return probability 

def twoTileH3DetR(boundary):                     #working
    """
    free edge on the right side
    returns probabilty of filling the hole
    """
    global tile
    global probs
    global elbows
    global lines
    
    probability = 0
    placeL = (boundary[0], boundary[1])
    placeR = (boundary[2],)
    
    #blank tile branch
    a = b = 0
    keepBL = whichTile2From(placeL, [tile[0]], 'L')     #left placement
    if keepBL != ():
        secondBRBoundary = (keepBL[2], boundary[2])
        probBLR = oneTile2Det(secondBRBoundary)
    keepBR = whichTile1From(placeR, [tile[0]])           #right placement
    if keepBR != ():
       secondBLBoundary = (boundary[0], boundary[1], keepBR[0])
       probBRL = oneTile3Det(secondBLBoundary)
    choice1st = (len(keepBL) + len(keepBR)) / 4
    if keepBL != ():
        a = probs[keepBL] * (1 / choice1st) * probBLR   
        probability += a  
    if keepBR != ():
        b = probs[keepBR] * (1 / choice1st) * probBRL
        probability += b
    #print('...blank branch =', a + b)   
  
    #crossing branch    
    c = d = 0
    keepCL = whichTile2From(placeL, [tile[7]], 'L')
    if keepCL != ():
        secondCRBoundary = (keepCL[2], boundary[2])
        probCLR = oneTile2Det(secondCRBoundary)
    keepCR = whichTile1From(placeR, [tile[7]])          
    if keepCR != ():
       secondCLBoundary = (boundary[0], boundary[1], keepCR[0])
       probCRL = oneTile3Det(secondCLBoundary)
    choice1st = (len(keepCL) + len(keepCR)) / 4
    if keepCL != ():
        c = probs[keepCL] * (1 / choice1st) * probCLR
        probability += c
    if keepCR != ():
        d = probs[keepCR] * (1 / choice1st) * probCRL
        probability += d
    #print('...crossing branch =', c + d)
   
    #elbow branch
    e = f = g = 0
    keepEL = whichTile2From(placeL, elbows, 'L')              
    if keepEL != ():
        secondERBoundary = (keepEL[2], boundary[2])
        probELR = oneTile2Det(secondERBoundary) #two tiles
    keepER = whichTile1From(placeR, elbows) #two tiles     
    if keepER != ():                                                #only branch that can have 2 options for R
       secondELBoundary1 = (boundary[0], boundary[1], keepER[0][0])
       probERL1 = oneTile3Det(secondELBoundary1)
       secondELBoundary2 = (boundary[0], boundary[1], keepER[1][0])
       probERL2 = oneTile3Det(secondELBoundary2)
    choice1st = (len(keepEL) / 4) + len(keepER)
    if keepEL != ():
        e = probs[keepEL] * (1 / choice1st) * probELR
        probability += e 
    if keepER != ():
        f = probs[keepER[0]] * (1 / choice1st) * probERL1
        g = probs[keepER[1]] * (1 / choice1st) * probERL2
        probability += f + g
    #print('...elbow branch =', e + f + g )
   
    #line branch
    h = i = 0
    keepLL = whichTile2From(placeL, lines, 'L')     #left placement
    if keepLL != ():
        secondLRBoundary = (keepLL[2], boundary[2])
        probLLR = oneTile2Det(secondLRBoundary)
    keepLR = whichTile1From(placeR, lines)           #right placement
    if keepLR != ():
       secondLLBoundary = (boundary[0], boundary[1], keepLR[0])
       probLRL = oneTile3Det(secondLLBoundary)
    choice1st = (len(keepLL) + len(keepLR)) / 4
    if keepLL != ():
        h = probs[keepLL] * (1 / choice1st) * probLLR      
        probability += h
    if keepLR != ():
        i = probs[keepLR] * (1 / choice1st) * probLRL
        probability += i
    #print('...line branch =', h + i) 
    return probability 

def twoTileV3Det(boundary):                     #working
    """
    boundary is a 3-element tuple
    returns the probability of filling the hole
    """
    global tile
    global probs
    global elbows
    global lines
    
    firstPlace = (boundary[1], boundary[2])
    probability = 0
    
    keepB = whichTile2From(firstPlace, [tile[0]], 'L')
    if keepB != ():
        secondBPlace = (boundary[0], keepB[1])
        keepB2nd = whichTile2(secondBPlace)
        probability += probs[keepB] * (1 / 2) * (probs[keepB2nd[0]] + probs[keepB2nd[1]])
        
    keepC = whichTile2From(firstPlace, [tile[7]], 'L')
    if keepC != ():
        secondCPlace = (boundary[0], keepC[1])
        keepC2nd = whichTile2(secondCPlace)
        probability += probs[keepC] * (1 / 2) * (probs[keepC2nd[0]] + probs[keepC2nd[1]])
        
    keepE = whichTile2From(firstPlace, elbows, 'L')
    if keepE != ():
        secondEPlace = (boundary[0], keepE[1])
        keepE2nd = whichTile2(secondEPlace)
        probability += probs[keepE] * (1 / 2) * (probs[keepE2nd[0]] + probs[keepE2nd[1]])
        
    keepL = whichTile2From(firstPlace, lines, 'L')
    if keepL != ():
        secondLPlace = (boundary[0], keepL[1])
        keepL2nd = whichTile2(secondLPlace)
        probability += probs[keepL] * (1 / 2) * (probs[keepL2nd[0]] + probs[keepL2nd[1]])
    return probability 


#functions below this line are still being written
def threeTileV4Det(boundary):                     #IN PROGRESS
    """
    boundary is a 4 tuple
    returns the probability of filling the hole
    """
    global tile
    global probs
    global elbows
    global lines
    
    firstPlace = (boundary[1], boundary[2])
    probability = 0
    #blank branch
    keepB = whichTile2From(firstPlace, [tile[0]], 'L')
    if keepB != ():
        secondBPlace = (boundary[0], keepB[1])
        keepB2nd = whichTile2(secondBPlace)
        thirdBPlace = (boundary[0], keepB2nd[1])
        keepB3rd = whichTile2(thirdBPlace)
        probability += probs[keepB] * (1 / 2) * (probs[keepB2nd[0]] + probs[keepB2nd[1]]) * (1 / 2) * (probs[keepB3rd[0]] + probs[keepB3rd[1]])
    #crossing branch    
    keepC = whichTile2From(firstPlace, [tile[7]], 'L')
    if keepC != ():
        secondCPlace = (boundary[0], keepC[1])
        keepC2nd = whichTile2(secondCPlace)
        thirdCPlace = (boundary[0], keepC2nd[1])
        keepC3rd = whichTile2(thirdCPlace)
        probability += probs[keepC] * (1 / 2) * (probs[keepC2nd[0]] + probs[keepC2nd[1]]) * (1 / 2) * (probs[keepC3rd[0]] + probs[keepC3rd[1]])
    #elbow branch    
    keepE = whichTile2From(firstPlace, elbows, 'L')
    if keepE != ():
        secondEPlace = (boundary[0], keepE[1])
        keepE2nd = whichTile2(secondEPlace)
        thirdEPlace = (boundary[0], keepE2nd[1])
        keepE3rd = whichTile2(thirdEPlace)
        probability += probs[keepE] * (1 / 2) * (probs[keepE2nd[0]] + probs[keepE2nd[1]]) * (1 / 2) * (probs[keepE3rd[0]] + probs[keepE3rd[1]])
    #line branch    
    keepL = whichTile2From(firstPlace, lines, 'L')
    if keepL != ():
        secondLPlace = (boundary[0], keepL[1])
        keepL2nd = whichTile2(secondLPlace)
        thirdLPlace = (boundary[0], keepL2nd[1])
        keepL3rd = whichTile2(thirdLPlace)
        probability += probs[keepL] * (1 / 2) * (probs[keepL2nd[0]] + probs[keepL2nd[1]]) * (1 / 2) * (probs[keepL3rd[0]] + probs[keepL3rd[1]])
    print('threeTileV4Det is still being written')        
    return probability 


def threeTileL6Det(boundary):                    #IN PROGRESS
    """
    returns random probability 
    """
    global probs
    global tile
    global elbows
    global lines
    
    probability = 0
    placeL = (boundary[0], boundary[1])
    placeR = (boundary[2], boundary[3], boundary[4])  
    checkTypes = ['blank', 'crossing', 'elbow', 'line']
    
    #right placement
    keepR = whichTile3(placeR)
    #print('keepR', keepR)
    twoTileH = (boundary[0], boundary[1], keepR[1], boundary[5])
    #check if valid left placement within tile type for keepR               
    keepL = ()
    if keepR == tile[0][1]:
        keepL = whichTile2From(placeL, [tile[0]], 'L')
        completed = 'blank'
    elif keepR == tile[7][1]:
        keepL = whichTile2From(placeL, [tile[7]], 'L')
        completed = 'crossing'
    elif keepR in [tile[1][1], tile[2][1], tile[3][1], tile[4][1]]:
        keepL = whichTile2From(placeL, elbows, 'L')
        completed = 'elbow'
    elif keepR in [tile[5][1], tile[6][1]]:
        keepL = whichTile2From(placeL, lines, 'L') 
        completed = 'line'
    
    choice = (len(keepR) + len(keepL)) / 4
    probability += (1 / choice) * probs[keepR] * twoTileH4Det(twoTileH)
    if keepL != (): 
        checkTypes.remove(completed)
        twoTileV = (keepL[2], boundary[2], boundary[3], boundary[4], boundary[5])
        probability += (1 / choice) * probs[keepL] * twoTileV5Det(twoTileV)
        wackPick = (1 / choice) * probs[keepL] * twoTileV5Det(twoTileV)
        smartPick = (1 / choice) * probs[keepR] * twoTileH4Det(twoTileH)
 
    #elbow branch
    if 'elbow' in checkTypes: 
        keepEL = whichTile2From(placeL, elbows, 'L')
        if keepEL != ():
            twoTileV = (keepEL[2], boundary[2], boundary[3], boundary[4], boundary[5])
            probability += probs[keepEL] * twoTileV5Det(twoTileV)
    
    #line branch
    if 'line' in checkTypes: 
        keepLL = whichTile2From(placeL, lines, 'L')
        if keepLL != ():
            twoTileV = (keepLL[2], boundary[2], boundary[3], boundary[4], boundary[5])
            probability += probs[keepLL] * twoTileV5Det(twoTileV)
    #blank branch
    if 'blank' in checkTypes:
        keepBL = whichTile2From(placeL, [tile[0]], 'L')
        if keepBL != ():
            twoTileV = (keepBL[2], boundary[2], boundary[3], boundary[4], boundary[5])
            probability += probs[keepBL] * twoTileV5Det(twoTileV)
    #crossing branch
    if 'crossing' in checkTypes: 
        keepCL = whichTile2From(placeL, [tile[7]], 'L')
        if keepCL != ():
            twoTileV = (keepCL[2], boundary[2], boundary[3], boundary[4], boundary[5])
            probability += probs[keepCL] * twoTileV5Det(twoTileV)
    
    if keepL != ():         
        smartProbability = probability - wackPick + smartPick  
    else: 
        smartProbability = probability 
    
    print('threeTileL6Det is still being written')
    return ('random probability:', probability, 'smart probability:', smartProbability)


def threeTileL6Det(boundary):                    #IN PROGRESS
    global probs
    global tile
    global elbows
    global lines
    
    probability = 0
    placeL = [boundary[0], boundary[1]]
    placeR = [boundary[2], boundary[3], boundary[4]]
    
    print('threeTileL6Det is still being written')       
    return  probability 


def threeTileL5DetFree(boundary, freeEdge):       #IN PROGRESS
    """
    """
    probability = 0
    print('threeTileL5DetFree is still being written')
    return probability 

def threeTileL5DetL(boundary):                   #IN PROGRESS
    """
    """
    probability = 0
    print('threeTileL5DetL is still being written')
    return probability

def threetileL4DetR(boundary):                  #IN PROGRESS
    """
    single free edge
    """
    probability = 0
    print('threetileL4DetR is still being written')
    return probability