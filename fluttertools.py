import os
import sys
from pyfiglet import Figlet
from colorama import Fore
import shutil
from time import sleep
import json
import re
import platform
import subprocess
import requests

currentPlatform = ""
if platform.system() == "Windows":
    currentPlatform = "win"
elif platform.system() == "Linux":
    currentPlatform = "linux"
elif platform.system() == "Darwin":
    currentPlatform = "mac"


def getPlatformVar(command, functions=[]):
    cmd = data["platforms"][0][command][currentPlatform]
    for placeholder in re.findall(r"%([^%]+)%", cmd):
        cmd = cmd.replace(f"%{placeholder}%", data[placeholder])
    for func in re.findall(r"\$([^$]+)\$", cmd):
        cmd = cmd.replace(f"${func}$", functions[int(func) - 1])
    return cmd.replace('!', ' ')


# check for new version
print(f'{Fore.YELLOW}[!] Checking for new version...{Fore.RESET}')
# get current version
version = "v0.1.0"
versionFormatted = ""
# get latest version
def checkVersion():
    global version
    global versionFormatted
    try:
        latestVersion = requests.get(
            'https://api.github.com/repos/HelloItsMeAdm/FlutterTools/releases/latest').json()['tag_name']
        if version != latestVersion:
            print(
                f'{Fore.YELLOW}\n[!] New version available: {latestVersion}\n[!] Current version: {version}{Fore.RESET}')
            print(
                f'\n{Fore.YELLOW}[!] Download new version here: https://github.com/HelloItsMeAdm/FlutterTools/releases/latest{Fore.RESET}')
            print(f'\n{Fore.RED}[!] DON\'T FORGET TO BACKUP THE CONFIG FILE!{Fore.RESET}')
            print(f'{Fore.RED}[!] DON\'T FORGET TO BACKUP THE CONFIG FILE!{Fore.RESET}')
            print(f'{Fore.RED}[!] DON\'T FORGET TO BACKUP THE CONFIG FILE!\n{Fore.RESET}')
            print(f'{Fore.YELLOW}[!] Exiting in 10 seconds...{Fore.RESET}')
            return True
        else:
            print(f'{Fore.GREEN}[✓] Up to date! ({version}){Fore.RESET}')
            versionFormatted = f'{Fore.GREEN}Version: {version} (Up to date)'
    except:
        print(f'{Fore.RED}[X] Failed to check for new version{Fore.RESET}')
        versionFormatted = f'{Fore.RED}Version: {version} (Failed to check for new version)'
    return False

if checkVersion():
    sleep(10)
    sys.exit(1)

# check if flutter is installed
print(f'{Fore.YELLOW}[!] Checking if flutter is installed...{Fore.RESET}')
flutterVersion = os.popen('flutter --version').read().split(' ')[1]
if flutterVersion == '':
    print(
        f'{Fore.RED}[X] Flutter is not installed or not added to PATH\nPlease install flutter and add it to PATH{Fore.RESET}')
    print(f'{Fore.YELLOW}[!] Exiting in 10 seconds...{Fore.RESET}')
    sleep(10)
    sys.exit(1)
else:
    print(f'{Fore.GREEN}[✓] Flutter is installed{Fore.RESET}')

emulators = []
data = {}
connectedDevices = {}
connectedDevicesTemp = []


def refreshDevices():
    global connectedDevicesTemp
    connectedDevicesTemp = list(filter(None, os.popen(
        getPlatformVar("getdevices")).read().split('\n')))
    # remove 'List of devices attached'
    connectedDevicesTemp.pop(0)
    # remove all emulators
    for i in range(len(connectedDevicesTemp)):
        if 'emulator' in connectedDevicesTemp[i]:
            connectedDevicesTemp.pop(i)


