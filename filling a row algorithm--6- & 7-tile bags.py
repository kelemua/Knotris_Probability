# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 09:07:27 2020

@author: kelem
"""
#Dictionary defining the 11 knot mosaic tiles   
    #The key of the dictionary is a tile ID, and the key is a tuple, where the 1st element is a decription of the tile, 
    #and the 2nd is a tuple BC. 
    #Boundary Condition of the tile is defined as (Left, Top, Right, Bottom) where 1 indicates there is a CP a 0 indicates
    #there is no CP. 
    
    #Since we are only concerned with suitably connectedness, and tiles 7-10 have the same connection points (CP). 
    #We can reduce the 11 knot mosaic tiles to 7 tiles, since tiles 7 through 10 have the same boundary conditions (BC). 
    #However, during gameplay tiles 7 & 8 (double elbow tile) and iles 9 & 10 (crossing tile) appear unique. 
    #Therefore to define rows that will appear unique to the player during gameplay we will consider both tiles
    #7 & 9. In order to represent them as unique, the crossing tile's BC will have a 5th element with a value of 1 
    #indicating the tile has a crossing. 
    
tiles = {}
tiles['t0'] = ('blank', (0,0,0,0)) 

tiles['t1'] = ('elbow bottom left', (1,0,0,1))
tiles['t2'] = ('elbow bottom right', (0,0,1,1))  
tiles['t3'] = ('elbow top right', (0,1,1,0)) 
tiles['t4'] = ('elbow top left', (1,1,0,0)) 

tiles['t5'] = ('horizontal line', (1,0,1,0)) 
tiles['t6'] = ('vertical line', (0,1,0,1)) 

tiles['t7'] = ('double elbow along right diagonal', (1,1,1,1)) 
#tiles['t8'] = ('double elbow along left diagonal', (1,1,1,1)) 
tiles['t9'] = ('crossVUnder', (1,1,1,1,1))      #the BC tuple has an additional element to indicate it's a crossing tile
#tiles['t10'] = ('crossVOver', (1,1,1,1)) 

#equivalence classes defined by rotation equivalence 
blank = [tiles['t0'][1]]
elbows = [tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1]]
lines = [tiles['t5'][1], tiles['t6'][1]]
fourConn = [tiles['t7'][1], tiles['t9'][1]]     #the crossing & double elbow tiles are not equivalent in terms of CPs

#define oBags, 6-tile bags with a single tile type from 7-tile bag omitted
oBlank = [elbows, elbows, lines, lines, fourConn, fourConn]
oElbow = [blank, elbows, lines, lines, fourConn, fourConn]
oLine = [blank, elbows, elbows, lines, fourConn, fourConn]
oFourConn = [blank, elbows, elbows, lines, lines, fourConn]

oBags = [oBlank, oElbow, oLine, oFourConn]

#define aBags, 6-tile bags composed of a single tile type
aBlank = [blank, blank, blank, blank, blank, blank]
aElbow = [elbows, elbows, elbows, elbows, elbows, elbows]
aLine = [lines, lines, lines, lines, lines, lines]
aFourConn = [fourConn, fourConn, fourConn, fourConn, fourConn, fourConn]

aBags = [aBlank, aElbow, aLine, aFourConn]

#define 7-tile bag we found to lead to the most natural gameplay
sevenTileBag = [blank, elbows, elbows, lines, lines, fourConn, fourConn]

#def combs6(cluster): #appears slower than function below
#    """
#    Combs takes a list of 6 tiles as a parameter, and returns clusterCombs, a 
#    list of the cartesian product of the tiles. 
#    **likely able to rewrite function to accomodate larger bags such that the 
#    cartesian product of the tiles is found then the unique combination tiles 
#    of a select quantity of tiles. This would be particularly helpful in 
#    evaluating the 7-tile bag
#    """
#    global clusterCombs
#    global uniClusterCombs
#    
#    import itertools 
#    clusterCombs = list(itertools.product(*cluster))
#    
#    #clusterCombs = list(product(*cluster)) #list of tuples
#    uniClusterCombs = list(set(clusterCombs))
#    print('number of combinations:', len(clusterCombs))
#    print('number of unique combinations:', len(uniClusterCombs))
#    return uniClusterCombs

def combs(bag):
    """
    Combs accept bag, a list of tuples representing a 6- or 7-tile bag, as a parameter, 
    find the cartesian product of tiles in the bag, and returns the unique 6-tile 
    combinations that can be assembled, uniClusterCombs.
    """
    global clusterCombs
    global uniClusterCombs
    global uniCartProduct
    
    from itertools import combinations
    
    if len(bag) == 6:
        cartProduct = [(a,b,c,d,e,f) for a in bag[0] for b in bag[1] for c in bag[2] for d in bag[3] for e in bag[4] for f in bag[5]]
        uniCartProduct = list(set(cartProduct))
    if len(bag) == 7:
        cartProduct = [(a,b,c,d,e,f,g) for a in bag[0] for b in bag[1] for c in bag[2] for d in bag[3] for e in bag[4] for f in bag[5] for g in bag[6]]
        uniCartProduct = list(set(cartProduct))
    
    clusterCombs = []
    for product in uniCartProduct:
        clusterCombs += list(combinations(product,6))
        
    uniClusterCombs = list(set(clusterCombs))             
    print('total number of 6-tile combinations:', len(clusterCombs))
    print('number of unique 6-tile combinations:', len(uniClusterCombs), '\n')    
      
    return uniClusterCombs

