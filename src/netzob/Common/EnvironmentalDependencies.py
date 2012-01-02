# -*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------- 
#| Global Imports
#+----------------------------------------------
import os
import logging
import socket
from uuid import getnode as get_mac_address
import time

#+---------------------------------------------------------------------------+
#| Local application imports
#+---------------------------------------------------------------------------+
from netzob.Common.EnvironmentalDependency import EnvironmentalDependency

#+---------------------------------------------- 
#| EnvDependancies :
#|     Handle environmental dependancies
#+---------------------------------------------- 
class EnvironmentalDependencies(object):
    
    #+---------------------------------------------- 
    #| Constructor :
    #+----------------------------------------------   
    def __init__(self):
        # create logger with the given configuration
        self.log = logging.getLogger('netzob.Import.EnvDependancies.py')
        self.envData = [] # List containing environmental data

    #+---------------------------------------------- 
    #| captureEnvData: 
    #|   Capture environmental data,
    #|   like local IP address, Ethernet address, etc.
    #+----------------------------------------------
    def captureEnvData(self):
        # OS specific
        self.envData.append( EnvironmentalDependency("os_name", "ascii", os.uname()[0]) ) # for example 'Linux'
        self.envData.append( EnvironmentalDependency("os_family", "ascii", os.name) ) # for example 'posix', 'nt', 'os2', 'ce', 'java', 'riscos'
        self.envData.append( EnvironmentalDependency("os_version", "ascii", os.uname()[2]) ) # result of 'uname -r' under linux
        self.envData.append( EnvironmentalDependency("os_arch", "ascii", os.uname()[4]) ) # result of 'uname -m' under linux

        # User specific
        self.envData.append( EnvironmentalDependency("user_home_dir", "ascii", os.environ['HOME']) )
        self.envData.append( EnvironmentalDependency("user_name", "ascii", os.environ['USERNAME']) )
        self.envData.append( EnvironmentalDependency("user_lang", "ascii", os.environ['LANG']) )

        # System specific
        self.envData.append( EnvironmentalDependency("hostname", "ascii", socket.gethostname()) )
        self.envData.append( EnvironmentalDependency("domainname", "ascii", "".join( socket.getfqdn().split(".", 1)[1:] )) )

        # Trick to retrieve the usual IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            ip_address = s.getsockname()[0]
            s.close()
        except:
            ip_address = "127.0.0.1"

        self.envData.append( EnvironmentalDependency("ip_address", "ascii", ip_address) )
        self.envData.append( EnvironmentalDependency("mac_address", "ascii", hex(int(get_mac_address()))[2:-1]) )

        # Misc        
        self.envData.append( EnvironmentalDependency("date", "ascii", str(time.time())) ) # elapsed second since epoch in UTC

    #+---------------------------------------------- 
    #| GETTERS
    #+----------------------------------------------
    def getEnvData(self):
        return self.envData