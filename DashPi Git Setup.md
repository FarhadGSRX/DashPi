# Set Up File Structure
/home/dietpi/DashPi
- rpi-rgb-led-matrix (hzeller library)
- ...rest of my git

# 
# Git lines
# How to use git on the RasPi

## Fetch things down

> git fetch

> git reset --hard origin/master

  

## Check repository status

> git status

  

## Stage, Commit, and Push things up

### stage the files you've edited -- Lets git know about the file changes, but not permanent in the repo

> git add hello.html

> git add .

### using '.' will just tell it to look at the whole current directory

> git log --pretty=oneline

### If you omit the -m flag, it'll drop you into an editor for more advanced commit message editing

> git commit -m "First commit"

> git push
---
## Setting up the connection to the DashPi Git Repo

### First, we initialize our git repo manually

> git clone https://github.com/FarhadGSRX/DashPi.git DashPi  

> cd DashPi  

> git init

  

## Setting up connection to ExProc Git Repo

> git clone *** still haven't done this part yet; will do it next time the nerve strikes me...

  

At this point, the git repos are made, and `git pull` can be called in there to update it at any time.



# RGB Matrix Setup - Hzeller
Inside of /home/dietpi:

> sudo apt update
> sudo apt -y install git libgraphicsmagick++-dev libwebp-dev libavcodec-dev libavformat-dev libswscale-dev initramfs-tools
> git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
> cd rpi-rgb-led-matrix/utils
> make led-image-viewer
> make video-viewer
> cd rpi-rgb-led-matrix/examples-api-use
> make

## DashPi doing set up for python3 bindings of Zeller's library

>> sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
>> cd rpi-rgb-led-matrix
>> make build-python PYTHON=python3
>> 
>> sudo make install-python PYTHON=python3
>> > Unclear if I actually need this line, this might be out of date or something


## Sound Module Error:
One line at a time:

> cat <<EOF | sudo tee /etc/modprobe.d/blacklist-rgb-matrix.conf
>
> > blacklist snd_bcm2835
> > EOF
>
> sudo update-initramfs -u
> sudo reboot

> [!tip]-

> Incase you have trouble finding the '|' character, on the Jelly Comb keyboard, inside DietPi, it's Right Alt + Shift + ` (The top-left-most button)
