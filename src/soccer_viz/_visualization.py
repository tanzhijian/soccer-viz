import plotly.graph_objects as go

from ._models import Colors, Coordinates, Point


class Pitch:
    def __init__(
        self,
        length: float = 105,
        width: float = 68,
    ) -> None:
        self.fig = go.Figure()
        self.coordinates = Coordinates(length, width)
        self._draw_pitch()

    def _draw_pitch(self) -> None:
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.pitch_area(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.centre_circle(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.centre_mark(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="line",
            layer="below",
            **self.coordinates.halfway_line(),
            line_color=Colors.dark_gray,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.left_penalty_arc(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.left_penalty_area(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.left_penalty_mark(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.left_goal_area(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.left_goal(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.right_penalty_arc(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.right_penalty_area(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.right_penalty_mark(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.right_goal_area(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.right_goal(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )

    def add_point(self, point: Point, text: str, color: str = Colors.red) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[point["x"]],
                y=[point["y"]],
                mode="markers+text",
                marker=dict(size=10, color=color),
                text=text,
                textposition="top center",
            )
        )

    def add_line(self, start: Point, end: Point, color: str = Colors.green) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[start["x"], end["x"]],
                y=[start["y"], end["y"]],
                mode="lines",
                line=dict(color=color, width=2),
            )
        )

    def show(self) -> None:
        self.fig.update_layout(
            width=800,
            height=600,
            title=f"{self.coordinates.length}m * {self.coordinates.width}m",
            xaxis=dict(
                range=[-5, self.coordinates.length + 5],
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                range=[-5, self.coordinates.width + 5],
                showgrid=False,
                zeroline=False,
                scaleanchor="x",
                scaleratio=1,
            ),
        )
        self.fig.show()
