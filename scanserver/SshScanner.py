
#Copyright 2016 Ruth Ogunnaike

"""
sshscanner, this code runs 462 combinations of common weak/default usernames  and passwords against port 22 in order
to have a login access into the host. It includes method to change user's password

Procedures
runScan(IP_Address),this method initiates and run the default/weak vulnerability scanner password. The parameter
ip_address is passed as a string value.

getStatus(), this function returns the login status of the scan. The return values are Success Scan Error and Failed
. Success and Scan Error should flag the host vulnerable and the Failed status flags the host as not-vulnerable.

isPasswordChanged(IP_Address), this is a Boolean function that fix the weak/default vulnerability by changing the password
 of the host.  A new password is generated using combinations of alphanumeric characters of length eight.
"""


from __future__ import print_function

from __future__ import absolute_import
from pexpect import pxssh
import pexpect
import os
import socket
import time
import string
import random
import subprocess
import sys, getpass

COMMAND_PROMPT = '[$#] '
TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'
SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'


try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

url = 'https://localhost:8834'

class sshscanner(object):
    def built_url(self, resource):
        return '{0}{1}'.format(url, resource)

def getStatus():
    return status;

def setStatus(value):
    global status
    status = value

# check if SSH-port is open
def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        print ("True")
        return True
    except:
        print ("False")
        return False

# func ScanHost
def scanhost(ip):
    global status, username, oldpassword

    port = "22"
    user = ["mininet", "root", "admin", "sysadmin", "oracle", "webmaster", "pi"]
    pswd = ["12345", "root", "toor", "admin", "000000", "1111", "111111", "11111111", "123", "123.com", "123123",
            "123123123", "1234", "umeah5c3", "123456", "1234567", "12345678", "123456789", "1234567890", "1234qwer",
            "123abc", "123qwe", "123qweasd", "147147", "1q2w3e", "1q2w3e4r", "1q2w3e4r5t", "1q2w3e4r5t6y", "1qaz2wsx",
            "1qaz2wsx3edc", "1qazxsw2", "abc123", "abc@123", "Admin@123", "P@ssw0rd", "Password1", "a123456", "admin1",
            "admin123", "admin@123", "adminadmin", "administrator", "changeme", "cisco", "cisco123", "default",
            "firewall", "letmein", "linux", "oracle", "p@ssw0rd", "passw0rd", "password", "q1w2e3r4", "q1w2e3r4t5",
            "qwerty", "r00t", "raspberry", "redhat", "root123", "rootpass", "rootroot", "server", "test", "test123",
            "zaq1xsw2"]

    # Log Scan
    txt = "\n*****************************\nScanning IP : %s" % (ip)
    print (txt)

    starttime = time.time()
    if isOpen(ip, port):  # if SSH-port is open
        txt = "Port %s (SSH) is accessible." % port
        print (txt)
        found = False  # default : credentials not found yet
        blocked = False  # default : not blocked by victim host
        tried = 0
        for usr in user:  # run through all default username
            if found == True:  # if credentials were found with previous combination -> exit
                break

            if blocked == True:  # if you are blocked by victim -> exit and go to next victim
                break

            for pwd in pswd:  # run through all default passwords for each username
                print('* Try %s:%s' % (usr, pwd)),
                #time.sleep(500.0 / 1000.0)  # slow down to prevent detection
                tried += 1


                try:  # try to connect
                    s = pxssh.pxssh()
                    s.login(ip, usr, pwd)
                    s.sendline('uptime')  # run a command
                    s.prompt()  # match the prompt
                    print ("@ %s     SUCCESS ***********" % (ip))
                    print("Scan Time: ", round((time.time() - starttime), 2))
                    print (s.before)  # print everything before the prompt.
                    txt = '%s:%s @ %s     SUCCESS ************/n%s' % (usr, pwd, ip, s.before)
                    print (txt)
                    found = True
                    username = usr
                    oldpassword = pwd
                    setStatus('Vulnerable')
                    print("Scan Time: ", round((time.time() - starttime), 2))
                    break
                except Exception as ex:  # can't connect with this credentials
                    print ("failed - ")
                    response = str(ex)
                    setStatus('Non-vulnerable')
                    print (response)
                    if response == "could not synchronize with original prompt" or response == "could not set shell prompt":
                        print("Scan Time: ", round((time.time() - starttime), 2))
                        txt = 'Stopped due to Error response'
                        print (txt)
                        blocked = True
                        setStatus('Vulnerable')
                        break
                    elif response[:17] == "End Of File (EOF)":
                        print("Scan Time: ", round((time.time() - starttime), 2))
                        txt = 'Stopped due to blocked by victim'
                        setStatus('Vulnerable')
                        print (txt)
                        blocked = True
                        break

        print("Scan Time: ", round((time.time() - starttime), 2))
        txt = "Tried " + str(tried) + " combinations"
        print (txt)


    else:  # if SSH-port is closed
        txt = "Port %s (SSH) is closed." % port
        setStatus('Non-vulnerable')
        print("Scan Time: ", round((time.time() - starttime), 3))
        print (txt)

