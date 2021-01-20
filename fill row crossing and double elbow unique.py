# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 14:46:51 2021

This code excutes the filling a row algorithm. 

@author: Kelemua Tesfaye
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
elbows = [tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1]]
lines = [tiles['t4'][1], tiles['t6'][1]]

#try with individual tiles instead of equivalence classes
#defined bags using individual tiles instead of equivalence classes 
sevenTileBag = [tiles['t0'][1], #blank
                
                tiles['t4'][1], tiles['t6'][1], #line class
                tiles['t4'][1], tiles['t6'][1], #line class
                
                tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class
                tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class
                
                tiles['t7'][1], #double elbow
                tiles['t9'][1], #crossing
                ]

#gamebag is composed of 3 of the 7-tle bags 
gamebag = [tiles['t0'][1], #blank
           tiles['t0'][1], 
           tiles['t0'][1], 
           
           tiles['t4'][1], tiles['t6'][1], #line class
           tiles['t4'][1], tiles['t6'][1], 
           tiles['t4'][1], tiles['t6'][1], 
           tiles['t4'][1], tiles['t6'][1], 
           tiles['t4'][1], tiles['t6'][1], 
           tiles['t4'][1], tiles['t6'][1], 
           
           tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class
           tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
           tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
           tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
           tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
           tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
           
           tiles['t7'][1], #double elbow
           tiles['t7'][1], 
           tiles['t7'][1], 
           tiles['t9'][1], #crossing
           tiles['t9'][1], 
           tiles['t9'][1]
          ]

#6-tile bags are all combinations of 1 tile omitted from the 7 tile distribution 
#o???, where ??? is name of tile omited so oBlank doesn't include a blank tile 
oBlank = [tiles['t4'][1], tiles['t6'][1], #line class
          tiles['t4'][1], tiles['t6'][1], 
            
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
            
          tiles['t7'][1], #double elbow
          tiles['t9'][1], #crossing
         ]

oElbow = [tiles['t0'][1], #blank
          
          tiles['t4'][1], tiles['t6'][1], #line class
          tiles['t4'][1], tiles['t6'][1], 
          
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class 
          
          tiles['t7'][1], #double elbow
          tiles['t9'][1], #crossing
         ]

oLine = [tiles['t0'][1], #blank
         
         tiles['t4'][1], tiles['t6'][1], #line class
         
         tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class    
         tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class 
         
         tiles['t7'][1], #double elbow
         tiles['t9'][1], #crossing
        ]

#oCrossing and oDoubleElbow have equivalent results so will only define oCrossing bag
oCrossing = [tiles['t0'][1], #blank
             
             tiles['t4'][1], tiles['t6'][1], #line class
             tiles['t4'][1], tiles['t6'][1], 
             
             tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class    
             tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
             
             tiles['t7'][1], #double elbow
            ]

aBlank = [tiles['t0'][1], #blank
          tiles['t0'][1], 
          tiles['t0'][1], 
          tiles['t0'][1],
          tiles['t0'][1],
          tiles['t0'][1]
         ]
          
aElbow = [tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], #elbow class
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1], 
          tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1]
         ]
          
          
aLine = [tiles['t4'][1], tiles['t6'][1], #line class
         tiles['t4'][1], tiles['t6'][1], 
         tiles['t4'][1], tiles['t6'][1], 
         tiles['t4'][1], tiles['t6'][1], 
         tiles['t4'][1], tiles['t6'][1], 
         tiles['t4'][1], tiles['t6'][1]
        ]
         
aCrossing = [tiles['t9'][1], #crossing 
             tiles['t9'][1], 
             tiles['t9'][1], 
             tiles['t9'][1], 
             tiles['t9'][1], 
             tiles['t9'][1]
            ]


def combos(tilebag):
    """
    Combos accepts a tilebag, a list of tuples, as an argument and returns uniRowCombos, a list of the unique 
    6-tile combinations as a list of tuples.
    """
    global uniRowCombos
        
    from itertools import combinations
    
    rowCombos = list(combinations(tilebag,6))    #finds all 6-tile combinations using tilebag
    uniRowCombos = list(set(rowCombos))                #keeps uniique 6-tile combinations
    print('total number of 6-tile combinations:', len(rowCombos))
    print('number of unique 6-tile combinations:', len(uniRowCombos), '\n')    
    
    return uniRowCombos

