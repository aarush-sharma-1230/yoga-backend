"""
Combined and shuffled posture catalogue.

Imports all postures from category-specific modules and exports a single
ALL_POSTURES list in randomized order (no particular category ordering).
"""

import random

from app.posture_docs.inversion_postures import INVERSION_POSTURES
from app.posture_docs.prone_postures import PRONE_POSTURES
from app.posture_docs.seated_postures import SEATED_POSTURES
from app.posture_docs.standing_postures import STANDING_POSTURES
from app.posture_docs.supine_postures import SUPINE_POSTURES

_all = (
    STANDING_POSTURES
    + SEATED_POSTURES
    + SUPINE_POSTURES
    + PRONE_POSTURES
    + INVERSION_POSTURES
)
random.shuffle(_all)

ALL_POSTURES = _all
