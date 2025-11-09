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
