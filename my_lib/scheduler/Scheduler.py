from typing import Union

from functools import partial

import my_lib.functional as F

SchedulerType = Union[
    'linear', 'linear-decay',
    'square', 'square-decay',
    'polynomial', 'polynomial-decay'
]


class Scheduler:
    def __init__(self, num_steps, value_range=(0, 1), progression_range=(0, 1), *,
          type: SchedulerType = 'linear', exponent=None):
        """Initialize a Scheduler object that generates progress values based on various functions.

        Args:
            num_steps: Total number of steps in the progression.
            value_range: Tuple of (min, max) values defining the output range that progress values
                          will be mapped to.
            progression_range: Tuple of (start, end) values between [0,1] defining the range of progress values.
                     Default is (0,1) for full range progression.
            type: Type of progression function to use. Options are:
                'linear': Linear progression (default)
                'linear-decay': Linear decay
                'squared': Squared progression
                'squared-decay': Squared decay
                'polynomial': Polynomial progression
                'polynomial-decay': Polynomial decay
            exponent: Exponent value for polynomial progression types (required when type is 'polynomial' or 'polynomial-decay')

        The scheduler can be used by either:
        - Calling the instance directly to get the current step value and using step() method to increment progress
        - Iterating over all values using for loop
        - Accessing specific step value using index
        """
        type_map = {
            'linear': F.linear_progress,
            'linear-decay': F.linear_decay_progress,
            'squared': F.squared_progress,
            'squared-decay': F.squared_decay_progress,
            'polynomial': partial(F.polynomial_progress, exponent=exponent),
            'polynomial-decay': partial(F.polynomial_decay_progress, exponent=exponent),
        }

        assert type is None or type in type_map
        assert 0 <= progression_range[0] <= progression_range[1] <= 1, 'range must be [0 <= start <= end <= 1]'

        self.num_steps = num_steps - 1
        self.value_range = value_range
        self.progression_range = progression_range
        self.exponent = exponent

        self.reset()

        if type:
            self._func = type_map[type]
            self.func = partial(self._func, T=self.num_steps, value_range=value_range, progression_range=progression_range)

    def __call__(self):
        return self.func(self._step)

    def __iter__(self):
        for i in range(self.num_steps + 1):
            yield self.func(i)

    def __getitem__(self, idx):
        return self.func(idx)

    def step(self):
        self._step += 1

    def reset(self):
        self._step = 0
