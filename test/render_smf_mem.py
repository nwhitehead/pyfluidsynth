#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Renders a Standard MIDI File (SMF) to an audio file using a given SF2 soundfont."""

import sys
from os.path import splitext
from fluidsynth import Synth, Player


def main(args=None):
    if len(args) < 2:
        return "Usage: render_smf.py <SF2 file> <SMF input file> [<audio output filename>]"
    else:
        sf2_filename = args.pop(0)
        smf_filename = args.pop(0)

    if args:
        output_filename = args.pop(0)
    else:
        output_filename = splitext(smf_filename)[0] + '.wav'

    def progress(fn, ft, num_samples, period_size):
        if not num_samples % (period_size * 16):
            print("%d samples written to '%s'." % (num_samples, fn))

    synth = Synth(samplerate=41000)
    synth.sfload(sf2_filename)
    player = Player(synth)

    with open(smf_filename, 'rb') as fp:
        data = fp.read()

    player.add_mem(data)

    player.play()
    player.render(output_filename, progress_callback=progress)
    player.delete()
    synth.delete()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)