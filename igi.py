#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#Author : https://github.com/N0x01X

import subprocess
import pathlib
from textwrap3 import dedent
import requests
from colorama import Fore

def check_go():
    checking = subprocess.run(['go version'],capture_output=True, shell=True)
    return_code = checking.returncode
    return return_code
def check_last_version():
    url = 'https://go.dev/VERSION?m=text'
    req = requests.get(url=url)
    version = req.text
    return version
def get_go(version):
    download_command = f"wget https://go.dev/dl/{version}.linux-amd64.tar.gz"
    download = subprocess.run([download_command],shell=True)    
def install_go(version):
    print(Fore.RED + "Cleaning previous installations")
    delete_last = subprocess.run(['sudo rm -rf /usr/local/go'],shell=True)
    print(Fore.BLUE +"Decompressing to /usr/local")
    decomp = subprocess.run([f"sudo tar -C /usr/local -xzf {version}.linux-amd64.tar.gz"],shell=True)
    print(Fore.BLUE +"Add variables to config files")
    add1 = subprocess.run(["echo 'export GOROOT=/usr/local/go' >> $HOME/.bashrc"],shell=True)
    add2 = subprocess.run(["echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc"],shell=True)
    add3 = subprocess.run(["echo 'export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH' >> $HOME/.bashrc "],shell=True)
    add3 = subprocess.run(["echo 'export PATH=$PATH:/usr/local/go/bin' >> $HOME/.profile "],shell=True)
    print(Fore.BLUE +"Reloading Bash and Profile")
    reload_auth = subprocess.run(['chmod +x source_changer.sh'],shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    reloading = subprocess.run(['./source_changer.sh'],shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    print(Fore.BLUE +"Check installation")
    code = check_go()
    if code != 127:
        print(Fore.GREEN + 'Successfully installed latest version of golang')
    else:
        print(Fore.RED + 'There was an error in installation ! , Try again')
def checkfile(version):
    script_dir = pathlib.Path( __file__ ).parent.absolute()
    file_name = f"{version}.linux-amd64.tar.gz"
    file_list = []
    d = pathlib.Path(script_dir)
    for entry in d.iterdir():
        # check if it a file
        if entry.is_file():
            name = str(entry)
            file_list.append(name)     
    for item in file_list:              
        if file_name in item:
            return True           


def main_installation():
    print(Fore.BLUE + 'Installation Started, Lets check the last version of golang ...')
    last_version = check_last_version()
    print(Fore.BLUE + "Downloading latest version ...")
    if checkfile(last_version):
        print(Fore.GREEN + "The last version has been already downloaded")
    else:    
        get_go(last_version)
    if checkfile(last_version) != True:
        print(Fore.RED + "File not found, Installation aborted")
    else:       
        print(Fore.GREEN + "Successfully downloaded latest version of golang")
        user_order = input(Fore.RED + "Do you wish to install (This process will delete all installed modules)? [Y/n] ")
        if user_order == 'Y' or user_order == 'y' or user_order == 'yes':
            install_go(last_version)
        else:
            print(Fore.RED + 'Installation aborted')    
def main():
    banner = dedent("""
        ____   ______   ____
       /  _/  / ____/  /  _/
       / /   / / __    / /  
     _/ /   / /_/ /  _/ /   
    /___/   \____/  /___/   
    """)
    print(Fore.RED + banner)
    print(Fore.RED + 'Intelligent Golang Installer , By Hoomaan Haghparast')
    code = check_go()
    if code == 127:
        user_order = input(Fore.BLUE + "Golang is not installed, Do you want to install it? [Y/n] ")
        if user_order == 'Y' or user_order == 'y' or user_order == 'yes':
            main_installation()
    else:
        user_order = input(Fore.RED + "Golang is installed, Do you want to install it again or update it(This process will delete all installed modules)? [Y/n] ")
        if user_order == 'Y' or user_order == 'y' or user_order == 'yes':
            main_installation()



if __name__ == "__main__":
    main()