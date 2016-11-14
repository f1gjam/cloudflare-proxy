#Cloudflare-Proxy

This Python script allows you to disable or restore the proxy setting for ALL DNS records in Cloudflare


**NOTE:** This script uses the [python-cloudflare](https://github.com/cloudflare/python-cloudflare).

##Installation
### Pre-requisites
Ensure that the following items are installed on your machine which will execute this script. Also ensure you have permissions to clone the repositories.

`git`
`python 2.7`
`pip`

**NOTE** Ensure you have installed cloudflare_backup (https://github.com/f1gjam/cloudflare-backup) script and have a backup created.

Clone the following python repositories

`git clone git@github.com:f1gjam/cloudflare-proxy.git`

Now you can install the cloudflare python module

`pip install cloudflare argparse`

Create the Cloudflare configuration directory and file (This should be under the user who will execute the script)
**DO NOT CHANGE THE LOCATION OF THE FILE**

`mkdir ~/.cloudflare/`
`nano -w ~/.cloudflare/cloudflare.cfg` - you can use whichever editor you like

**Example contents for the file below**
```
[CloudFlare]
email = my_cloudflare_email@somewhere.com
token = jkhwj24h9812h12jkdwuykk2108721321asdl
certtoken = v1.0-...
```

##How to use

To disable the proxy
`python <path to script>/cloudflare_proxy.py --disable`

To restore proxy settings from backup file
`python <path to script>/cloudflare_proxy.py --restore`

**NOTE** Both disabling and restoring require a backup to have been run and the backup files to be in /tmp

The script will read ALL dns zones and associated records and disable or restore the proxy setting
