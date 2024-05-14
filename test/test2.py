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

s = []

fs = fluidsynth.Synth()

# Initial silence is 1 second
s = numpy.append(s, fs.get_samples(44100 * 1))

sfid = fs.sfload(local_file_path("example.sf2"))
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

# Chord is held for 2 seconds
s = numpy.append(s, fs.get_samples(44100 * 2))

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

# Decay of chord is held for 1 second
s = numpy.append(s, fs.get_samples(44100 * 1))

fs.delete()

samps = fluidsynth.raw_audio_string(s)

print(len(samps))
print('Starting playback')
strm.write(samps)
