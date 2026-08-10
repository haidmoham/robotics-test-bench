"""Canonical rolling MuJoCo telemetry stacks for test-bench viewers."""

from collections import deque

import mujoco
import numpy as np


PLOT_INTERVAL = 0.02
PLOT_HISTORY_SECONDS = 6.0

# C-1N's readable simulation palette. Experiments may choose different signal
# meanings, but use these named defaults before inventing a new visual system.
PAPER = np.array([0.91, 0.925, 0.945])
INK = np.array([0.01, 0.01, 0.015])
SIGNAL_BLUE = np.array([0.184, 0.412, 0.678])
MUTED_SLATE = np.array([0.302, 0.408, 0.518])
WARM_RED = np.array([0.71, 0.263, 0.247])
WARM_ORANGE = np.array([0.95, 0.55, 0.10])
SIGNAL_GREEN = np.array([0.25, 0.80, 0.40])
OVERLAY_ALPHA = 0.72


def make_figure(title, series):
    """Create one graph using C-1N's readable viewer styling."""
    figure = mujoco.MjvFigure()
    figure.title = title
    figure.xlabel = ""
    figure.flg_extend = 0
    figure.flg_legend = 1
    figure.flg_ticklabel[:] = 1
    figure.linewidth = 2.0
    figure.figurergba = np.array([0.05, 0.05, 0.05, 0.32])
    figure.panergba = np.array([0.12, 0.12, 0.12, 0.48])
    figure.gridrgb = MUTED_SLATE
    for index, (name, color) in enumerate(series):
        figure.linename[index] = name
        figure.linergb[index] = np.array(color)
    return figure


def rolling_samples():
    """Return the standard bounded history buffer for viewer telemetry."""
    return deque(maxlen=round(PLOT_HISTORY_SECONDS / PLOT_INTERVAL))


def update_figure(figure, samples, value_index, value_range=None):
    """Draw one vector-valued telemetry field from rolling samples."""
    if not samples:
        return
    times = np.array([sample[0] for sample in samples])
    values = np.array([sample[value_index] for sample in samples])
    figure.linepnt[:] = 0
    for index in range(values.shape[1]):
        figure.linepnt[index] = len(times)
        figure.linedata[index, : 2 * len(times)] = np.column_stack(
            (times, values[:, index])
        ).reshape(-1)

    figure.range[0] = (times[0], max(times[-1], times[0] + PLOT_INTERVAL))
    if value_range is None:
        lower = float(np.min(values))
        upper = float(np.max(values))
        padding = max((upper - lower) * 0.12, 0.01)
        figure.range[1] = (lower - padding, upper + padding)
    else:
        figure.range[1] = value_range


def update_stacks(
    viewer,
    left_figures,
    right_figures,
    samples,
    left_fields,
    right_fields,
    left_ranges=None,
    right_ranges=None,
):
    """Place up to two three-panel stacks in the viewer, following C-1N's layout."""
    left_ranges = left_ranges or (None,) * len(left_figures)
    right_ranges = right_ranges or (None,) * len(right_figures)
    for figure, field, value_range in zip(left_figures, left_fields, left_ranges):
        update_figure(figure, samples, field, value_range)
    for figure, field, value_range in zip(right_figures, right_fields, right_ranges):
        update_figure(figure, samples, field, value_range)

    viewport = viewer.viewport
    margin = max(6, min(12, viewport.width // 100))
    gap = max(4, min(8, viewport.height // 120))
    preferred_width = int(viewport.width * 0.32)
    non_overlapping_width = (viewport.width - 3 * margin) // 2
    width = max(180, min(480, preferred_width, non_overlapping_width))
    available_height = viewport.height - 2 * margin - 2 * gap
    height = max(100, min(260, available_height // 3))
    top = viewport.bottom + viewport.height

    def stack_viewports(left):
        return [
            mujoco.MjrRect(
                left,
                top - margin - height * (index + 1) - gap * index,
                width,
                height,
            )
            for index in range(3)
        ]

    left_viewports = stack_viewports(viewport.left + margin)
    right_viewports = stack_viewports(viewport.left + viewport.width - width - margin)
    viewer.set_figures(
        list(zip(left_viewports, left_figures)) + list(zip(right_viewports, right_figures))
    )
