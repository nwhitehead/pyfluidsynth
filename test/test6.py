import numpy
import pyaudio

import fluidsynth


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)

pa = pyaudio.PyAudio()
strm = pa.open(
    format = pyaudio.paInt16,
    channels = 2,
    rate = 44100,
    output = True)

fs = fluidsynth.Synth()
fs.custom_router_callback = None

sfid = fs.sfload(local_file_path("example.sf2"))
fs.program_select(0, sfid, 0, 0)

fs.play_midi_file(local_file_path("1080-c01.mid"))

# Generate 10 seconds of audio into s
s = []
for _ in range(10):
    s = numpy.append(s, fs.get_samples(44100))
    if fluidsynth.fluid_player_get_status(fs.player) != fluidsynth.FLUID_PLAYER_PLAYING:
        break

fs.delete()

samps = fluidsynth.raw_audio_string(s)
print('Starting playback')
strm.write(samps)
