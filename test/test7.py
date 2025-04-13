#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyfluidsynth",
# ]
# ///

import fluidsynth


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)

fs = fluidsynth.Synth()
sfid = fs.sfload(local_file_path("example.sf2"))
fs.midi2audio(local_file_path("1080-c01.mid"), local_file_path("1080-c01.wav"))
# A Synth object can synthesize multiple files. For example:
# fs.midi2audio(local_file_path("1080-c02.mid"), local_file_path("1080-c02.wav"))
# fs.midi2audio(local_file_path("1080-c03.mid"), local_file_path("1080-c03.wav"))

fs.delete()
