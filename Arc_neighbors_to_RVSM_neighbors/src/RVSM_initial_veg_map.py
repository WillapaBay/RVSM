'''
Convert ARC initial vegetation map output to RVSM initial vegetation map input

Author: Todd Steissberg, Hydrologic Engineering Center (HEC), U.S. Army Corps of Engineers
May 2018
'''

def initialVegMap(infile, outfile):
    # Open input and output files
    f = open(infile, 'r')
    g = open(outfile, 'w')

    # Initialize dictionaries for collecting the ARC table input data
    # These will contain a list for each polygon ID (dictionary key)
    CommunityID = {}
    PercentArea = {}

    # Read data
    lines = f.readlines()
    f.close()

    # Parse data, skipping one header row
    # Input file format:
    # NewID,Area,Veg_Com_No,Veg_Area,Per_Area
    print 'Reading ARC input data...'
    for line in lines[1:]:
        data = line.strip().split(',')
        polygonID = int(data[0])
        communityID = int(data[2])
        pctArea = float(data[4])

        # For each polygon ID, append the neighbors (communityID) to a list
        if polygonID not in CommunityID.keys():
            CommunityID[polygonID] = [communityID]
        else:
            CommunityID[polygonID].append(communityID)

        # For each polygon ID, append the percent area to a list
        if polygonID not in PercentArea.keys():
            PercentArea[polygonID] = [pctArea]
        else:
            PercentArea[polygonID].append(pctArea)

    # Write RVSM initial vegetation map file
    print 'Writing RVSM initial vegetation map output file...'

    # Compute and write maximum number of communities
    maxNumCommunities = 0
    for polygonID in CommunityID.keys():
        communityIDList = CommunityID[polygonID]
        numCommunities = len(communityIDList)
        if numCommunities > maxNumCommunities:
            maxNumCommunities = numCommunities
    hline = "%d\n" % maxNumCommunities # Left-aligned
    g.write(hline)

    # Get and sort list of keys
    keys = CommunityID.keys()
    keys.sort()

    # Write data lines to the output file
    # Format:
    # Polygon ID, Number of communities, Community ID #1, Percent Area #1, Community ID #2, Percent Area #2, ...
    for polygonID in keys:
        communityIDList = CommunityID[polygonID]
        percentAreaList = PercentArea[polygonID]
        numCommunities = len(communityIDList)
        hline = "{0:>8d}".format(polygonID, 8)
        hline += "{0:>8d}".format(numCommunities, 8)
        for (communityID, percentArea) in zip(communityIDList, percentAreaList):
            hline += "{0:>8d}{1:>8.4f}".format(communityID, percentArea)
        hline += '\n'
        g.write(hline)

    # Close output file
    g.close()

if __name__ == '__main__':
    infile = 'Prelim_Initial_Veg_0502_2018.csv'
    outfile = 'initialVeg_mapping_table.txt'
    initialVegMap(infile, outfile)

