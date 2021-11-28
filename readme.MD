# Monitor and Resize Digital Ocean Linnode Volumes

# Clone Git Repo

`git clone https://github.com/johnashu/digital_ocean_volume_resize.git`

To update use `git pull`

# Create .env file

Create a file named `.env` 

Add the following:

> Generate a token in the API section of your provider.

> Use whole numbers for the Percentages

> Add Email information - See your email provider..

> If using Linnode, make sure to setup Email
> https://www.linode.com/community/questions/19082/i-just-created-my-first-linode-and-i-cant-send-emails-why

> Add Vstats Token.  On Telegram -> @vStatsBot - use command `/volumetoken` to generate a token.

> Toggle the `SEND_EMAIL` & `SEND_ALERT_TO_VSTATS` choose `True` / `False` to send alerts to these 2.

```
# Choose DO (Digital Ocean) / LN (Linnode)
PROVIDER=DO
VOLUME_NAME=volume-fra1-01

# API Key
TOKEN=<PROVIDER API TOKEN>

# Percentage to trigger and Amount
INCREASE_BY_PERCENTAGE=2 
BELOW_THIS_PERCENT_TO_RESIZE=5

# Hours in-between checks
HOURS=6

# Email Options
SEND_EMAIL=False
EMAIL_SMTP=smtp.123-reg.co.uk
EMAIL_PASS=<EMaiL PASSWORD>
EMAIL_FROM=john@maffaz.com
EMAIL_TO=mennovandevlees@gmail.com

# Vstats Telegram Bot Options
SEND_ALERT_TO_VSTATS=True
VSTATS_TOKEN=<VSTATS BOT>

```

# install dependencies

`sudo apt update && sudo apt upgrade -y`

`apt install python3-pip`

`pip3 install -r requirements.txt`

# Run program.

`python3 main.py`


# create systemd

> if you are unsure of the location of `/path/to/digital_ocean_volume_resize`
> navigate to the dir and run the command `pwd` (Path Current Directoy)
> This will give you the location , i.e. `/maffaz/harmony/digital_ocean_volume_resize`

``` bash 

cat<<-EOF > /etc/systemd/system/resize_volume.service
[Unit]
Description=resize_volume daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=<USER>
WorkingDirectory=/path/to/digital_ocean_volume_resize
ExecStart=python3 main.py
SyslogIdentifier=resize_volume
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
EOF

```
# Trigger SystemD and Check Status

`sudo systemctl daemon-reload`

`sudo chmod 755 /etc/systemd/system/resize_volume.service`

`sudo systemctl enable resize_volume.service`

`sudo service resize_volume start `

`sudo service resize_volume status`


# Read Logs

`tail -f /var/log/syslog`

`journalctl  -xefu resize_volume`

log file is in `logs/data.log`


# NOTES

Please be aware that there are discrepencies between what is Reported by the Provider and what is reported by the System

In the Email and alerts you will see 2 seperate values.

1. **Resized Digital Ocean Volume volume-sfo3-02 resizing from 649 GB -> 655 GB**
    > This is the Size that will be displayed in the Volume when you log in to your provider website and check your volume online. 

2. **System Original Size : 644 | System New Size: 650**
    > This is the size that will be displayed on your node if you run the command `df -h | grep /mnt/<VOLUME_NAME>`
    
    i.e.
    
    `df -h | grep /mnt/volume_sfo3_02`
    > */dev/sda* **650G** *412G  210G  67% /mnt/volume_sfo3_02*

