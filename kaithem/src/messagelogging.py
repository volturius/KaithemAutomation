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

import messagebus
import unitsofmeasure
import cherrypy
import pages
import time
import threading
import directories
import json
import os
import util
import bz2
import gzip
import re
import workers
from cherrypy.lib.static import serve_file

from config import config
from collections import defaultdict
#this flag tells if we need to save the list of what to log
loglistchanged = False

approxtotallogentries = 0

savelock = threading.RLock()

toSave = set()
with open(os.path.join(directories.logdir,"whattosave.txt"),'r') as f:
    x = f.read()
    
for line in x.split('\n'):
    toSave.add(line.strip())

del x
log = defaultdict(list)

def dumpLogFile():
    
    if config['log-format'] == 'normal':
        def dump(j,f):
            f.write(json.dumps(j,sort_keys=True,indent=1).encode())
            
    elif config['log-format'] == 'tiny':
        def dump(j,f):
            f.write(json.dumps(j,sort_keys=True,separators=(',',':')).encode())
    
    elif config['log-format'] == 'pretty':
        def dump(j,f):
            f.write(json.dumps(j,sort_keys=True,indent=4, separators=(',', ': ')).encode())
    
    else:
        def dump(j,f):
            f.write(json.dumps(j,sort_keys=True,indent=1).encode())
            messagebus.postMessage("system/notifications","Invalid config option for 'log-format' so defaulting to normal")
    
    if config['log-compress'] == 'bz2':
        openlog=  bz2.BZ2File
        ext = '.json.bz2'
    
    elif config['log-compress'] == 'gzip':
        openlog = gzip.GzipFile
        ext = '.json.gz'
    elif config['log-compress'] == 'none':
        openlog = open
        ext = '.json'
        
    else:
        openlog = open
        messagebus.postMessage("system/notifications","Invalid config option for 'log-compress' so defaulting to no compression")
        
     
    global log,loglistchanged
    global approxtotallogentries
    
    with savelock:
        temp = log
        log = defaultdict(list)
        approxtotallogentries = 0
        
        if loglistchanged:
            #Save the list of things to dump
            with open(os.path.join(directories.logdir,"whattosave.txt"),'w') as f:
                for i in toSave:
                    f.write(i+'\n')
            loglistchanged = False
                
        #Get rid of anything that is not in the list of things to dump to the log
        temp2 = {}
        saveset = set(toSave)
        for i in temp:
            #Parsetopic is a function that returns all subscriptions that would match a topic
            if not set(messagebus.MessageBus.parseTopic(i)).isdisjoint(saveset):
                temp2[i] = temp[i]
        temp = temp2
        
        #If there is no log entries to save, don't dump an empty file.
        if not temp:
            return
                

                
                
        where =os.path.join(directories.logdir,'dumps')
        #Actually dump the log.
        with openlog(os.path.join(where,str(time.time())+ext),'wb') as f:
            print()
            dump(temp,f)
            f.close()
        
        
        asnumbers = {}
        for i in util.get_files(where):
                try:
                    #Remove extensions
                    if i.endswith(".json"):
                        asnumbers[float(i[:-5])] = i
                    elif i.endswith(".json.gz"):
                        asnumbers[float(i[:-8])] = i
                    elif i.endswith(".json.bz2"):
                        asnumbers[float(i[:-9])] = i
                except ValueError:
                    pass
        
        maxsize = unitsofmeasure.strToIntWithSIMultipliers(config['keep-log-files'])
        size = 0
        #Loop over all the old log dumps and add up the sizes
        for i in util.get_files(where):
            size = size + os.path.getsize(os.path.join(where,i))
        
        #Get rid of oldest log dumps until the total size is within the limit
        for i in sorted(asnumbers.keys()):
            if size <= maxsize:
                break
            size = size - os.path.getsize(os.path.join(where,i))
            os.remove(os.path.join(where,asnumbers[i]))


def messagelistener(topic,message):
    global log
    global approxtotallogentries
    if topic not in log:
        log[topic] = []
    
    log[topic].append((time.time(),message))
    #This is not threadsafe. Hence the approx.
    approxtotallogentries +=1
    if approxtotallogentries > config['log-dump-size']:
        print('dumped')
        workers.do(dumpLogFile)


messagebus.subscribe('/',messagelistener)

def listlogdumps():
    where =os.path.join(directories.logdir,'dumps')
    logz = []
    r = re.compile(r'^([0-9]*\.[0-9]*)\.json(\.gz|\.bz2)?$')
    for i in util.get_files(where):
        m = r.match(i)
        if not m == None:
            #Make time,fn,ext,size tuple
            logz.append((float(m.groups('')[0]), os.path.join(where,i),m.groups('Uncompressed')[1],os.path.getsize(os.path.join(where,i))))
    return logz


class WebInterface(object):
    @cherrypy.expose
    def index(self, ):
        pages.require('/users/logs.view')
        return pages.get_template('logging/index.html').render()
    
    @cherrypy.expose
    def startlogging(self,topic):
        pages.require('/admin/logging.edit')
        global loglistchanged
        loglistchanged = True
        toSave.add(topic)
        return pages.get_template('logging/index.html').render()
    
    @cherrypy.expose
    def stoplogging(self,topic):
        pages.require('/admin/logging.edit')
        global loglistchanged
        loglistchanged = True
        toSave.discard(topic)
        return pages.get_template('logging/index.html').render()
    
    @cherrypy.expose
    def setlogging(self, txt):
        pages.require('/admin/logging.edit')
        global loglistchanged
        loglistchanged = True
        global toSave
        toSave = set()
        for line in txt.split("\n"):
            line = line.strip()
            if line.startswith("/"):
                line = line[1:]
            toSave.add(line)
        return pages.get_template('logging/index.html').render()
    
    @cherrypy.expose
    def flushlogs(self):
        pages.require('/admin/logging.edit')
        return pages.get_template('logging/dump.html').render()
    
    @cherrypy.expose
    def dumpfiletarget(self):
        pages.require('/admin/logging.edit')
        dumpLogFile()
        return pages.get_template('logging/index.html').render()
        
    @cherrypy.expose
    def archive(self):
        pages.require('/users/logs.view')
        return pages.get_template('logging/archive.html').render(files = listlogdumps())
            
    @cherrypy.expose
    def viewall(self, topic):
        pages.require('/users/logs.view')
        return pages.get_template('logging/topic.html').render(topicname=topic)
    
    @cherrypy.expose
    def clearall(self,topic):
        pages.require('/admin/logging.edit')
        log.pop(topic)
        return pages.get_template('logging/index.html').render()
    
    @cherrypy.expose
    def servelog(self,filename):
        pages.require('/users/logs.view')
        #Make sure the user can't acess any file on the server like this
        print(filename)
        if not filename.startswith(os.path.join(directories.logdir,'dumps')):
            raise RuntimeError("Security Violation")
        return serve_file(filename, "application/x-download",os.path.split(filename)[1])
    
