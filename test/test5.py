import time

import fluidsynth


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)

fs = fluidsynth.Synth()
fs.start()
## Your installation of FluidSynth may require a different driver.
## Use something like:
# fs.start(driver="pulseaudio")

sfid = fs.sfload(local_file_path("example.sf2"))
fs.program_select(0, sfid, 0, 0)

fs.play_midi_file(local_file_path("1080-c01.mid"))
while fluidsynth.fluid_player_get_status(fs.player) == fluidsynth.FLUID_PLAYER_PLAYING:
    time.sleep(1)

fs.delete()
