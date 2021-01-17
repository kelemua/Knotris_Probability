"""
Created on Tue Dec 17 15:21:56 2019
Last Modified: 1/20/2020                                   

This code: 
- Assembles all row permutations of a given cluster of tiles 
- Keeps only the rows that are suitably connected  
- Records the unique boundary conditions and corresponding frequency among the rows 

@author: Kelemua Tesfaye
"""

#tiles are defined as 2-element tuples, where the 1st tuple is the tile label and 
    #the second tuple defines the tile edge info
#tiles are defined as tuple summarizing edge info (Left,Top,Right,Bottom,Crossing)
    #if Left, Top, Right, or Bottom is 1 there is a CP along that edge of the tile
    #if Left, Top, Right, or Bottom is 0 there is no CP along that edge of the tile
    #if Crossing = 1, there is a crossing on the tile
        #if Crossing = 0, there is not crossing on the tile 
#only concerned with tiles being suitably connected (SC) thus tiles 7-10 are 
    #equivalent with respect to connection points so we will only consider tile 7 

#tile dictionary contains 11 knot mosaic tiles 
tiles = {}
tiles['t0'] = ('blank', (0,0,0,0,0)) 

tiles['t1'] = ('elbow bottom left', (1,0,0,1,0))
tiles['t2'] = ('elbow bottom right', (0,0,1,1,0))  
tiles['t3'] = ('elbow top right', (0,1,1,0,0)) 
tiles['t4'] = ('elbow top left', (1,1,0,0,0)) 

tiles['t5'] = ('horizontal', (1,0,1,0,0)) 
tiles['t6'] = ('vertical', (0,1,0,1,0)) 

tiles['t7'] = ('double elbow along right diagonal', (1,1,1,1,0)) 
#tiles['t8'] = ('double elbow along left diagonal', (1,1,1,1,0)) 
#tiles['t9'] = ('crossVUnder', (1,1,1,1,1)) 
#tiles['t10'] = ('crossVOver', (1,1,1,1,1)) 

#equivalence classes wrt rotation
elbows = [tiles['t1'][1], tiles['t2'][1], tiles['t3'][1], tiles['t4'][1]]
lines = [tiles['t4'][1], tiles['t6'][1]]

"""
#find all boundary conditions for a 6x1 row
pickCP = [0,1]
boundarypick = [pickCP, pickCP, pickCP, pickCP, pickCP, pickCP]
from itertools import product 
boundaryCombs = list(product(*boundarypick)) 
"""

def combs(cluster):
    """
    Combs takes a list of tiles as a parameter, and returns clusterCombs, a 
    list of the cartesian product of the tiles. The cartesian product of tiles 
    is the combination of all tiles.
    """
    global clusterCombs
    
    from itertools import product 
    
    clusterCombs = list(product(*cluster)) #list of tuples
    print('number of combinations:', len(clusterCombs))
    return clusterCombs


def perms(combs):
    """
    Perms takes a list of all combinations of tiles as a parameter, and returns
    a list of all permuatations (all rows). 
    """
    global clusterPerms
    global clusterPermsUpperBoundary
    
    from itertools import permutations
    
    clusterPerms = []
    for cluster in combs:
        clusterPerms += permutations(cluster)
    print('number of permutations:', len(clusterPerms))
    
    ###here to find an error
    clusterPermsUpperBoundary = []
    for i in range(len(clusterPerms)):
        rowBoundary = []
        for j in range(len(clusterPerms[i])):
            rowBoundary.append(clusterPerms[i][j][1])    
        clusterPermsUpperBoundary.append(tuple(rowBoundary))  
    return clusterPerms


def checkSC(clusterPerms):
    """
    CheckSC takes list of permutations (rows) as a parameter, and retuns a list of the 
    suitably connected (SC) permutations (rows). 
    """
    global clusterPermsSC
    
    clusterPermsNSC = [] 
    clusterPermsSC = []
    for i in range(len(clusterPerms)):
        suitablyConn = True
        for j in range(len(clusterPerms[i]) - 1):
            if clusterPerms[i][j][2] != clusterPerms[i][j+1][0]:
                suitablyConn = False
                clusterPermsNSC.append(clusterPerms[i])
                break
        if suitablyConn == True:
            clusterPermsSC.append(clusterPerms[i])

    print('number of NSC permutations:', len(clusterPermsNSC))       
    print('number of SC permutations:',len(clusterPermsSC))
    return clusterPermsSC


def boundary(clusterPermsSC):      
    """
    Boundary takes a list of SC permutations as a parameter, and returns a list
    of the upper boundary information of each row.
    """
    global clusterPermsSCBoundary
    global duplicateBoundary
    
    global boundaryCounter
    
    clusterPermsSCBoundary = []
    for i in range(len(clusterPermsSC)):
        rowBoundary = []
        for j in range(len(clusterPermsSC[i])):
            rowBoundary.append((clusterPermsSC[i][j][1]))        
        clusterPermsSCBoundary.append(tuple(rowBoundary))
    
    print('size of the set of boundary conditions of SC permutations:',len(set(clusterPermsSCBoundary))) 
    print('number of duplicate boundaries of SC permutations:', 
              len(clusterPermsSCBoundary) - len(set(clusterPermsSCBoundary)) )
    
    #here to find an error
    print('boundary counter')
    boundaryCounter = {}  
    for boundary in clusterPermsSCBoundary:
        if boundary in boundaryCounter.keys():
            boundaryCounter[boundary] += 1
        else:
            boundaryCounter[boundary] = 1
    for i in boundaryCounter:
        print(i, boundaryCounter[i])
    ###
    
    if len(clusterPermsSCBoundary) != len(set(clusterPermsSCBoundary)):    
        print('\nduplicate boundary conditions and the number of corresponding permutations')    
        duplicateBoundary = {}
        for boundary in clusterPermsSCBoundary:
            if boundary in duplicateBoundary.keys():
                duplicateBoundary[boundary] += 1
            else: 
                duplicateBoundary[boundary] = 1
        duplicateBoundary = {key:value for key,value in duplicateBoundary.items() if value > 1} 
        for i in duplicateBoundary: 
            print(i, duplicateBoundary[i])
    return clusterPermsSCBoundary


