#Copyright Daniel Black 2013
#This file is part of Kaithem Automation.

#Kaithem Automation is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, version 3.

#Kaithem Automation is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Kaithem Automation.  If not, see <http://www.gnu.org/licenses/>.

import yaml,argparse,sys,os


argp = argparse.ArgumentParser()

#Manually specify a confifuration file, or else there must be one in /etc/kaithem
argp.add_argument("-c")
argp.add_argument("-p")
argcmd = argp.parse_args(sys.argv[1:])

dn = os.path.dirname(os.path.realpath(__file__))

#This can't bw gotten from directories or wed get a circular import
with open(os.path.join(dn,"../data/default_configuration.txt")) as f:
    defconfig = yaml.load(f)

#Attempt to open any manually specified config file
if argcmd.c:
    with open(argcmd.c) as f:
        usr_config = yaml.load(f)
        
elif os.path.isfile("/etc/kaithem/kaithemconfig.txt"):
    with open("/etc/kaithem/kaithem.cfg") as f:
        usr_config = yaml.load(f)
        print("Loaded CFG from /etc")
else:
    usr_config ={}
    print ("No CFG File Found. Using Defaults.")
        

#Config starts out as the default but individual options
#Can be added or overridden by the user's settings.
config = defconfig.copy()

for i in usr_config:
    config[i] = usr_cfg[i]
    
if argcmd.p:
    config['port'] = int(argcmd.p)
