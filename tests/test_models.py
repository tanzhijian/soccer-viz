import pytest

from soccer_viz._models import PitchCoordinates, PitchMarkings


def scale_100(value: float) -> int:
    return int(round(value * 100))


def test_pitch_markings_change_scale() -> None:
    markings = PitchMarkings()
    markings.change_scale(xaxis_scale=2, yaxis_scale=1.5)
    # y_scale
    assert scale_100(markings.center_circle_radius) == scale_100(9.15 * 1.5)
    assert scale_100(markings.goal_width) == scale_100(7.32 * 1.5)
    assert scale_100(markings.goal_height) == scale_100(2.44 * 1.5)
    # y_scale
    assert scale_100(markings.penalty_area_length) == scale_100(16.5 * 2)
    assert scale_100(markings.penalty_mark_distance) == scale_100(11 * 2)
    assert scale_100(markings.goal_area_length) == scale_100(5.5 * 2)
    assert scale_100(markings.corner_arc_radius) == scale_100(1.0 * 2)


def test_pitch_markings_vertical_change_scale() -> None:
    markings = PitchMarkings()
    markings.change_scale(xaxis_scale=1.5, yaxis_scale=2, vertical=True)
    assert scale_100(markings.center_circle_radius) == scale_100(9.15 * 1.5)
    assert scale_100(markings.penalty_area_length) == scale_100(16.5 * 2)

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

    def test_initialization(self, coordinates: PitchCoordinates) -> None:
        assert int(coordinates.length) == 105
        assert int(coordinates.width) == 68
        assert int(coordinates.xaxis_scale) == 1
        assert int(coordinates.yaxis_scale) == 1
        assert int(coordinates.markings.penalty_mark_distance) == 11

    def test_equality(self, coordinates: PitchCoordinates) -> None:
        assert coordinates == PitchCoordinates()
        assert coordinates != PitchCoordinates(xaxis_range=(-60, 60))

    def test_pitch_area(self, coordinates: PitchCoordinates) -> None:
        pitch_area = coordinates.pitch_area()
        assert int(pitch_area["x0"]) == 0
        assert int(pitch_area["x1"] - pitch_area["x0"]) == 105
        assert int(pitch_area["y1"] - pitch_area["y0"]) == 68

    def test_centre_circle(self, coordinates: PitchCoordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert scale_100(centre_circle["x0"]) == scale_100((52.5 - 9.15))
        assert scale_100(abs(centre_circle["x1"] - centre_circle["x0"])) == scale_100(
            9.15 * 2
        )

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
        assert round((left_penalty_area["y1"] - left_penalty_area["y0"])) == round(
            (16.5 * 2 + 7.32)
        )

    def test_left_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        left_penalty_mark = coordinates.left_penalty_mark()
        assert round(left_penalty_mark["x0"]) == round((11 - 0.2))
        assert scale_100(left_penalty_mark["y0"]) == scale_100(34 - 0.2)

    def test_left_goal_area(self, coordinates: PitchCoordinates) -> None:
        left_goal_area = coordinates.left_goal_area()
        assert int(left_goal_area["x0"]) == 0
        assert scale_100(left_goal_area["x1"] - left_goal_area["x0"]) == scale_100(5.5)
        assert scale_100(left_goal_area["y1"] - left_goal_area["y0"]) == scale_100(
            7.32 + 5.5 * 2
        )

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
        assert scale_100(right_goal_area["x0"] - right_goal_area["x1"]) == scale_100(
            5.5
        )
        assert scale_100(right_goal_area["y1"] - right_goal_area["y0"]) == scale_100(
            7.32 + 5.5 * 2
        )

    def test_right_goal(self, coordinates: PitchCoordinates) -> None:
        right_goal = coordinates.right_goal()
        assert scale_100(right_goal["x1"]) == scale_100(105 + 2.44)


class TestCustomCoordinates:
    @pytest.fixture(scope="class")
    def coordinates(self) -> PitchCoordinates:
        markings = PitchMarkings(
            center_circle_radius=10,
            penalty_area_length=18,
            penalty_mark_distance=12,
            goal_area_length=6,
            goal_width=8,
            goal_height=2.67,
        )
        return PitchCoordinates(
            xaxis_range=(-60, 60),
            yaxis_range=(80, 0),
            markings=markings,
        )

    def test_initialization(self, coordinates: PitchCoordinates) -> None:
        assert int(coordinates.length) == 120
        assert int(coordinates.width) == 80
        assert scale_100(coordinates.xaxis_scale) == scale_100(1.14)
        assert coordinates.xaxis_start == -60
        assert coordinates.xaxis_end == 60
        assert coordinates.yaxis_start == 80
        assert coordinates.yaxis_end == 0

    def test_pitch_area(self, coordinates: PitchCoordinates) -> None:
        area = coordinates.pitch_area()
        assert scale_100(area["x0"]) == scale_100(-60)
        assert abs(scale_100(area["x1"] - area["x0"])) == scale_100(120)
        assert abs(scale_100(area["y1"] - area["y0"])) == scale_100(80)

    def test_centre_circle(self, coordinates: PitchCoordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert scale_100(centre_circle["x0"]) == scale_100(-10)
        assert abs(scale_100(centre_circle["x1"] - centre_circle["x0"])) == scale_100(
            20
        )

    def test_centre_mark(self, coordinates: PitchCoordinates) -> None:
        centre_mark = coordinates.centre_mark()
        assert scale_100(centre_mark["x0"]) == scale_100(-0.2)
        assert scale_100(centre_mark["y1"]) == scale_100(40 - 0.2)

    def test_halfway_line(self, coordinates: PitchCoordinates) -> None:
        halfway_line = coordinates.halfway_line()
        assert scale_100(halfway_line["x0"]) == scale_100(0)
        assert abs(halfway_line["y1"] - halfway_line["y0"]) == 80

    def test_left_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        left_penalty_arc = coordinates.left_penalty_arc()
        assert scale_100(left_penalty_arc["x0"]) == scale_100(-60 + 12 - 10)

    def test_left_penalty_area(self, coordinates: PitchCoordinates) -> None:
        left_penalty_area = coordinates.left_penalty_area()
        assert int(left_penalty_area["x0"]) == -60
        assert scale_100(
            left_penalty_area["x1"] - left_penalty_area["x0"]
        ) == scale_100(18)
        assert scale_100(
            abs(left_penalty_area["y1"] - left_penalty_area["y0"])
        ) == scale_100((18 * 2 + 8))

    def test_left_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        left_penalty_mark = coordinates.left_penalty_mark()
        assert scale_100(left_penalty_mark["x0"]) == scale_100(-60 + 12 - 0.2)
        assert scale_100(left_penalty_mark["y0"]) == scale_100(40 + 0.2)

    def test_left_goal_area(self, coordinates: PitchCoordinates) -> None:
        left_goal_area = coordinates.left_goal_area()
        assert int(left_goal_area["x0"]) == -60
        assert scale_100(left_goal_area["x1"] - left_goal_area["x0"]) == scale_100(6)
        assert scale_100(abs(left_goal_area["y1"] - left_goal_area["y0"])) == scale_100(
            8 + 6 * 2
        )

    def test_left_goal(self, coordinates: PitchCoordinates) -> None:
        left_goal = coordinates.left_goal()
        assert scale_100(left_goal["x0"]) == scale_100(-60 - 2.67)

    def test_right_penalty_arc(self, coordinates: PitchCoordinates) -> None:
        right_penalty_arc = coordinates.right_penalty_arc()
        assert scale_100(right_penalty_arc["x0"]) == scale_100(60 - 12 - 10)

    def test_right_penalty_area(self, coordinates: PitchCoordinates) -> None:
        right_penalty_area = coordinates.right_penalty_area()
        assert scale_100(right_penalty_area["x1"]) == scale_100(60 - 18)
        assert scale_100(
            right_penalty_area["x0"] - right_penalty_area["x1"]
        ) == scale_100(18)
        assert scale_100(
            abs(right_penalty_area["y1"] - right_penalty_area["y0"])
        ) == scale_100((18 * 2 + 8))

    def test_right_penalty_mark(self, coordinates: PitchCoordinates) -> None:
        right_penalty_mark = coordinates.right_penalty_mark()
        assert scale_100(right_penalty_mark["x0"]) == scale_100(60 - 12 - 0.2)
        assert scale_100(right_penalty_mark["y0"]) == scale_100(40 + 0.2)

    def test_right_goal_area(self, coordinates: PitchCoordinates) -> None:
        right_goal_area = coordinates.right_goal_area()
        assert scale_100(right_goal_area["x1"]) == scale_100(60 - 6)
        assert scale_100(right_goal_area["x0"] - right_goal_area["x1"]) == scale_100(6)
        assert scale_100(
            abs(right_goal_area["y1"] - right_goal_area["y0"])
        ) == scale_100(8 + 6 * 2)

    def test_right_goal(self, coordinates: PitchCoordinates) -> None:
        right_goal = coordinates.right_goal()
        assert scale_100(right_goal["x1"]) == scale_100(60 + 2.67)


class TestVerticalCoordinates:
    @pytest.fixture(scope="class")
    def coordinates(self) -> PitchCoordinates:
        return PitchCoordinates(
            vertical=True,
        )

    def test_initialization(self, coordinates: PitchCoordinates) -> None:
        assert int(coordinates.length) == 68
        assert int(coordinates.width) == 105
        assert int(coordinates.xaxis_scale) == 1
        assert int(coordinates.yaxis_scale) == 1
        assert int(coordinates.markings.penalty_mark_distance) == 11

    def test_pitch_area(self, coordinates: PitchCoordinates) -> None:
        pitch_area = coordinates.pitch_area()
        assert int(pitch_area["x0"]) == 0
        assert int(pitch_area["x1"] - pitch_area["x0"]) == 68
        assert int(pitch_area["y1"] - pitch_area["y0"]) == 105

    def test_centre_circle(self, coordinates: PitchCoordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert scale_100(centre_circle["x0"]) == scale_100((34 - 9.15))
        assert scale_100(abs(centre_circle["x1"] - centre_circle["x0"])) == scale_100(
            9.15 * 2
        )

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
        assert scale_100(left_goal_area["x1"] - left_goal_area["x0"]) == scale_100(
            7.32 + 5.5 * 2
        )
        assert scale_100(left_goal_area["y1"] - left_goal_area["y0"]) == scale_100(5.5)

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
