<p align="center">
    <img alt="Flutter" src="logo.png">
</p>

# FlutterTools

Python tools to make Flutter development easier!

## Features

- **Saving physical devices** - Store the IP addresses of your frequently used physical devices for fast connection.
- **Quickly open ADB terminal** - Quickly open a terminal with adb to run commands.
- **Quickly open emulator terminal** - Quickly open a terminal with emulator to run commands.
- **Nice UI** - A nice UI to make the experience better.
- **Auto-update** - The script will automatically check for updates and update itself.
- **Cross-platform** - Works on Windows, Linux and macOS.
- And more to come!

## Installation

First, clone the repository to your local machine:

```bash
git clone https://github.com/HelloItsMeAdm/FlutterTools.git
```

Then, install the required packages:

```bash
# Navigate to the directory
cd FlutterTools

# Install packages
pip install -r requirements.txt
```

Finally, run the script:

```bash
python fluttertools.py
```

Please note that first time running the script you will have to enter the path to your ADB, emulator executables and base IP [(explained here)](#running-for-the-first-time). This is only required once.

## Updating

**IMPORTANT: Make sure to backup `config.json` before updating!**

To update the script, you have to manually download the latest version from the repository:

```bash
# Navigate to the directory
cd FlutterTools

# Download the latest version
git clone https://github.com/HelloItsMeAdm/FlutterTools.git
```

## Usage

### Base IP vs Device IP

The base IP is the IP that is the same for all of your devices. On the other hand, the device IP is the IP that is different for each device.

For example, if your device's IP is `192.168.2.123` your base IP is `192.168.2` and your device IP is `123`.

**It is important to know the difference between the two! Also don't put dots on the end of base IP or on the start of device IP.**

To get the IP of your phone you need to go to `Developer Settings > Wireless debugging > IP address`. If you don't have Developer Settings enabled, [read this](https://developer.android.com/studio/debug/dev-options).

_Note: The path to Developer Settings may be different on your device._

#### ADB path

Enter the path to your ADB executable. This is usually located in the Android SDK folder. If you don't have ADB installed, you can download it [here](https://developer.android.com/tools/releases/platform-tools).

**IMPORTANT: Do not include the executable name in the path.** For example, if your ADB executable is located in `C:\Users\YourUsername\AppData\Local\Android\Sdk\platform-tools\adb.exe`, you should enter `C:\Users\YourUsername\AppData\Local\Android\Sdk\platform-tools` as the path.

**Example paths:**

```bash
# Windows
C:\Users\YourUsername\AppData\Local\Android\Sdk\platform-tools

# Linux
/home/YourUsername/Android/Sdk/platform-tools

# macOS
/Users/YourUsername/Library/Android/sdk/platform-tools
```

#### Emulator path

Same as ADB path, but for the emulator executable. If you don't have the emulator installed, you can download it [here](https://developer.android.com/studio/releases/emulator).

**IMPORTANT: Do not include the executable name in the path.** For example, if your emulator executable is located in `C:\Users\YourUsername\AppData\Local\Android\Sdk\emulator\emulator.exe`, you should enter `C:\Users\YourUsername\AppData\Local\Android\Sdk\emulator` as the path.

**Example paths:**

```bash
# Windows
C:\Users\YourUsername\AppData\Local\Android\Sdk\emulator

# Linux
/home/YourUsername/Android/Sdk/emulator

# macOS
/Users/YourUsername/Library/Android/sdk/emulator
```

#### Base IP

Enter the base IP of your physical devices. If you don't know what the base IP is, [read the difference between base IP and device IP](#base-ip-vs-device-ip).

### Connecting/Disconnecting to a physical device

To quickly connect or disconnect to a physical device you can just write the device ID. This can be found in the list of devices.

#### Example

```bash
# Connecting to a device named Xiaomi Redmi Note 9 Pro
• c1/d1 - Xiaomi Redmi Note 9 Pro (192.168.2.123) (Disconnected)
...

# Writing c1 in the terminal will connect to the device
c1

# Writing d1 in the terminal will disconnect from the device
d1
```

### Starting an emulator

To quickly start an emulator you can just write the emulator ID. This can be found in the list of emulators.

#### Example

```bash
# Starting an emulator named Pixel 3a API 30
• e1 - Pixel_4_API_30
...

# Writing e1 in the terminal will start the emulator
e1
```

### Saving physical devices

To add a new physical device select 1 in the main menu.

#### Device name

Enter the name of the device. This is only used to identify the device in the list.

#### Device IP

Enter the IP of the device. If you don't know what the device IP is, [read the difference between base IP and device IP](#base-ip-vs-device-ip).

### Opening ADB terminal

To open an ADB terminal select `2` in the main menu. This will open new terminal with path to ADB.

### Opening emulator terminal

To open an emulator terminal select `3` in the main menu. This will open new terminal with path to emulator.

## License

- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
- Flutter Terms of Service can be found [here](https://policies.google.com/terms) and Flutter Privacy Policy can be found [here](https://policies.google.com/privacy).

<h1 class='parent' align="center">
  <div class='child' style="display: inline-block; margin:2vh 0">
    <a href="https://www.vojtech-adam.cz/" target="_blank">www.vojtech-adam.cz</a>
  </div>
</h1>