def welcome(showPhones=True, showEmulators=True, showMenu=True, phoneId=0):
    global emulators
    os.system(getPlatformVar('clear'))
    # print nice welcome message
    for _ in range(shutil.get_terminal_size().columns):
        print(Fore.CYAN + '#', end='')
    f = Figlet(font='standard')

    def DrawText(text):
        print(*[x.center(shutil.get_terminal_size().columns)
                for x in f.renderText(text).split("\n")], sep="\n")

    DrawText('FlutterTools')
    print('By HelloItsMeAdm'.center(shutil.get_terminal_size().columns))
    print(f'{versionFormatted}{Fore.CYAN}'.center(
        shutil.get_terminal_size().columns + 10))
    print(f'{Fore.GREEN}Flutter version: {flutterVersion}{Fore.CYAN}\n'.center(
        shutil.get_terminal_size().columns + 10))
    for _ in range(shutil.get_terminal_size().columns):
        print('#', end='')
    print(Fore.RESET + '\n')

    if showPhones:
        # print phones
        refreshDevices()
        if len(connectedDevicesTemp) > 0:
            for i in range(len(connectedDevicesTemp)):
                if 'offline' in connectedDevicesTemp[i]:
                    continue
                connectedDevices[data["baseIp"] + "." + connectedDevicesTemp[i].split(
                    ':')[0].split('.')[3]] = connectedDevicesTemp[i].split('\t')[0].split(':')[1]
        if len(data['phones']) > 0:
            print(
                f'Available physical devices: {Fore.CYAN}({len(data["phones"])}){Fore.RESET}\n• {Fore.LIGHTWHITE_EX}ID{Fore.RESET} - Name (IP) {Fore.GREEN}(Connected :PORT) {Fore.YELLOW}(Disconnected){Fore.RESET}\n')
            pos = 0
            for i in data['phones']:
                pos += 1
                if phoneId == pos or phoneId == 0:
                    phoneLine = f'• {Fore.LIGHTWHITE_EX}c{pos}{Fore.RESET}/{Fore.LIGHTWHITE_EX}d{pos}{Fore.RESET} - {i["name"]} ({data["baseIp"]}.{i["ip"]})'
                    if data["baseIp"] + "." + i['ip'] in connectedDevices:
                        print(
                            f'{phoneLine} {Fore.GREEN}(Connected :{connectedDevices[data["baseIp"] + "." + i["ip"]]}){Fore.RESET}')
                    else:
                        print(
                            f'{phoneLine} {Fore.YELLOW}(Disconnected){Fore.RESET}')
        else:
            print(
                f'{Fore.YELLOW}[!] No available physical devices{Fore.RESET}\n')
        for _ in range(shutil.get_terminal_size().columns):
            print('-', end='')

    if showEmulators:
        # print emulators
        emulatorsResult = os.popen(getPlatformVar("getavds")).read()
        emulators = list(filter(None, emulatorsResult.split('\n')))
        if len(emulatorsResult.split()) > 0:
            print(
                f'Available emulators: {Fore.CYAN}({len(emulatorsResult.split())}){Fore.RESET}\n• {Fore.LIGHTWHITE_EX}ID{Fore.RESET} - Name\n')
            pos = 0
            for i in emulatorsResult.split('\n'):
                pos += 1
                if i != '':
                    print(f'• {Fore.LIGHTWHITE_EX}e{pos}{Fore.RESET} - {i}')
        else:
            print(
                f'{Fore.YELLOW}[!] No available emulators{Fore.RESET}\n')
        for _ in range(shutil.get_terminal_size().columns):
            print('-', end='')

    if showMenu:
        # print menu
        print(f.renderText('Menu'))
        print(f'{Fore.LIGHTWHITE_EX}0){Fore.RESET} Refresh everything')
        print(f'{Fore.LIGHTWHITE_EX}1){Fore.RESET} Add new physical device')
        print(f'{Fore.LIGHTWHITE_EX}2){Fore.RESET} Edit physical device')
        print(f'{Fore.LIGHTWHITE_EX}3){Fore.RESET} Remove physical device')
        print(f'{Fore.LIGHTWHITE_EX}4){Fore.RESET} Open terminal with adb')
        print(f'{Fore.LIGHTWHITE_EX}5){Fore.RESET} Open terminal with emulator')
        print(f'{Fore.LIGHTWHITE_EX}6){Fore.RESET} Check for updates')
        print(f'{Fore.LIGHTWHITE_EX}7){Fore.RESET} Exit\n')


