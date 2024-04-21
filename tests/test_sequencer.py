#!/usr/bin/env python3

import time
import fluidsynth
from ctypes import *

seqduration = 1000

def schedule_next_callback():
	# I want to be called back before the end of the next sequence
	callbackdate = int(now + seqduration/2)
	sequencer.timer(callbackdate, dest=mySeqID)

def schedule_next_sequence():
	global now
	# the sequence to play
	# the beat : 2 beats per sequence
	sequencer.note(int(now + seqduration * 1/2), 0, 60, duration=250, velocity=80, dest=synthSeqID)
	sequencer.note(int(now + seqduration * 2/2), 0, 60, duration=250, velocity=80, dest=synthSeqID)
	# melody
	sequencer.note(int(now + seqduration*1/10), 1, 45, duration=250, velocity=int(127*2/3), dest=synthSeqID)
	sequencer.note(int(now + seqduration*4/10), 1, 50, duration=250, velocity=int(127*2/3), dest=synthSeqID)
	sequencer.note(int(now + seqduration*8/10), 1, 55, duration=250, velocity=int(127*3/3), dest=synthSeqID)
	# so that we are called back early enough to schedule the next sequence
	schedule_next_callback()
	
	now = now + seqduration

def seq_callback(time, event, seq, data):
	schedule_next_sequence()

if __name__=="__main__":
	global sequencer, fs, mySeqID, synthSeqID, now
	fs = fluidsynth.Synth()
	fs.start()
	# you might have to use other drivers:
	#fs.start(driver="alsa", midi_driver="alsa_seq")

	sfid = fs.sfload("example.sf2")
	fs.program_select(0, sfid, 0, 0)
	fs.program_select(1, sfid, 0, 0) # use the same program for channel 2 for cheapness

	sequencer = fluidsynth.Sequencer()
	synthSeqID = sequencer.register_fluidsynth(fs)
	mySeqID = sequencer.register_client("mycallback", seq_callback)
	now = sequencer.get_tick()
	schedule_next_sequence()
	
	time.sleep(10)
	
	sequencer.delete()
	fs.delete()
