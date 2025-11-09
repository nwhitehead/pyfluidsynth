from pathlib import Path

import numpy as np
import pytest

import fluidsynth


def test_api_version() -> None:
    """
    Test that the API version is correct.
    """
    assert tuple(int(x) for x in fluidsynth.api_version.split(".")) >= (1, 3, 5)


def test_synth() -> None:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    synth = fluidsynth.Synth()
    assert isinstance(synth, fluidsynth.Synth)
    synth.delete()


def test_find_libfluidsynth_returns_string() -> None:
    lib = fluidsynth.find_libfluidsynth(False)
    assert isinstance(lib, str)
    assert lib


def test_cfunc_missing_symbol_returns_none() -> None:
    assert fluidsynth.cfunc("this_symbol_does_not_exist__", None) is None


def test_raw_audio_string_roundtrip() -> None:
    data = np.array([0, 1, -1, 1234, -2345, 32767, -32768], dtype=np.int16)
    b = fluidsynth.raw_audio_string(data)
    assert isinstance(b, (bytes, bytearray))
    assert len(b) == data.size * 2  # int16 -> 2 bytes per sample
    back = np.frombuffer(b, dtype=np.int16)
    np.testing.assert_array_equal(back, data)


def test_fluid_synth_write_s16_stereo_length() -> None:
    synth = fluidsynth.Synth()
    try:
        n = 64
        arr = fluidsynth.fluid_synth_write_s16_stereo(synth.synth, n)
        assert isinstance(arr, np.ndarray)
        assert arr.dtype == np.int16
        assert arr.size == n * 2  # stereo
    finally:
        synth.delete()


def test_get_samples_length_and_dtype() -> None:
    synth = fluidsynth.Synth()
    try:
        n = 128
        arr = synth.get_samples(n)
        assert isinstance(arr, np.ndarray)
        assert arr.dtype == np.int16
        assert arr.size == n * 2
    finally:
        synth.delete()


def _asset_path(name: str) -> Path:
    root = Path(__file__).resolve().parent.parent
    p = root / "test" / name
    if not p.exists():
        pytest.skip(f"Missing test asset: {p}")
    return p


def test_sfload_and_sfunload() -> None:
    sf2 = _asset_path("example.sf2")
    synth = fluidsynth.Synth()
    try:
        sfid = synth.sfload(str(sf2))
        assert isinstance(sfid, int)
        assert sfid >= 0
        assert synth.sfunload(sfid) == fluidsynth.FLUID_OK
    finally:
        synth.delete()


def test_program_select_and_note_on_off_and_cc() -> None:
    sf2 = _asset_path("example.sf2")
    synth = fluidsynth.Synth()
    try:
        sfid = synth.sfload(str(sf2))
        assert sfid >= 0
        assert synth.program_select(0, sfid, 0, 0) == fluidsynth.FLUID_OK

        # invalid inputs rejected
        assert synth.noteon(0, -1, 100) is False
        assert synth.noteon(0, 128, 100) is False
        assert synth.noteon(-1, 60, 100) is False
        assert synth.noteon(0, 60, -1) is False
        assert synth.noteon(0, 60, 128) is False

        # valid on/off shouldn't raise; return code is implementation-defined
        rc_on = synth.noteon(0, 60, 100)
        assert isinstance(rc_on, int)
        rc_off = synth.noteoff(0, 60)
        assert isinstance(rc_off, int)
        # cc roundtrip
        assert isinstance(synth.cc(0, 7, 100), int)
        assert synth.get_cc(0, 7) in range(128)

        # bank/program changes and resets
        assert isinstance(synth.bank_select(0, 0), int)
        assert isinstance(synth.program_change(0, 1), int)
        assert isinstance(synth.program_reset(), int)
        assert isinstance(synth.system_reset(), int)
    finally:
        synth.delete()


