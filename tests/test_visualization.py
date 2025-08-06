import pytest

from soccer_viz import Pitch


class TestPitch:
    @pytest.fixture(scope="class")
    def pitch(self) -> Pitch:
        return Pitch()
    
    def test_properties(self, pitch: Pitch) -> None:
        assert pitch.xaxis_range == (0, 105)
        assert pitch.yaxis_range == (0, 68)

    def test_add_point(self, pitch: Pitch) -> None:
        pitch.add_point(
            x=10,
            y=20,
            size=15,
            number=20,
            text="A",
            color="#123456",
            symbol="square",
            opacity=0.5,
        )
        trace = pitch.fig.data[0]
        assert trace.x == (10,)
        assert trace.y == (20,)
        assert trace.marker.size == 15
        assert trace.marker.color == "#123456"
        assert trace.marker.symbol == "square"
        assert trace.text == "A"
        assert trace.textposition == "top center"
        assert trace.opacity == 0.5

        number_trace = pitch.fig.data[-1]
        assert number_trace.text == "20"
        assert number_trace.textposition == "middle center"

    def test_add_line(self, pitch: Pitch) -> None:
        pitch.add_line(
            start_x=10,
            start_y=20,
            end_x=30,
            end_y=40,
            color="#654321",
            width=5,
            opacity=0.8,
        )
        trace = pitch.fig.data[-1]
        assert trace.x == (10, 30)
        assert trace.y == (20, 40)
        assert trace.line.color == "#654321"
        assert trace.line.width == 5
        assert trace.opacity == 0.8

    def test_add_gradient_line(self, pitch: Pitch) -> None:
        pitch.add_gradient_line(
            start_x=10,
            start_y=20,
            end_x=30,
            end_y=40,
            color="#abcdef",
        )
        trace = pitch.fig.data[-1]
        assert trace.line.color == "#abcdef"
        assert trace.line.width != 4
        assert trace.opacity != 1

    def test_add_annotation(self, pitch: Pitch) -> None:
        pitch.add_annotation(
            start_x=15,
            start_y=25,
            end_x=35,
            end_y=45,
            color="#ff0000",
            width=2,
            opacity=0.6,
        )
