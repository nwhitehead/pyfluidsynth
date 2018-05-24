"""
================================================================================

    pyFluidSynth

    Python bindings for FluidSynth

    Copyright 2008, Nathan Whitehead <nwhitehe@gmail.com>


    Released under the LGPL

    This module contains python bindings for FluidSynth.  FluidSynth is a
    software synthesizer for generating music.  It works like a MIDI
    synthesizer.  You load patches, set parameters, then send NOTEON and
    NOTEOFF events to play notes.  Instruments are defined in SoundFonts,
    generally files with the extension SF2.  FluidSynth can either be used
    to play audio itself, or you can call a function that returns chunks
    of audio data and output the data to the soundcard yourself.
    FluidSynth works on all major platforms, so pyFluidSynth should also.

================================================================================

Added lots of bindings and stuff to help with playing live -- Bill Peterson <albedozero@gmail.com>
Added sequencer support -- Christian Romberg <distjubo@gmail.com>
"""

from ctypes import *
from ctypes.util import find_library
from future.utils import iteritems

# A short circuited or expression to find the FluidSynth library
# (mostly needed for Windows distributions of libfluidsynth supplied with QSynth)

lib = find_library('fluidsynth') or \
    find_library('libfluidsynth') or \
    find_library('libfluidsynth-1')

if lib is None:
    raise ImportError("Couldn't find the FluidSynth library.")

# Dynamically link the FluidSynth library
_fl = CDLL(lib)

# Helper function for declaring function prototypes
def cfunc(name, result, *args):
    """Build and apply a ctypes prototype complete with parameter flags"""
    atypes = []
    aflags = []
    for arg in args:
        atypes.append(arg[1])
        aflags.append((arg[2], arg[0]) + arg[3:])
    return CFUNCTYPE(result, *atypes)((name, _fl), tuple(aflags))


# Bump this up when changing the interface for users
api_version = '1.2.5'

# Function prototypes for C versions of functions

FLUID_OK = 0
FLUID_FAILED = -1

# fluid settings
new_fluid_settings = cfunc('new_fluid_settings', c_void_p)

fluid_settings_setstr = cfunc('fluid_settings_setstr', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('str', c_char_p, 1))

fluid_settings_setnum = cfunc('fluid_settings_setnum', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', c_double, 1))

fluid_settings_setint = cfunc('fluid_settings_setint', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', c_int, 1))

delete_fluid_settings = cfunc('delete_fluid_settings', None,
                              ('settings', c_void_p, 1))

# fluid synth
new_fluid_synth = cfunc('new_fluid_synth', c_void_p,
                        ('settings', c_void_p, 1))

delete_fluid_synth = cfunc('delete_fluid_synth', None,
                           ('synth', c_void_p, 1))

fluid_synth_sfload = cfunc('fluid_synth_sfload', c_int,
                           ('synth', c_void_p, 1),
                           ('filename', c_char_p, 1),
                           ('update_midi_presets', c_int, 1))

fluid_synth_sfunload = cfunc('fluid_synth_sfunload', c_int,
                           ('synth', c_void_p, 1),
                           ('sfid', c_int, 1),
                           ('update_midi_presets', c_int, 1))

fluid_synth_program_select = cfunc('fluid_synth_program_select', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1),
                                   ('sfid', c_int, 1),
                                   ('bank', c_int, 1),
                                   ('preset', c_int, 1))

fluid_synth_noteon = cfunc('fluid_synth_noteon', c_int,
                           ('synth', c_void_p, 1),
                           ('chan', c_int, 1),
                           ('key', c_int, 1),
                           ('vel', c_int, 1))

fluid_synth_noteoff = cfunc('fluid_synth_noteoff', c_int,
                            ('synth', c_void_p, 1),
                            ('chan', c_int, 1),
                            ('key', c_int, 1))

fluid_synth_pitch_bend = cfunc('fluid_synth_pitch_bend', c_int,
                               ('synth', c_void_p, 1),
                               ('chan', c_int, 1),
                               ('val', c_int, 1))

fluid_synth_cc = cfunc('fluid_synth_cc', c_int,
                       ('synth', c_void_p, 1),
                       ('chan', c_int, 1),
                       ('ctrl', c_int, 1),
                       ('val', c_int, 1))

fluid_synth_get_cc = cfunc('fluid_synth_get_cc', c_int,
                       ('synth', c_void_p, 1),
                       ('chan', c_int, 1),
                       ('num', c_int, 1),
                       ('pval', POINTER(c_int), 1))

fluid_synth_program_change = cfunc('fluid_synth_program_change', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1),
                                   ('prg', c_int, 1))

