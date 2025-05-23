from typing import TypedDict


class Colors:
    light_gray = "#f8f9fa"
    dark_gray = "#dee2e6"
    red = "#dc3545"
    blue = "#0d6efd"
    green = "#198754"
    transparent = "rgba(0, 0, 0, 0)"


class Area(TypedDict):
    x0: float
    y0: float
    x1: float
    y1: float


class Point(TypedDict):
    x: float
    y: float


class PitchMarkings:
    def __init__(
        self,
        *,
        center_circle_radius: float = 9.15,
        penalty_area_length: float = 16.5,
        penalty_mark_distance: float = 11,
        goal_area_length: float = 5.5,
        corner_arc_radius: float = 1,
        goal_width: float = 7.32,
        goal_height: float = 2.44,
    ) -> None:
        self.center_circle_radius = center_circle_radius
        self.penalty_area_length = penalty_area_length
        self.penalty_mark_distance = penalty_mark_distance
        self.goal_area_length = goal_area_length
        self.corner_arc_radius = corner_arc_radius
        self.goal_width = goal_width
        self.goal_height = goal_height

    def change_scale(
        self,
        xaxis_scale: float,
        yaxis_scale,
        vertical: bool = False,
    ) -> None:
        if vertical:
            xaxis_scale, yaxis_scale = yaxis_scale, xaxis_scale

        self.center_circle_radius *= yaxis_scale
        self.penalty_area_length *= xaxis_scale
        self.penalty_mark_distance *= xaxis_scale
        self.goal_area_length *= xaxis_scale
        self.corner_arc_radius *= xaxis_scale
        self.goal_width *= yaxis_scale
        self.goal_height *= yaxis_scale


