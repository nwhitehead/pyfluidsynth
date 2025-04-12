#!/usr/bin/env python3

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyfluidsynth",
# ]
# ///

import unittest

import fluidsynth as fs


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)


class TestModulatorMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fs = fs.Synth()
        cls.modulator = fs.Modulator()

        ## Your installation of FluidSynth may require a different driver.
        ## Use something like:
        # fs.start(driver="pulseaudio")
        cls.fs.start()
        cls.sfid = cls.fs.sfload(local_file_path("example.sf2"))
        cls.fs.program_select(0, cls.sfid, 0, 0)

    @classmethod
    def tearDownClass(cls):
        cls.fs.delete()

    def test_dest(self):
        assert self.modulator.has_dest(5) is None
        self.modulator.set_dest(5)
        assert self.modulator.has_dest(5) == 1
        assert self.modulator.get_dest() == 5

    def test_flags(self):
        assert self.modulator.get_source1() is None
        self.modulator.set_source1(fs.FLUID_MOD_KEY, fs.FLUID_MOD_CONVEX)
        assert self.modulator.get_source1() == fs.FLUID_MOD_KEY
        assert self.modulator.get_flags1() == fs.FLUID_MOD_CONVEX

        assert self.modulator.get_source2() is None
        self.modulator.set_source2(fs.FLUID_MOD_VELOCITY, fs.FLUID_MOD_CONCAVE)
        assert self.modulator.get_source2() == fs.FLUID_MOD_VELOCITY
        assert self.modulator.get_flags2() == fs.FLUID_MOD_CONCAVE

    def test_transforms(self):
        assert self.modulator.get_transform() is None
        self.modulator.set_transform(fs.FLUID_MOD_TRANSFORM_ABS)
        assert self.modulator.get_transform() == fs.FLUID_MOD_TRANSFORM_ABS


if __name__ == "__main__":
    unittest.main()
