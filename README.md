
# TrueNAS alerting via system beep

# Getting speaker to work

1. connect [PC speaker](https://en.wikipedia.org/wiki/PC_speaker) to the motherboard
1. download `kernel.txz` for the appropriate FreeBSD kernel version (https://download.freebsd.org/ftp/releases/amd64/)
1. extract `/boot/kernel/speaker.ko`: `xz -dc kernel.txz | tar xvf -` (for some reason trying to extract individual file results in corrupted file with `Line too long` the error message emitted by `tar`)
1. `kldload speaker`
1. `spkrtest`
1. ensure the speaker module is loaded on every boot: `echo 'speaker_load="YES"' >> /boot/loader.conf`
1. peruse `/usr/sbin/spkrtest` (shell script) can be used to test the speaker

## Alerting for ZFS via shell script (done)

Create a simple script to play a melody (spkr(4) has detailed guide how to play the device) whenever a resource fails (e.g. ZFS pool health).

Add a cron job (via UI) to run the script as `root` (for write access to the `/dev/speaker` device - no need in this case to complicate this with delegating privileges to non-root user via `devfs`) once every hour

The script:
```shell
#!/bin/sh

speaker="/dev/speaker"
music="msl16oldcd4mll8pcb-agf+4.g4p4<msl16dcd4mll8pa.a+f+4p16g4"

zpool list -H -o health | while read state; do
	if [ "x$state" != "xONLINE" ]; then
		echo ${music} > ${speaker}
	fi
done
```

## Alerting for all events via Python (TODO)

It is possible to get list of alerts via the RESTful API (https://www.truenas.com/docs/hub/additional-topics/api/rest_api/).

1. Create API token (right top: Settings -> API keys)
1. use the token:
```
curl -s --insecure -L -X GET "http://nas.local.lab.devnull.cz/api/v2.0/alert/list" \
    -H "accept: */*" -H "Authorization: Bearer XXX" | jq
```

Best to be done via Python `requests` module.