class PitchCoordinates:
    def __init__(
        self,
        *,
        xaxis_range: tuple[float, float] | None = None,
        yaxis_range: tuple[float, float] | None = None,
        markings: PitchMarkings | None = None,
        vertical: bool = False,
        lock_markings: bool = True,
    ) -> None:
        self.vertical = vertical
        self.xaxis_range = self._init_axis_range(xaxis_range, vertical, is_x=True)
        self.yaxis_range = self._init_axis_range(yaxis_range, vertical, is_x=False)
        self.xaxis_start, self.xaxis_end = self.xaxis_range
        self.yaxis_start, self.yaxis_end = self.yaxis_range
        self.length = abs(self.xaxis_end - self.xaxis_start)
        self.width = abs(self.yaxis_end - self.yaxis_start)

        self.xaxis_scale, self.yaxis_scale = self._init_scale()
        self.markings = markings if markings is not None else PitchMarkings()
        if not lock_markings:
            self.markings.change_scale(self.xaxis_scale, self.yaxis_scale, vertical)

    def _init_axis_range(self, axis_range, vertical, is_x):
        if axis_range is not None:
            return axis_range
        if is_x:
            length = 68 if vertical else 105
            return (0.0, length)
        else:
            width = 105 if vertical else 68
            return (0.0, width)

    def _init_scale(self):
        return self.length / 105, self.width / 68

    def _xaxis_operate(self, value: float) -> float:
        if self.xaxis_start < self.xaxis_end:
            return self.xaxis_start + value
        return self.xaxis_start - value

    def _yaxis_operate(self, value: float) -> float:
        if self.yaxis_start < self.yaxis_end:
            return self.yaxis_start + value
        return self.yaxis_start - value

    def pitch_area(self) -> Area:
        return {
            "x0": self.xaxis_start,
            "y0": self.yaxis_start,
            "x1": self.xaxis_end,
            "y1": self.yaxis_end,
        }

    def centre_circle(self) -> Area:
        return {
            "x0": self._xaxis_operate(
                self.length / 2 - self.markings.center_circle_radius
            ),
            "y0": self._yaxis_operate(
                self.width / 2 - self.markings.center_circle_radius
            ),
            "x1": self._xaxis_operate(
                self.length / 2 + self.markings.center_circle_radius
            ),
            "y1": self._yaxis_operate(
                self.width / 2 + self.markings.center_circle_radius
            ),
        }

    def centre_mark(self) -> Area:
        return {
            "x0": self._xaxis_operate(self.length / 2 - 0.2),
            "y0": self._yaxis_operate(self.width / 2 - 0.2),
            "x1": self._xaxis_operate(self.length / 2 + 0.2),
            "y1": self._yaxis_operate(self.width / 2 + 0.2),
        }

    def halfway_line(self) -> Area:
        if self.vertical:
            return {
                "x0": self.xaxis_start,
                "y0": self._yaxis_operate(self.width / 2),
                "x1": self.xaxis_end,
                "y1": self._yaxis_operate(self.width / 2),
            }
        return {
            "x0": self._xaxis_operate(self.length / 2),
            "y0": self.yaxis_start,
            "x1": self._xaxis_operate(self.length / 2),
            "y1": self.yaxis_end,
        }

    def left_penalty_arc(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.markings.center_circle_radius
                ),
                "y0": self._yaxis_operate(
                    self.markings.penalty_mark_distance
                    - self.markings.center_circle_radius
                ),
                "x1": self._xaxis_operate(
                    self.length / 2 + self.markings.center_circle_radius
                ),
                "y1": self._yaxis_operate(
                    self.markings.penalty_mark_distance
                    + self.markings.center_circle_radius
                ),
            }
        return {
            "x0": self._xaxis_operate(
                self.markings.penalty_mark_distance - self.markings.center_circle_radius
            ),
            "y0": self._yaxis_operate(
                self.width / 2 - self.markings.center_circle_radius
            ),
            "x1": self._xaxis_operate(
                self.markings.penalty_mark_distance + self.markings.center_circle_radius
            ),
            "y1": self._yaxis_operate(
                self.width / 2 + self.markings.center_circle_radius
            ),
        }

    def left_penalty_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2
                    - self.markings.goal_width / 2
                    - self.markings.penalty_area_length
                ),
                "y0": self.yaxis_start,
                "x1": self._xaxis_operate(
                    self.length / 2
                    + self.markings.goal_width / 2
                    + self.markings.penalty_area_length
                ),
                "y1": self._yaxis_operate(self.markings.penalty_area_length),
            }
        return {
            "x0": self.xaxis_start,
            "y0": self._yaxis_operate(
                self.width / 2
                - self.markings.goal_width / 2
                - self.markings.penalty_area_length
            ),
            "x1": self._xaxis_operate(self.markings.penalty_area_length),
            "y1": self._yaxis_operate(
                self.width / 2
                + self.markings.goal_width / 2
                + self.markings.penalty_area_length
            ),
        }

    def left_penalty_mark(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - 0.2),
                "y0": self._yaxis_operate(self.markings.penalty_mark_distance - 0.2),
                "x1": self._xaxis_operate(self.length / 2 + 0.2),
                "y1": self._yaxis_operate(self.markings.penalty_mark_distance + 0.2),
            }
        return {
            "x0": self._xaxis_operate(self.markings.penalty_mark_distance - 0.2),
            "y0": self._yaxis_operate(self.width / 2 - 0.2),
            "x1": self._xaxis_operate(self.markings.penalty_mark_distance + 0.2),
            "y1": self._yaxis_operate(self.width / 2 + 0.2),
        }

    def left_goal_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2
                    - self.markings.goal_width / 2
                    - self.markings.goal_area_length
                ),
                "y0": self.yaxis_start,
                "x1": self._xaxis_operate(
                    self.length / 2
                    + self.markings.goal_width / 2
                    + self.markings.goal_area_length
                ),
                "y1": self._yaxis_operate(self.markings.goal_area_length),
            }
        return {
            "x0": self.xaxis_start,
            "y0": self._yaxis_operate(
                self.width / 2
                - self.markings.goal_width / 2
                - self.markings.goal_area_length
            ),
            "x1": self._xaxis_operate(self.markings.goal_area_length),
            "y1": self._yaxis_operate(
                self.width / 2
                + self.markings.goal_width / 2
                + self.markings.goal_area_length
            ),
        }

    def left_goal(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.markings.goal_width / 2
                ),
                "y0": self.yaxis_start,
                "x1": self._xaxis_operate(
                    self.length / 2 + self.markings.goal_width / 2
                ),
                "y1": self._yaxis_operate(-self.markings.goal_height),
            }
        return {
            "x0": self._xaxis_operate(-self.markings.goal_height),
            "y0": self._yaxis_operate(self.width / 2 - self.markings.goal_width / 2),
            "x1": self.xaxis_start,
            "y1": self._yaxis_operate(self.width / 2 + self.markings.goal_width / 2),
        }

    def right_penalty_arc(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.markings.center_circle_radius
                ),
                "y0": self._yaxis_operate(
                    self.width
                    - self.markings.penalty_mark_distance
                    - self.markings.center_circle_radius
                ),
                "x1": self._xaxis_operate(
                    self.length / 2 + self.markings.center_circle_radius
                ),
                "y1": self._yaxis_operate(
                    self.width
                    - self.markings.penalty_mark_distance
                    + self.markings.center_circle_radius
                ),
            }
        return {
            "x0": self._xaxis_operate(
                self.length
                - self.markings.penalty_mark_distance
                - self.markings.center_circle_radius
            ),
            "y0": self._yaxis_operate(
                self.width / 2 - self.markings.center_circle_radius
            ),
            "x1": self._xaxis_operate(
                self.length
                - self.markings.penalty_mark_distance
                + self.markings.center_circle_radius
            ),
            "y1": self._yaxis_operate(
                self.width / 2 + self.markings.center_circle_radius
            ),
        }

    def right_penalty_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2
                    - self.markings.goal_width / 2
                    - self.markings.penalty_area_length
                ),
                "y0": self.yaxis_end,
                "x1": self._xaxis_operate(
                    self.length / 2
                    + self.markings.goal_width / 2
                    + self.markings.penalty_area_length
                ),
                "y1": self._yaxis_operate(
                    self.width - self.markings.penalty_area_length
                ),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(
                self.width / 2
                - self.markings.goal_width / 2
                - self.markings.penalty_area_length
            ),
            "x1": self._xaxis_operate(self.length - self.markings.penalty_area_length),
            "y1": self._yaxis_operate(
                self.width / 2
                + self.markings.goal_width / 2
                + self.markings.penalty_area_length
            ),
        }

    def right_penalty_mark(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - 0.2),
                "y0": self._yaxis_operate(
                    self.width - self.markings.penalty_mark_distance - 0.2
                ),
                "x1": self._xaxis_operate(self.length / 2 + 0.2),
                "y1": self._yaxis_operate(
                    self.width - self.markings.penalty_mark_distance + 0.2
                ),
            }
        return {
            "x0": self._xaxis_operate(
                self.length - self.markings.penalty_mark_distance - 0.2
            ),
            "y0": self._yaxis_operate(self.width / 2 - 0.2),
            "x1": self._xaxis_operate(
                self.length - self.markings.penalty_mark_distance + 0.2
            ),
            "y1": self._yaxis_operate(self.width / 2 + 0.2),
        }

    def right_goal_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2
                    - self.markings.goal_width / 2
                    - self.markings.goal_area_length
                ),
                "y0": self.yaxis_end,
                "x1": self._xaxis_operate(
                    self.length / 2
                    + self.markings.goal_width / 2
                    + self.markings.goal_area_length
                ),
                "y1": self._yaxis_operate(self.width - self.markings.goal_area_length),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(
                self.width / 2
                - self.markings.goal_width / 2
                - self.markings.goal_area_length
            ),
            "x1": self._xaxis_operate(self.length - self.markings.goal_area_length),
            "y1": self._yaxis_operate(
                self.width / 2
                + self.markings.goal_width / 2
                + self.markings.goal_area_length
            ),
        }

    def right_goal(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.markings.goal_width / 2
                ),
                "y0": self.yaxis_end,
                "x1": self._xaxis_operate(
                    self.length / 2 + self.markings.goal_width / 2
                ),
                "y1": self._yaxis_operate(self.width + self.markings.goal_height),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(self.width / 2 - self.markings.goal_width / 2),
            "x1": self._xaxis_operate(self.length + self.markings.goal_height),
            "y1": self._yaxis_operate(self.width / 2 + self.markings.goal_width / 2),
        }
