import plotly.graph_objects as go

from ._models import Colors, PitchCoordinates


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

    def add_point(
        self,
        x: float,
        y: float,
        text: str,
        color: str = Colors.red,
    ) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=10, color=color),
                text=text,
                textposition="top center",
            )
        )

    def add_line(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        color: str = Colors.green,
    ) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[start_x, end_x],
                y=[start_y, end_y],
                mode="lines",
                line=dict(color=color, width=2),
            )
        )

    def _calc_axis_range(self, axis_range: tuple[float, float]) -> tuple[float, float]:
        a, b = axis_range
        if a < b:
            return (a - 5, b + 5)
        return (a + 5, b - 5)

    def show(self) -> None:
        fig_width = 800
        fig_height = 600
        if self.coordinates.vertical:
            fig_width, fig_height = fig_height, fig_width

        self.fig.update_layout(
            width=fig_width,
            height=fig_height,
            title=f"{self.coordinates.length}m * {self.coordinates.width}m",
            xaxis=dict(
                range=self._calc_axis_range(self.coordinates.xaxis_range),
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                range=self._calc_axis_range(self.coordinates.yaxis_range),
                showgrid=False,
                zeroline=False,
                scaleanchor="x",
                scaleratio=1,
            ),
        )
        self.fig.show()
