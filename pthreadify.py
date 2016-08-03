#!/usr/bin/env python
import os
import sys
import xml.etree.ElementTree as ET


#arg 0 = script
#arg 1 = entry_points xml file
#arg 2 = mychauffeur executable

#Parse args
args = sys.argv
usg = "Need 2 positional args, (1) entry point xml file, (2) myChauffeur executable"
assert len(args) == 3, usg
eps = args[1]
myc = args[2]
assert os.path.exists(eps), "entry point file not found"
assert os.path.exists(myc), "myChauffeur executable not found"


#Loop through drivers, rewrite for completed categories
completed = ["char"]
t = ET.parse(eps)
root = t.getroot()
for driver in root.iter('driver'):
    dfile = driver.attrib["name"]
    #If driver group is not in the completed list, skip driver
    if(dfile.split('/')[1] not in completed):
        continue
    for epp in driver.iter("pair"):
        ep1 = epp.attrib['ep1']
        ep2 = epp.attrib['ep2']
        bug = epp.attrib['bug'] in ['true', 'True']
        
        print(dfile + '\t' + str(bug) + '\t' + ep1 + '\t' + ep2)

