import time
import fluidsynth

fs = fluidsynth.Synth()
fs.start()
## Your installation of FluidSynth may require a different driver.
## Use something like:
# fs.start(driver="pulseaudio")

sfid = fs.sfload("example.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
time.sleep(0.3)

for i in range(10):
    fs.cc(0, 93, 127)
    fs.pitch_bend(0, i * 512)
    time.sleep(0.1)
fs.noteoff(0, 60)

time.sleep(1.0)

fs.delete()