def badConfig(code):
    # 0 = created
    # 1 = corrupted
    # 2 = missing info
    if code == 0:
        print(f'{Fore.YELLOW}[!] Please fill out config.json{Fore.RESET}')
        data['baseIp'] = input('Enter base IP (e.g. 192.168.1): ')
        if re.match(r'^(?:[0-9]{1,3}\.){2}[0-9]{1,3}$', data['baseIp']) == None:
            print(
                f'{Fore.RED}[X] Invalid IP address (e.g. "192.168.1"){Fore.RESET}')
            sleep(3)
            badConfig(0)
            return
        data['platformToolsPath'] = input(
            f'Enter platform-tools path (e.g. {getPlatformVar("platformToolsPathExample")}): ').replace(' ', '!')
        if os.path.isdir(data['platformToolsPath'].replace('!', ' ')) == False:
            print(
                f'{Fore.RED}[X] Invalid platform-tools path{Fore.RESET}')
            sleep(3)
            badConfig(0)
            return
        data['emulatorPath'] = input(
            f'Enter emulator path (e.g. {getPlatformVar("emulatorPathExample")}): ').replace(' ', '!')
        if os.path.isdir(data['emulatorPath'].replace('!', ' ')) == False:
            print(f'{Fore.RED}[X] Invalid emulator path{Fore.RESET}')
            sleep(3)
            badConfig(0)
            return
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f'{Fore.GREEN}[√] Saved config.json{Fore.RESET}')
        sleep(3)
        welcome()
    elif code == 1:
        print(
            f'{Fore.RED}[X] config.json is corrupted! Try restarting the program or deleting config.json{Fore.RESET}')
        print(f'{Fore.YELLOW}[!] Exiting in 10 seconds...{Fore.RESET}')
        sleep(10)
        sys.exit(1)
    elif code == 2:
        print(
            f'{Fore.RED}[X] config.json is missing info or info is invalid{Fore.RESET}')
        if data['baseIp'] == '' or re.match(r'^(?:[0-9]{1,3}\.){2}[0-9]{1,3}$', data['baseIp']) == None:
            data['baseIp'] = input('Enter base IP (e.g. 192.168.1): ')
            if re.match(r'^(?:[0-9]{1,3}\.){2}[0-9]{1,3}$', data['baseIp']) == None:
                print(
                    f'{Fore.RED}[X] Invalid IP address (e.g. "192.168.1"){Fore.RESET}')
                sleep(3)
                badConfig(2)
                return
        if data['platformToolsPath'] == '' or os.path.isdir(data['platformToolsPath'].replace('!', ' ')) == False:
            data['platformToolsPath'] = input(
                f'Enter platform-tools path (e.g. {getPlatformVar("platformToolsPathExample")}): ').replace(' ', '!')
            if os.path.isdir(data['platformToolsPath'].replace('!', ' ')) == False:
                print(
                    f'{Fore.RED}[X] Invalid platform-tools path{Fore.RESET}')
                sleep(3)
                badConfig(2)
                return
        if data['emulatorPath'] == '' or os.path.isdir(data['emulatorPath'].replace('!', ' ')) == False:
            data['emulatorPath'] = input(
                f'Enter emulator path (e.g. {getPlatformVar("emulatorPathExample")}): ').replace(' ', '!')
            if os.path.isdir(data['emulatorPath'].replace('!', ' ')) == False:
                print(f'{Fore.RED}[X] Invalid emulator path{Fore.RESET}')
                sleep(3)
                badConfig(2)
                return
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f'{Fore.GREEN}[√] Saved config.json{Fore.RESET}')
        sleep(3)
        welcome()


print(f'{Fore.YELLOW}[!] Loading config.json...{Fore.RESET}')
# check if file config.json exists
if not os.path.isfile('config.json'):
    print(f'{Fore.RED}[X] config.json not found{Fore.RESET}')
    print(f'{Fore.YELLOW}[!] Creating config.json{Fore.RESET}')
    data = {
        "baseIp": "",
        "platformToolsPath": "",
        "emulatorPath": "",
        "phones": []
    }
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f'{Fore.GREEN}[√] Created config.json{Fore.RESET}')
    badConfig(0)
else:
    # load config.json
    with open('config.json', 'r') as f:
        try:
            data = json.load(f)
            print(f'{Fore.GREEN}[√] Loaded config.json{Fore.RESET}')
            if data['baseIp'] == '' or re.match(r'^(?:[0-9]{1,3}\.){2}[0-9]{1,3}$', data['baseIp']) == None or data['platformToolsPath'] == '' or os.path.isdir(data['platformToolsPath'].replace('!', ' ')) == False or data['emulatorPath'] == '' or os.path.isdir(data['emulatorPath'].replace('!', ' ')) == False:
                badConfig(2)
            else:
                print(f'{Fore.YELLOW}[!] Checking ADB status...{Fore.RESET}')
                connectedDevicesTemp = []
                connectedDevicesTemp = list(filter(None, os.popen(
                    getPlatformVar("getdevices")).read().split('\n')))
                # remove 'List of devices attached'
                connectedDevicesTemp.pop(0)
                print(connectedDevicesTemp)
                welcome()
        except:
            badConfig(1)


