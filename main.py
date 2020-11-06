from subprocess import Popen, PIPE
from time import sleep

class Radio:

    def __init__(self):
        self.playing = False

    def play(self, url):
        self.p = Popen(['mplayer', url], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.playing = True
    
    def stop(self):
        if self.playing:
            self.p.communicate(input="q".encode())
            self.playing = False

radio_stations_file = open("radio_stations.txt", "r")
radio_stations = radio_stations_file.read().split("\n")

radio = Radio()

for url in radio_stations:
    print("Start: " + url)
    radio.play(url)
    sleep(7)
    radio.stop()
    