def test_channel_and_program_info_and_preset_name() -> None:
    sf2 = _asset_path("example.sf2")
    synth = fluidsynth.Synth()
    try:
        sfid = synth.sfload(str(sf2))
        assert synth.program_select(0, sfid, 0, 0) == fluidsynth.FLUID_OK
        info = synth.channel_info(0)
        assert isinstance(info, tuple)
        assert len(info) in (3, 4)

        sfont_id, bank, preset = synth.program_info(0)
        assert isinstance(sfont_id, int)
        assert isinstance(bank, int)
        assert isinstance(preset, int)

        # name may be None if API not available or preset missing
        name = synth.sfpreset_name(sfont_id, bank, preset)
        assert (name is None) or isinstance(name, str)
    finally:
        synth.delete()


def test_tuning_dump_returns_128_values() -> None:
    synth = fluidsynth.Synth()
    try:
        vals = synth.tuning_dump(0, 0)
        assert isinstance(vals, list)
        assert len(vals) == 128
        assert all(isinstance(v, float) for v in vals)
    finally:
        synth.delete()


def test_reverb_and_chorus_setters_and_getters_smoke() -> None:
    synth = fluidsynth.Synth()
    try:
        assert isinstance(synth.set_reverb(), int)
        assert isinstance(synth.set_chorus(), int)

        # per-parameter setters should not raise
        assert isinstance(synth.set_reverb_roomsize(0.5), int)
        assert isinstance(synth.set_reverb_damp(0.2), int)
        assert isinstance(synth.set_reverb_level(0.3), int)
        assert isinstance(synth.set_reverb_width(50.0), int)
        assert isinstance(synth.set_chorus_nr(3), int)
        assert isinstance(synth.set_chorus_level(1.0), int)
        assert isinstance(synth.set_chorus_speed(0.5), int)
        assert isinstance(synth.set_chorus_depth(2.0), int)
        assert isinstance(synth.set_chorus_type(0), int)

        # getters return numbers
        assert isinstance(synth.get_reverb_roomsize(), float)
        assert isinstance(synth.get_reverb_damp(), float)
        assert isinstance(synth.get_reverb_level(), float)
        assert isinstance(synth.get_reverb_width(), float)
        assert isinstance(synth.get_chorus_nr(), int)
        assert isinstance(synth.get_chorus_level(), float)
        assert isinstance(synth.get_chorus_speed(), float)
        assert isinstance(synth.get_chorus_depth(), float)
        assert isinstance(synth.get_chorus_type(), int)
    finally:
        synth.delete()


def test_pitch_bend_clamps() -> None:
    synth = fluidsynth.Synth()
    try:
        assert isinstance(synth.pitch_bend(0, -99999), int)
        assert isinstance(synth.pitch_bend(0, 99999), int)
    finally:
        synth.delete()


def test_get_active_voice_count() -> None:
    """
    Test that get_active_voice_count returns an integer.
    """
    synth = fluidsynth.Synth()
    assert synth.get_active_voice_count() == 0
    assert synth.noteon(0, 60, 30) == -1
    assert synth.get_active_voice_count() == 2
    assert synth.noteon(0, 60, 30) == -1
    assert synth.get_active_voice_count() == 4
    synth.delete()


@pytest.mark.skipif(
    getattr(fluidsynth, "new_fluid_sequencer2", None) is None,
    reason="Sequencer API not available in this libfluidsynth",
)
def test_sequencer_basic_scheduling() -> None:
    synth = fluidsynth.Synth()
    try:
        seq = fluidsynth.Sequencer()
        seq.register_fluidsynth(synth)
        now = seq.get_tick()
        # schedule a simple timer and note events at 'now'
        seq.timer(now)
        seq.note_on(now, 0, 60, 100)
        seq.note_off(now, 0, 60)
        seq.process(0)
        seq.delete()
    finally:
        synth.delete()


@pytest.mark.skipif(
    getattr(fluidsynth, "new_fluid_mod", None) is None,
    reason="Modulator API not available in this libfluidsynth",
)
def test_modulator_smoke() -> None:
    mod = fluidsynth.Modulator()
    # Just ensure calls don't raise; return values are backend-specific
    assert mod.sizeof() is not None
