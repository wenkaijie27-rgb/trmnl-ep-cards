"""Sanitizer-proof semantic SVG generators for EP knowledge cards."""

from .anatomy_intervals import BUILDERS as ANATOMY_INTERVALS_BUILDERS
from .mechanisms_svt import BUILDERS as MECHANISMS_SVT_BUILDERS
from .wpw_pacing import BUILDERS as WPW_PACING_BUILDERS
from .vt_ablation import BUILDERS as VT_ABLATION_BUILDERS
from .adv_anatomy_intervals import BUILDERS as ADV_ANATOMY_INTERVALS_BUILDERS
from .adv_mechanisms_svt import BUILDERS as ADV_MECHANISMS_SVT_BUILDERS
from .adv_wpw_pacing import BUILDERS as ADV_WPW_PACING_BUILDERS
from .adv_vt_ablation import BUILDERS as ADV_VT_ABLATION_BUILDERS

ALL_BUILDERS = {
    **ANATOMY_INTERVALS_BUILDERS,
    **MECHANISMS_SVT_BUILDERS,
    **WPW_PACING_BUILDERS,
    **VT_ABLATION_BUILDERS,
    **ADV_ANATOMY_INTERVALS_BUILDERS,
    **ADV_MECHANISMS_SVT_BUILDERS,
    **ADV_WPW_PACING_BUILDERS,
    **ADV_VT_ABLATION_BUILDERS,
}

__all__ = ["ALL_BUILDERS"]
