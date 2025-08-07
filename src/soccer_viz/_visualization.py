from typing import Any, Literal

import plotly.graph_objects as go

from ._models import Coordinates, PitchCoordinates, PitchMarkings


class Theme:
    transparent = "rgba(0, 0, 0, 0)"

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
        *,
        length_range: tuple[float, float] | None = None,
        width_range: tuple[float, float] | None = None,
        markings: PitchMarkings | None = None,
        vertical: bool = False,
        side: Literal["left", "right", "both"] = "both",
        theme: Theme | None = None,
    ) -> None:
        self._vertical = vertical
        self._side = side

        self._markings = markings if markings is not None else PitchMarkings()
        self._pitch_coordinates = PitchCoordinates(
            markings=self._markings, vertical=vertical, side=side
        )
        self._overlay_coordinates = Coordinates(
            length_range=length_range,
            width_range=width_range,
            markings=self._markings,
            vertical=vertical,
            side=side,
        )
        self.theme = theme if theme is not None else DefaultTheme()
        self.fig = go.Figure()
        self._draw_pitch()

    @property
    def xaxis_range(self) -> tuple[float, float]:
        return self._overlay_coordinates.xaxis_range

    @property
    def yaxis_range(self) -> tuple[float, float]:
        return self._overlay_coordinates.yaxis_range

    def _draw_background(self) -> None:
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.pitch_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )

    def _draw_centre(self) -> None:
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self._pitch_coordinates.centre_circle(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self._pitch_coordinates.centre_mark(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="line",
            layer="below",
            **self._pitch_coordinates.halfway_line(),
            line_color=self.theme.border,
            xref="x",
            yref="y",
        )

    def _draw_left_side(self) -> None:
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self._pitch_coordinates.left_penalty_arc(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.left_penalty_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self._pitch_coordinates.left_penalty_mark(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.left_goal_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.left_goal(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )

    def _draw_right_side(self) -> None:
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self._pitch_coordinates.right_penalty_arc(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.right_penalty_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="circle",
            layer="below",
            **self._pitch_coordinates.right_penalty_mark(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.right_goal_area(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )
        self.fig.add_shape(
            type="rect",
            layer="below",
            **self._pitch_coordinates.right_goal(),
            line_color=self.theme.border,
            fillcolor=self.theme.background,
            xref="x",
            yref="y",
        )

    def _draw_pitch(self) -> None:
        self._draw_background()
        if self._side in ("left", "both"):
            self._draw_left_side()
        if self._side in ("right", "both"):
            self._draw_right_side()
        if self._side == "both":
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
                xaxis="x2",
                yaxis="y2",
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
                    xaxis="x2",
                    yaxis="y2",
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
                    xaxis="x2",
                    yaxis="y2",
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
                    xaxis="x2",
                    yaxis="y2",
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
                xaxis="x2",
                yaxis="y2",
            )
        )

    def _extend_axis_range(
        self, axis_range: tuple[float, float]
    ) -> tuple[float, float]:
        value = abs(axis_range[1] - axis_range[0]) * 0.05
        a, b = axis_range
        if a < b:
            return (a - value, b + value)
        return (a + value, b - value)

    def _calc_fig_size(
        self,
        length: int | float | None,
        width: int | float | None,
    ) -> tuple[int | float, int | float]:
        if length is None:
            if self._side != "both":
                length = 768
            else:
                length = 1024
        if width is None:
            if self._side != "both":
                width = length
            else:
                width = (
                    length * self._pitch_coordinates.aspect_ratio
                    + length * 0.07
                )
        if self._pitch_coordinates.vertical:
            length, width = width, length
        return length, width

    def show(
        self,
        fig_length: int | float | None = None,
        fig_width: int | float | None = None,
    ) -> None:
        fig_length, fig_width = self._calc_fig_size(fig_length, fig_width)

        axis: dict[str, Any] = dict(
            xaxis=dict(
                range=self._extend_axis_range(
                    self._pitch_coordinates.xaxis_range
                ),
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=self._extend_axis_range(
                    self._pitch_coordinates.yaxis_range
                ),
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            xaxis2=dict(
                range=self._extend_axis_range(
                    self._overlay_coordinates.xaxis_range
                ),
                showgrid=False,
                zeroline=False,
                overlaying="x",
            ),
            yaxis2=dict(
                range=self._extend_axis_range(
                    self._overlay_coordinates.yaxis_range
                ),
                showgrid=False,
                zeroline=False,
                overlaying="y",
            ),
        )
        if self._vertical:
            axis["xaxis"]["scaleanchor"] = "y"
            axis["xaxis"]["scaleratio"] = 1
            axis["xaxis2"]["scaleanchor"] = "y2"
            axis["xaxis2"]["scaleratio"] = (
                self._pitch_coordinates.aspect_ratio
                / self._overlay_coordinates.aspect_ratio
            )
        else:
            axis["yaxis"]["scaleanchor"] = "x"
            axis["yaxis"]["scaleratio"] = 1
            axis["yaxis2"]["scaleanchor"] = "x2"
            axis["yaxis2"]["scaleratio"] = (
                self._pitch_coordinates.aspect_ratio
                / self._overlay_coordinates.aspect_ratio
            )

        self.fig.update_layout(
            **axis,
            paper_bgcolor=self.theme.background,
            width=fig_length,
            height=fig_width,
        )

        self.fig.show()
