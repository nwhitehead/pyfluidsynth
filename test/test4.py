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

# Note that reverb send amount from presets is also determined by SF2 file.
# If needed you can edit SF2 files with Polytope. To add reverb:
#   * Open SF2 file in Polytope.
#   * Choose the desired preset in Polytope in left panel.
#   * Scroll down to "Reverb (%)".
#   * In "Global" column of "Reverb (%)" row set to 100.0 or appropriate percentage.
#   * Save SF2 file.
fs.set_reverb(roomsize=0.8, damping=0.2, width=50.0, level=0.5)
fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(2.0)
fs.pitch_bend(0, -8192)
time.sleep(2.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(2.0)

fs.delete()
