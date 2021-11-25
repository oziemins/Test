import re, sys, csv, collections
import os
import collections
import time
import pandas as pd
import numpy as np
import xlsxwriter

start_time = time.time()
print("script v1.0")

"""
    Device name          slot          linecard-model        software version
HU-BUD-BP14-BPE02     0/RSP0/CPU0   A9K-RSP440-SE        6.1.4
HU-BUD-BP14-BPE02     0/1/CPU0      A9K-MOD80-TR         6.1.4             
HU-BUD-BP14-BPE02     0/1/0         A9K-MPA-20X1GE       6.1.4
HU-BUD-BP14-BPE02     0/1/1         A9K-MPA-20X1GE       6.1.4
HU-BUD-BP14-BPE02     0/2/CPU0      A9K-36x10GE-TR       6.1.4
"""
path = os.getcwd()

def createData(filename):

    # Inicialized the collections.OrderedDictionary that will store all the info
    deviceinfo = collections.OrderedDict()
    deviceinfo = {
        "DeviceName": [],
        "Slot": [],
        "LineCardModel": [],
        "Software": [],
        "Filename": []
    }

    # Open the file


    #filename = 'UK_MNC03B_RA2'
    #with open (filename) as myfile:
    #    for myline in myfile:                   # For each line in the file,
    #        mylines.append(myline.rstrip('\n')) # strip newline and add to list.
    #        if myline.find("#show platform") != -1:
    #            show_platform = myline
    #            print("show platform", show_platform)
    #        #print("my line", myline)
    #    for element in mylines:                     
    #        print(element)

    #path = 'Scripts'
    #files = os.listdir(path)
    #for filename in files:
    ### open the file 
    #print ("Current working dir : %s" % os.getcwd())
    #path = os.getcwd()
    #files = os.listdir(path)


    #filenames = ['CH_MLRZUI991']

    findSplit = False
    #for filename in filenames:
    with open (filename) as myfile:
        #ASSIGN FILENAME
        deviceinfo["Filename"] = filename

        while(findSplit == False):
        #for i in range(10):
            header = next(myfile)

            if header.find("#show platform") != -1:
                show_platform = header
                #print("show platform", show_platform)
                #GET THE ROUTER NAME
                show_platform_start = show_platform.find('#show platform')
                router_name_field = show_platform[:show_platform_start]
                router_name_start = router_name_field.find(':')
                router = router_name_field[router_name_start+1:]
                #print("ROUTER", router)
                router = router.strip("'")
                deviceinfo["DeviceName"] = router
            
            #print("HEADER", header, type(header))
            if header.startswith('---'):
                findSplit = True
        for line in myfile:
            if line.find("#show") != -1:
                break
            #line = line.split(' ')
            #print("First line!")
            
            fields = line.split()
            node, type_linecard, state, *rest = fields
            #print((node, type_linecard, state, *rest))
            #print("NODE", node)    
            #print("type, slot", type_linecard)
            node = node.strip("'")
            type_linecard = type_linecard.strip("'")
            deviceinfo["Slot"].append(node)
            deviceinfo["LineCardModel"].append(type_linecard)
        for line in myfile:
            if line.find("asr9k-xr") != -1:
                show_software = line
                #print("show platform", show_platform)
                #GET THE ROUTER NAME
                show_software_start = show_software.find('asr9k-xr')
                software_name_field = show_software[:show_software_start]
                print("software", show_software)
                deviceinfo["Software"] = show_software
                #print("software", software_name_field)

                #software_name_start = router_name_field.find(':')
                #router = router_name_field[router_name_start+1:]
                #print("ROUTER", router)
                #router = router.strip("'")
                #deviceinfo["DeviceName"] = router

            #print(line)
            #print(show_platform)
            #print(router)
            #print(deviceinfo)
    return deviceinfo

file = 'RO_HD02A_RD4.AORTA.NET'
deviceinfo = createData(file)
print("DEVICE", deviceinfo)

def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += "x"
    return dict_list

def max_list(dict_list):
    lmax = 0
    for lname in dict_list.keys():
        if lname == 'Slot':
            lmax = max(lmax, len(dict_list[lname]))
            print(lmax)
    print("max", lmax)
    return lmax

number = max_list(deviceinfo)

pad_dict_list(deviceinfo, '')
device_dataframe = pd.DataFrame.from_dict(deviceinfo, orient='index')
#device_dataframe.transpose()

#dataframe = pd.read_csv('device_info.csv')
#print(dataframe)


print(deviceinfo)
print("devie", len(deviceinfo))
print("devicee", max_list(deviceinfo))
maxi = max_list(deviceinfo)
#lengthrow = max(len(deviceinfo.values()))
print(type(maxi))
daf = pd.DataFrame(deviceinfo, index=['Row']*maxi)
print(len(daf))
daf.to_csv(file+'.csv', index=False,header=True, encoding='utf-8')



arr = os.listdir(path)
print(arr)



