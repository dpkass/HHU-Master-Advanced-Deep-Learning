import numpy as np


def _linear_progress(t, T, progression_range=(0, 1)):
    start_at, max_at = progression_range

    assert 0 <= start_at <= max_at <= 1, 'progression_range must be [0 <= start <= end <= 1]'

    step_offset = T * start_at
    effective_num_steps = 1 if start_at == max_at else T * (max_at - start_at)
    effective_step = np.clip(t - step_offset, 0, effective_num_steps)
    return effective_step / effective_num_steps


def polynomial_progress(t, T, exponent, value_range=(0, 1), progression_range=(0, 1)):
    min_val, max_val = value_range
    val_span = max_val - min_val
    scale = _linear_progress(t, T, progression_range)
    return scale ** exponent * val_span + min_val


def polynomial_decay_progress(t, T, exponent, value_range=(0, 1), progression_range=(0, 1)):
    min_val, max_val = value_range
    val_span = max_val - min_val
    scale = _linear_progress(t, T, progression_range)
    return (1 - scale) ** exponent * val_span + min_val


def linear_progress(t, T, value_range=(0, 1), progression_range=(0, 1)):
    return polynomial_progress(t, T, 1, value_range, progression_range)


def linear_decay_progress(t, T, value_range=(0, 1), progression_range=(0, 1)):
    return polynomial_decay_progress(t, T, 1, value_range, progression_range)


def squared_progress(t, T, value_range=(0, 1), progression_range=(0, 1)):
    return polynomial_progress(t, T, 2, value_range, progression_range)


def squared_decay_progress(t, T, value_range=(0, 1), progression_range=(0, 1)):
    return polynomial_decay_progress(t, T, 2, value_range, progression_range)
