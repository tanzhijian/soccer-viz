from dataclasses import dataclass
from math import isclose
from typing import Literal, TypedDict


class Area(TypedDict):
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass
class PitchMarkings:
    center_circle_radius: float = 9.15
    penalty_area_length: float = 16.5
    penalty_mark_distance: float = 11
    goal_area_length: float = 5.5
    corner_arc_radius: float = 1
    goal_width: float = 7.32
    goal_height: float = 2.44

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PitchMarkings):
            return NotImplemented
        return all(
            isclose(getattr(self, field), getattr(other, field))
            for field in self.__dataclass_fields__
        )

    def change_scale(
        self,
        xaxis_scale: float,
        yaxis_scale: float,
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
        side: Literal["left", "right", "both"] = "both",
        lock_markings: bool = True,
    ) -> None:
        self.vertical = vertical
        self.side = side
        self.xaxis_range = self._set_axis_range(
            xaxis_range, vertical, is_x=True
        )
        self.yaxis_range = self._set_axis_range(
            yaxis_range, vertical, is_x=False
        )
        if side != "both":
            if vertical:
                self.yaxis_range = self._set_side(side, self.yaxis_range)
            else:
                self.xaxis_range = self._set_side(side, self.xaxis_range)
        self.xaxis_start, self.xaxis_end = self.xaxis_range
        self.yaxis_start, self.yaxis_end = self.yaxis_range
        self.length = abs(self.xaxis_end - self.xaxis_start)
        self.width = abs(self.yaxis_end - self.yaxis_start)

        self.xaxis_scale, self.yaxis_scale = self._set_scale()
        self.markings = markings if markings is not None else PitchMarkings()
        if not lock_markings:
            self.markings.change_scale(
                self.xaxis_scale, self.yaxis_scale, vertical
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PitchCoordinates):
            return NotImplemented
        xaxis_equal = isclose(self.xaxis_start, other.xaxis_start) and isclose(
            self.xaxis_end, other.xaxis_end
        )
        yaxis_equal = isclose(self.yaxis_start, other.yaxis_start) and isclose(
            self.yaxis_end, other.yaxis_end
        )
        return (
            xaxis_equal
            and yaxis_equal
            and self.vertical == other.vertical
            and self.markings == other.markings
        )

    def _set_axis_range(
        self,
        axis_range: tuple[float, float] | None,
        vertical: bool,
        is_x: bool,
    ) -> tuple[float, float]:
        if axis_range is not None:
            return axis_range
        if is_x:
            length = 68 if vertical else 105
            return (0.0, length)
        else:
            width = 105 if vertical else 68
            return (0.0, width)

    def _set_side(
        self,
        side: str,
        axis: tuple[float, float],
    ) -> tuple[float, float]:
        if side == "both":
            return axis
        if side == "left":
            return (axis[0], axis[0] + (axis[1] - axis[0]) / 2)
        if side == "right":
            return (axis[0] + (axis[1] - axis[0]) / 2, axis[1])
        raise ValueError(
            f"Invalid side: {side}. Choose 'left', 'right', or 'both'."
        )

    def _set_scale(self) -> tuple[float, float]:
        standard_length = 105.0
        standard_width = 68.0
        if self.side != "both":
            standard_length /= 2
        if self.vertical:
            standard_length, standard_width = standard_width, standard_length
        return self.length / standard_length, self.width / standard_width

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
                self.markings.penalty_mark_distance
                - self.markings.center_circle_radius
            ),
            "y0": self._yaxis_operate(
                self.width / 2 - self.markings.center_circle_radius
            ),
            "x1": self._xaxis_operate(
                self.markings.penalty_mark_distance
                + self.markings.center_circle_radius
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
                "y0": self._yaxis_operate(
                    self.markings.penalty_mark_distance - 0.2
                ),
                "x1": self._xaxis_operate(self.length / 2 + 0.2),
                "y1": self._yaxis_operate(
                    self.markings.penalty_mark_distance + 0.2
                ),
            }
        return {
            "x0": self._xaxis_operate(
                self.markings.penalty_mark_distance - 0.2
            ),
            "y0": self._yaxis_operate(self.width / 2 - 0.2),
            "x1": self._xaxis_operate(
                self.markings.penalty_mark_distance + 0.2
            ),
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
            "y0": self._yaxis_operate(
                self.width / 2 - self.markings.goal_width / 2
            ),
            "x1": self.xaxis_start,
            "y1": self._yaxis_operate(
                self.width / 2 + self.markings.goal_width / 2
            ),
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
            "x1": self._xaxis_operate(
                self.length - self.markings.penalty_area_length
            ),
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
                "y1": self._yaxis_operate(
                    self.width - self.markings.goal_area_length
                ),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(
                self.width / 2
                - self.markings.goal_width / 2
                - self.markings.goal_area_length
            ),
            "x1": self._xaxis_operate(
                self.length - self.markings.goal_area_length
            ),
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
                "y1": self._yaxis_operate(
                    self.width + self.markings.goal_height
                ),
            }
        return {
            "x0": self.xaxis_end,
            "y0": self._yaxis_operate(
                self.width / 2 - self.markings.goal_width / 2
            ),
            "x1": self._xaxis_operate(self.length + self.markings.goal_height),
            "y1": self._yaxis_operate(
                self.width / 2 + self.markings.goal_width / 2
            ),
        }
