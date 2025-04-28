import numpy as np
from orbiter.core.states import StateRV

def test_roundtrip():
    r = np.array([7000e3, 0, 0])
    v = np.array([0, 7.546e3, 1.0])
    coe = StateRV(r, v).as_coe()
    r2, v2 = coe.as_rv()
    assert np.allclose(r, r2, atol=1e-6)
    assert np.allclose(v, v2, atol=1e-6)
