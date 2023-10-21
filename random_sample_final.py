# Python script: random_sample_final.py
# Author: Paul Zandbergen, modified by Stephen Bond
# This script creates a random sample of input features based on
# a specified count and saves the results as a new feature class.
# This script is the final version with all edits made in the lecture demo.


# Import modules.
import arcpy
import random
import sys

# Set inputs and outputs. Inputfc can be a shapefile or geodatabase
# feature class. Outcount cannot exceed the feature count of inputfc.
inputfc = arcpy.GetParameterAsText(0)
outputfc = arcpy.GetParameterAsText(1)
outcount = arcpy.GetParameter(2)
fcount = arcpy.management.GetCount(inputfc)[0]

# Check to make sure the number of features selected isn't greater
# than the number of features in the feature class.
if outcount > int(fcount):
    arcpy.AddError("The number of features to be selected is greater "
                  "than the number of input features.")
    sys.exit(1)

else:
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

# Add a warning if the number of sleected features is equal to the
# number of input features
    if outcount == int(fcount):
        arcpy.AddWarning("The number of features to be selected is equal "
                    "to the number of input features, so the output is "
                    "a copy instead of a sample.")


