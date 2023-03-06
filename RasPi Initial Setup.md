---
Date Created: 03/05/2023 01:55:58
Last Updated: 03/05/2023 17:44:37
---

```toc
```

# Hardware Details
- RasPi 3b+
	- Architecture: armhf

# Choice of OS
- DietPi: Much lighter, recommended by Hzeller. Uses fewer GPIO pins.

- [ ] GPIO 27, Pin 13 on the Raspi, is probably being used for something, and getting in the way of being used to address the RGB Matrix. (Hzeller mentions this in his troubleshooting section, but I was naive and ignored him…)

# Installing DietPi

> Last done March 5th, 2023 → v8.14

## Flashing the SD Card
Download DietPi image from their website. Use Rufus or some other app to flash your SD card with the image.

> [!example]- Rufus Config
> ![[Pasted image 20230305021138.png|400]]

## Unattended Install (Optional)

Open `/boot/dietpi.txt` on the drive.
- **Network configuration** (e.g. WiFi, network and proxy settings)
- **System options** (e.g. timezone, hostname, root password)
- **Software preferences** (e.g. SSH server, file server, web server)
- **Software options** (e.g. VNC, Nextcloud, DietPi Dashboard)
- **Automatic software installation** (packages from `dietpi-software`)
- **User script** pre and post initial installation
- **Restore** from a previous made system backup

## Manual Install
Pop in the microSD card and boot up the RasPi.
1. Connect to WiFi network.
2. Let it finish updating.
3. Change global software password for DietPi-Software installs:
	1. KDashPiM
4. Change root and user passwords:
	1. KDietPiUserM
5. Serial/UART disabled.

### DietPi-Config (Software Selection)
1. Audio Options > Install ALSA
	1. Sound Card: rpi-bcm2835-auto
2. Advanced Options > Bluetooth > On
3. Language/Regional
	1. Timezone > Chicago
4. Security Options > Change Hostname > DashPi_v2

### DietPi-Software
- Cloud & Backup > Rclone[^1]
- System Stats & Management > Webmin
- Remote Access > Remote.It
- Hardware Projects > Python 3 RPi.GPIO
- Development & Programming > Git, Python 3
- Text Editors > Neovim
- File Servers > vsftpd[^2]
- SSH Server > Dropbear
## Confirm Upgrades
If you try to run the following commands, it should say there's nothing to install/update. (Cuz it already ran it above.)

> sudo apt-get update
> sudo apt full-upgrade

### Misc Programs
tmux: Allows terminal splitting for multi-window work

> sudo apt-get install tmux

Allows the "make" command

> sudo apt-get install build-essential

# Installing Python
Already installed via the installer above, but just in case:

> sudo apt-get install python3

## Package Managers

> sudo pip install setuptools, ez_setup
> sudo apt-get install pipenv

[^1]: Sync to various cloud file storages including GDrive
[^2]: FTP client
