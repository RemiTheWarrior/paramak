from paramak import RotateMixedShape


class CenterColumnShieldFlatTopHyperbola(RotateMixedShape):
    """A center column shield volume with a hyperbolic outer profile joined to flat profiles
    at the top and bottom of the shield, and a constant cylindrical inner profile.

    :param height: height of the center column shield
    :type height: float
    :param arc_height: height of the curved profile of the center column shield
    :type arc_height: float
    :param inner_radius: inner radius of the center column shield
    :type inner_radius: float
    :param mid_radius: inner radius of outer curved profile of the center column shield
    :type mid_radius: float
    :param outer_radius: outer_radius of the center column shield
    :type outer_radius: float

    :return: a shape object that has generic functionality
    :rtype: a paramak shape object
    """

    def __init__(
        self,
        height,
        arc_height,
        inner_radius,
        mid_radius,
        outer_radius,
        rotation_angle=360,
        stp_filename="CenterColumnFlatTopHyperbola.stp",
        color=None,
        name="center_column",
        material_tag="center_column_shield_mat",
        azimuth_placement_angle=0,
        **kwargs
    ):

        default_dict = {'points':None,
                        'workplane':"XZ",
                        'solid':None,
                        'hash_value':None,
                        'intersect':None,
                        'cut':None,
                        'union':None
        }

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            rotation_angle=rotation_angle,
            **default_dict
        )

        self.height = height
        self.arc_height = arc_height
        self.mid_radius = mid_radius
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

    @property
    def points(self):
        self.find_points()
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def arc_height(self):
        return self._arc_height

    @arc_height.setter
    def arc_height(self, arc_height):
        self._arc_height = arc_height

    @property
    def inner_radius(self):
        return self._inner_radius

    @inner_radius.setter
    def inner_radius(self, inner_radius):
        self._inner_radius = inner_radius

    @property
    def mid_radius(self):
        return self._mid_radius

    @mid_radius.setter
    def mid_radius(self, mid_radius):
        self._mid_radius = mid_radius

    @property
    def outer_radius(self):
        return self._outer_radius

    @outer_radius.setter
    def outer_radius(self, outer_radius):
        self._outer_radius = outer_radius

    def find_points(self):
        """Finds the XZ points and connection types (straight and spline) that
        describe the 2D profile of the center column shield shape."""

        if self.inner_radius >= self.outer_radius:
            raise ValueError(
                "inner_radius ({}) is larger than outer_radius ({})".format(
                    self.inner_radius, self.outer_radius
                )
            )

        if self.mid_radius >= self.outer_radius:
            raise ValueError(
                "mid_radius ({}) is larger than outer_radius ({})".format(
                    self.mid_radius, self.outer_radius
                )
            )

        if self.arc_height >= self.height:
            raise ValueError(
                "arc_height ({}) is larger than height ({})".format(
                    self.arc_height, self.height
                )
            )

        points = [
            (self.inner_radius, 0, "straight"),
            (self.inner_radius, self.height / 2, "straight"),
            (self.outer_radius, self.height / 2, "straight"),
            (self.outer_radius, self.arc_height / 2, "spline"),
            (self.mid_radius, 0, "spline"),
            (self.outer_radius, -self.arc_height / 2, "straight"),
            (self.outer_radius, -self.height / 2, "straight"),
            (self.inner_radius, -self.height / 2, "straight"),
            (self.inner_radius, 0, "straight"),
        ]

        self.points = points
