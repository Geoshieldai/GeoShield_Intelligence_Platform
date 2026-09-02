import os
import glob
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

# ============================================================
# GEOSHIELD SENTINEL-2 TRUE NDVI PROCESSOR
# B04 = Red
# B08 = Near Infrared
# SCL = Scene Classification Layer
# ============================================================

SAFE_ROOT = r"data/sentinel2/S2A_MSIL2A_20260812T074031_N0512_R092_T37MBU_20260812T125812.SAFE"
OUTPUT_DIR = r"data/ndvi"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def find_band(pattern):
    matches = glob.glob(
        os.path.join(SAFE_ROOT, "**", pattern),
        recursive=True
    )

    if not matches:
        raise FileNotFoundError(
            f"Could not find Sentinel-2 asset: {pattern}"
        )

    return matches[0]


def read_band(path):
    with rasterio.open(path) as src:
        data = src.read(1).astype(np.float32)
        profile = src.profile.copy()
        transform = src.transform
        crs = src.crs
        nodata = src.nodata

    return data, profile, transform, crs, nodata


def resample_to_reference(
    source_path,
    reference_profile,
    reference_transform,
    reference_crs,
):
    with rasterio.open(source_path) as src:
        destination = np.zeros(
            (
                reference_profile["height"],
                reference_profile["width"],
            ),
            dtype=np.uint8,
        )

        reproject(
            source=src.read(1),
            destination=destination,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=reference_transform,
            dst_crs=reference_crs,
            resampling=Resampling.nearest,
        )

    return destination


print("===== GEOSHIELD SENTINEL-2 TRUE NDVI PROCESSOR =====")

b04_path = find_band("*B04_10m.jp2")
b08_path = find_band("*B08_10m.jp2")
scl_path = find_band("*SCL_20m.jp2")

print()
print("B04:", b04_path)
print("B08:", b08_path)
print("SCL:", scl_path)

red, profile, transform, crs, _ = read_band(b04_path)
nir, _, _, _, _ = read_band(b08_path)

if red.shape != nir.shape:
    raise RuntimeError(
        f"B04/B08 dimensions differ: {red.shape} vs {nir.shape}"
    )

print()
print("B04 shape:", red.shape)
print("B08 shape:", nir.shape)
print("CRS:", crs)
print("Resolution:", profile["transform"].a, profile["transform"].e)

# ------------------------------------------------------------
# Sentinel-2 SCL classes that are considered invalid
#
# 0  No data
# 1  Saturated / defective
# 3  Cloud shadow
# 8  Cloud medium probability
# 9  Cloud high probability
# 10 Thin cirrus
# 11 Snow / ice
# ------------------------------------------------------------

scl = resample_to_reference(
    scl_path,
    profile,
    transform,
    crs,
)

invalid_classes = {
    0,
    1,
    3,
    8,
    9,
    10,
    11,
}

quality_mask = np.ones(scl.shape, dtype=bool)

for class_value in invalid_classes:
    quality_mask &= scl != class_value

# ------------------------------------------------------------
# Sentinel-2 L2A reflectance scaling
# ------------------------------------------------------------

red = red / 10000.0
nir = nir / 10000.0

denominator = nir + red

valid = (
    quality_mask
    & np.isfinite(red)
    & np.isfinite(nir)
    & (denominator != 0)
)

ndvi = np.full(
    red.shape,
    np.nan,
    dtype=np.float32,
)

ndvi[valid] = (
    (nir[valid] - red[valid])
    / denominator[valid]
)

# Physically useful NDVI range
ndvi[
    (ndvi < -1.0)
    | (ndvi > 1.0)
] = np.nan

output_path = os.path.join(
    OUTPUT_DIR,
    "sentinel2_20260812_T37MBU_ndvi.tif"
)

profile.update(
    driver="GTiff",
    dtype="float32",
    count=1,
    compress="deflate",
    predictor=3,
    nodata=np.nan,
)

with rasterio.open(output_path, "w", **profile) as dst:
    dst.write(ndvi, 1)

valid_pixels = np.isfinite(ndvi)

print()
print("===== NDVI SUMMARY =====")
print("Valid pixels:", int(valid_pixels.sum()))

if valid_pixels.any():
    print(
        "Mean NDVI:",
        float(np.nanmean(ndvi))
    )
    print(
        "Minimum NDVI:",
        float(np.nanmin(ndvi))
    )
    print(
        "Maximum NDVI:",
        float(np.nanmax(ndvi))
    )

print()
print("Output:", output_path)
print()
print("SENTINEL-2 TRUE NDVI PROCESSOR COMPLETE")