def run(choice):
    global connectedDevices
    global connectedDevicesTemp
    if choice == 0:
        print(f'{Fore.YELLOW}[!] Refreshing...{Fore.RESET}')
        refreshDevices()
        welcome()
        return
    elif choice == 1:
        welcome(False, False, False)
        # get user input
        name = input('Enter device name ("M" menu): ')
        if name.lower() == 'm':
            welcome()
            return
        ip = input(
            f'Enter device IP ("X" to change base IP | "M" menu): {data["baseIp"]}.')
        # check if ip is valid
        if ip.lower() == 'x':
            def askNewBaseIp():
                welcome(False, False, False)
                currentBaseIp = 'Current base IP is not configured'
                baseIpQuestion = 'Enter new base IP (e.g. "192.168.1" | "M" menu): '
                if 'baseIp' in data:
                    currentBaseIp = f'Current base IP is: {data["baseIp"]}\n'
                    baseIpQuestion = f'Enter new base IP ("M" menu): '
                print(currentBaseIp)
                baseIpInput = input(baseIpQuestion)
                if baseIpInput.lower() == 'm':
                    welcome()
                    return
                if re.match(r'^(?:[0-9]{1,3}\.){2}[0-9]{1,3}$', baseIpInput):
                    data['baseIp'] = baseIpInput
                    with open('config.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    print(
                        f'{Fore.GREEN}[✓] Base IP changed successfully{Fore.RESET}')
                    sleep(3)
                    run(choice)
                    return
                else:
                    print(
                        f'{Fore.RED}[X] Invalid IP address (e.g. "192.168.1"){Fore.RESET}')
                    sleep(3)
                    askNewBaseIp()
                    return

            askNewBaseIp()
            return
        elif ip.lower() == 'm':
            welcome()
            return
        elif not ip.isdigit() or int(ip) > 255 or int(ip) < 0:
            print(f'{Fore.RED}[X] Invalid IP address{Fore.RESET}')
            sleep(3)
            run(choice)
            return
        # check if device already exists
        for i in data['phones']:
            if i['ip'] == ip:
                print(
                    f'{Fore.RED}[X] Device with this IP already exists{Fore.RESET}')
                sleep(3)
                run(choice)
                return
        # add device to config
        data['phones'].append({'name': name, 'ip': ip})
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f'{Fore.GREEN}[✓] Device added successfully{Fore.RESET}')
        sleep(3)
        welcome()
        return
    elif choice == 2:
        # check if there are any devices
        if len(data['phones']) == 0:
            print(f'{Fore.RED}[X] No devices to edit{Fore.RESET}')
            sleep(3)
            welcome()
            return

        # print devices
        def editDevicePrint():
            welcome(True, False, False)
            for i in data['phones']:
                if data['baseIp'] + "." + i['ip'] in connectedDevices:
                    print(
                        f'{Fore.YELLOW}[!] Device {i["name"]} is connected!{Fore.RESET}')
            # get user input
            choice = input(
                'Enter device id to edit (e.g. "c1" | "M" to go back to menu): ')
            if choice.lower() == 'm':
                welcome()
                return
            elif not choice.lower().startswith('c') or not not choice.lower().startswith('d') or not choice[1:].isdigit() or int(choice[1:]) > len(data['phones']) or int(choice[1:]) < 1:
                print(f'{Fore.RED}[X] Invalid device id{Fore.RESET}')
                sleep(3)
                editDevicePrint()
                return
            # get user input for new name
            newName = input(
                f'Enter new device name ("C" to keep "{data["phones"][int(choice[1:]) - 1]["name"]}" | "M" to go back to menu): ')
            if newName.lower() == 'm':
                welcome()
                return
            elif newName.lower() == 'c':
                newName = data['phones'][int(choice[1:]) - 1]['name']

            # get user input for new ip
            def askNewIp():
                changedIp = False
                for _ in data['phones']:
                    if data['baseIp'] + "." + data['phones'][int(choice[1:]) - 1]['ip'] in connectedDevices:
                        print(
                            f'{Fore.YELLOW}[!] Device {data["phones"][int(choice[1:]) - 1]["name"]} is connected! ("D" disconnect menu){Fore.RESET}')

                newIp = input(
                    f'Enter new device IP ("C" to keep "{data["baseIp"]}.{data["phones"][int(choice[1:]) - 1]["ip"]}" | "M" to go back to menu): ')
                if newIp.lower() == 'm':
                    welcome()
                    return
                elif newIp.lower() == 'c':
                    newIp = data['phones'][int(choice[1:]) - 1]['ip']
                elif not newIp.isdigit() or int(newIp) > 255 or int(newIp) < 0:
                    print(
                        f'{Fore.RED}[X] Invalid IP address{Fore.RESET}')
                    sleep(3)
                    askNewIp()
                    return
                else:
                    changedIp = True
                # check if device already exists but only if ip changed
                for i in data['phones']:
                    if i['ip'] == newIp and changedIp:
                        print(
                            f'{Fore.RED}[X] Device with this IP already exists{Fore.RESET}')
                        sleep(3)
                        askNewIp()
                        return
                # update device
                data['phones'][int(choice[1:]) - 1]['name'] = newName
                data['phones'][int(choice[1:]) - 1]['ip'] = newIp
                with open('config.json', 'w') as f:
                    json.dump(data, f, indent=4)
                print(
                    f'{Fore.GREEN}[✓] Device updated successfully{Fore.RESET}')
                sleep(3)
                welcome()
                return
            askNewIp()

        editDevicePrint()
        return
    elif choice == 3:
        # check if there are any devices
        if len(data['phones']) == 0:
            print(f'{Fore.RED}[X] No devices to delete{Fore.RESET}')
            sleep(3)
            welcome()
            return

        # print devices
        def deleteDevicePrint():
            welcome(True, False, False)
            for i in data['phones']:
                if data['baseIp'] + "." + i['ip'] in connectedDevices:
                    print(
                        f'{Fore.YELLOW}[!] Device {i["name"]} is connected!{Fore.RESET}')

            # get user input
            choice = input(
                '\nEnter device id to remove (e.g. "c1" | "M" to go back to menu): ')
            if choice.lower() == 'm':
                welcome()
                return
            # check if device exists
            if int(choice[1:]) > len(data['phones']):
                print(f'{Fore.RED}[X] Invalid device id{Fore.RESET}')
                sleep(3)
                deleteDevicePrint()
                return
            else:
                # remove device
                data['phones'].pop(int(choice[1:]) - 1)
                with open('config.json', 'w') as f:
                    json.dump(data, f, indent=4)
                print(
                    f'{Fore.GREEN}[✓] Device removed successfully{Fore.RESET}')
                sleep(3)
                welcome()
                return

        deleteDevicePrint()
    elif choice == 4:
        os.system(getPlatformVar("openAdb", ["%platformToolsPath%"]))
        welcome()
        return
    elif choice == 5:
        os.system(getPlatformVar("openEmulator", ["%emulatorPath%"]))
        welcome()
        return
    elif choice == 6:
        if checkVersion():
            sleep(10)
            sys.exit(1)
        else:
            sleep(3)
            welcome()
            return
    elif choice == 7:
        print(f'{Fore.YELLOW}[!] Exiting...{Fore.RESET}')
        sys.exit(0)
    elif choice.startswith('e'):
        # check if emulator exists
        if int(choice[1:]) > len(emulators):
            print(f'{Fore.RED}[X] Emulator does not exist{Fore.RESET}')
            sleep(3)
            welcome()
            return
        else:
            # start emulator
            print(
                f'{Fore.YELLOW}[!] Starting emulator {emulators[int(choice[1:]) - 1]}...{Fore.RESET}')
            os.system(
                getPlatformVar("startEmulator", [emulators[int(choice[1:]) - 1]]))
            sleep(3)
            welcome()
            return
    elif choice.startswith('c'):
        # check if device exists
        if int(choice[1:]) > len(data['phones']):
            print(f'{Fore.RED}[X] Device does not exist{Fore.RESET}')
            sleep(3)
            welcome()
            return
        else:
            def askPort():
                welcome(True, False, False, int(choice[1:]))
                # if the phone is already connected show warning
                for _ in data['phones']:
                    if data['baseIp'] + "." + data['phones'][int(choice[1:]) - 1]['ip'] in connectedDevices:
                        print(
                            f'{Fore.YELLOW}[!] Device {data["phones"][int(choice[1:]) - 1]["name"]} is already connected! ("D" disconnect menu){Fore.RESET}')

                port = input(
                    f'Enter port to connect to (e.g. "5555" | "M" menu | "D" disconnect menu): ')
                if port.lower() == 'm':
                    welcome()
                    return
                elif port.lower() == 'd':
                    run(f'd{choice[1:]}')
                    return
                elif not port.isdigit():
                    print(f'{Fore.RED}[X] Invalid port{Fore.RESET}')
                    sleep(3)
                    askPort()
                    return
                else:
                    print(
                        f'{Fore.YELLOW}[!] Connecting to device {data["phones"][int(choice[1:]) - 1]["name"]}...{Fore.RESET}')
                    cmd = subprocess.Popen(getPlatformVar("connectPhone", [
                        data["baseIp"] + "." + data["phones"][int(choice[1:]) - 1]["ip"] + ":" + port]), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    # wait for the cmd to finish
                    while cmd.poll() is None:
                        pass
                    output = cmd.stdout.read().decode('utf-8')
                    if output == "":
                        output = cmd.stderr.read().decode('utf-8')
                    if "cannot" not in output:
                        print(
                            f'{Fore.GREEN}[✓] Device connected successfully{Fore.RESET}')
                        sleep(3)
                        welcome()
                        return
                    else:
                        print(
                            f'\n{Fore.RED}[X] Failed to connect to device:{Fore.RESET}\n{output}')
                        sleep(10)
                        askPort()
                        return
            askPort()
    elif choice.startswith('d'):
        # check if device exists
        if int(choice[1:]) > len(data['phones']):
            print(f'{Fore.RED}[X] Device does not exist{Fore.RESET}')
            sleep(3)
            welcome()
            return
        else:
            def askPort():
                welcome(True, False, False, int(choice[1:]))
                # if the phone is not connected show warning
                for _ in data['phones']:
                    if data['baseIp'] + "." + data['phones'][int(choice[1:]) - 1]['ip'] not in connectedDevices:
                        print(
                            f'{Fore.YELLOW}[!] Device {data["phones"][int(choice[1:]) - 1]["name"]} is not connected! ("C" connect menu){Fore.RESET}')

                port = input(
                    f'Enter port to disconnect from (e.g. "5555" | "M" menu | "C" connect menu): ')
                if port.lower() == 'm':
                    welcome()
                    return
                elif port.lower() == 'c':
                    run(f'c{choice[1:]}')
                    return
                elif not port.isdigit():
                    print(f'{Fore.RED}[X] Invalid port{Fore.RESET}')
                    sleep(3)
                    askPort()
                    return
                else:
                    print(
                        f'{Fore.YELLOW}[!] Disconnecting from device {data["phones"][int(choice[1:]) - 1]["name"]}...{Fore.RESET}')
                    cmd = subprocess.Popen(getPlatformVar("disconnectPhone", [
                        data["baseIp"] + "." + data["phones"][int(choice[1:]) - 1]["ip"] + ":" + port]), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    # wait for the cmd to finish and store its output
                    while cmd.poll() is None:
                        pass
                    output = cmd.stdout.read().decode('utf-8')
                    if output == "":
                        output = cmd.stderr.read().decode('utf-8')

                    if "disconnected" in output:
                        print(
                            f'{Fore.GREEN}[✓] Device disconnected successfully{Fore.RESET}')
                        sleep(3)
                        welcome()
                        return
                    else:
                        print(
                            f'\n{Fore.RED}[X] Failed to disconnect from device:{Fore.RESET}\n{output}')
                        sleep(10)
                        askPort()
                        return
            askPort()


# get user input
while True:
    try:
        choice = input('Enter your choice: ')
        if choice.isdigit():
            if int(choice) > 7 or int(choice) < 0:
                raise ValueError
            else:
                run(int(choice))
        else:
            if choice.startswith('e'):
                if int(choice[1:]) > len(emulators):
                    raise ValueError
                else:
                    run(choice)
            elif choice.startswith('c'):
                if int(choice[1:]) > len(data['phones']):
                    raise ValueError
                else:
                    run(choice)
            elif choice.startswith('d'):
                if int(choice[1:]) > len(data['phones']):
                    raise ValueError
                else:
                    run(choice)
            else:
                raise ValueError

    except ValueError:
        print(
            f'{Fore.RED}[X] Invalid choice.\nPlease enter a number between 0 and 7 or a valid emulator ID or a valid device ID.{Fore.RESET}')
        sleep(5)
        welcome()
