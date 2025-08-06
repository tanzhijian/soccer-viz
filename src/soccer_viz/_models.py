from math import isclose
from typing import Literal, TypedDict

from ._utils import calc_half_axix_range


class Area(TypedDict):
    x0: float
    y0: float
    x1: float
    y1: float


class Standard:
    LENGTH = 105.0
    WIDTH = 68.0
    CENTER_CIRCLE_RADIUS = 9.15
    PENALTY_AREA_LENGTH = 16.5
    PENALTY_MARK_DISTANCE = 11.0
    GOAL_AREA_LENGTH = 5.5
    CORNER_ARC_RADIUS = 1.0
    GOAL_WIDTH = 7.32
    GOAL_HEIGHT = 2.44
    MARK_RADIUS = 0.2


class PitchMarkings:
    def __init__(
        self,
        *,
        length: float | None = None,
        width: float | None = None,
        use_standard: bool = True,
        center_circle_radius: float | None = None,
        penalty_area_length: float | None = None,
        penalty_mark_distance: float | None = None,
        goal_area_length: float | None = None,
        corner_arc_radius: float | None = None,
        goal_width: float | None = None,
        goal_height: float | None = None,
        mark_radius: float | None = None,
    ) -> None:
        self._length = length
        self._width = width
        self._use_standard = use_standard
        self._center_circle_radius = center_circle_radius
        self._penalty_area_length = penalty_area_length
        self._penalty_mark_distance = penalty_mark_distance
        self._goal_area_length = goal_area_length
        self._corner_arc_radius = corner_arc_radius
        self._goal_width = goal_width
        self._goal_height = goal_height
        self._mark_radius = mark_radius

    @property
    def length(self) -> float:
        return self._length if self._length is not None else Standard.LENGTH

    @property
    def width(self) -> float:
        return self._width if self._width is not None else Standard.WIDTH

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.length

    @property
    def _length_ratio(self) -> float:
        return self.length / Standard.LENGTH

    @property
    def center_circle_radius(self) -> float:
        if self._center_circle_radius is None:
            if self._use_standard:
                return Standard.CENTER_CIRCLE_RADIUS
            return self._length_ratio * Standard.CENTER_CIRCLE_RADIUS
        return self._center_circle_radius

    @property
    def penalty_area_length(self) -> float:
        if self._penalty_area_length is None:
            if self._use_standard:
                return Standard.PENALTY_AREA_LENGTH
            return self._length_ratio * Standard.PENALTY_AREA_LENGTH
        return self._penalty_area_length

    @property
    def penalty_mark_distance(self) -> float:
        if self._penalty_mark_distance is None:
            if self._use_standard:
                return Standard.PENALTY_MARK_DISTANCE
            return self._length_ratio * Standard.PENALTY_MARK_DISTANCE
        return self._penalty_mark_distance

    @property
    def goal_area_length(self) -> float:
        if self._goal_area_length is None:
            if self._use_standard:
                return Standard.GOAL_AREA_LENGTH
            return self._length_ratio * Standard.GOAL_AREA_LENGTH
        return self._goal_area_length

    @property
    def corner_arc_radius(self) -> float:
        if self._corner_arc_radius is None:
            if self._use_standard:
                return Standard.CORNER_ARC_RADIUS
            return self._length_ratio * Standard.CORNER_ARC_RADIUS
        return self._corner_arc_radius

    @property
    def goal_width(self) -> float:
        if self._goal_width is None:
            if self._use_standard:
                return Standard.GOAL_WIDTH
            return self._length_ratio * Standard.GOAL_WIDTH
        return self._goal_width

    @property
    def goal_height(self) -> float:
        if self._goal_height is None:
            if self._use_standard:
                return Standard.GOAL_HEIGHT
            return self._length_ratio * Standard.GOAL_HEIGHT
        return self._goal_height

    @property
    def mark_radius(self) -> float:
        if self._mark_radius is None:
            if self._use_standard:
                return Standard.MARK_RADIUS
            return self._length_ratio * Standard.MARK_RADIUS
        return self._mark_radius

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PitchMarkings):
            return NotImplemented
        return (
            isclose(self.length, value.length)
            and isclose(self.width, value.width)
            and isclose(self.center_circle_radius, value.center_circle_radius)
            and isclose(self.penalty_area_length, value.penalty_area_length)
            and isclose(
                self.penalty_mark_distance, value.penalty_mark_distance
            )
            and isclose(self.goal_area_length, value.goal_area_length)
            and isclose(self.corner_arc_radius, value.corner_arc_radius)
            and isclose(self.goal_width, value.goal_width)
            and isclose(self.goal_height, value.goal_height)
            and isclose(self.mark_radius, value.mark_radius)
        )

    def __repr__(self) -> str:
        return (
            f"PitchMarkings("
            f"length={self.length}, "
            f"width={self.width}, "
            f"center_circle_radius={self.center_circle_radius}, "
            f"penalty_area_length={self.penalty_area_length}, "
            f"penalty_mark_distance={self.penalty_mark_distance}, "
            f"goal_area_length={self.goal_area_length}, "
            f"corner_arc_radius={self.corner_arc_radius}, "
            f"goal_width={self.goal_width}, "
            f"goal_height={self.goal_height}, "
            f"mark_radius={self.mark_radius}"
            f")"
        )