def writeIntoCSV(boundaryCounter):#FIX ME!!
    """
    Writes boundary conditions and frequencies into csv
    **when opened in excel need to delete empty rows in array
    """
    import csv
    
    with open('fix.csv', mode='w') as csv_file:
        fieldnames = ['Boundary', 'Frequency']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
        writer.writeheader()
        for key in boundaryCounter:
            writer.writerow({'Boundary': key, 'Frequency': boundaryCounter[key]})
        
    """
    global boundaryCombs
    boundaryFrequency = []
    for boundary in boundaryCombs: 
        boundaryTagged = {}
        boundaryTagged['boundary'] = boundary
        if boundary in duplicateBoundary:
            boundaryTagged['frequency'] = duplicateBoundary[boundary]
        else:
            boundaryTagged['frequency'] = 0
        boundaryFrequency.append(boundaryTagged)

    fields = ['boundary', 'frequency']
    filename = "boundary_frequency_TEMP.csv"
      
    with open(filename, 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader()           
        writer.writerows(boundaryFrequency) 
    """
    return 


"""
confirms catches all boundaries
sum = 0
for i in duplicateBoundary:
    print(duplicateBoundary[i])
    sum += duplicateBoundary[i]
print('sum', sum)
"""

if __name__ == '__main__':

    #7 tile distribution: 1 of crossing, swoop, and blank
    #                     2 of elbows and lines 
    #6 tile bags are all combinations of 1 tile omitted from the 7 tile distribution 
    #o???, where ??? is name of tile omited so oBlank doesn't include a blank tile 
    oBlank = [elbows,
              elbows,
              lines,
              lines,
              [tiles['t7'][1]],
              [tiles['t7'][1]]]
    
    oElbow = [[tiles['t0'][1]],
              elbows,
              lines,
              lines,
              [tiles['t7'][1]],
              [tiles['t7'][1]]]
    
    oLine = [[tiles['t0'][1]],
              elbows,
              elbows,
              lines,
              [tiles['t7'][1]],
              [tiles['t7'][1]]]
    
    oCrossing = [[tiles['t0'][1]],
              elbows,
              elbows,
              lines,
              lines,
              [tiles['t7'][1]]]
    
    #6 tiles cluster only containing one type of tile 
    #a???, where ??? is the tile type in the list
    aBlank = [[tiles['t0'][1]], [tiles['t0'][1]], [tiles['t0'][1]], [tiles['t0'][1]], [tiles['t0'][1]] ,[tiles['t0'][1]]]
    aLine = [lines, lines, lines, lines, lines, lines]
    aElbow = [elbows, elbows, elbows, elbows, elbows, elbows]
    aCrossing = [[tiles['t7'][1]],[tiles['t7'][1]],[tiles['t7'][1]],[tiles['t7'][1]],[tiles['t7'][1]],[tiles['t7'][1]]]
    
    
    #Enter a tiLe cluster as a list
        #NOTE: all elements of the list need to be a list even if it is a 
        #       single tile, see oBlank for reference
    cluster = oElbow

    combs(cluster)
    perms(clusterCombs)    
    checkSC(clusterPerms)
    boundary(clusterPermsSC)
    writeIntoCSV(boundaryCounter)


"""
#find all boundary conditions for a 1x6 row
    pickCP = [0,1]
    boundarypick = [pickCP, pickCP, pickCP, pickCP, pickCP, pickCP]
    
    from itertools import product 
    boundaryCombs = list(product(*boundarypick)) 
"""
"""
test cluster = [[tiles['t0'][1]],[tiles['t7'][1]],elbows] 

expected output, verified by hand
number of combinations: 4
number of permutations: 24
number of NSC permutations: 20
number of SC permutations: 4
size of the set of boundary conditions of SC permutations: 4
number of duplicate boundaries of SC permutations: 0

"""

#def color(clusterPermsSCBoundary): #N/A 
#    """
#    Color takes a list of boundary information of SC permutations, and prints
#    color coded boundaries as red and black pair of lines corresponding to a 
#    crossing point and not respectively.
#    """
#    from colorama import Fore, Style
#    
#    for i in range(len(set(clusterPermsSCBoundary))):
#        for j in range(len(clusterPermsSCBoundary[i])):
#            if clusterPermsSCBoundary[i][j][0] == 1:
#                print(Fore.RED + '--', end = ' ')
#            else: 
#                print(Fore.BLACK + '--', end = ' ')
#        print()
#        for j in range(len(clusterPermsSCBoundary[i])):
#            if clusterPermsSCBoundary[i][j][1] == 1:
#                print(Fore.RED + '--', end = ' ')
#            else: 
#                print(Fore.BLACK + '--', end = ' ')
#        print('\n')
#        
#    print(Style.RESET_ALL)
#    return
