### Crontab and Reboot

#### The reboot process in order:

1. Enter DashPi folder

2. Use root user's crontab to run /home/dietpi/on_reboot.sh

3. That bash file should cd to DashPi folder, and run the following steps:

    3a. Git Pull or Fetch, Incorporate changes or whatever

    3b. Run Dashpi

  

**sudo crontab -u root -e**

  

    # @reboot bash /home/dietpi/DashPi/testing_reboot.sh

    @reboot /home/pi/on_reboot.sh

    0 4 * * * sudo reboot

  

**on_reboot.sh**

  

    cd /home/dietpi/DashPi

    git fetch --all >> dashpi_reboot_log.txt

    wait

    git reset --hard origin/master >> dashpi_reboot_log.txt

    wait

    pip3 install -r requirements.txt >> dashpi_reboot_log.txt

    wait

    python3 dashpi.py >> dashpi_log.txt