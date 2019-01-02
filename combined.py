#Import libraries
from __future__ import with_statement
from fabric import state
from fabric.contrib.files import exists
from fabric.api import *
from paramiko import *
from os.path import dirname, abspath, join
from os import listdir
from paramiko import Transport
from fabric.contrib.files import exists, append, sed
from StringIO import StringIO
from functools import wraps
import traceback
import time
import io
from fabric.api import run, env
import os
import subprocess
from pprint import pprint
from datetime import datetime
import datetime, time
import ConfigParser, os
import urllib, json
import sys
import os
import datetime
import shutil
from shutil import copyfile
from subprocess import call
import re
import json
import urllib, json
import subprocess
import urllib2
import urllib2, json


#DEFAULT_KEY_LOCATION = "/home/build/.ssh/fabric_keys"
#POOL_SIZE = 50



# Create .env file path.
# Accessing variables.
#Addressing Json file and SVN URL to import variables dynamically
url = urllib2.urlopen('http://svn.proddev.text.com:8090/svn/build-support/branches/development-mo/ohs/context.json')
object = json.load(url)

domain = object["domain"]
environment = object["environment"]
admin_host = domain+"adm001."+environment+".aws.test.com"
ohs_name = object["ohs_name"]
ohs_version = object["ohs_version"]

host1 = object["ohs_config"][0]["ohs_host"]["host"]
ohs_port1 = object["ohs_config"][0]["ohs_port"]
ohs_local_port1 = object["ohs_config"][0]["ohs_local_port"]
ohs_remote_port1 = object["ohs_config"][0]["ohs_remote_port"]
mod1_path1 = object["ohs_config"][0]["mod_wl_ohs"]["locations"][0]["path"]

#    print(v['ohs_port'])
#ohs_lines_toadd=['OHS|intf001.tsa.aws.test.com|MO_OHS_300|OHS|1000|2000|3000|wlohs_11116|','OHS|intf002.tsa.aws.test.com|MO_OHS_300|OHS|1000|2000|3000|wlohs_11116|']
ohs_lines_toadd=['OHS|'+host1+'|'+ohs_name+'|OHS|'+ohs_port1+'|'+ohs_local_port1+'|'+ohs_remote_port1+'|'+ohs_version+'|','OHS|'+host2+'|'+ohs_name+'|OHS|'+ohs_port2+'|'+ohs_local_port2+'|'+ohs_remote_port2+'|'+ohs_version+'|']



#env.key_filename = os.getenv('KEY_PATH') #listdir_fullpath(DEFAULT_KEY_LOCATION)
env.key_filename = 'C:\Users\srazeghi\Desktop\env-test-keypair-useast.pem'   #

#env.key_filename = listdir_fullpath(DEFAULT_KEY_LOCATION)
env.roledefs['selection'] = [admin_host]
env.roledefs['manage1'] = [host1]
env.roledefs['manage2'] = [host2]
env.user = 'root'
env.eagerly_disconnect = True
env.warn_only = True  # disable errors
env.skip_bad_hosts = True
env.output_prefix = False
env.hosts = [admin_host]



#Config
#function definition
def listdir_fullpath(d):
    """ Return all filenames (full path) in a directory. """
    return [join(d, f) for f in listdir(d)]

#this funtion just print which user is logging

@roles('selection')
def ls():
    run("ls")


#################3backup
def backup():
	with cd("/tools/appsw/appsautm/config"):
         domain_capital = domain.upper()
         run("cp "+domain_capital+"_config " +domain_capital+"_config_"+time.strftime("%Y%m%d"))

#going to right directory and editing config file
def edit():
    with cd("/tools/appsw/appsautm/config"):
         run("ls")
         domain_capital = domain.upper()
         domain_config = domain_capital+"_config"
#         print(domain_config)
         run("sed -i '2,$d' "+domain_config)
         run('echo "' + ohs_lines_toadd[0] + '" >> ' +domain_config   )
         run('echo "' + ohs_lines_toadd[1] + '" >> ' +domain_config   )

#as root, preparing ohs_lines_toadddef mo_test0():
def prepare():
    with cd("/tools/appsw/appsautm/builds"):
         run('./appswtl_prepareMyBuilds.sh -prepareohs '+domain)

