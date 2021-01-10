import socket
import alsaaudio
import math
from mplayer import Player, CmdPrefix

# ----------- UDP ------------

localIP     = "192.168.1.136"
localPort   = 44444
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# ---------- ALSA ------------

# Init alsa mixer
m = alsaaudio.Mixer('Digital')

# ---------- MPlayer ----------

# Set default prefix for all Player instances
Player.cmd_prefix = CmdPrefix.PAUSING_KEEP

# Since autospawn is True by default, no need to call player.spawn() manually
player = Player()

# -------- RADIO ----------

# Load Radio URLs
radio_stations_file = open("radio_stations.txt", "r")
radio_stations = radio_stations_file.read().split("\n")
radio_id = 0

player.loadfile(radio_stations[radio_id])

# ---------- LOOP ------------

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    if message == "Play":
        player.loadfile(radio_stations[radio_id])
    elif message == "Stop":
        player.pause()
    elif message == "Next":
        if radio_id+1 < len(radio_stations):
            radio_id = radio_id + 1
        else:
            radio_id = 0
        
        player.loadfile(radio_stations[radio_id])
    elif message == "Exit":
        player.quit()
        exit()

    # Extract volume
    vol = message[5]

    # Set volume
    m.setvolume(int(50.0*math.log10(1.0 + vol/255.0*99.0)))

player.quit()
