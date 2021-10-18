
# on MacOS
# vlc *.mp4 --video-on-top --random --loop --fullscreen --no-video-title --autoscale

# Start cvlc and keep it running
#   cvlc experiments/data/* --random --loop --fullscreen --no-video-title --autoscale --intf http --http-host localhost --http-port 9090 --http-password vlc
# Use the http interface to send comnmands
#   https://wiki.videolan.org/Interfaces/
#   https://wiki.videolan.org/VLC_HTTP_requests/
#   ex: curl http://localhost:9090/requests/playlist.xml -u :vlc

# add <mrl> to playlist and start playback: status.xml?command=in_play&input=<mrl>

# add <mrl> to playlist:    status.xml?command=in_enqueue&input=<mrl>

# empty playlist:  status.xml?command=pl_empty

# toggle random playback:   status.xml?command=pl_random

# toggle loop:  status.xml?command=pl_loop

# toggle fullscreen:    status.xml?command=fullscreen

# get <dir>'s filelist:     browse.xml?dir=<dir>
# curl -u :vlc http://localhost:9090/requests/browse.json?dir=blackrockstation/experiments/data