fluid_synth_bank_select = cfunc('fluid_synth_bank_select', c_int,
                                ('synth', c_void_p, 1),
                                ('chan', c_int, 1),
                                ('bank', c_int, 1))

fluid_synth_sfont_select = cfunc('fluid_synth_sfont_select', c_int,
                                 ('synth', c_void_p, 1),
                                 ('chan', c_int, 1),
                                 ('sfid', c_int, 1))

fluid_synth_program_reset = cfunc('fluid_synth_program_reset', c_int,
                                  ('synth', c_void_p, 1))

fluid_synth_system_reset = cfunc('fluid_synth_system_reset', c_int,
                                  ('synth', c_void_p, 1))

fluid_synth_write_s16 = cfunc('fluid_synth_write_s16', c_void_p,
                              ('synth', c_void_p, 1),
                              ('len', c_int, 1),
                              ('lbuf', c_void_p, 1),
                              ('loff', c_int, 1),
                              ('lincr', c_int, 1),
                              ('rbuf', c_void_p, 1),
                              ('roff', c_int, 1),
                              ('rincr', c_int, 1))

class fluid_synth_channel_info_t(Structure):
    _fields_ = [
        ('assigned', c_int),
        ('sfont_id', c_int),
        ('bank', c_int),
        ('program', c_int),
        ('name', c_char*32),
        ('reserved', c_char*32)]

fluid_synth_get_channel_info = cfunc('fluid_synth_get_channel_info', c_int,
                                  ('synth', c_void_p, 1),
                                  ('chan', c_int, 1),
                                  ('info', POINTER(fluid_synth_channel_info_t), 1))

fluid_synth_set_reverb_full = cfunc('fluid_synth_set_reverb_full', c_int,
                                    ('synth', c_void_p, 1),
                                    ('set', c_int, 1),
                                    ('roomsize', c_double, 1),
                                    ('damping', c_double, 1),
                                    ('width', c_double, 1),
                                    ('level', c_double, 1))
                                    
fluid_synth_set_chorus_full = cfunc('fluid_synth_set_chorus_full', c_int,
                                    ('synth', c_void_p, 1),
                                    ('set', c_int, 1),
                                    ('nr', c_int, 1),
                                    ('level', c_double, 1),
                                    ('speed', c_double, 1),
                                    ('depth_ms', c_double, 1),
                                    ('type', c_int, 1))

