from setuptools import setup

setup (name = 'pyFluidSynth',
       version = '1.3.1',
       author = 'Nathan Whitehead',
       author_email = 'nwhitehe@gmail.com',
       url = 'https://github.com/nwhitehead/pyfluidsynth',
       description = 'Python bindings for FluidSynth, a MIDI synthesizer that uses SoundFont instruments',
      long_description = '''
This module contains python bindings for FluidSynth.  FluidSynth is a
software synthesizer for generating music.  It works like a MIDI
synthesizer.  You load patches, set parameters, then send NOTEON and
NOTEOFF events to play notes.  Instruments are defined in SoundFonts,
generally files with the extension SF2.  FluidSynth can either be used
to play audio itself, or you can call a function that returns chunks
of audio data and output the data to the soundcard yourself.
''',
       py_modules = ['fluidsynth'],
       install_requires = ['numpy'])
