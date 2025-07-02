from typing import Literal

import plotly.graph_objects as go

from ._models import PitchCoordinates


class Theme:
    @property
    def background(self) -> str:
        raise NotImplementedError

    @property
    def text(self) -> str:
        raise NotImplementedError

    @property
    def border(self) -> str:
        raise NotImplementedError

    @property
    def line(self) -> str:
        raise NotImplementedError

    @property
    def home_team(self) -> str:
        raise NotImplementedError

    @property
    def away_team(self) -> str:
        raise NotImplementedError

    @property
    def number(self) -> str:
        raise NotImplementedError


class DefaultTheme(Theme):
    """https://getbootstrap.com/docs/5.3/customize/color/"""

    white = "#ffffff"
    black = "#000000"
    gray_100 = "#f8f9fa"
    gray_300 = "#dee2e6"
    gray_500 = "#adb5bd"
    gray_900 = "#212529"
    red_500 = "#dc3545"
    blue_500 = "#0d6efd"
    green_500 = "#198754"
    transparent = "rgba(0, 0, 0, 0)"

    def __init__(self, name: Literal["light", "dark"] = "light") -> None:
        self.name = name

    @property
    def background(self) -> str:
        return self.gray_100 if self.name == "light" else self.gray_900

    @property
    def text(self) -> str:
        return self.black if self.name == "light" else self.white

    @property
    def border(self) -> str:
        return self.gray_300

    @property
    def line(self) -> str:
        return self.gray_500

    @property
    def home_team(self) -> str:
        return self.red_500

    @property
    def away_team(self) -> str:
        return self.blue_500

    @property
    def number(self) -> str:
        return self.white


class Pitch:
    def __init__(
        self,
        coordinates: PitchCoordinates | None = None,
        theme: Theme | None = None,
    ) -> None:
        self.coordinates = (
            coordinates if coordinates is not None else PitchCoordinates()
        )
        self.theme = theme if theme is not None else DefaultTheme()
        self.fig = go.Figure()
        self._draw_pitch()

    def _draw_background(self) -> None:
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.pitch_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )

    def _draw_centre(self) -> None:
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.centre_circle(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.centre_mark(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="line",
            layer="below",
            **self.coordinates.halfway_line(),
            line_color=self.theme.border,
        )

    def _draw_left_side(self) -> None:
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.left_penalty_arc(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.left_penalty_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.left_penalty_mark(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.left_goal_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.left_goal(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )

    def _draw_right_side(self) -> None:
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.right_penalty_arc(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.right_penalty_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self.coordinates.right_penalty_mark(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.right_goal_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self.coordinates.right_goal(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
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
        x: float,
        y: float,
        *,
        size: int = 20,
        text: str | None = None,
        number: int | None = None,
        color: str | None = None,
        opacity: float = 1.0,
        symbol: Literal["circle", "square", "triangle-up"] = "circle",
    ) -> None:
        if color is None:
            color = self.theme.home_team
        self.fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker={"size": size, "color": color, "symbol": symbol},
                text=text if text is not None else "",
                textposition="top center",
                textfont={"color": self.theme.text},
                opacity=opacity,
            )
        )
        if number is not None:
            self.fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="text",
                    text=str(number),
                    textposition="middle center",
                    textfont={"color": self.theme.number},
                    showlegend=False,
                )
            )

    def add_line(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        *,
        color: str | None = None,
        width: float = 2,
        opacity: float = 1.0,
        dash: Literal["solid", "dot", "dash", "longdash", "dashdot"] = "solid",
        gradient: bool = False,
    ) -> None:
        if color is None:
            color = self.theme.line
        if not gradient:
            self.fig.add_trace(
                go.Scatter(
                    x=[start_x, end_x],
                    y=[start_y, end_y],
                    mode="lines",
                    line=dict(color=color, width=width, dash=dash),
                    opacity=opacity,
                )
            )
        else:
            self.add_gradient_line(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                color=color,
                width_start=width / 4,
                width_end=width,
                opacity_start=opacity * 0.1,
                opacity_end=opacity,
            )

    def add_gradient_line(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        *,
        color: str | None = None,
        width_start: float = 1,
        width_end: float = 4,
        opacity_start: float = 0.1,
        opacity_end: float = 1.0,
        steps: int = 20,
    ) -> None:
        if color is None:
            color = self.theme.line

        for i in range(steps):
            t0 = i / steps
            t1 = (i + 1) / steps
            x0 = start_x + (end_x - start_x) * t0
            y0 = start_y + (end_y - start_y) * t0
            x1 = start_x + (end_x - start_x) * t1
            y1 = start_y + (end_y - start_y) * t1
            width = width_start + (width_end - width_start) * t0
            opacity = opacity_start + (opacity_end - opacity_start) * t0
            self.fig.add_trace(
                go.Scatter(
                    x=[x0, x1],
                    y=[y0, y1],
                    mode="lines",
                    line=dict(color=color, width=width),
                    opacity=opacity,
                    showlegend=False,
                )
            )

    def add_annotation(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        *,
        color: str | None = None,
        width: float = 2,
        opacity: float = 1.0,
    ) -> None:
        if color is None:
            color = self.theme.line

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
        *,
        color: str | None = None,
        opacity: float = 1,
    ) -> None:
        if color is None:
            color = self.theme.line
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

    def _calc_axis_range(
        self, axis_range: tuple[float, float]
    ) -> tuple[float, float]:
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
