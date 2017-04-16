#!/usr/bin/env python3.3

# housing -- evaluate each house on campus based on location

import xml.etree.ElementTree as ET
from datetime import date
from sys import argv
import re
import math

template = '{:<12} {:>7} {:>6} {:>6} {:>6}'

def dist(text):
    data = re.split(' ',text)
    num = int(data[0])
    if (data[1] == "blocks"):
        return (200 * num)
    else: 
        return num


class Building(object):
    near_buildings = ['dist_to_lib','dist_to_dining','dist_to_quad']

    def __init__(self,element):
        self.building = element.find('name').text
        for field in Building.near_buildings:
            setattr(self,field,dist(element.find(field).text))
        self.avg_dist = math.sqrt(sum(map(lambda field: (getattr(self,field)), Building.near_buildings)))

    def __str__(self):
        return  template.format(self.building,
                                (self.dist_to_lib),
                                self.dist_to_dining,
                                self.dist_to_quad,
                                '{: 6.3f}'.format(self.avg_dist))


    def __lt__(self,other):
        return self.avg_dist < other.avg_dist

# grab the XML

doc = ET.parse(argv[1])
housing = doc.getroot()

# print the header

print(housing.get('info'))
print()
print(template.format('Building','library','dining','quad ','avg_dist'))
print(template.format('----------','--------','------','------','------'))

# print the table entries

dorms = list(map(Building,doc.findall('.//dorm_building')))
dorms.sort()
for dorm in dorms:
    print(dorm)


# Sample interaction:

# $ ./housing.py housing.xml
# University of Chicago Dorms by Distance to Necessities

# Building     library dining  quad  avg_dist
# ----------   -------- ------ ------ ------
# Snitchcock         5     30      2  6.083
# Max Palevsky       2      2    400  20.100
# South            400      2    600  31.654
# I House         1000   1400   1200  60.000
# $ 

