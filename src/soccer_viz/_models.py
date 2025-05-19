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


class Coordinates:
    def __init__(
        self,
        length: float,
        width: float,
        *,
        lock_standard_values: bool = True,
        center_circle_radius: float = 9.15,
        penalty_area_length: float = 16.5,
        penalty_mark_distance: float = 11,
        goal_area_length: float = 5.5,
        corner_arc_radius: float = 1,
        goal_width: float = 7.32,
        goal_height: float = 2.44,
    ) -> None:
        self.length = length
        self.width = width

        self.xaxis_scale = length / 105
        self.yaxis_scale = width / 68

        self.center_circle_radius = (
            center_circle_radius * self.xaxis_scale
            if lock_standard_values
            else center_circle_radius
        )
        self.penalty_area_length = (
            penalty_area_length * self.xaxis_scale
            if lock_standard_values
            else penalty_area_length
        )
        self.penalty_mark_distance = (
            penalty_mark_distance * self.xaxis_scale
            if lock_standard_values
            else penalty_mark_distance
        )
        self.goal_area_length = (
            goal_area_length * self.xaxis_scale
            if lock_standard_values
            else goal_area_length
        )
        self.corner_arc_radius = (
            corner_arc_radius * self.xaxis_scale
            if lock_standard_values
            else corner_arc_radius
        )
        self.goal_width = (
            goal_width * self.xaxis_scale
            if lock_standard_values
            else goal_width
        )
        self.goal_height = (
            goal_height * self.xaxis_scale
            if lock_standard_values
            else goal_height
        )

    def pitch_area(self) -> Area:
        return {
            "x0": 0,
            "y0": 0,
            "x1": self.length,
            "y1": self.width,
        }

    def centre_circle(self) -> Area:
        return {
            "x0": self.length / 2 - self.center_circle_radius,
            "y0": self.width / 2 - self.center_circle_radius,
            "x1": self.length / 2 + self.center_circle_radius,
            "y1": self.width / 2 + self.center_circle_radius,
        }

    def centre_mark(self) -> Area:
        return {
            "x0": self.length / 2 - 0.2,
            "y0": self.width / 2 - 0.2,
            "x1": self.length / 2 + 0.2,
            "y1": self.width / 2 + 0.2,
        }

    def halfway_line(self) -> Area:
        return {
            "x0": self.length / 2,
            "y0": 0,
            "x1": self.length / 2,
            "y1": self.width,
        }
    
    def left_penalty_arc(self) -> Area:
        return {
            "x0": self.penalty_mark_distance - self.center_circle_radius,
            "y0": self.width / 2 - self.center_circle_radius,
            "x1": self.penalty_mark_distance + self.center_circle_radius,
            "y1": self.width / 2 + self.center_circle_radius,
        }
    
    def left_penalty_area(self) -> Area:
        return {
            "x0": 0,
            "y0": self.width / 2 - self.goal_width / 2 - self.penalty_area_length,
            "x1": self.penalty_area_length,
            "y1": self.width / 2 + self.goal_width / 2 + self.penalty_area_length,
        }
    
    def left_penalty_mark(self) -> Area:
        return {
            "x0": self.penalty_mark_distance - 0.2,
            "y0": self.width / 2 - 0.2,
            "x1": self.penalty_mark_distance + 0.2,
            "y1": self.width / 2 + 0.2,
        }
    
    def left_goal_area(self) -> Area:
        return {
            "x0": 0,
            "y0": self.width / 2 - self.goal_width / 2 - self.goal_area_length,
            "x1": self.goal_area_length,
            "y1": self.width / 2 + self.goal_width / 2 + self.goal_area_length,
        }
    
    def left_goal(self) -> Area:
        return {
            "x0": -self.goal_height,
            "y0": self.width / 2 - self.goal_width / 2,
            "x1": 0,
            "y1": self.width / 2 + self.goal_width / 2,
        }
    
    def right_penalty_arc(self) -> Area:
        return {
            "x0": self.length - self.penalty_mark_distance - self.center_circle_radius,
            "y0": self.width / 2 - self.center_circle_radius,
            "x1": self.length - self.penalty_mark_distance + self.center_circle_radius,
            "y1": self.width / 2 + self.center_circle_radius,
        }
    
    def right_penalty_area(self) -> Area:
        return {
            "x0": self.length,
            "y0": self.width / 2 - self.goal_width / 2 - self.penalty_area_length,
            "x1": self.length - self.penalty_area_length,
            "y1": self.width / 2 + self.goal_width / 2 + self.penalty_area_length,
        }
    
    def right_penalty_mark(self) -> Area:
        return {
            "x0": self.length - self.penalty_mark_distance - 0.2,
            "y0": self.width / 2 - 0.2,
            "x1": self.length - self.penalty_mark_distance + 0.2,
            "y1": self.width / 2 + 0.2,
        }
    
    def right_goal_area(self) -> Area:
        return {
            "x0": self.length,
            "y0": self.width / 2 - self.goal_width / 2 - self.goal_area_length,
            "x1": self.length - self.goal_area_length,
            "y1": self.width / 2 + self.goal_width / 2 + self.goal_area_length,
        }
    
    def right_goal(self) -> Area:
        return {
            "x0": self.length,
            "y0": self.width / 2 - self.goal_width / 2,
            "x1": self.length + self.goal_height,
            "y1": self.width / 2 + self.goal_width / 2,
        }