def permuts(uniRowCombos):
    """
    Permuts accepts uniRowCombos, a list of the unique 6-tile combinations, as an argument and returns uniRowPermuts,
    a list of the unique permutations(or rows that can be assembled).
    permutations unique b/c combos were unique
    """
    global uniRowPermuts
    
    from itertools import permutations
       
    rowPermuts = []
    for row in uniRowCombos:
        rowPermuts += permutations(row)
    uniRowPermuts = list(set(rowPermuts))    
    print('number of permutations (rows):', len(rowPermuts))
    print('number of unique permutations (rows):', len(uniRowPermuts), '\n')
    
    return uniRowPermuts

def checkSC(uniRowPermuts):
    """
    CheckSC accepts uniRowPermuts as a an arugment, a list of unique rows, and returns a list of the suitably connected (SC) rows,
    uniRowPermutsSC. 
    
    CheckSC evaluates whether a row is internally suitably connected (SC) or not internally suitably connected (NSC) and sort it 
    into the appropriate list, uniRowPermutsSC or uniRowPermutsNSC. A row is internally suitably connected if the Left and Right edges of 
    the internal tiles have their connection points satisifed. Meaning, tiles with shared edges must have the same value for the edge in the 
    boundary condition they share. 
    """
    global uniRowPermutsSC
    global uniRowPermutsNSC
    
    uniRowPermutsSC = []
    uniRowPermutsNSC = []
    
    for i in range(len(uniRowPermuts)):
        suitablyConn = True
        for j in range(len(uniRowPermuts[i]) - 1):
            if uniRowPermuts[i][j][2] != uniRowPermuts[i][j+1][0]:
                suitablyConn = False
                uniRowPermutsNSC.append(uniRowPermuts[i])
                break
        if suitablyConn == True:
                uniRowPermutsSC.append(uniRowPermuts[i])
                
    print('number of unique not suitably connected (NSC) rows:', len(uniRowPermutsNSC))
    print('number of unique suitably connected (SC) rows:', len(uniRowPermutsSC), '\n')

    return uniRowPermutsSC

def boundary(uniRowPermutsSC):
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
    for i in range(len(uniRowPermutsSC)): 
        rowBoundary = []
        for j in range(len(uniRowPermutsSC[i])):
            rowBoundary.append(uniRowPermutsSC[i][j][1])
        boundarySC.append(tuple(rowBoundary))
    print('number of duplicate boundary conditions:', len(boundarySC) - len(set(boundarySC)))
   
    #record boundary conditions and respective frequency in unique rows
    boundaryCounter = {}
    for boundary in boundarySC:
        if boundary in boundarySC:
            if boundary in boundaryCounter.keys():
                boundaryCounter[boundary] += 1
            else:
                boundaryCounter[boundary] = 1
    print('\nAll Boundary Conditions')          #Comment out FROM this line...
    print('Boundary Condition|Frequency')       
    for i in rowBoundaries:                     
        if i in boundaryCounter:
            print(i, boundaryCounter[i])    
        else: 
            print(i, 0)                         #...THROUGH this line if output is too long
    
    #condensed BCs composed of single BC from each symmetric pair 
        #For example (0,0,0,0,0,1) and (1,0,0,0,0,0) are a symmetric pair and only (0,0,0,0,0,1) will be displayed
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



#NOTE: Console may not be able to see entriety of print statements becuase of length
    #If you would like ot view all print statements at once consider:
        #1)Commenting lines 266-272 (if lines don't match up perfectly there is a note at the lines where to comment)  -OR-
        #2)Running a few bags at a time
#NOTE: NONE of the arguments of the functions should be changed only the value of bag 
print('\n**GAMEBAG**')
bag = gamebag      #can use any of the bags defined at the top or any list of 6 or more 4-element tuples 
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**SEVEN TILE BAG**')
bag = sevenTileBag
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

#oBags
print('\n**OBLANK BAG**')
bag = oBlank
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**OELBOW BAG**')
bag = oElbow
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**OLINE BAG**')
bag = oLine
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**OCROSSING BAG**')
bag = oCrossing
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

#aBags
print('\n**ABLANK BAG**')
bag = aBlank
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**AELBOW BAG**')
bag = aElbow
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**ALINE BAG**')
bag = aLine
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)

print('\n**ACROSSING BAG**')
bag = aCrossing
combos(bag)    
permuts(uniRowCombos)
checkSC(uniRowPermuts)
boundary(uniRowPermutsSC)