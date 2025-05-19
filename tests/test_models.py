import pytest

from soccer_viz._models import Coordinates


class TestStandardCoordinates:
    @pytest.fixture(scope="class")
    def coordinates(self) -> Coordinates:
        return Coordinates(
            length=105,
            width=68,
        )

    def test_initialization(self, coordinates: Coordinates) -> None:
        assert coordinates.length == 105
        assert coordinates.width == 68
        assert coordinates.xaxis_scale == 1.0
        assert coordinates.yaxis_scale == 1.0
        assert coordinates.center_circle_radius == 9.15
        assert coordinates.penalty_area_length == 16.5
        assert coordinates.penalty_mark_distance == 11
        assert coordinates.goal_area_length == 5.5
        assert coordinates.corner_arc_radius == 1
        assert coordinates.goal_width == 7.32
        assert coordinates.goal_height == 2.44

    def test_pitch_area(self, coordinates: Coordinates) -> None:
        pitch_area = coordinates.pitch_area()
        assert pitch_area["x0"] == 0
        assert pitch_area["y0"] == 0
        assert int(pitch_area["x1"]) == 105
        assert int(pitch_area["y1"]) == 68

    def test_centre_circle(self, coordinates: Coordinates) -> None:
        centre_circle = coordinates.centre_circle()
        assert int(centre_circle["x0"] * 100) == 4335
        assert int(centre_circle["y0"] * 100) == 2485
        assert int(centre_circle["x1"] * 100) == 6165
        assert int(centre_circle["y1"] * 100) == 4315

    def test_centre_mark(self, coordinates: Coordinates) -> None:
        centre_mark = coordinates.centre_mark()
        assert int(centre_mark["x0"] * 100) == 5230
        assert int(centre_mark["y0"] * 100) == 3379
        assert int(centre_mark["x1"] * 100) == 5270
        assert int(centre_mark["y1"] * 100) == 3420

    def test_halfway_line(self, coordinates: Coordinates) -> None:
        halfway_line = coordinates.halfway_line()
        assert int(halfway_line["x0"] * 100) == 5250
        assert int(halfway_line["y0"] * 100) == 0
        assert int(halfway_line["x1"] * 100) == 5250
        assert int(halfway_line["y1"] * 100) == 6800

    def test_left_penalty_arc(self, coordinates: Coordinates) -> None:
        left_penalty_arc = coordinates.left_penalty_arc()
        assert int(left_penalty_arc["x0"] * 100) == 184
        assert int(left_penalty_arc["y0"] * 100) == 2485
        assert int(left_penalty_arc["x1"] * 100) == 2014
        assert int(left_penalty_arc["y1"] * 100) == 4315

    def test_left_penalty_area(self, coordinates: Coordinates) -> None:
        left_penalty_area = coordinates.left_penalty_area()
        assert int(left_penalty_area["x0"] * 100) == 0
        assert int(left_penalty_area["y0"] * 100) == 1384
        assert int(left_penalty_area["x1"] * 100) == 1650
        assert int(left_penalty_area["y1"] * 100) == 5416

    def test_left_penalty_mark(self, coordinates: Coordinates) -> None:
        left_penalty_mark = coordinates.left_penalty_mark()
        assert int(left_penalty_mark["x0"] * 100) == 1080
        assert int(left_penalty_mark["y0"] * 100) == 3379
        assert int(left_penalty_mark["x1"] * 100) == 1120
        assert int(left_penalty_mark["y1"] * 100) == 3420

    def test_left_goal_area(self, coordinates: Coordinates) -> None:
        left_goal_area = coordinates.left_goal_area()
        assert int(left_goal_area["x0"] * 100) == 0
        assert int(left_goal_area["y0"] * 100) == 2484
        assert int(left_goal_area["x1"] * 100) == 550
        assert int(left_goal_area["y1"] * 100) == 4316

    def test_left_goal(self, coordinates: Coordinates) -> None:
        left_goal = coordinates.left_goal()
        assert int(left_goal["x0"] * 100) == -244
        assert int(left_goal["y0"] * 100) == 3034
        assert int(left_goal["x1"] * 100) == 0
        assert int(left_goal["y1"] * 100) == 3765

    def test_right_penalty_arc(self, coordinates: Coordinates) -> None:
        right_penalty_arc = coordinates.right_penalty_arc()
        assert int(right_penalty_arc["x0"] * 100) == 8485
        assert int(right_penalty_arc["y0"] * 100) == 2485
        assert int(right_penalty_arc["x1"] * 100) == 10315
        assert int(right_penalty_arc["y1"] * 100) == 4315

    def test_right_penalty_area(self, coordinates: Coordinates) -> None:
        right_penalty_area = coordinates.right_penalty_area()
        assert int(right_penalty_area["x0"] * 100) == 10500
        assert int(right_penalty_area["y0"] * 100) == 1384
        assert int(right_penalty_area["x1"] * 100) == 8850
        assert int(right_penalty_area["y1"] * 100) == 5416

    def test_right_penalty_mark(self, coordinates: Coordinates) -> None:
        right_penalty_mark = coordinates.right_penalty_mark()
        assert int(right_penalty_mark["x0"] * 100) == 9380
        assert int(right_penalty_mark["y0"] * 100) == 3379
        assert int(right_penalty_mark["x1"] * 100) == 9420
        assert int(right_penalty_mark["y1"] * 100) == 3420

    def test_right_goal_area(self, coordinates: Coordinates) -> None:
        right_goal_area = coordinates.right_goal_area()
        assert int(right_goal_area["x0"] * 100) == 10500
        assert int(right_goal_area["y0"] * 100) == 2484
        assert int(right_goal_area["x1"] * 100) == 9950
        assert int(right_goal_area["y1"] * 100) == 4316

    def test_right_goal(self, coordinates: Coordinates) -> None:
        right_goal = coordinates.right_goal()
        assert int(right_goal["x0"] * 100) == 10500
        assert int(right_goal["y0"] * 100) == 3034
        assert int(right_goal["x1"] * 100) == 10744
        assert int(right_goal["y1"] * 100) == 3765
