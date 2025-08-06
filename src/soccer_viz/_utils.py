def calc_half_axix_range(
    axis_range: tuple[float, float], side: str
) -> tuple[float, float]:
    if side == "left":
        return (
            axis_range[0],
            axis_range[0] + (axis_range[1] - axis_range[0]) / 2,
        )
    if side == "right":
        return (
            axis_range[0] + (axis_range[1] - axis_range[0]) / 2,
            axis_range[1],
        )
    raise ValueError(f"Invalid side: {side}. Expected 'left' or 'right'.")