class PitchCoordinates:
    def __init__(
        self,
        *,
        markings: PitchMarkings | None = None,
        vertical: bool = False,
        side: Literal["left", "right", "both"] = "both",
    ) -> None:
        self._vertical = vertical
        self._side = side
        self._markings = markings if markings is not None else PitchMarkings()
        self._xaxis_range, self._yaxis_range = self._calc_axis_range(
            self._markings.length,
            self._markings.width,
        )

    def _set_axis_range(
        self, length: float, width: float
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        if self._vertical:
            return (0, width), (0, length)
        return (0, length), (0, width)

    def _calc_axis_range(
        self, length: float, width: float
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        xaxis_range, yaxis_range = self._set_axis_range(length, width)
        if self._vertical:
            if self._side != "both":
                yaxis_range = calc_half_axix_range(yaxis_range, self._side)
        else:
            if self._side != "both":
                xaxis_range = calc_half_axix_range(xaxis_range, self._side)
        return xaxis_range, yaxis_range

    @property
    def vertical(self) -> bool:
        return self._vertical

    @property
    def side(self) -> str:
        return self._side

    @property
    def xaxis_start(self) -> float:
        return self._xaxis_range[0]

    @property
    def xaxis_end(self) -> float:
        return self._xaxis_range[1]

    @property
    def yaxis_start(self) -> float:
        return self._yaxis_range[0]

    @property
    def yaxis_end(self) -> float:
        return self._yaxis_range[1]

    @property
    def xaxis_range(self) -> tuple[float, float]:
        return self._xaxis_range

    @property
    def yaxis_range(self) -> tuple[float, float]:
        return self._yaxis_range

    @property
    def aspect_ratio(self) -> float:
        if self._side != "both":
            return self._markings.aspect_ratio * 2
        return self._markings.aspect_ratio

    @property
    def _xaxis_length(self) -> float:
        return (
            self._markings.length
            if not self._vertical
            else self._markings.width
        )

    @property
    def _yaxis_length(self) -> float:
        return (
            self._markings.width
            if not self._vertical
            else self._markings.length
        )

    @property
    def markings(self) -> PitchMarkings:
        return self._markings

    def pitch_area(self) -> Area:
        return Area(
            x0=self.xaxis_start,
            y0=self.yaxis_start,
            x1=self.xaxis_end,
            y1=self.yaxis_end,
        )

    def centre_circle(self) -> Area:
        return {
            "x0": self._xaxis_length / 2 - self.markings.center_circle_radius,
            "y0": self._yaxis_length / 2 - self.markings.center_circle_radius,
            "x1": self._xaxis_length / 2 + self.markings.center_circle_radius,
            "y1": self._yaxis_length / 2 + self.markings.center_circle_radius,
        }

    def centre_mark(self) -> Area:
        return {
            "x0": self._xaxis_length / 2 - self.markings.mark_radius,
            "y0": self._yaxis_length / 2 - self.markings.mark_radius,
            "x1": self._xaxis_length / 2 + self.markings.mark_radius,
            "y1": self._yaxis_length / 2 + self.markings.mark_radius,
        }

    def halfway_line(self) -> Area:
        if self._vertical:
            return {
                "x0": self.xaxis_start,
                "y0": self._yaxis_length / 2,
                "x1": self.xaxis_end,
                "y1": self._yaxis_length / 2,
            }
        return {
            "x0": self._xaxis_length / 2,
            "y0": self.yaxis_start,
            "x1": self._xaxis_length / 2,
            "y1": self.yaxis_end,
        }

    def left_penalty_arc(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2
                - self.markings.center_circle_radius,
                "y0": self.markings.penalty_mark_distance
                - self.markings.center_circle_radius,
                "x1": self._xaxis_length / 2
                + self.markings.center_circle_radius,
                "y1": self.markings.penalty_mark_distance
                + self.markings.center_circle_radius,
            }
        return {
            "x0": self.markings.penalty_mark_distance
            - self.markings.center_circle_radius,
            "y0": self._yaxis_length / 2 - self.markings.center_circle_radius,
            "x1": self.markings.penalty_mark_distance
            + self.markings.center_circle_radius,
            "y1": self._yaxis_length / 2 + self.markings.center_circle_radius,
        }

    def left_penalty_area(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2
                - self.markings.goal_width / 2
                - self.markings.penalty_area_length,
                "y0": self.yaxis_start,
                "x1": self._xaxis_length / 2
                + self.markings.goal_width / 2
                + self.markings.penalty_area_length,
                "y1": self.markings.penalty_area_length,
            }
        return {
            "x0": self.xaxis_start,
            "y0": self._yaxis_length / 2
            - self.markings.goal_width / 2
            - self.markings.penalty_area_length,
            "x1": self.markings.penalty_area_length,
            "y1": self._yaxis_length / 2
            + self.markings.goal_width / 2
            + self.markings.penalty_area_length,
        }

    def left_penalty_mark(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2 - self.markings.mark_radius,
                "y0": self.markings.penalty_mark_distance
                - self.markings.mark_radius,
                "x1": self._xaxis_length / 2 + self.markings.mark_radius,
                "y1": self.markings.penalty_mark_distance
                + self.markings.mark_radius,
            }
        return {
            "x0": self.markings.penalty_mark_distance
            - self.markings.mark_radius,
            "y0": self._yaxis_length / 2 - self.markings.mark_radius,
            "x1": self.markings.penalty_mark_distance
            + self.markings.mark_radius,
            "y1": self._yaxis_length / 2 + self.markings.mark_radius,
        }

    def left_goal_area(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2
                - self.markings.goal_width / 2
                - self.markings.goal_area_length,
                "y0": self.yaxis_start,
                "x1": self._xaxis_length / 2
                + self.markings.goal_width / 2
                + self.markings.goal_area_length,
                "y1": self.markings.goal_area_length,
            }
        return {
            "x0": self.xaxis_start,
            "y0": self._yaxis_length / 2
            - self.markings.goal_width / 2
            - self.markings.goal_area_length,
            "x1": self.markings.goal_area_length,
            "y1": self._yaxis_length / 2
            + self.markings.goal_width / 2
            + self.markings.goal_area_length,
        }

    def left_goal(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2 - self.markings.goal_width / 2,
                "y0": self.yaxis_start,
                "x1": self._xaxis_length / 2 + self.markings.goal_width / 2,
                "y1": -self.markings.goal_height,
            }
        return {
            "x0": -self.markings.goal_height,
            "y0": self._yaxis_length / 2 - self.markings.goal_width / 2,
            "x1": self.xaxis_start,
            "y1": self._yaxis_length / 2 + self.markings.goal_width / 2,
        }

    def right_penalty_arc(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2
                - self.markings.center_circle_radius,
                "y0": self._yaxis_length
                - self.markings.penalty_mark_distance
                - self.markings.center_circle_radius,
                "x1": self._xaxis_length / 2
                + self.markings.center_circle_radius,
                "y1": self._yaxis_length
                - self.markings.penalty_mark_distance
                + self.markings.center_circle_radius,
            }
        return {
            "x0": self._xaxis_length
            - self.markings.penalty_mark_distance
            - self.markings.center_circle_radius,
            "y0": self._yaxis_length / 2 - self.markings.center_circle_radius,
            "x1": self._xaxis_length
            - self.markings.penalty_mark_distance
            + self.markings.center_circle_radius,
            "y1": self._yaxis_length / 2 + self.markings.center_circle_radius,
        }

    def right_penalty_area(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2
                - self.markings.goal_width / 2
                - self.markings.penalty_area_length,
                "y0": self.yaxis_end,
                "x1": self._xaxis_length / 2
                + self.markings.goal_width / 2
                + self.markings.penalty_area_length,
                "y1": self._yaxis_length - self.markings.penalty_area_length,
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_length / 2
            - self.markings.goal_width / 2
            - self.markings.penalty_area_length,
            "x1": self._xaxis_length - self.markings.penalty_area_length,
            "y1": self._yaxis_length / 2
            + self.markings.goal_width / 2
            + self.markings.penalty_area_length,
        }

    def right_penalty_mark(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2 - self.markings.mark_radius,
                "y0": self._yaxis_length
                - self.markings.penalty_mark_distance
                - self.markings.mark_radius,
                "x1": self._xaxis_length / 2 + self.markings.mark_radius,
                "y1": self._yaxis_length
                - self.markings.penalty_mark_distance
                + self.markings.mark_radius,
            }
        return {
            "x0": self._xaxis_length
            - self.markings.penalty_mark_distance
            - self.markings.mark_radius,
            "y0": self._yaxis_length / 2 - self.markings.mark_radius,
            "x1": self._xaxis_length
            - self.markings.penalty_mark_distance
            + self.markings.mark_radius,
            "y1": self._yaxis_length / 2 + self.markings.mark_radius,
        }

    def right_goal_area(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2
                - self.markings.goal_width / 2
                - self.markings.goal_area_length,
                "y0": self.yaxis_end,
                "x1": self._xaxis_length / 2
                + self.markings.goal_width / 2
                + self.markings.goal_area_length,
                "y1": self._yaxis_length - self.markings.goal_area_length,
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_length / 2
            - self.markings.goal_width / 2
            - self.markings.goal_area_length,
            "x1": self._xaxis_length - self.markings.goal_area_length,
            "y1": self._yaxis_length / 2
            + self.markings.goal_width / 2
            + self.markings.goal_area_length,
        }

    def right_goal(self) -> Area:
        if self._vertical:
            return {
                "x0": self._xaxis_length / 2 - self.markings.goal_width / 2,
                "y0": self.yaxis_end,
                "x1": self._xaxis_length / 2 + self.markings.goal_width / 2,
                "y1": self._yaxis_length + self.markings.goal_height,
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_length / 2 - self.markings.goal_width / 2,
            "x1": self._xaxis_length + self.markings.goal_height,
            "y1": self._yaxis_length / 2 + self.markings.goal_width / 2,
        }
