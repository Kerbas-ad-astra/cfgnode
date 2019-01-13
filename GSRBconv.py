# vim:ts=4:et
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# Converts LaunchSites.cfg (from RSS's KSCSwitcher patch) into RecoveryBeacons.cfg

from cfgnode import *
import sys
import io

def convert(file, LSnode):
    RBnode = ConfigNode()
    beaconsnode = ConfigNode()
    beaconsnode.AddNewNode("!Beacon,*")
    headNode = LSnode.GetNode("@RemoteTechSettings:FOR[RealSolarSystem]")
    launchsites = headNode.GetNode("GroundStations")
    llstring = "launchSites = ["
    for launchsite in launchsites.GetNodes("STATION"):
        lsname = launchsite.GetValue("Name").replace(' - ','_').replace(' ','_').lower()
        lslat = launchsite.GetValue("Latitude")
        lslon = launchsite.GetValue("Longitude")
        beacon = ConfigNode()
        beacon.AddValue("name",lsname)
        beacon.AddValue("latitude",lslat)
        beacon.AddValue("longitude",lslon)
        beacon.AddValue("range",1000000)
        beaconsnode.AddNode("Beacon",beacon)
        llstring += "{0},{1};...\n".format(lslat, lslon)
    llstring += "];"
    RBnode.AddNode("@Beacons",beaconsnode)
    fname = arg.split(".")[0] + "_rb.cfg"
    fname2 = arg.split(".")[0] + "_rb_mat.txt"
    text_file = open(fname, 'w')
    text_file.write("// Automatically generated from {0}\n".format(arg))
    text_file.write("// 500 km range because that's now far downrange the Mercury-Redstone rockets flew.\n")
    text_file.write("@NIMBY:FOR[RealSolarSystem]\n")
    text_file.write(RBnode.ToString())
    text_file.close()
    text_file = open(fname2,'w')
    text_file.write(llstring)
    text_file.close()
    

for arg in sys.argv[1:]:
    with io.open(arg,'r',encoding='utf8') as f:
        text = f.read()
    try:
        cfg = ConfigNode.load(text)
    except ConfigNodeError as e:
        print(arg+e.message)
        continue
    convert(arg, cfg)
