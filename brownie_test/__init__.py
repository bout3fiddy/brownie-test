#!/usr/bin/python3
"""
Test utils borrowed from Brownie.
"""


import warnings

import hypothesis
from hypothesis.errors import HypothesisDeprecationWarning

from .strategies import strategy  # NOQA: F401

# hypothesis warns against combining function-scoped fixtures with @given
# but in brownie this is a documented and useful behaviour
warnings.filterwarnings("ignore", category=HypothesisDeprecationWarning)


class BoaTestWarning(Warning):
    pass


def given(*given_args, **given_kwargs):
    """Wrapper around hypothesis.given, a decorator for turning a test function
    that accepts arguments into a randomized test.

    This is the main entry point to Hypothesis when using Boa.
    """

    def outer_wrapper(test):

        # hypothesis.given must wrap the target test to correctly
        # impersonate the call signature for pytest
        hy_given = _hypothesis_given(*given_args, **given_kwargs)
        hy_wrapped = hy_given(test)

        if hasattr(hy_wrapped, "hypothesis"):
            hy_wrapped.hypothesis.inner_test = test

        # NOTE: unlike brownie's test utils, there's no inner wrapper. so,
        # first figure out if that's gonna bork something!
        return hy_wrapped

    return outer_wrapper


def _given_warning_wrapper(*args, **kwargs):
    warnings.warn(
        "Directly importing `hypothesis.given` may result in improper isolation"
        " between test runs. You should import `boa.test.given` instead.",
        BoaTestWarning,
    )
    return _hypothesis_given(*args, **kwargs)


def _apply_given_wrapper():
    hypothesis.given = _given_warning_wrapper


_hypothesis_given = hypothesis.given
