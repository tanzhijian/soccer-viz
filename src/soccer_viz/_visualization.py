import plotly.graph_objects as go

from ._models import Colors, PitchCoordinates, Point


class Pitch:
    def __init__(
        self,
        coordinates: PitchCoordinates | None = None,
    ) -> None:
        self.fig = go.Figure()
        self.coordinates = (
            coordinates if coordinates is not None else PitchCoordinates()
        )
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
        fig_width = 800
        fig_height = 600
        if self.coordinates.vertical:
            fig_width, fig_height = fig_height, fig_width

        xaxis_start, xaxis_end = -5.0, self.coordinates.length + 5.0
        if self.coordinates.invert_xaxis:
            xaxis_start, xaxis_end = xaxis_end, xaxis_start
        yaxis_start, yaxis_end = -5.0, self.coordinates.width + 5.0
        if self.coordinates.invert_yaxis:
            yaxis_start, yaxis_end = yaxis_end, yaxis_start

        self.fig.update_layout(
            width=fig_width,
            height=fig_height,
            title=f"{self.coordinates.length}m * {self.coordinates.width}m",
            xaxis=dict(
                range=[xaxis_start, xaxis_end],
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                range=[yaxis_start, yaxis_end],
                showgrid=False,
                zeroline=False,
                scaleanchor="x",
                scaleratio=1,
            ),
        )
        self.fig.show()
