#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyfluidsynth",
# ]
# ///

import io
import wave

import numpy

import fluidsynth


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)


output_audio_samplerate = 16000
default_channels = 2
# only initialize it once if run on the server side.
fs = fluidsynth.Synth(samplerate=output_audio_samplerate)
fs.sfload(local_file_path("example.sf2"))


def midi2audio_bytes(midi_file_path: str) -> bytes:
    """
    Convert a MIDI file to audio bytes.
    """
    fs.play_midi_file(midi_file_path)
    samples = []
    while True:
        samples = numpy.append(samples, fs.get_samples(output_audio_samplerate))
        if fluidsynth.fluid_player_get_status(fs.player) != fluidsynth.FLUID_PLAYER_PLAYING:
            break
    # release after each playback is complete
    fs.play_midi_stop()
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(default_channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(output_audio_samplerate)
        wf.writeframesraw(fluidsynth.raw_audio_string(samples))
    return wav_buffer.getvalue()


if __name__ == "__main__":
    midi_bytes = midi2audio_bytes(local_file_path("1080-c01.mid"))
    with open(local_file_path("1080-c01.wav"), "wb") as f:
        f.write(midi_bytes)
