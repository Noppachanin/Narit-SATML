import numpy as np
from astropy.modeling import models, fitting


from photutils.centroids import centroid_com

# ===================== 1. ฟังก์ชันคำนวณ FWHM จาก radial profile ===================== #

def compute_radial_fwhm(data, position, box_size=50):
    x0, y0 = position
    half_size = box_size // 2
    x0, y0 = int(x0), int(y0)

    subimg = data[y0 - half_size:y0 + half_size, x0 - half_size:x0 + half_size]

    # หา centroid ใหม่ภายใน subimage
    centroid = centroid_com(subimg)
    cy, cx = centroid
    cy += y0 - half_size
    cx += x0 - half_size

    # สร้าง radial distance map
    y_indices, x_indices = np.indices(data.shape)
    r = np.sqrt((x_indices - cx)**2 + (y_indices - cy)**2)
    r = r.astype(int)

    # จำกัดเฉพาะ pixel รอบดาวเท่านั้น
    mask = r < 10
    r = r[mask]
    flux = data[mask]

    # สร้าง radial profile
    r_max = r.max()
    radial_profile = np.zeros(r_max + 1)
    for i in range(r_max + 1):
        radial_profile[i] = flux[r == i].mean() if np.any(r == i) else 0

    # ฟิต Gaussian
    radii = np.arange(len(radial_profile))
    g_init = models.Gaussian1D(amplitude=radial_profile.max(), mean=3, stddev=2)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, radii, radial_profile)

    fwhm = 2.355 * g.stddev.value
    return fwhm, (cx, cy), radial_profile

# ===================== 1. ฟังก์ชันคำนวณ FWHM จาก radial profile ===================== #
