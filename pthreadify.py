#!/usr/bin/env python
import os
import subprocess
import sys
import xml.etree.ElementTree as ET


#arg 0 = script
#arg 1 = entry_points xml file
#arg 2 = mychauffeur executable

#Parse args
args = sys.argv
usg = 'Need 2 positional args, (1) entry point xml file, (2) myChauffeur executable.  If 3rd positional arg is provided, it selects a single driver as target (use driver folder name, without category folder, e.g., "generic_nvram")'
assert len(args) == 4 or len(args) == 3, usg
eps = args[1]
myc = args[2]
targetDriver = args[3] if len(args)==4 else ""
assert os.path.exists(eps), "entry point file not found"
assert os.path.exists(myc), "myChauffeur executable not found"


#Loop through drivers, rewrite for completed categories
completed = ["char"]
t = ET.parse(eps)
root = t.getroot()
foundDriver = False
for driver in root.iter('driver'):
    dfile = driver.attrib["name"]
    #If driver group is not in the completed list, skip driver
    if(dfile.split('/')[1] not in completed):
        continue
    if(targetDriver not in dfile):
       continue
    foundDriver = True
    for epp in driver.iter("pair"):
        # Call myChauffeur for current ep pair
        ep1 = epp.attrib['ep1']
        ep2 = epp.attrib['ep2']
        if ep1 == ep2:
            continue
        noBug = "false" if epp.attrib['bug'] in ['true', 'True'] else "true"

        cmd = [myc, dfile, "-ep1=" + ep1, "-ep2=" + ep2,
               "-noBug=" + noBug, "--", "-w", "-I", "./Model/"]
        
        subprocess.call(cmd)

        # Generate resultant file name, and do preprocessing
        group = dfile.split('/')[1]
        dName = dfile.split('/')[2]
        folder = dfile[:dfile.rfind('/')]
        rewrittenDriverBase = folder + '/' + group + "_" + dName + "_"
        rewrittenDriverBase += ep1 + "_" + ep2 + "_" + noBug + "-unreach-call"
        print(os.path.exists(rewrittenDriverBase + ".c"))

        cmd = ["clang", "-E", "-P", rewrittenDriverBase + ".c", 
               "-I", "./Model/", "-m32", ]
        with file(rewrittenDriverBase + ".i", 'w') as outfile:
            subprocess.call(cmd, stdout=outfile)

if(not foundDriver):
    print("No driver found")
    
