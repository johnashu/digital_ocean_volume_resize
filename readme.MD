# Monitor and Resize Digital Ocean Linnode Volumes

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

INCREASE_BY_PERCENTAGE=2 
BELOW_THIS_PERCENT_TO_RESIZE=5

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

``` bash 

cat<<-EOF > /etc/systemd/system/resize_hdd.service
[Unit]
Description=resize_hdd daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=<USER>
WorkingDirectory=/path/to/digital_ocean_volume_resize
ExecStart=python3 main.py
SyslogIdentifier=resize_hdd
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
EOF

```
# Trigger SystemD and Check Status

`sudo systemctl daemon-reload`

`sudo chmod 755 /etc/systemd/system/resize_hdd.service`

`sudo systemctl enable resize_hdd.service`

`sudo service resize_hdd start `

`sudo service resize_hdd status`


# Read Logs

`tail -f /var/log/syslog`

`journalctl  -xefu resize_hdd`

log file is in `logs/data.log`
