
import paramak
import pytest
import unittest


class test_ToroidalFieldCoilPrincetonD(unittest.TestCase):
    def test_ToroidalFieldCoilPrincetonD_creation(self):
        """Creates a ToroidalFieldCoilPrincetonD object and checks a solid is
        created."""

        test_shape = paramak.ToroidalFieldCoilPrincetonD(
            R1=100,
            R2=300,
            thickness=50,
            distance=50,
            number_of_coils=2,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_ToroidalFieldCoilPrincetonD_with_leg(self):
        """Creates a ToroidalFieldCoilPrincetonD object and checks a inboard
        leg can also be created."""

        my_magnet = paramak.ToroidalFieldCoilPrincetonD(
            R1=0.29, R2=0.91, thickness=0.05, distance=0.05, number_of_coils=1)
        my_magnet.export_stp('princeton.stp')

        my_leg = paramak.ExtrudeStraightShape(
            points=my_magnet.inner_leg_connection_points, distance=0.05)

        assert my_leg.solid is not None

    def test_ToroidalFieldCoilPrincetonD_rotation_angle(self):
        """Creates a tf coil with a rotation_angle < 360 degrees and checks
        that the correct cut is performed and the volume is correct."""

        test_shape = paramak.ToroidalFieldCoilPrincetonD(
            R1=50,
            R2=150,
            thickness=30,
            distance=30,
            number_of_coils=8,
        )

        test_shape.rotation_angle = 360
        test_shape.workplane = "XZ"
        test_volume = test_shape.volume
        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_volume * 0.5, rel=0.01)

        test_shape.rotation_angle = 360
        test_shape.workplane = "YZ"
        test_volume = test_shape.volume
        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_volume * 0.5, rel=0.01)

        # this test will remain commented until workplane issue #308 is resolved
        # currently causes terminal to crash due to large number of unions
        # test_shape.rotation_angle = 360
        # test_shape.workplane = "XY"
        # test_volume = test_shape.volume
        # test_shape.rotation_angle = 180
        # assert test_shape.volume == pytest.approx(test_volume * 0.5)
