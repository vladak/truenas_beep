
# TrueNAS alerting via system beep

For my home NAS I wanted to get a notification without relying on external system. Using system beeper made sense to me, however TrueNAS does not support that out of the box. This already did its job when one of the disks died.

# Getting speaker to work

1. connect [PC speaker](https://en.wikipedia.org/wiki/PC_speaker) to the motherboard
1. download `kernel.txz` for the **appropriate** FreeBSD kernel version (https://download.freebsd.org/ftp/releases/amd64/)
1. extract `/boot/kernel/speaker.ko`: `xz -dc kernel.txz | tar xvf -` (for some reason trying to extract individual file results in corrupted file with `Line too long` the error message emitted by `tar`)
1. `kldload speaker`
1. ensure the speaker module is loaded on every boot: `echo 'speaker_load="YES"' >> /boot/loader.conf`
1. `/usr/sbin/spkrtest` (shell script) can be used to test the speaker

## Alerting for all events via Python

Create a simple script to play a melody ([spkr(4)](https://www.freebsd.org/cgi/man.cgi?query=spkr&apropos=0&sektion=0&manpath=FreeBSD+12.2-RELEASE+and+Ports&arch=default&format=html) has detailed guide how to play the device) whenever a resource fails (e.g. ZFS pool health).

Add a cron job (via UI) to run the script as `root` (for write access to the
`/dev/speaker` device - no need in this case to complicate this with delegating
privileges to non-root user via `devfs`) once every hour.

It is possible to get list of alerts via the RESTful API (https://www.truenas.com/docs/hub/additional-topics/api/rest_api/).

1. Create API token in the TrueNAS web UI (right top: Settings -> API keys)
2. install the requirements
```
   python3 -m venv env
   . ./env/bin/activate
   pip install -r requirements.txt
```
3. use the token:
```
   sudo ./beep.py --token <INSERT_TOKEN_VALUE> --url https://NAS
```

It would be much more convenient if the speaker could be listed as a Alert service in the TrueNAS GUI. Filed https://jira.ixsystems.com/browse/NAS-108740 to track this enhancement.
