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

import time

class DayOfWeek(str):
    """This class it a value object that will appear like a string but will support intelliget comparisions like Dow=='Thu' etc.
        supports upper ad lower case and abbreviations and numbers(monday=0).
        If you don't pass it a weekday day when initializing it it will default to today in local time
    
    """
    def __init__(self,day=""):
    
        #If no day supplied, default to today
        if day == "":
            day = time.localtime().tm_wday
            
        self.namestonumbers= {
                'Mon':0,'Monday':0,'M':0, 0:0,
                'Tue':1,'Tuesday':1, 'Tues':1,'Tu':1, 1:1,
                'Wed':2,'Wednesday':'2', 'W':2, 2:2,
                'Thu':3,"Thursday":3, 'Th':3,'Thurs':3,'Thur':3, 3:3,
                "Fri":4,'Friday':4, 4:4,
                'Sat':5,'Saturday':5, 5:5,
                'Sun':6,'Sunday':6,
                6:6,
               }
               
        self.numberstonames=[
                        ['Monday','Mon'],
                        ['Tuesday','Tue','Tu','Tues'],
                        ['Wednesday','Wed'],
                        ['Thursday','Thu','Th','Thurs','Thur'],
                        ['Friday','Fri'],
                        ['Saturday','Sat'],
                        ['Sunday','Sun']
                      ]
        try:
            if isinstance(day,str):
                day=day.capitalize()
            self.__day = self.namestonumbers[day]
        except Exception as e:
            raise e#ValueError('Does not appear to be any valid day of the week')
     
    def __str__(self):
        return(self.numberstonames[self.__day][0])
     
    def __repr__(self):
         return(self.numberstonames[self.__day][0])
     
    def __eq__(self,other):
         try:
             if isinstance(other,str):
                 other=other.capitalize()
             if self.namestonumbers[other] == self.__day:
                 return True
             else:
                 return False
         except KeyError:
             return False

time_as_seconds ={
'year' : 60*60*24*365,
'week' : 60*60*24*7,
'day' : 60*60*24,
"hour" : 60*60,
"minute" : 60,
"second" : 1,
"millisecond" : 0.001
}

def timeIntervalFromString(s):
    s = s.strip()
    #deal with plurals
    if s.endswith("s"):
        s = s[:-1]
    
    s = s.split(" ")
    multiplier= time_as_seconds(s[-1].lower())
    number = int(s[0])
    return number*multiplier

def formatTimeInterval(t,maxunits):
    """Take a length of time t in seconds, and return a nicely formatted string
    like "2 hours, 4 minutes, 12 seconds".
    maxunits is the maximum number of units to use in the string(7 will add a milliseconds field to times in years)
    
    """
    s = ""
    for i in sorted(time_as_seconds.items(),key= lambda x:x[1], reverse=True):
        if maxunits == 0:
            return s[:-2]
        x = t%i[1]
        b=(t-x)
        y=(t-x)/i[1]
        
        t = t-b
        if y>1:
            s += str(int(round(y))) + " " + i[0]+"s, "
            maxunits -=1
        elif y==1:
            s += str(int(round(y))) + " " + i[0]+", "
            maxunits -=1
    return s[:-2]
    
def strToIntWithSIMultipliers(s):
    s=s.lower().strip()
    #This piece of code interprets a string like 89m or 50k as a number like 89 millon or 50,000
    if s.endswith('k'):
        return int(s[:-1])*1000
    elif s.endswith('m'):
        return int(s[:-1])*1000000
    elif s.endswith('g'):
        return int(s[:-1])*1000000000
    else:
        return int(s[:-1])