#Build ohs as orainst
def build():
    run("ls")
    with cd('/tools/appsw/oracle/'+domain+'/builds'):
         sudo('./appsctl_ohsbuilds.sh -buildohs '+domain,user='orainst')



############## keeping OLD OHS
@roles('selection')
def set_old_ohs():
    with cd("/tools/appsw/appsautm/config"):
         domain_capital = domain.upper()
         domain_config = domain_capital+"_config"
         run("cp "+domain_capital+"_config " +domain_capital+"_config_"+time.strftime("%Y%m%d"))
         run("cp "+domain_capital+"_config_"+time.strftime("%Y%m%d")+" "+domain_capital+"_config2")
         sudo("sed -i '1d' "+domain_capital+"_config2")
         sudo("cat "+domain_capital+"_config2 >> "+domain_capital+"_config")
#sed '$d' domain_config
#cat INTF_config >> INTF_config2


#this funtion get back of the  OHS config files on manages servers
@roles('manage1')
def backupmod1():
	with cd('/oracle/'+domain+'/'+ohs_name+'/config/OHS/'+ohs_name):
         sudo("cp mod_wl_ohs.conf mod_wl_ohs.conf_"+time.strftime("%Y%m%d")+time.strftime("%H%M"),user='orainst')


####################### lookinf for VirtualHost
@roles('manage2')
def backupmod2():
	with cd('/oracle/'+domain+'/'+ohs_name+'/config/OHS/'+ohs_name):
         sudo("cp mod_wl_ohs.conf mod_wl_ohs.conf_"+time.strftime("%Y%m%d")+time.strftime("%H%M"),user='orainst')



#print(new_line)
# print(new_line)


#Overriding the updated mod_wl_ohs.conf with new locations spec


############edit mod_ohs
@roles('manage1')
def edit_ohs1():
    with cd('/oracle/'+domain+'/'+ohs_name+'/config/OHS/'+ohs_name):
		 run('ls -lsrta mod_wl_ohs.conf')

		 config_template_lines = [
			 "<Location /{{ path}}>",
			 "	SetHandler weblogic-",
			 "	WebLogicHost {{ host }}",
			 "	WeblogicPort  {{ port }}",
			 "</Location>"
		 ]

		 template1 = Template("\n".join(config_template_lines))
		 value = ""
		 value += template1.render(path=mod1_path1, host=host1, port=mod1_port1) + "\n"
		 value += template1.render(path=mod1_path2, host=host2, port=mod1_port2)

		 run('echo "' + value + '" >> mod_wl_ohs.conf')

@roles('manage2')
def edit_ohs1():
    with cd('/oracle/'+domain+'/'+ohs_name+'/config/OHS/'+ohs_name):
		 run('ls -lsrta mod_wl_ohs.conf')

		 config_template_lines2 = [
			 "<Location /{{ path}}>",
			 "	SetHandler weblogic-",
			 "	WebLogicHost {{ host }}",
			 "	WeblogicPort  {{ port }}",
			 "</Location>"
		 ]

		 template2 = Template("\n".join(config_template_lines2))
		 value = ""
		 value += template2.render(path=mod2_path1, host=host1, port=mod2_port1) + "\n"
		 value += template2.render(path=mod2_path2, host=host2, port=mod2_port2)

		 run('echo "' + value + '" >> mod_wl_ohs.conf')

#starting first ohs with orainst
@roles('manage1')
def start1():
    with cd('/oracle/'+domain+'/'+ohs_name+'/bin'):
         sudo('pwd')
         sudo("./opmnctl startall",user='orainst')
         sudo("./opmnctl status",user='orainst')

#starting second ohs
@roles('manage2')
def start2():
    with cd('/oracle/'+domain+'/'+ohs_name+'/bin'):
         sudo("./opmnctl startall",user='orainst')
         sudo("./opmnctl status",user='orainst')

#################executing all functions
#execute(listdir_fullpath)
execute(ls)
execute(backup)
execute(edit)
execute(prepare)
execute(build)
execute(start1)
execute(start2)
execute(set_old_ohs)
execute(backupmod1)
execute(backupmod2)
execute(edit_ohs1)
execute(edit_ohs2)
execute(start1)
execute(start2)
