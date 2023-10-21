# Python script: random_sample_start.py
# Author: Paul Zandbergen, modified by Stephen Bond
# This script creates a random sample of input features based on
# a specified count and saves the results as a new feature class.
# This script is the initial version with no changes from the lecture demo.


# Import modules.
import arcpy
import random

# Set workspace
arcpy.env.workspace = r"Data\IntroToPython.gdb"

# Set inputs and outputs. Inputfc can be a shapefile or geodatabase
# feature class. Outcount cannot exceed the feature count of inputfc.
inputfc = "County"
outputfc = "random"
outcount = 5

# Create a list of all the IDs of the input features.
inlist = []
with arcpy.da.SearchCursor(inputfc, "OID@") as cursor:
    for row in cursor:
        id = row[0]
        inlist.append(id)
    
# Create a random sample of IDs from the list of all IDs.
randomlist = random.sample(inlist, outcount)

# Use the random sample of IDs to create a new feature class.
desc = arcpy.Describe(inputfc)
fldname = desc.OIDFieldName
sqlfield = arcpy.AddFieldDelimiters(inputfc, fldname)
sqlexp = f"{sqlfield} IN {tuple(randomlist)}"
arcpy.analysis.Select(inputfc, outputfc, sqlexp)


