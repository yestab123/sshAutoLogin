#!/usr/bin/python
import os

# Genrate mode: 1 for using shc to change key message file to binary.
# 0 for using original infomartion (password will be seen directly)
gen_mode = 1

def ssh_password(name, ip, port, user, password):
    buff = '''#!/usr/bin/expect -f
      set user %s
      set host %s
      set password %s
      set port %d
      set timeout -1

      spawn ssh $user@$host -p $port
      expect "*assword:*"
      send "$password\r"
      interact
      expect eof''' % (str(user), str(ip), str(password), int(port))

    fd = open("%s.sh" % str(name), "w")
    fd.write(buff)
    fd.close()

    os.system("chmod 700 %s.sh" % (str(name)))

def ssh_key(name, ip, port, user, password, key):
    buff = '''#!/usr/bin/expect -f
      set user %s
      set host %s
      set password %s
      set port %d
      set timeout -1
      set key %s

      spawn ssh -i $key $user@$host -p $port
      expect "*passphrase*"
      send "$password\r"
      interact
      expect eof''' % (str(user), str(ip), str(password), int(port), str(key))

    fd = open("%s.sh" % str(name), "w")
    fd.write(buff)
    fd.close()

    os.system("chmod 700 %s.sh" % (str(name)))

def shc_shell_script(name):
    os.system("CFLAGs=-static shc -e 10/10/2020 -r -f %s.sh" % str(name))
    os.system("shc -v -f %s.sh" % str(name))
    os.system("rm -f %s.sh.x.c" % str(name))
    os.system("mv %s.sh.x %s.sh" % (str(name), str(name)))
    os.system("chmod 700 %s.sh" % (str(name)))

def ssh_password_sh(name, ip, port, user, password):
    buff = '''#!/bin/bash
    ./login/password_login %s %d %s %s''' % (str(ip), int(port), str(user), str(password))

    fd = open("%s.sh" % str(name), "w")
    fd.write(buff)
    fd.close()

    shc_shell_script(name)

def ssh_key_sh(name, ip, port, user, password, key):
    buff = '''#!/bin/bash
    ./login/key_login %s %d %s %s %s''' % (str(ip), int(port), str(user), str(password), str(key))

    fd = open("%s.sh" % str(name), "w")
    fd.write(buff)
    fd.close()

    shc_shell_script(name)

if __name__ == '__main__':
    sh_name = raw_input("ssh name:")
    sh_ip   = raw_input("ssh ip:")
    sh_port = raw_input("ssh port:")
    if sh_port == '':
        sh_port = 22
    sh_user = raw_input("ssh user:")
    sh_work_s = raw_input("ssh work(0 for password, 1 for key):")
    if sh_work_s == '':
        sh_work_s = 0
    sh_password = raw_input("ssh(key) password:")
    sh_work = int(sh_work_s)
    if sh_work == 0:
        if gen_mode == 0:
            ssh_password(sh_name, sh_ip, sh_port, sh_user, sh_password)
        else:
            ssh_password_sh(sh_name, sh_ip, sh_port, sh_user, sh_password)
    else:
        sh_key = raw_input("ssh key path:")
        if gen_mode == 0:
            ssh_key(sh_name, sh_ip, sh_port, sh_user, sh_password, sh_key)
        else:
            ssh_key_sh(sh_name, sh_ip, sh_port, sh_user, sh_password, sh_key)
