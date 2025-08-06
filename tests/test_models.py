from typing import Literal

import pytest

from soccer_viz._models import PitchCoordinates, PitchMarkings


def scale_100(value: float) -> int:
    return int(round(value * 100))


def test_pitch_markings_defaults() -> None:
    markings = PitchMarkings()
    assert scale_100(markings.center_circle_radius) == scale_100(9.15)
    assert scale_100(markings.penalty_area_length) == scale_100(16.5)
    assert scale_100(markings.penalty_mark_distance) == scale_100(11)
    assert scale_100(markings.goal_area_length) == scale_100(5.5)
    assert scale_100(markings.goal_width) == scale_100(7.32)
    assert scale_100(markings.goal_height) == scale_100(2.44)


def test_pitch_markings_vertical_custom() -> None:
    markings = PitchMarkings(
        length=120,
        width=80,
        use_standard=False,
        center_circle_radius=10,
        penalty_area_length=18,
        penalty_mark_distance=12,
        goal_area_length=6,
        goal_width=8,
        goal_height=2.67,
    )
    assert scale_100(markings.center_circle_radius) == scale_100(10)
    assert scale_100(markings.penalty_area_length) == scale_100(18)
    assert scale_100(markings.penalty_mark_distance) == scale_100(12)
    assert scale_100(markings.goal_area_length) == scale_100(6)
    assert scale_100(markings.goal_width) == scale_100(8)
    assert scale_100(markings.goal_height) == scale_100(2.67)


def test_pitch_markings_equality() -> None:
    markings1 = PitchMarkings(center_circle_radius=0.1 + 0.2)
    markings2 = PitchMarkings(center_circle_radius=0.3)
    assert markings1 == markings2

    markings3 = PitchMarkings(center_circle_radius=10)
    assert markings1 != markings3