def perms(uniClusterCombs):
    """
    Perms takes a list of all combinations of tiles as a parameter, and returns
    a list of all permuatations. 
    """
    global uniClusterPerms
    
    from itertools import permutations
    
    clusterPerms = []
    for cluster in uniClusterCombs:
        clusterPerms += permutations(cluster)
    print('number of permutations:', len(clusterPerms))
    uniClusterPerms = list(set(clusterPerms))
    print('number of unique permutations:', len(uniClusterPerms))
    return uniClusterPerms

def checkSC(uniClusterPerms):
    """
    CheckSC takes list of permutations as a parameter, and retuns a list of the 
    SC permutations. 
    """
    global uniClusterPermsSC
    global uniClusterPermsNSC
    
    uniClusterPermsNSC = [] 
    uniClusterPermsSC = []

    for row in uniClusterPerms:
        if row[0][2]==row[1][0] and row[1][2]==row[2][0] and row[2][2]==row[3][0] and row[3][2]==row[4][0] and row[4][2]==row[5][0]:
            uniClusterPermsSC.append(row)
        else: 
            uniClusterPermsNSC.append(row)
    
#    for i in range(len(uniClusterPerms)):
#        suitablyConn = True
#        for j in range(len(uniClusterPerms[i]) - 1):
#            if uniClusterPerms[i][j][2] != uniClusterPerms[i][j+1][0]:
#                suitablyConn = False
#                uniClusterPermsNSC.append(uniClusterPerms[i])
#                break
#        if suitablyConn == True:
#            uniClusterPermsSC.append(uniClusterPerms[i])

    print('number of unique NSC rows (permutations):', len(uniClusterPermsNSC))       
    print('number unique of SC rows (permutations):',len(uniClusterPermsSC))

    return uniClusterPermsSC

def boundary(uniClusterPermsSC):    
    """
    Boundary accepts uniRowPermutsSC, a list of suitably connected rows, as an argument, and returns boundarySC,
    a list of the lower boundary conditions of the suitably connected rows. Boundary also prints a summary of 
    the boundary conditions and respective frequency among the unique suitably connected rows, in a long form 
    list containing all 64 BCs and a condensed list of 36 BCs.
    """
    global boundarySC
    global boundaryCounter
    global rowBoundaries
    
    boundarySC = []
    
    from itertools import product

    #creates all possible boundary conditions for a row
    pickCP = [0,1]
    pickBoundary = [pickCP, pickCP, pickCP, pickCP, pickCP, pickCP]
    rowBoundaries = list(product(*pickBoundary)) #list of 6-element tuples
    
    #records upper boundary conditions of each row
        #doesn't matter if upper or boundary condition recorded b/c of symmetry
    for i in range(len(uniClusterPermsSC)): 
        rowBoundary = []
        for j in range(len(uniClusterPermsSC[i])):
            rowBoundary.append(uniClusterPermsSC[i][j][1])
        boundarySC.append(tuple(rowBoundary))
    print('number of duplicate boundary conditions:', len(boundarySC) - len(set(boundarySC)))
   
    #record boundary conditions and respective frequency in unique rows
    boundaryCounter = {}
    for boundary in boundarySC:
        if boundary in boundaryCounter:
            boundaryCounter[boundary] += 1
        else:
            boundaryCounter[boundary] = 1
#    print('\nAll Boundary Conditions')          #Comment out FROM this line...
#    print('Boundary Condition|Frequency')       
#    for i in rowBoundaries:                     
#        if i in boundaryCounter:
#            print(i, boundaryCounter[i])    
#        else: 
#            print(i, 0)                         #...THROUGH this line if output is too long
    
    #condensed BCs composed of single BC from each symmetric pair 
        #For example (0,0,0,0,0,1) and (1,0,0,0,0,0) are a symmetric pair and only (0,0,0,0,0,1) will be displayed
        #no information about results is lost, just eliminates redundancy
    print('\nCondensed Boundary Conditions')      #condensed boundary conditions 
    print('Boundary Condition|Frequency')       
    condensedRowBoundaries = []    
    for boundaryCond in rowBoundaries:
        if (boundaryCond[5], boundaryCond[4], boundaryCond[3], boundaryCond[2], boundaryCond[1], boundaryCond[0]) not in condensedRowBoundaries:
            condensedRowBoundaries.append(boundaryCond)
    for i in condensedRowBoundaries: 
        if i in boundaryCounter:
            print(i, boundaryCounter[i])
        else: 
            print(i, 0)
            
    return boundarySC

#NOTE: Console may not be able display entriety of print statements because of length
    #If you would like ot view BC and frequency of all bags once consider:
        #1)Commenting lines 196-202 (if lines don't match up perfectly there is a note at the lines where to comment)  to only show condensed outputs-OR-
        #2)Running a few bags at a time
#NOTE: NONE of the arguments of the functions should be changed only the value of bag print('\n**SEVEN TILE BAG**')
bag = sevenTileBag
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

#oBags
print('\n**OBLANK BAG**')
bag = oBlank
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

print('\n**OELBOW BAG**')
bag = oElbow
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

print('\n**OLINE BAG**')
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

print('\n**OFOURCONN BAG**')
bag = oFourConn
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

#aBags
print('\n**ABLANK BAG**')
bag = aBlank
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

print('\n**AELBOW BAG**')
bag = aElbow
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

print('\n**ALINE BAG**')
bag = aLine
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)

print('\n**ACROSSING BAG**')
bag = aFourConn
combs(bag)    
perms(uniClusterCombs)
checkSC(uniClusterPerms)
boundary(uniClusterPermsSC)