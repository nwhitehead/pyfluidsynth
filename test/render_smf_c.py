#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A direct translation of the following C code from the fluidsynth
documentation::

    #include <fluidsynth.h>

    int main() {
        fluid_settings_t * settings;
        fluid_synth_t * synth;
        fluid_player_t * player;
        fluid_file_renderer_t * renderer;

        settings = new_fluid_settings();
        // specify the file to store the audio to
        // make sure you compiled fluidsynth with libsndfile to get a real wave file
        // otherwise this file will only contain raw s16 stereo PCM
        fluid_settings_setstr(settings, "audio.file.name", "test.wav");
        // use number of samples processed as timing source, rather than the system timer
        fluid_settings_setstr(settings, "player.timing-source", "sample");
        // since this is a non-realtime szenario, there is no need to pin the sample data
        fluid_settings_setint(settings, "synth.lock-memory", 0);

        synth = new_fluid_synth(settings);
        fluid_synth_sfload(synth, "example.sf2", 0);

        player = new_fluid_player(synth);
        fluid_player_add(player, "test.mid");
        fluid_player_play(player);

        renderer = new_fluid_file_renderer(synth);

        while (fluid_player_get_status(player) == FLUID_PLAYER_PLAYING) {
            if (fluid_file_renderer_process_block(renderer) != FLUID_OK) {
                break;
            }
        }

        // just for sure: stop the playback explicitly and wait until finished
        fluid_player_stop(player);
        fluid_player_join(player);

        delete_fluid_file_renderer(renderer);
        delete_fluid_player(player);
        delete_fluid_synth(synth);
        delete_fluid_settings(settings);
    }

If you put this into a file name ``render_smf.c`` you can compile it with:

    gcc -o render_smf `pkg-config --cflags --libs fluidsynth` render_smf.c

"""

from fluidsynth import *

def main():
    settings = new_fluid_settings()
    # specify the file to store the audio to
    # make sure you compiled fluidsynth with libsndfile to get a real wave file
    # otherwise this file will only contain raw s16 stereo PCM
    fluid_settings_setstr(settings, b"audio.file.name", b"test.wav")
    # use number of samples processed as timing source, rather than the system timer
    fluid_settings_setstr(settings, b"player.timing-source", b"sample")
    # since this is a non-realtime szenario, there is no need to pin the sample data
    fluid_settings_setint(settings, b"synth.lock-memory", 0)

    synth = new_fluid_synth(settings)
    fluid_synth_sfload(synth, b"example.sf2", 0)

    player = new_fluid_player(synth)
    fluid_player_add(player, b"test.mid")
    fluid_player_play(player)

    renderer = new_fluid_file_renderer(synth)

    while fluid_player_get_status(player) == FLUID_PLAYER_PLAYING:
        if fluid_file_renderer_process_block(renderer) != FLUID_OK:
            break

    # just for sure: stop the playback explicitly and wait until finished
    fluid_player_stop(player)
    fluid_player_join(player)

    delete_fluid_file_renderer(renderer)
    delete_fluid_player(player)
    delete_fluid_synth(synth)
    delete_fluid_settings(settings)


if __name__ == '__main__':
    import sys
    sys.exit(main() or 0)