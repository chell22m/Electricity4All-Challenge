#!/usr/bin/env python
"""
#Electricity4All Challenge
Monica Chelliah
    
TODO Description
"""

from ast import literal_eval
from collections import defaultdict
from copy import deepcopy
import csv as csv
import numpy as np
import pandas as pd
import time

def parseValue(parse_value):
    """
    Parse the given value from string to a Python literal if possible.
    Else, an error is printed out.
    
    @param parse_value: input to be parsed
    @type parse_value: List of str or str
    
    @return: return the input as actual types
    @rtype: List of variable type or variable type
    """
    try:
        if isinstance(parse_value, list):
            return [literal_eval(item) for item in parse_value]
        else:
            return literal_eval(parse_value)
    except ValueError, SyntaxError:
        print 'The following value cannot be parsed: {0}\nPlease check your input files.'.format(str(parse_value))

def readGISData(gis_input):
    """
    Read the GIS Input data, which should include the x and y location data,
    the population, along with the distance boundaries to be used for all the
    scenarios.
        
    @param gis_input: filepath to the GIS Input
    @type gis_input: str
    """
    gis_csv_file_obj = csv.reader(open(gis_input, 'rb'))
    
    # Read in distances
    gis_csv_file_obj.next()  # ignore header
    distance = parseValue(gis_csv_file_obj.next())

    # Read in X, Y, Pop
    gis_csv_file_obj.next()  # ignore header
    gis_data = []
    for row in gis_csv_file_obj:
        gis_data.append(parseValue([row[0], row[1], row[2]]))

    return distance, gis_data

def readScenarioData(scenario_input):
    """
    Read the Scenario input data, which should include the Number of People
    boundary conditions, as well as the current electricity status for each of
    the locations listed in the GIS Input file.
    
    @param scenario_input: filepath to the Scenario input
    @type scenario_input: str
    """
    sce_csv_file_obj = csv.reader(open(scenario_input, 'rb'))
    
    # Read in number of people
    sce_csv_file_obj.next()  # ignore header
    num_people = parseValue(sce_csv_file_obj.next())
    
    # Read in Electricity status
    sce_csv_file_obj.next()  # ignore header
    elec_status = []  # current electricity status
    cell_path = []  # keeps track of the km of lines built
    for row in sce_csv_file_obj:
        elec_status.append(parseValue(row[0]))
        cell_path.append([0,0])
    
    return num_people, elec_status, cell_path

def separateElecStatus(elec_status):
    """
    Separate out the electrified and unelectrified states from list
    
    @param elec_status: electricity status for each location
    @type elec_status: list of int
    """
    electrified = []
    unelectrified = []

    for i, status in enumerate(elec_status):
        if status:
            electrified.append(i)
        else:
            unelectrified.append(i)
    return electrified, unelectrified

def get2DHashTable(gis_data, unelectrified, distance_limit):
    """
    Generates the 2D Hash Table with the unelectrified locations hashed
    into the table for easy O(1) access.
        
    TODO params and return docstring
    """
    hash_table = defaultdict(lambda: defaultdict(list))
    for unelec_row in unelectrified:
        hash_x = int(gis_data[unelec_row][0]/distance_limit)
        hash_y = int(gis_data[unelec_row][1]/distance_limit)
        hash_table[hash_x][hash_y].append(unelec_row)
    return hash_table

def getUnelectrifiedRows(hash_table, elec_row, gis_data, distance_limit):
    """
    Returns all the unelectrified locations close to the electrified location
    based on the distance boundary limit specified by asking the 2D hash table.
        
    TODO params and return docstring
    """
    unelec_list = []
    hash_x = int(gis_data[elec_row][0]/distance_limit)
    hash_y = int(gis_data[elec_row][1]/distance_limit)

    unelec_list.extend(hash_table.get(hash_x, {}).get(hash_y, []))
    unelec_list.extend(hash_table.get(hash_x, {}).get(hash_y-1, []))
    unelec_list.extend(hash_table.get(hash_x, {}).get(hash_y+1, []))

    unelec_list.extend(hash_table.get(hash_x+1, {}).get(hash_y, []))
    unelec_list.extend(hash_table.get(hash_x+1, {}).get(hash_y-1, []))
    unelec_list.extend(hash_table.get(hash_x+1, {}).get(hash_y+1, []))

    unelec_list.extend(hash_table.get(hash_x-1, {}).get(hash_y, []))
    unelec_list.extend(hash_table.get(hash_x-1, {}).get(hash_y-1, []))
    unelec_list.extend(hash_table.get(hash_x-1, {}).get(hash_y+1, []))

    return unelec_list

