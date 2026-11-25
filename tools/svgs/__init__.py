"""Sanitizer-proof semantic SVG generators for EP knowledge cards."""

from .anatomy_intervals import BUILDERS as ANATOMY_INTERVALS_BUILDERS
from .mechanisms_svt import BUILDERS as MECHANISMS_SVT_BUILDERS
from .wpw_pacing import BUILDERS as WPW_PACING_BUILDERS
from .vt_ablation import BUILDERS as VT_ABLATION_BUILDERS

ALL_BUILDERS = {
    **ANATOMY_INTERVALS_BUILDERS,
    **MECHANISMS_SVT_BUILDERS,
    **WPW_PACING_BUILDERS,
    **VT_ABLATION_BUILDERS,
}

__all__ = ["ALL_BUILDERS"]
