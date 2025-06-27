import plotly.graph_objects as go

from ._models import Colors, PitchCoordinates


class Pitch:
    def __init__(
        self,
        coordinates: PitchCoordinates | None = None,
    ) -> None:
        self.coordinates = (
            coordinates if coordinates is not None else PitchCoordinates()
        )
        self.fig = go.Figure()
        self._draw_pitch()

    def _draw_background(self) -> None:
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.pitch_area(),
            line_color=Colors.dark_gray,
            fillcolor=Colors.light_gray,
        )

    def _draw_centre(self) -> None:
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

    def _draw_left_side(self) -> None:
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

    def _draw_right_side(self) -> None:
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

    def _draw_pitch(self) -> None:
        self._draw_background()
        if self.coordinates.side in ("left", "both"):
            self._draw_left_side()
        if self.coordinates.side in ("right", "both"):
            self._draw_right_side()
        if self.coordinates.side == "both":
            self._draw_centre()

    def add_point(
        self,
        *,
        x: float,
        y: float,
        size: int = 20,
        text: str | None = None,
        shirt_number: int | None = None,
        color: str = Colors.red,
        opacity: float = 1.0,
    ) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker={'size': size, 'color': color},
                text=text if text is not None else "",
                textposition='top center',
                textfont={'color': Colors.black},
                opacity=opacity,
            )
        )
        if shirt_number is not None:
            self.fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="text",
                    text=str(shirt_number),
                    textposition="middle center",
                    textfont={'color': Colors.white},
                    showlegend=False,
                )
            )

    def add_line(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        color: str = Colors.green,
        width: float = 2,
        opacity: float = 1.0,
    ) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[start_x, end_x],
                y=[start_y, end_y],
                mode="lines",
                line=dict(color=color, width=width),
                opacity=opacity,
            )
        )

    def add_annotation(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        color: str = Colors.green,
        width: float = 2,
        opacity: float = 1.0,
    ) -> None:
        self.fig.add_annotation(
            ax=start_x,
            ay=start_y,
            x=end_x,
            y=end_y,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=width,
            arrowcolor=color,
            opacity=opacity,
        )

    def add_triangle(
        self,
        a_x: float,
        a_y: float,
        b_x: float,
        b_y: float,
        c_x: float,
        c_y: float,
        color: str = Colors.red,
        opacity: float = 1,
    ) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=[a_x, b_x, c_x, a_x],
                y=[a_y, b_y, c_y, a_y],
                mode="lines",
                fill="toself",
                fillcolor=color,
                line=dict(color=color, width=2),
                opacity=opacity,
            )
        )

    def _calc_axis_range(self, axis_range: tuple[float, float]) -> tuple[float, float]:
        a, b = axis_range
        if a < b:
            return (a - 5, b + 5)
        return (a + 5, b - 5)

    def show(self) -> None:
        fig_width = 1024
        fig_height = 768
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