def runAlgorithm(gis_input_file, scenario_input_file):
    """
    Runs the model algorithm from the VBA code.
        
    TODO params and return docstring
    """
    
    distance, gis_data = readGISData(gis_input_file)
    num_people, elec_status, cell_path = readScenarioData(scenario_input_file)
    
    setupInitialOutput(gis_data, elec_status)
    
    for distance_limit, population_limit in zip(distance, num_people):
        counter = 0
        electrified, unelectrified = separateElecStatus(elec_status)
        
        hash_table = get2DHashTable(gis_data, unelectrified, distance_limit)
        # print str(hash_table) # TO DEBUG

        elec_changes = []
        counter2 = 2

        while counter2 >= 1:
            counter2 = 0
            # Iteration based on number of electrified
            # cells at this stage of the calculation.
            for elec_row in electrified:

                unelec_rows = getUnelectrifiedRows(hash_table, elec_row, gis_data, distance_limit)
                
                for unelec_row in unelec_rows:
                    # km of line build prior + line km building
                    existing_grid = cell_path[elec_row][0] + cell_path[elec_row][1]
                    # Check if really unelectrified
                    el = elec_status[unelec_row] == 0
                    dx = abs(gis_data[elec_row][0] - gis_data[unelec_row][0]) < distance_limit
                    dy = abs(gis_data[elec_row][1] - gis_data[unelec_row][1]) < distance_limit
                    not_same_point = dx > 0 or dy > 0
                    pop = gis_data[unelec_row][2] > population_limit + distance_limit*(15.702 * (existing_grid + 7006) / 1000 - 110) / 4400
                    ok_to_extend = existing_grid < 50000

                    if el and dx and dy and not_same_point and pop and ok_to_extend:
                        if unelec_row not in elec_changes:
                            counter2 += 1
                            elec_changes.append(unelec_row)
                            elec_status[unelec_row] = 1
                            cell_path[unelec_row] = [existing_grid, distance_limit]

            if counter2 != 0:
                electrified = [item for item in elec_changes]
                elec_changes = []
            counter += 1
            #end while loop

        title_str = 'Distance={0} Number of People={1}'.format(distance_limit, population_limit)
        addElecColumn(elec_status, str(title_str))


def setupInitialOutput(gis_data, elec_status):
    """
    Setup the output file to include the initial and constant GIS Data.
        
    TODO params and return docstring
    """
    gis_data_copy = deepcopy(gis_data)
    gis_data_copy.insert(0, ['','',''])
    df = pd.DataFrame(gis_data_copy, columns=["X", "Y", "Pop"])

    elec_status_copy = deepcopy(elec_status)
    elec_status_copy.insert(0, sum(elec_status))
    df['ele'] = elec_status_copy
    df.to_csv('output.txt', index=False)

def addElecColumn(elec_status, iteration):
    """
    Add the updated electricity status column to the output data
    and also add the sum of all electrified locations below the title.
        
    TODO params and return docstring
    """
    elec_status_copy = deepcopy(elec_status)
    elec_status_copy.insert(0, sum(elec_status))
    
    data = pd.read_csv("output.txt")
    data[iteration] = elec_status_copy
    data.to_csv('output.txt', index=False)

if __name__ == '__main__':
    print 'This program is being run by itself'
    running = True
    while(running):
        var = raw_input("Please enter the scenario filename: ")
        print "Processing scenario file: ", var
        start_time = time.time()
        runAlgorithm('GIS_Input.txt', var)
        elapsed_time = time.time() - start_time
        print "Elapsed time: " + str(elapsed_time)
else:
    # TODO imported from another module
    pass