fluid_synth_get_reverb_roomsize = cfunc('fluid_synth_get_reverb_roomsize', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_reverb_damp = cfunc('fluid_synth_get_reverb_damp', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_reverb_level = cfunc('fluid_synth_get_reverb_level', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_reverb_width = cfunc('fluid_synth_get_reverb_width', c_double,
                                    ('synth', c_void_p, 1))

                                    
fluid_synth_get_chorus_nr = cfunc('fluid_synth_get_chorus_nr', c_int,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_level = cfunc('fluid_synth_get_chorus_level', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_speed_Hz = cfunc('fluid_synth_get_chorus_speed_Hz', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_depth_ms = cfunc('fluid_synth_get_chorus_depth_ms', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_type = cfunc('fluid_synth_get_chorus_type', c_int,
                                    ('synth', c_void_p, 1))

fluid_synth_set_midi_router = cfunc('fluid_synth_set_midi_router', None,
                               ('synth', c_void_p, 1),
                               ('router', c_void_p, 1))

fluid_synth_handle_midi_event = cfunc('fluid_synth_handle_midi_event', POINTER(c_int),
                               ('data', c_void_p, 1),
                               ('event', c_void_p, 1))

# fluid sequencer
new_fluid_sequencer2 = cfunc('new_fluid_sequencer2', c_void_p,
                             ('use_system_timer', c_int, 1))

fluid_sequencer_process = cfunc('fluid_sequencer_process', None,
                               ('seq', c_void_p, 1),
                               ('msec', c_uint, 1))

fluid_sequencer_register_fluidsynth = cfunc('fluid_sequencer_register_fluidsynth', c_short,
                               ('seq', c_void_p, 1),
                               ('synth', c_void_p, 1))

fluid_sequencer_register_client = cfunc('fluid_sequencer_register_client', c_short,
                              ('seq', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('callback', CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p), 1),
                              ('data', c_void_p, 1))

fluid_sequencer_get_tick = cfunc('fluid_sequencer_get_tick', c_uint,
                                ('seq', c_void_p, 1))

fluid_sequencer_set_time_scale = cfunc('fluid_sequencer_set_time_scale', None,
                                      ('seq', c_void_p, 1),
                                      ('scale', c_double, 1))

fluid_sequencer_get_time_scale = cfunc('fluid_sequencer_get_time_scale', c_double,
                                      ('seq', c_void_p, 1))

fluid_sequencer_send_at = cfunc('fluid_sequencer_send_at', c_int,
                               ('seq', c_void_p, 1),
                               ('evt', c_void_p, 1),
                               ('time', c_uint, 1),
                               ('absolute', c_int, 1))
                               

delete_fluid_sequencer = cfunc('delete_fluid_sequencer', None,
                              ('seq', c_void_p, 1))

# fluid event
new_fluid_event = cfunc('new_fluid_event', c_void_p)

fluid_event_set_source = cfunc('fluid_event_set_source', None,
                              ('evt', c_void_p, 1),
                              ('src', c_void_p, 1))

fluid_event_set_dest = cfunc('fluid_event_set_dest', None,
                            ('evt', c_void_p, 1),
                            ('dest', c_void_p, 1))

fluid_event_timer = cfunc('fluid_event_timer', None,
                         ('evt', c_void_p, 1),
                         ('data', c_void_p, 1))

fluid_event_note = cfunc('fluid_event_note', None,
                         ('evt', c_void_p, 1),
                         ('channel', c_int, 1),
                         ('key', c_short, 1),
                         ('vel', c_short, 1),
                         ('duration', c_uint, 1))

fluid_event_noteon = cfunc('fluid_event_noteon', None,
                         ('evt', c_void_p, 1),
                         ('channel', c_int, 1),
                         ('key', c_short, 1),
                         ('vel', c_short, 1))

fluid_event_noteoff = cfunc('fluid_event_noteoff', None,
                         ('evt', c_void_p, 1),
                         ('channel', c_int, 1),
                         ('key', c_short, 1))


delete_fluid_event = cfunc('delete_fluid_event', None,
                          ('evt', c_void_p, 1))

# fluid audio driver
new_fluid_audio_driver = cfunc('new_fluid_audio_driver', c_void_p,
                               ('settings', c_void_p, 1),
                               ('synth', c_void_p, 1))

delete_fluid_audio_driver = cfunc('delete_fluid_audio_driver', None,
                                  ('driver', c_void_p, 1))

# fluid midi driver
new_fluid_midi_driver = cfunc('new_fluid_midi_driver', c_void_p,
                               ('settings', c_void_p, 1),
                               ('handler', CFUNCTYPE(POINTER(c_int), c_void_p, c_void_p), 1),
                               ('event_handler_data', c_void_p, 1))


# fluid midi router rule
class fluid_midi_router_t(Structure):
    _fields_ = [
        ('synth', c_void_p),
        ('rules_mutex', c_void_p),
        ('rules', c_void_p*6),
        ('free_rules', c_void_p),
        ('event_handler', c_void_p),
        ('event_handler_data', c_void_p),
        ('nr_midi_channels', c_int),
        ('cmd_rule', c_void_p),
        ('cmd_rule_type', POINTER(c_int))]

delete_fluid_midi_router_rule = cfunc('delete_fluid_midi_router_rule', c_int,
                                    ('rule', c_void_p, 1))
                                    
new_fluid_midi_router_rule = cfunc('new_fluid_midi_router_rule', c_void_p)

fluid_midi_router_rule_set_chan = cfunc('fluid_midi_router_rule_set_chan', None,
                                    ('rule', c_void_p, 1),
                                    ('min', c_int, 1),
                                    ('max', c_int, 1),
                                    ('mul', c_float, 1),
                                    ('add', c_int, 1))
                                    
fluid_midi_router_rule_set_param1 = cfunc('fluid_midi_router_rule_set_param1', None,
                                    ('rule', c_void_p, 1),
                                    ('min', c_int, 1),
                                    ('max', c_int, 1),
                                    ('mul', c_float, 1),
                                    ('add', c_int, 1))
                                    
fluid_midi_router_rule_set_param2 = cfunc('fluid_midi_router_rule_set_param2', None,
                                    ('rule', c_void_p, 1),
                                    ('min', c_int, 1),
                                    ('max', c_int, 1),
                                    ('mul', c_float, 1),
                                    ('add', c_int, 1))

# fluid midi router
new_fluid_midi_router = cfunc('new_fluid_midi_router', POINTER(fluid_midi_router_t),
                               ('settings', c_void_p, 1),
                               ('handler', CFUNCTYPE(POINTER(c_int), c_void_p, c_void_p), 1),
                               ('event_handler_data', c_void_p, 1))

fluid_midi_router_handle_midi_event = cfunc('fluid_midi_router_handle_midi_event', POINTER(c_int),
                               ('data', c_void_p, 1),
                               ('event', c_void_p, 1))

fluid_midi_router_clear_rules = cfunc('fluid_midi_router_clear_rules', c_int,
                                    ('router', POINTER(fluid_midi_router_t), 1))

fluid_midi_router_set_default_rules = cfunc('fluid_midi_router_set_default_rules', c_int,
                                    ('router', POINTER(fluid_midi_router_t), 1))

fluid_midi_router_add_rule = cfunc('fluid_midi_router_add_rule', c_int,
                                    ('router', POINTER(fluid_midi_router_t), 1),
                                    ('rule', c_void_p, 1),
                                    ('type', c_int, 1))
        
def fluid_synth_write_s16_stereo(synth, len):
    """Return generated samples in stereo 16-bit format
    
    Return value is a Numpy array of samples.
    
    """
    import numpy
    buf = create_string_buffer(len * 4)
    fluid_synth_write_s16(synth, len, buf, 0, 2, buf, 1, 2)
    return numpy.fromstring(buf[:], dtype=numpy.int16)


# Object-oriented interface, simplifies access to functions

class Synth:
    """Synth represents a FluidSynth synthesizer"""
    def __init__(self, gain=0.2, samplerate=44100, channels=256, **kwargs):
        """Create new synthesizer object to control sound generation

        Optional keyword arguments:
        gain : scale factor for audio output, default is 0.2
        lower values are quieter, allow more simultaneous notes
        samplerate : output samplerate in Hz, default is 44100 Hz
        added capability for passing arbitrary fluid settings using args
        """
        st = new_fluid_settings()
        fluid_settings_setnum(st, b'synth.gain', gain)
        fluid_settings_setnum(st, b'synth.sample-rate', samplerate)
        fluid_settings_setint(st, b'synth.midi-channels', channels)
        for opt,val in iteritems(kwargs):
            self.setting(opt, val)
        self.settings = st
        self.synth = new_fluid_synth(st)
        self.audio_driver = None
        self.midi_driver = None
        self.router = None
    def setting(self, opt, val):
        """change an arbitrary synth setting, type-smart"""
        opt = opt.encode()
        if isinstance(val, basestring):
            fluid_settings_setstr(self.settings, opt, val)
        elif isinstance(val, int):
            fluid_settings_setint(self.settings, opt, val)
        elif isinstance(val, float):
            fluid_settings_setnum(self.settings, opt, val)
    def start(self, driver=None, device=None, midi_driver=None):
        """Start audio output driver in separate background thread

        Call this function any time after creating the Synth object.
        If you don't call this function, use get_samples() to generate
        samples.

        Optional keyword argument:
        driver : which audio driver to use for output
        Possible choices:
        'alsa', 'oss', 'jack', 'portaudio'
        'sndmgr', 'coreaudio', 'Direct Sound'
        device: the device to use for audio output

        Not all drivers will be available for every platform, it
        depends on which drivers were compiled into FluidSynth for
        your platform.

        """
        if driver is not None:
            assert (driver in ['alsa', 'oss', 'jack', 'portaudio', 'sndmgr', 'coreaudio', 'Direct Sound']) 
            fluid_settings_setstr(self.settings, b'audio.driver', driver.encode())
            if device is not None:
                fluid_settings_setstr(self.settings, str('audio.%s.device' % (driver)).encode(), device.encode())
            self.audio_driver = new_fluid_audio_driver(self.settings, self.synth)
        if midi_driver is not None:
            assert (midi_driver in ['alsa_seq', 'alsa_raw', 'oss', 'winmidi', 'midishare', 'coremidi'])
            fluid_settings_setstr(self.settings, b'midi.driver', midi_driver.encode())
            self.router = new_fluid_midi_router(self.settings, fluid_synth_handle_midi_event, self.synth)
            fluid_synth_set_midi_router(self.synth, self.router)
            self.midi_driver = new_fluid_midi_driver(self.settings, fluid_midi_router_handle_midi_event, self.router)
    def delete(self):
        if self.audio_driver is not None:
            delete_fluid_audio_driver(self.audio_driver)
        delete_fluid_synth(self.synth)
        delete_fluid_settings(self.settings)
    def sfload(self, filename, update_midi_preset=0):
        """Load SoundFont and return its ID"""
        return fluid_synth_sfload(self.synth, filename.encode(), update_midi_preset)
    def sfunload(self, sfid, update_midi_preset=0):
        """Unload a SoundFont and free memory it used"""
        return fluid_synth_sfunload(self.synth, sfid, update_midi_preset)
    def program_select(self, chan, sfid, bank, preset):
        """Select a program"""
        return fluid_synth_program_select(self.synth, chan, sfid, bank, preset)
    def channel_info(self, chan):
        """get soundfont, bank, prog, preset name of channel"""
        info=fluid_synth_channel_info_t()
        fluid_synth_get_channel_info(self.synth, chan, byref(info))
        return (info.sfont_id, info.bank, info.program, info.name)
    def router_clear(self):
        if self.router is not None:
            fluid_midi_router_clear_rules(self.router)
    def router_default(self):
        if self.router is not None:
            fluid_midi_router_set_default_rules(self.router)
    def router_begin(self, type):
        """types are [note|cc|prog|pbend|cpress|kpress]"""
        if self.router is not None:
            if type=='note':
                self.router.cmd_rule_type=0
            elif type=='cc':
                self.router.cmd_rule_type=1
            elif type=='prog':
                self.router.cmd_rule_type=2
            elif type=='pbend':
                self.router.cmd_rule_type=3
            elif type=='cpress':
                self.router.cmd_rule_type=4
            elif type=='kpress':
                self.router.cmd_rule_type=5
            if 'self.router.cmd_rule' in globals():
                delete_fluid_midi_router_rule(self.router.cmd_rule)
            self.router.cmd_rule = new_fluid_midi_router_rule()
    def router_end(self):
        if self.router is not None:
            if self.router.cmd_rule is None:
                return
            if fluid_midi_router_add_rule(self.router, self.router.cmd_rule, self.router.cmd_rule_type)<0:
                delete_fluid_midi_router_rule(self.router.cmd_rule)
            self.router.cmd_rule=None
    def router_chan(self, min, max, mul, add):
        if self.router is not None:
            fluid_midi_router_rule_set_chan(self.router.cmd_rule, min, max, mul, add)
    def router_par1(self, min, max, mul, add):
        if self.router is not None:
            fluid_midi_router_rule_set_param1(self.router.cmd_rule, min, max, mul, add)
    def router_par2(self, min, max, mul, add):
        if self.router is not None:
            fluid_midi_router_rule_set_param2(self.router.cmd_rule, min, max, mul, add)
    def set_reverb(self, roomsize=-1.0, damping=-1.0, width=-1.0, level=-1.0):
        """                                  
        roomsize Reverb room size value (0.0-1.2)
        damping Reverb damping value (0.0-1.0)
        width Reverb width value (0.0-100.0)
        level Reverb level value (0.0-1.0)
        """
        set=0
        if roomsize>=0:
            set+=0b0001
        if damping>=0:
            set+=0b0010
        if width>=0:
            set+=0b0100
        if level>=0:
            set+=0b1000
        return fluid_synth_set_reverb_full(self.synth, set, roomsize, damping, width, level)
    def set_chorus(self, nr=-1, level=-1.0, speed=-1.0, depth=-1.0, type=-1):
        """                                  
        nr Chorus voice count (0-99, CPU time consumption proportional to this value)
        level Chorus level (0.0-10.0)
        speed Chorus speed in Hz (0.29-5.0)
        depth_ms Chorus depth (max value depends on synth sample rate, 0.0-21.0 is safe for sample rate values up to 96KHz)
        type Chorus waveform type (0=sine, 1=triangle)
        """
        set=0
        if nr>=0:
            set+=0b00001
        if level>=0:
            set+=0b00010
        if speed>=0:
            set+=0b00100
        if depth>=0:
            set+=0b01000
        if type>=0:
            set+=0b10000
        return fluid_synth_set_chorus_full(self.synth, set, nr, level, speed, depth, type)
    def get_reverb_roomsize(self):
        return fluid_synth_get_reverb_roomsize(self.synth)
    def get_reverb_damp(self):
        return fluid_synth_get_reverb_damp(self.synth)
    def get_reverb_level(self):
        return fluid_synth_get_reverb_level(self.synth)
    def get_reverb_width(self):
        return fluid_synth_get_reverb_width(self.synth)
    def get_chorus_nr(self):
        return fluid_synth_get_chorus_nr(self.synth)
    def get_chorus_level(self):
        return fluid_synth_get_reverb_level(self.synth)
    def get_chorus_speed(self):
        return fluid_synth_get_chorus_speed_Hz(self.synth)
    def get_chorus_depth(self):
        return fluid_synth_get_chorus_depth_ms(self.synth)
    def get_chorus_type(self):
        return fluid_synth_get_chorus_type(self.synth)
    def noteon(self, chan, key, vel):
        """Play a note"""
        if key < 0 or key > 128:
            return False
        if chan < 0:
            return False
        if vel < 0 or vel > 128:
            return False
        return fluid_synth_noteon(self.synth, chan, key, vel)
    def noteoff(self, chan, key):
        """Stop a note"""
        if key < 0 or key > 128:
            return False
        if chan < 0:
            return False
        return fluid_synth_noteoff(self.synth, chan, key)
    def pitch_bend(self, chan, val):
        """Adjust pitch of a playing channel by small amounts

        A pitch bend value of 0 is no pitch change from default.
        A value of -2048 is 1 semitone down.
        A value of 2048 is 1 semitone up.
        Maximum values are -8192 to +8192 (transposing by 4 semitones).
        
        """
        return fluid_synth_pitch_bend(self.synth, chan, val + 8192)
    def cc(self, chan, ctrl, val):
        """Send control change value

        The controls that are recognized are dependent on the
        SoundFont.  Values are always 0 to 127.  Typical controls
        include:
          1 : vibrato
          7 : volume
          10 : pan (left to right)
          11 : expression (soft to loud)
          64 : sustain
          91 : reverb
          93 : chorus
        """
        return fluid_synth_cc(self.synth, chan, ctrl, val)
    def get_cc(self, chan, num):
        i=c_int()
        fluid_synth_get_cc(self.synth, chan, num, byref(i))
        return i.value
    def program_change(self, chan, prg):
        """Change the program"""
        return fluid_synth_program_change(self.synth, chan, prg)
    def bank_select(self, chan, bank):
        """Choose a bank"""
        return fluid_synth_bank_select(self.synth, chan, bank)
    def sfont_select(self, chan, sfid):
        """Choose a SoundFont"""
        return fluid_synth_sfont_select(self.synth, chan, sfid)
    def program_reset(self):
        """Reset the programs on all channels"""
        return fluid_synth_program_reset(self.synth)
    def system_reset(self):
        """Stop all notes and reset all programs"""
        return fluid_synth_system_reset(self.synth)
    def get_samples(self, len=1024):
        """Generate audio samples

        The return value will be a NumPy array containing the given
        length of audio samples.  If the synth is set to stereo output
        (the default) the array will be size 2 * len.

        """
        return fluid_synth_write_s16_stereo(self.synth, len)

class Sequencer:
    def __init__(self, time_scale=1000, use_system_timer=True):
        """Create new sequencer object to control and schedule timing of midi events

        Optional keyword arguments:
        time_scale: ticks per second, defaults to 1000
        use_system_timer: whether the sequencer should advance by itself
        """
        self.client_callbacks = []
        self.sequencer = new_fluid_sequencer2(use_system_timer)
        fluid_sequencer_set_time_scale(self.sequencer, time_scale)

    def register_fluidsynth(self, synth):
        response = fluid_sequencer_register_fluidsynth(self.sequencer, synth.synth)
        if response == FLUID_FAILED:
        	raise Error("Registering fluid synth failed")
        return response

    def register_client(self, name, callback, data=None):
        c_callback = CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p)(callback)
        response = fluid_sequencer_register_client(self.sequencer, name.encode(), c_callback, data)
        if response == FLUID_FAILED:
        	raise Error("Registering client failed")

        # store in a list to prevent garbage collection
        self.client_callbacks.append(c_callback)

        return response

    def note(self, time, channel, key, velocity, duration, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_note(evt, channel, key, velocity, duration)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def note_on(self, time, channel, key, velocity=127, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_noteon(evt, channel, key, velocity)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def note_off(self, time, channel, key, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_noteoff(evt, channel, key)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def timer(self, time, data=None, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_timer(evt, data)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def _create_event(self, source=-1, dest=-1):
        evt = new_fluid_event()
        fluid_event_set_source(evt, source)
        fluid_event_set_dest(evt, dest)
        return evt

    def _schedule_event(self, evt, time, absolute=True):
        response = fluid_sequencer_send_at(self.sequencer, evt, time, absolute)
        if response == FLUID_FAILED:
            raise Error("Scheduling event failed")

    def get_tick(self):
        return fluid_sequencer_get_tick(self.sequencer)

    def process(self, msec):
        fluid_sequencer_process(self.sequencer, msec)

    def delete(self):
        delete_fluid_sequencer(self.sequencer)

def raw_audio_string(data):
    """Return a string of bytes to send to soundcard

    Input is a numpy array of samples.  Default output format
    is 16-bit signed (other formats not currently supported).
    
    """
    import numpy
    return (data.astype(numpy.int16)).tostring()
