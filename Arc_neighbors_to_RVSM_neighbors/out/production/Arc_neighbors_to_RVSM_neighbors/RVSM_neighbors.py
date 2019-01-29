'''
Convert ARC neighbors output to RVSM neighbors input

Author: Todd Steissberg, Hydrologic Engineering Center (HEC), U.S. Army Corps of Engineers
May 2018
'''

def arcToRVSM_Neighbors(infile, outfile):
    # Open input and output files
    f = open(infile, 'r')
    g = open(outfile, 'w')

    # Initialize dictionary for collecting the ARC table input data
    # This will contain a list of neighbors for each source ID (dictionary key)
    NeighborID = {}

    # Read data
    lines = f.readlines()
    f.close()

    # Parse data, skipping the one header line
    print 'Reading ARC input data...'
    for line in lines[1:]:
        data = line.strip().split(',')
        data = map(int, data)

        # objectID = data[0]
        srcID = data[1]
        nbrID = data[2]

        # Append the neighbors for each object ID to a list, by object ID
        if srcID not in NeighborID.keys():
            NeighborID[srcID] = [nbrID]
        else:
            NeighborID[srcID].append(nbrID)

    # Get and sort list of keys
    srcKeys = NeighborID.keys()
    srcKeys.sort()

    # Compute and write maximum number of neighbors
    maxNumNeighbors = 0
    for polygonID in NeighborID.keys():
        neighborsList = NeighborID[polygonID]
        numNeighbors = len(neighborsList)
        if numNeighbors > maxNumNeighbors:
            maxNumNeighbors = numNeighbors
    # hline = "%d\n" % maxNumNeighbors # Left-aligned
    hline = "{0:>12d}\n".format(maxNumNeighbors, 12) # Right-alighed, to 12th column
    g.write(hline)

    # Write RVSM Vegetation Polygons file
    # Format:
    # sourceID, sourceCount, neighbor1, neighbor2, ...
    print 'Writing RVSM output data...'
    for srcID in srcKeys:
        neighbors = NeighborID[srcID]
        hline = "{0:>8d}".format(srcID, 8)
        hline += "{0:>8d}".format(len(neighbors), 8)
        for neighbor in neighbors:
            hline += "{0:>8d}".format(neighbor, 8)
        hline += '\n'
        g.write(hline)

    # Close output file
    g.close()

if __name__ == '__main__':
    infile = 'Neighbors_R9.csv'
    outfile = 'veg_polygon_neighbors.txt'
    arcToRVSM_Neighbors(infile, outfile)