# func Exit
def func_exit():
    print ("Scan is complete")

# ++ PROGRAM ++#
os.system('clear')


def runScan(ip):
    scanhost(ip);

def generatePassword():
    chars = string.ascii_lowercase  + string.digits
    size = 8
    password= ''.join(random.choice(chars) for _ in range (size))
    return password

# (current) UNIX password:
def change_password(child):
    newpassword = generatePassword()
    print (newpassword)
    child.sendline('passwd')
    #The first expected command is to enter the current password
    i = child.expect(['Changing', 'current','Changing password for mininet. ',   '[Oo]ld [Pp]assword', '.current.*password', '[Nn]ew [Pp]assword'])
    if i != -1:
        print (oldpassword)
    else:
        print ("Wrong expected command")

    #Expected command is to enter the current password
    i = child.expect(['(current)', 'Enter current', '[E/e]nter', '[#\$] '], timeout=60)
    if i != -1:
        child.sendline(oldpassword)
    if i == 3:
        print("This is the next command: ", child.after)

    #Expected command is to enter the new password
    i = child.expect(['Enter current', '[E/e]nter', '[#\$] ', 'Retype'])
    if i != -1:
        child.sendline(newpassword)

    #Expected command is to retype the new password
    i = child.expect(['New password', 'Retype', 'Re-enter'], timeout=120)
    if i != -1:
        child.sendline(newpassword)

    #Expected command is to password update failed or successful
    i = child.expect(['password', 'updated', 'success'], timeout=120)
    if i != -1:
            print("Success")
    else:
        print ("Error occured")

def isPasswordChanged(host):
    changeTime = time.time()
    loginchild= login(host, username, oldpassword)
    if loginchild ==None:
        print ("Cannot login to host:", host)
        print("Resolution Time: ", round((time.time() - changeTime), 3))
        return False
    else:
        print("Changing Password for host:", host)
        change_password(loginchild)
        child.expect(COMMAND_PROMPT)
        print("Resolution Time: ", round((time.time() - changeTime), 3))
        return True


def login(host, user, password):
    global child
    child = pexpect.spawn('ssh -l %s %s'%(user, host))
    fout = file ("LOG.TXT","wb")
    child.logfile_read = fout #use child.logfile to also log writes (passwords!)

    i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, '[Pp]assword: '])
    if i == 0: # Timeout
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        sys.exit (1)
    if i == 1: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('[Pp]assword: ')
    child.sendline(password)
    # Now we are either at the command prompt or
    # the login process is asking for our terminal type.
    i = child.expect (['Permission denied', TERMINAL_PROMPT, COMMAND_PROMPT])
    if i == 0:
        print('Permission denied on host:', host)
        sys.exit (1)
    if i == 1:
        child.sendline (TERMINAL_TYPE)
        child.expect (COMMAND_PROMPT)
    return child


