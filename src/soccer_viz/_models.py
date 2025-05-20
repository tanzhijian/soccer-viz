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


class PitchCoordinates:
    def __init__(
        self,
        length: float | None = None,
        width: float | None = None,
        *,
        vertical: bool = False,
        xaxis_range: tuple[float, float] | None = None,
        yaxis_range: tuple[float, float] | None = None,
        lock_standard_values: bool = True,
        center_circle_radius: float = 9.15,
        penalty_area_length: float = 16.5,
        penalty_mark_distance: float = 11,
        goal_area_length: float = 5.5,
        corner_arc_radius: float = 1,
        goal_width: float = 7.32,
        goal_height: float = 2.44,
    ) -> None:
        if length is None:
            if vertical:
                length = 68
            else:
                length = 105
        if width is None:
            if vertical:
                width = 105
            else:
                width = 68
        self.length = length
        self.width = width
        self.vertical = vertical

        self.xaxis_range = xaxis_range if xaxis_range is not None else (0.0, length)
        self.yaxis_range = yaxis_range if yaxis_range is not None else (0.0, width)

        self.xaxis_scale = length / 105
        self.yaxis_scale = width / 68

        self.center_circle_radius = (
            center_circle_radius
            if lock_standard_values
            else center_circle_radius * self.xaxis_scale
        )
        self.penalty_area_length = (
            penalty_area_length
            if lock_standard_values
            else penalty_area_length * self.xaxis_scale
        )
        self.penalty_mark_distance = (
            penalty_mark_distance
            if lock_standard_values
            else penalty_mark_distance * self.xaxis_scale
        )
        self.goal_area_length = (
            goal_area_length
            if lock_standard_values
            else goal_area_length * self.xaxis_scale
        )
        self.corner_arc_radius = (
            corner_arc_radius
            if lock_standard_values
            else corner_arc_radius * self.xaxis_scale
        )
        self.goal_width = (
            goal_width if lock_standard_values else goal_width * self.xaxis_scale
        )
        self.goal_height = (
            goal_height if lock_standard_values else goal_height * self.xaxis_scale
        )

    @property
    def xaxis_start(self) -> float:
        return self.xaxis_range[0]

    @property
    def xaxis_end(self) -> float:
        return self.xaxis_range[1]

    @property
    def yaxis_start(self) -> float:
        return self.yaxis_range[0]

    @property
    def yaxis_end(self) -> float:
        return self.yaxis_range[1]

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
            "x0": self._xaxis_operate(self.length / 2 - self.center_circle_radius),
            "y0": self._yaxis_operate(self.width / 2 - self.center_circle_radius),
            "x1": self._xaxis_operate(self.length / 2 + self.center_circle_radius),
            "y1": self._yaxis_operate(self.width / 2 + self.center_circle_radius),
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
                "x0": self._xaxis_operate(self.length / 2 - self.center_circle_radius),
                "y0": self._yaxis_operate(
                    self.penalty_mark_distance - self.center_circle_radius
                ),
                "x1": self._xaxis_operate(self.length / 2 + self.center_circle_radius),
                "y1": self._yaxis_operate(
                    self.penalty_mark_distance + self.center_circle_radius
                ),
            }
        return {
            "x0": self._xaxis_operate(
                self.penalty_mark_distance - self.center_circle_radius
            ),
            "y0": self._yaxis_operate(self.width / 2 - self.center_circle_radius),
            "x1": self._xaxis_operate(
                self.penalty_mark_distance + self.center_circle_radius
            ),
            "y1": self._yaxis_operate(self.width / 2 + self.center_circle_radius),
        }

    def left_penalty_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.goal_width / 2 - self.penalty_area_length
                ),
                "y0": self.yaxis_start,
                "x1": self._xaxis_operate(
                    self.length / 2 + self.goal_width / 2 + self.penalty_area_length
                ),
                "y1": self._yaxis_operate(self.penalty_area_length),
            }
        return {
            "x0": self.xaxis_start,
            "y0": self._yaxis_operate(
                self.width / 2 - self.goal_width / 2 - self.penalty_area_length
            ),
            "x1": self._xaxis_operate(self.penalty_area_length),
            "y1": self._yaxis_operate(
                self.width / 2 + self.goal_width / 2 + self.penalty_area_length
            ),
        }

    def left_penalty_mark(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - 0.2),
                "y0": self._yaxis_operate(self.penalty_mark_distance - 0.2),
                "x1": self._xaxis_operate(self.length / 2 + 0.2),
                "y1": self._yaxis_operate(self.penalty_mark_distance + 0.2),
            }
        return {
            "x0": self._xaxis_operate(self.penalty_mark_distance - 0.2),
            "y0": self._yaxis_operate(self.width / 2 - 0.2),
            "x1": self._xaxis_operate(self.penalty_mark_distance + 0.2),
            "y1": self._yaxis_operate(self.width / 2 + 0.2),
        }

    def left_goal_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.goal_width / 2 - self.goal_area_length
                ),
                "y0": self.yaxis_start,
                "x1": self._xaxis_operate(
                    self.length / 2 + self.goal_width / 2 + self.goal_area_length
                ),
                "y1": self._yaxis_operate(self.goal_area_length),
            }
        return {
            "x0": self.xaxis_start,
            "y0": self._yaxis_operate(
                self.width / 2 - self.goal_width / 2 - self.goal_area_length
            ),
            "x1": self._xaxis_operate(self.goal_area_length),
            "y1": self._yaxis_operate(
                self.width / 2 + self.goal_width / 2 + self.goal_area_length
            ),
        }

    def left_goal(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - self.goal_width / 2),
                "y0": self.yaxis_start,
                "x1": self._xaxis_operate(self.length / 2 + self.goal_width / 2),
                "y1": self._yaxis_operate(-self.goal_height),
            }
        return {
            "x0": self._xaxis_operate(-self.goal_height),
            "y0": self._yaxis_operate(self.width / 2 - self.goal_width / 2),
            "x1": self.xaxis_start,
            "y1": self._yaxis_operate(self.width / 2 + self.goal_width / 2),
        }

    def right_penalty_arc(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - self.center_circle_radius),
                "y0": self._yaxis_operate(
                    self.width - self.penalty_mark_distance - self.center_circle_radius
                ),
                "x1": self._xaxis_operate(self.length / 2 + self.center_circle_radius),
                "y1": self._yaxis_operate(
                    self.width - self.penalty_mark_distance + self.center_circle_radius
                ),
            }
        return {
            "x0": self._xaxis_operate(
                self.length - self.penalty_mark_distance - self.center_circle_radius
            ),
            "y0": self._yaxis_operate(self.width / 2 - self.center_circle_radius),
            "x1": self._xaxis_operate(
                self.length - self.penalty_mark_distance + self.center_circle_radius
            ),
            "y1": self._yaxis_operate(self.width / 2 + self.center_circle_radius),
        }

    def right_penalty_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.goal_width / 2 - self.penalty_area_length
                ),
                "y0": self.yaxis_end,
                "x1": self._xaxis_operate(
                    self.length / 2 + self.goal_width / 2 + self.penalty_area_length
                ),
                "y1": self._yaxis_operate(self.width - self.penalty_area_length),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(
                self.width / 2 - self.goal_width / 2 - self.penalty_area_length
            ),
            "x1": self._xaxis_operate(self.length - self.penalty_area_length),
            "y1": self._yaxis_operate(
                self.width / 2 + self.goal_width / 2 + self.penalty_area_length
            ),
        }

    def right_penalty_mark(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - 0.2),
                "y0": self._yaxis_operate(
                    self.width - self.penalty_mark_distance - 0.2
                ),
                "x1": self._xaxis_operate(self.length / 2 + 0.2),
                "y1": self._yaxis_operate(
                    self.width - self.penalty_mark_distance + 0.2
                ),
            }
        return {
            "x0": self._xaxis_operate(self.length - self.penalty_mark_distance - 0.2),
            "y0": self._yaxis_operate(self.width / 2 - 0.2),
            "x1": self._xaxis_operate(self.length - self.penalty_mark_distance + 0.2),
            "y1": self._yaxis_operate(self.width / 2 + 0.2),
        }

    def right_goal_area(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(
                    self.length / 2 - self.goal_width / 2 - self.goal_area_length
                ),
                "y0": self.yaxis_end,
                "x1": self._xaxis_operate(
                    self.length / 2 + self.goal_width / 2 + self.goal_area_length
                ),
                "y1": self._yaxis_operate(self.width - self.goal_area_length),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(
                self.width / 2 - self.goal_width / 2 - self.goal_area_length
            ),
            "x1": self._xaxis_operate(self.length - self.goal_area_length),
            "y1": self._yaxis_operate(
                self.width / 2 + self.goal_width / 2 + self.goal_area_length
            ),
        }

    def right_goal(self) -> Area:
        if self.vertical:
            return {
                "x0": self._xaxis_operate(self.length / 2 - self.goal_width / 2),
                "y0": self.yaxis_end,
                "x1": self._xaxis_operate(self.length / 2 + self.goal_width / 2),
                "y1": self._yaxis_operate(self.width + self.goal_height),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(self.width / 2 - self.goal_width / 2),
            "x1": self._xaxis_operate(self.length + self.goal_height),
            "y1": self._yaxis_operate(self.width / 2 + self.goal_width / 2),
        }