class TestStandardCoordinates:
    @pytest.fixture(scope="class")
    def coordinates(self) -> PitchCoordinates:
        return PitchCoordinates()

    def test_properties(self, coordinates: PitchCoordinates) -> None:
        assert coordinates.vertical is False
        assert coordinates.side == "both"
        assert coordinates.xaxis_start == 0
        assert coordinates.xaxis_end == 105
        assert coordinates.yaxis_start == 0
        assert coordinates.yaxis_end == 68
        assert scale_100(coordinates.aspect_ratio) == scale_100(68 / 105)

    def test_pitch_area(self, coordinates: PitchCoordinates) -> None:
        pitch_area = coordinates.pitch_area()
        assert int(pitch_area["x0"]) == 0
        assert int(pitch_area["x1"] - pitch_area["x0"]) == 105
        assert int(pitch_area["y1"] - pitch_area["y0"]) == 68

    def test_centre_circle(self, coordinates: PitchCoordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert scale_100(centre_circle["x0"]) == scale_100((52.5 - 9.15))
        assert scale_100(
            abs(centre_circle["x1"] - centre_circle["x0"])
        ) == scale_100(9.15 * 2)

    def test_centre_mark(self, coordinates: PitchCoordinates) -> None:
        centre_mark = coordinates.centre_mark()
        assert scale_100(centre_mark["x0"]) == scale_100(52.5 - 0.2)
        assert scale_100(centre_mark["y1"]) == scale_100(34 + 0.2)

    def test_halfway_line(self, coordinates: PitchCoordinates) -> None:
        halfway_line = coordinates.halfway_line()
        assert scale_100(halfway_line["x0"]) == scale_100(52.5)
        assert int((halfway_line["y1"] - halfway_line["y0"])) == 68

    def test_left_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        left_penalty_arc = coordinates.left_penalty_arc()
        assert scale_100(left_penalty_arc["x0"]) == scale_100(11 - 9.15)

    def test_left_penalty_area(self, coordinates: PitchCoordinates) -> None:
        left_penalty_area = coordinates.left_penalty_area()
        assert int(left_penalty_area["x0"]) == 0
        assert scale_100(
            (left_penalty_area["x1"] - left_penalty_area["x0"])
        ) == scale_100(16.5)
        assert round(
            (left_penalty_area["y1"] - left_penalty_area["y0"])
        ) == round((16.5 * 2 + 7.32))

    def test_left_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        left_penalty_mark = coordinates.left_penalty_mark()
        assert round(left_penalty_mark["x0"]) == round((11 - 0.2))
        assert scale_100(left_penalty_mark["y0"]) == scale_100(34 - 0.2)

    def test_left_goal_area(self, coordinates: PitchCoordinates) -> None:
        left_goal_area = coordinates.left_goal_area()
        assert int(left_goal_area["x0"]) == 0
        assert scale_100(
            left_goal_area["x1"] - left_goal_area["x0"]
        ) == scale_100(5.5)
        assert scale_100(
            left_goal_area["y1"] - left_goal_area["y0"]
        ) == scale_100(7.32 + 5.5 * 2)

    def test_left_goal(self, coordinates: PitchCoordinates) -> None:
        left_goal = coordinates.left_goal()
        assert scale_100(left_goal["x0"]) == scale_100(-2.44)

    def test_right_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        right_penalty_arc = coordinates.right_penalty_arc()
        assert scale_100(right_penalty_arc["x0"]) == scale_100(105 - 11 - 9.15)

    def test_right_penalty_area(self, coordinates: PitchCoordinates) -> None:
        right_penalty_area = coordinates.right_penalty_area()
        assert scale_100(right_penalty_area["x1"]) == scale_100(105 - 16.5)
        assert scale_100(
            (right_penalty_area["x0"] - right_penalty_area["x1"])
        ) == scale_100(16.5)
        assert scale_100(
            (right_penalty_area["y1"] - right_penalty_area["y0"])
        ) == scale_100((16.5 * 2 + 7.32))

    def test_right_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        right_penalty_mark = coordinates.right_penalty_mark()
        assert scale_100(right_penalty_mark["x0"]) == scale_100(105 - 11 - 0.2)
        assert scale_100(right_penalty_mark["y0"]) == scale_100(34 - 0.2)

    def test_right_goal_area(self, coordinates: PitchCoordinates) -> None:
        right_goal_area = coordinates.right_goal_area()
        assert scale_100(right_goal_area["x1"]) == scale_100(105 - 5.5)
        assert scale_100(
            right_goal_area["x0"] - right_goal_area["x1"]
        ) == scale_100(5.5)
        assert scale_100(
            right_goal_area["y1"] - right_goal_area["y0"]
        ) == scale_100(7.32 + 5.5 * 2)

    def test_right_goal(self, coordinates: PitchCoordinates) -> None:
        right_goal = coordinates.right_goal()
        assert scale_100(right_goal["x1"]) == scale_100(105 + 2.44)


class TestCustomCoordinates:
    @pytest.fixture(scope="class")
    def coordinates(self) -> PitchCoordinates:
        markings = PitchMarkings(
            length=120,
            width=80,
            center_circle_radius=10,
            penalty_area_length=18,
            penalty_mark_distance=12,
            goal_area_length=6,
            goal_width=8,
            goal_height=2.67,
        )
        return PitchCoordinates(markings=markings)

    def test_properties(self, coordinates: PitchCoordinates) -> None:
        assert coordinates.xaxis_end == 120
        assert coordinates.yaxis_end == 80
        assert scale_100(coordinates.aspect_ratio) == scale_100(80 / 120)

    def test_pitch_area(self, coordinates: PitchCoordinates) -> None:
        area = coordinates.pitch_area()
        assert area["x0"] == 0
        assert abs(scale_100(area["x1"] - area["x0"])) == scale_100(120)
        assert abs(scale_100(area["y1"] - area["y0"])) == scale_100(80)

    def test_centre_circle(self, coordinates: PitchCoordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert scale_100(centre_circle["x0"]) == scale_100(60 - 10)
        assert scale_100(
            centre_circle["x1"] - centre_circle["x0"]
        ) == scale_100(20)

    def test_centre_mark(self, coordinates: PitchCoordinates) -> None:
        centre_mark = coordinates.centre_mark()
        assert scale_100(centre_mark["x0"]) == scale_100(60 - 0.2)
        assert scale_100(centre_mark["y1"]) == scale_100(40 + 0.2)

    def test_halfway_line(self, coordinates: PitchCoordinates) -> None:
        halfway_line = coordinates.halfway_line()
        assert scale_100(halfway_line["x0"]) == scale_100(60)
        assert abs(halfway_line["y1"] - halfway_line["y0"]) == 80

    def test_left_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        left_penalty_arc = coordinates.left_penalty_arc()
        assert scale_100(left_penalty_arc["x0"]) == scale_100(12 - 10)

    def test_left_penalty_area(self, coordinates: PitchCoordinates) -> None:
        left_penalty_area = coordinates.left_penalty_area()
        assert left_penalty_area["x0"] == 0
        assert scale_100(
            left_penalty_area["x1"] - left_penalty_area["x0"]
        ) == scale_100(18)
        assert scale_100(
            abs(left_penalty_area["y1"] - left_penalty_area["y0"])
        ) == scale_100((18 * 2 + 8))

    def test_left_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        left_penalty_mark = coordinates.left_penalty_mark()
        assert scale_100(left_penalty_mark["x0"]) == scale_100(12 - 0.2)
        assert scale_100(left_penalty_mark["y0"]) == scale_100(40 - 0.2)

    def test_left_goal_area(self, coordinates: PitchCoordinates) -> None:
        left_goal_area = coordinates.left_goal_area()
        assert left_goal_area["x0"] == 0
        assert scale_100(
            left_goal_area["x1"] - left_goal_area["x0"]
        ) == scale_100(6)
        assert scale_100(
            abs(left_goal_area["y1"] - left_goal_area["y0"])
        ) == scale_100(8 + 6 * 2)

    def test_left_goal(self, coordinates: PitchCoordinates) -> None:
        left_goal = coordinates.left_goal()
        assert scale_100(left_goal["x0"]) == scale_100(-2.67)

    def test_right_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        right_penalty_arc = coordinates.right_penalty_arc()
        assert scale_100(right_penalty_arc["x0"]) == scale_100(120 - 12 - 10)

    def test_right_penalty_area(self, coordinates: PitchCoordinates) -> None:
        right_penalty_area = coordinates.right_penalty_area()
        assert scale_100(right_penalty_area["x1"]) == scale_100(120 - 18)
        assert scale_100(
            right_penalty_area["x0"] - right_penalty_area["x1"]
        ) == scale_100(18)
        assert scale_100(
            abs(right_penalty_area["y1"] - right_penalty_area["y0"])
        ) == scale_100((18 * 2 + 8))

    def test_right_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        right_penalty_mark = coordinates.right_penalty_mark()
        assert scale_100(right_penalty_mark["x0"]) == scale_100(120 - 12 - 0.2)
        assert scale_100(right_penalty_mark["y0"]) == scale_100(40 - 0.2)

    def test_right_goal_area(self, coordinates: PitchCoordinates) -> None:
        right_goal_area = coordinates.right_goal_area()
        assert scale_100(right_goal_area["x1"]) == scale_100(120 - 6)
        assert scale_100(
            right_goal_area["x0"] - right_goal_area["x1"]
        ) == scale_100(6)
        assert scale_100(
            abs(right_goal_area["y1"] - right_goal_area["y0"])
        ) == scale_100(8 + 6 * 2)

    def test_right_goal(self, coordinates: PitchCoordinates) -> None:
        right_goal = coordinates.right_goal()
        assert scale_100(right_goal["x1"]) == scale_100(120 + 2.67)


class TestVerticalCoordinates:
    @pytest.fixture(scope="class")
    def coordinates(self) -> PitchCoordinates:
        return PitchCoordinates(
            vertical=True,
        )

    def test_properties(self, coordinates: PitchCoordinates) -> None:
        assert int(coordinates.xaxis_end) == 68
        assert int(coordinates.yaxis_end) == 105
        assert scale_100(coordinates.aspect_ratio) == scale_100(68 / 105)

    def test_pitch_area(self, coordinates: PitchCoordinates) -> None:
        pitch_area = coordinates.pitch_area()
        assert int(pitch_area["x0"]) == 0
        assert int(pitch_area["x1"] - pitch_area["x0"]) == 68
        assert int(pitch_area["y1"] - pitch_area["y0"]) == 105

    def test_centre_circle(self, coordinates: PitchCoordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert scale_100(centre_circle["x0"]) == scale_100((34 - 9.15))
        assert scale_100(
            abs(centre_circle["x1"] - centre_circle["x0"])
        ) == scale_100(9.15 * 2)

    def test_centre_mark(self, coordinates: PitchCoordinates) -> None:
        centre_mark = coordinates.centre_mark()
        assert scale_100(centre_mark["x0"]) == scale_100(34 - 0.2)
        assert scale_100(centre_mark["y1"]) == scale_100(52.5 + 0.2)

    def test_halfway_line(self, coordinates: PitchCoordinates) -> None:
        halfway_line = coordinates.halfway_line()
        assert scale_100(halfway_line["x0"]) == scale_100(0)
        assert int((halfway_line["x1"] - halfway_line["x0"])) == 68

    def test_left_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        left_penalty_arc = coordinates.left_penalty_arc()
        assert scale_100(left_penalty_arc["y0"]) == scale_100(11 - 9.15)

    def test_left_penalty_area(self, coordinates: PitchCoordinates) -> None:
        left_penalty_area = coordinates.left_penalty_area()
        assert int(left_penalty_area["y0"]) == 0
        assert scale_100(
            (left_penalty_area["x1"] - left_penalty_area["x0"])
        ) == scale_100((16.5 * 2 + 7.32))
        assert scale_100(
            (left_penalty_area["y1"] - left_penalty_area["y0"])
        ) == scale_100(16.5)

    def test_left_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        left_penalty_mark = coordinates.left_penalty_mark()
        assert scale_100(left_penalty_mark["y0"]) == scale_100((11 - 0.2))
        assert scale_100(left_penalty_mark["x0"]) == scale_100(34 - 0.2)

    def test_left_goal_area(self, coordinates: PitchCoordinates) -> None:
        left_goal_area = coordinates.left_goal_area()
        assert int(left_goal_area["y0"]) == 0
        assert scale_100(
            left_goal_area["x1"] - left_goal_area["x0"]
        ) == scale_100(7.32 + 5.5 * 2)
        assert scale_100(
            left_goal_area["y1"] - left_goal_area["y0"]
        ) == scale_100(5.5)

    def test_left_goal(self, coordinates: PitchCoordinates) -> None:
        left_goal = coordinates.left_goal()
        assert scale_100(left_goal["y1"]) == scale_100(-2.44)

    def test_right_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        right_penalty_arc = coordinates.right_penalty_arc()
        assert scale_100(right_penalty_arc["y0"]) == scale_100(105 - 11 - 9.15)

    def test_right_penalty_area(self, coordinates: PitchCoordinates) -> None:
        right_penalty_area = coordinates.right_penalty_area()
        assert scale_100(right_penalty_area["y1"]) == scale_100(105 - 16.5)
        assert scale_100(
            abs(right_penalty_area["x0"] - right_penalty_area["x1"])
        ) == scale_100((16.5 * 2 + 7.32))
        assert scale_100(
            abs(right_penalty_area["y1"] - right_penalty_area["y0"])
        ) == scale_100(16.5)

    def test_right_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        right_penalty_mark = coordinates.right_penalty_mark()
        assert scale_100(right_penalty_mark["y0"]) == scale_100(105 - 11 - 0.2)
        assert scale_100(right_penalty_mark["x0"]) == scale_100(34 - 0.2)

    def test_right_goal_area(self, coordinates: PitchCoordinates) -> None:
        right_goal_area = coordinates.right_goal_area()
        assert scale_100(right_goal_area["y1"]) == scale_100(105 - 5.5)
        assert scale_100(
            abs(right_goal_area["x0"] - right_goal_area["x1"])
        ) == scale_100(7.32 + 5.5 * 2)
        assert scale_100(
            abs(right_goal_area["y1"] - right_goal_area["y0"])
        ) == scale_100(5.5)

    def test_right_goal(self, coordinates: PitchCoordinates) -> None:
        right_goal = coordinates.right_goal()
        assert scale_100(right_goal["y1"]) == scale_100(105 + 2.44)


@pytest.mark.parametrize(
    "side, vertical, result",
    [
        ("left", False, (0, 52.5)),
        ("right", False, (52.5, 105)),
        ("left", True, (0, 52.5)),
        ("right", True, (52.5, 105)),
    ],
)
def test_side_coordinates(
    side: Literal["left", "right"],
    vertical: bool,
    result: tuple[float, float],
) -> None:
    coordinates = PitchCoordinates(vertical=vertical, side=side)
    if not vertical:
        assert scale_100(coordinates.xaxis_start) == scale_100(result[0])
        assert scale_100(coordinates.xaxis_end) == scale_100(result[1])
    else:
        assert scale_100(coordinates.yaxis_start) == scale_100(result[0])
        assert scale_100(coordinates.yaxis_end) == scale_100(result[1])
