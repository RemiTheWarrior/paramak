
from plasmaboundaries import get_separatrix_coordinates

from paramak import Plasma


class PlasmaBoundaries(Plasma):
    """Creates a double null tokamak plasma shape that is controlled
    by 5 shaping parameters using the plasmaboundaries package to calculate
    points. For more details see:
    http://github.com/RemDelaporteMathurin/plasma-boundaries

    Args:
        A (float, optional): plasma parameter see plasmaboundaries doc.
            Defaults to 0.05.
        elongation (float, optional): the elongation of the plasma.
            Defaults to 2.0.
        major_radius (float, optional): the major radius of the plasma
            (cm). Defaults to 450.0.
        minor_radius (float, optional): the minor radius of the plasma
            (cm). Defaults to 150.0.
        triangularity (float, optional): the triangularity of the plasma.
            Defaults to 0.55.
        vertical_displacement (float, optional): the vertical_displacement
            of the plasma (cm). Defaults to 0.0.
        configuration (str, optional): plasma configuration
            ("non-null", "single-null", "double-null").
            Defaults to "non-null".
        x_point_shift (float, optional): Shift parameters for locating the
            X points in [0, 1]. Defaults to 0.1.
    """

    def __init__(
        self,
        A=0.05,
        elongation=2.0,
        major_radius=450.0,
        minor_radius=150.0,
        triangularity=0.55,
        vertical_displacement=0.0,
        configuration="non-null",
        x_point_shift=0.1,
        **kwargs
    ):

        super().__init__(
            elongation=elongation,
            major_radius=major_radius,
            minor_radius=minor_radius,
            triangularity=triangularity,
            vertical_displacement=vertical_displacement,
            configuration=configuration,
            x_point_shift=x_point_shift,
            **kwargs
        )

        # properties needed for plasma shapes
        self.A = A

    def find_points(self):
        """Finds the XZ points that describe the 2D profile of the plasma."""
        aspect_ratio = self.minor_radius / self.major_radius
        params = {
            "A": self.A,
            "aspect_ratio": aspect_ratio,
            "elongation": self.elongation,
            "triangularity": self.triangularity,
        }
        points = get_separatrix_coordinates(params, self.configuration)
        # add vertical displacement
        points[:, 1] += self.vertical_displacement
        # rescale to cm
        points[:] *= self.major_radius

        # remove unnecessary points
        lower_x_point, upper_x_point = self.compute_x_points()
        # if non-null these are the y bounds
        lower_point_y = (
            -self.elongation * self.minor_radius + self.vertical_displacement
        )
        upper_point_y = self.elongation * self.minor_radius + \
            self.vertical_displacement
        # else use x points
        if self.configuration in ["single-null", "double-null"]:
            lower_point_y = lower_x_point[1]
            if self.configuration == "double-null":
                upper_point_y = upper_x_point[1]
        points2 = []
        for p in points:
            if p[1] >= lower_point_y and p[1] <= upper_point_y:
                points2.append(p)
        points = points2

        self.points = [(p[0], p[1]) for p in points[:-1]]

        # set the points of interest
        self.high_point = (
            self.major_radius - self.triangularity * self.minor_radius,
            self.elongation * self.minor_radius,
        )
        self.low_point = (
            self.major_radius - self.triangularity * self.minor_radius,
            -self.elongation * self.minor_radius,
        )
        self.outer_equatorial_point = (
            self.major_radius + self.minor_radius, 0)
        self.inner_equatorial_point = (
            self.major_radius - self.minor_radius, 0)
