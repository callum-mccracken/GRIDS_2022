from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

fit_points = [
    # (delay in nanoseconds, counts per sec)
    (188, 2.333333333),
    (261, 1.633333333),
    (319, 1.257142857),
    (314, 1.419047619),
    (309, 1.352380952),
    (573, 1.008333333),
    (705, 0.9833333333),
    (441, 1.108333333),
    (393, 1.1),
    #(132, 4.15),
    (261, 2.133333333),
    (324, 1.666666667),
    (324, 1.6),
]
delays, counts = map(np.array, list(zip(*fit_points)))

plt.scatter(delays, counts)

def fit_func(t, a, b, lam):
    return a+b*np.exp(-t*lam)

fit_params, *_ = curve_fit(fit_func, delays, counts, p0=(1, 4, 2e-3))
a, b, lam = fit_params

print(f"fit: a + be^(-t * lam), {a = }, {b = }, {lam = }")

half_life = np.log(2)/lam

print(f"{half_life = } ns")



x = np.arange(min(delays), max(delays), 1)
y = fit_func(x, *fit_params)
plt.plot(x, y)

plt.savefig("BiPo.png")


