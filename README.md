# pyFluidSynth

_Python bindings for FluidSynth_

This package contains Python bindings for FluidSynth.  FluidSynth is a software
synthesizer for generating music.  It works like a MIDI synthesizer.  You load
patches, set parameters, then send NOTEON and NOTEOFF events to play notes.
Instruments are defined in SoundFonts, generally files with the extension SF2.
FluidSynth can either be used to play audio itself, or you can call a function
that returns chunks of audio data and output the data to the soundcard yourself.
FluidSynth works on all major platforms, so pyFluidSynth should also.

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nwhitehead/pyfluidsynth/ci.yml) | ![PyPI - Version](https://img.shields.io/pypi/v/pyFluidSynth) | ![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pyFluidSynth) | 


## Requirements

[FluidSynth](http://www.fluidsynth.org/) (2.0.0 or later)
* [Windows/Android FluidSynth Releases](https://github.com/FluidSynth/fluidsynth/releases)
* [MacOS/Linux Distributions](https://github.com/FluidSynth/fluidsynth/wiki/Download#distributions)
* [Building from Source](https://github.com/FluidSynth/fluidsynth/wiki/BuildingWithCMake)

(optional) [NumPy](http://numpy.org/) 1.0 or later for some features

NOTE: If you don't need all the features of FluidSynth you may be interested in
[tinysoundfont-pybind](https://github.com/nwhitehead/tinysoundfont-pybind) which
is a self-contained Python package that includes
[TinySoundFont](https://github.com/schellingb/TinySoundFont) for SoundFont
playback and is permissively licensed.


## Installation

To use the latest official release:

    pip install pyfluidsynth


## Pre-release Versions

To use pre-release versions of this package, clone this repository, go to the
repository directory, then do:

    pip install --editable .


## Example

Here is a program that plays a chord for a second.

```python
import time
import fluidsynth

fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload("example.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()
```

First a Synth object is created to control playback.
The `start()` method starts audio output in a separate thread.

To get sound, you need to choose an instrument.  First load a
SoundFont with `sfload()`, then select a bank and preset with
`program_select()`.

```python
program_select(track, soundfontid, banknum, presetnum)
```

To start a note, use the noteon() method.

```python
noteon(track, midinum, velocity)
```

To stop a note, use noteoff().

```python
noteoff(track, midinum)
```


## Managing Audio

You can also manage audio IO yourself and just use FluidSynth to
calculate the samples for the music.  You might do this, for example,
in a game with WAV sound effects and algorithmically generated music.
To do this, create the Synth object but don't call `start()`.  To
generate the next chunk of audio, call `get_samples()`.

```python
get_samples(len)
```

The length you pass will be the number of audio samples. Unless
specified otherwise, FluidSynth assumes an output rate of 44100 Hz.
The return value will be a Numpy array of samples.  By default
FluidSynth generates stereo sound, so the return array will be
length `2 * len`.

To join arrays together, use `numpy.append()`.

To convert an array of samples into a string of bytes suitable for sending
to the soundcard, use `fluidsynth.raw_audio_string(samples)`.

Here is an example that generates a chord then plays the data using
PyAudio.

```python
import time
import numpy
import pyaudio
import fluidsynth

pa = pyaudio.PyAudio()
strm = pa.open(
    format = pyaudio.paInt16,
    channels = 2, 
    rate = 44100, 
    output = True)

s = []

fl = fluidsynth.Synth()

# Initial silence is 1 second
s = numpy.append(s, fl.get_samples(44100 * 1))

sfid = fl.sfload("example.sf2")
fl.program_select(0, sfid, 0, 0)

fl.noteon(0, 60, 30)
fl.noteon(0, 67, 30)
fl.noteon(0, 76, 30)

# Chord is held for 2 seconds
s = numpy.append(s, fl.get_samples(44100 * 2))

fl.noteoff(0, 60)
fl.noteoff(0, 67)
fl.noteoff(0, 76)

# Decay of chord is held for 1 second
s = numpy.append(s, fl.get_samples(44100 * 1))

fl.delete()

samps = fluidsynth.raw_audio_string(s)

print(len(samps))
print('Starting playback')
strm.write(samps)
```

## Using the Sequencer

You can create a sequencer as follows:
```python
import fluidsynth

seq = fluidsynth.Sequencer()
```
This will by default create a sequencer that will advance at 
a rate of 1000 ticks per second. To change the rate at which
the sequencer advances, you can give it the optional `time_scale`
parameter. As a clock source, it will use your system clock. In
order to manually advance the sequencer, you can give it the
parameter `use_system_timer=False`. You will then have to advance
it using `sequencer.process`.

In order to make the sequencer aware of your synthesizer, you have to
register it:
```python
fs = fluidsynth.Synth()
# init and start the synthesizer as described above…

synth_id = seq.register_fluidsynth(fs)
```
You have to keep `synth_id` and use it as a `target` for the midi events
you want to schedule. Now, you can sequence actual notes:
```python
seq.note_on(time=500, absolute=False, channel=0, key=60, velocity=80, dest=synth_id)
```
If you use relative timing like above, the sequencer will
schedule the event the specified time from the current position.
Otherwise, if `absolute` is `True` (the default), you have to use
absolute track positions (in ticks). So the following code snippet
will do the same as the one above:
```python
current_time = seq.get_tick()
seq.note_on(current_time + 500, 0, 60, 80, dest=synth_id)
```
You can also register your own callback functions to be called at
certain ticks:
```python
def seq_callback(time, event, seq, data):
    print('callback called!')

callback_id = sequencer.register_client("myCallback", seq_callback)

sequencer.timer(current_time + 2000, dest=callback_id)
```
Note that event and seq are low-level objects, not actual Python objects.

You can find a complete example (inspired by [this one from the fluidsynth library](http://www.fluidsynth.org/api/index.html#Sequencer)) in the test folder.


## Bugs and Limitations

Not all functions in FluidSynth are bound.

Not much error checking, FluidSynth will segfault/crash if you call
the functions incorrectly sometimes.


## Authors

This project was originally created by Nathan Whitehead `nwhitehe@gmail.com` but is the work of many. See [CONTRIBUTORS](./CONTRIBUTORS.md).


## License

Released under the LGPL v2.1 or any later
version (this is the same as FluidSynth).

Copyright 2008--2024, Nathan Whitehead and contributors.
