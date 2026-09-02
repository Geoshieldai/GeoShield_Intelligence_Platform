import os
import glob
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

# ============================================================
# GEOSHIELD SENTINEL-2 QUALITY MASK ENGINE
# ============================================================

SAFE_ROOT = r"data/sentinel2/S2A_MSIL2A_20260812T074031_N0512_R092_T37MBU_20260812T125812.SAFE"
OUTPUT_DIR = r"data/ndvi"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def find_asset(pattern):
    matches = glob.glob(
        os.path.join(SAFE_ROOT, "**", pattern),
        recursive=True,
    )

    if not matches:
        raise FileNotFoundError(
            f"Asset not found: {pattern}"
        )

    return matches[0]


b04_path = find_asset("*B04_10m.jp2")
scl_path = find_asset("*SCL_20m.jp2")

print("===== GEOSHIELD SENTINEL-2 QUALITY MASK =====")
print()
print("Reference B04:", b04_path)
print("SCL:", scl_path)

with rasterio.open(b04_path) as reference:
    profile = reference.profile.copy()
    transform = reference.transform
    crs = reference.crs
    width = reference.width
    height = reference.height

mask = np.zeros(
    (height, width),
    dtype=np.uint8,
)

with rasterio.open(scl_path) as scl:
    reproject(
        source=scl.read(1),
        destination=mask,
        src_transform=scl.transform,
        src_crs=scl.crs,
        dst_transform=transform,
        dst_crs=crs,
        resampling=Resampling.nearest,
    )

# Valid SCL classes:
#
# 2  Dark area / shadows
# 4  Vegetation
# 5  Bare soil
# 6  Water
# 7  Unclassified
#
# We deliberately reject:
# 0  No data
# 1  Saturated / defective
# 3  Cloud shadow
# 8  Cloud medium probability
# 9  Cloud high probability
# 10 Thin cirrus
# 11 Snow / ice

invalid = np.isin(
    mask,
    [0, 1, 3, 8, 9, 10, 11],
)

quality = np.where(
    invalid,
    0,
    1,
).astype(np.uint8)

output = os.path.join(
    OUTPUT_DIR,
    "sentinel2_20260812_T37MBU_quality_mask.tif",
)

profile.update(
    driver="GTiff",
    dtype="uint8",
    count=1,
    compress="deflate",
    nodata=0,
)

with rasterio.open(output, "w", **profile) as dst:
    dst.write(quality, 1)

valid_pixels = int((quality == 1).sum())
invalid_pixels = int((quality == 0).sum())

print()
print("===== QUALITY SUMMARY =====")
print("Valid pixels:", valid_pixels)
print("Invalid pixels:", invalid_pixels)

total = valid_pixels + invalid_pixels

if total:
    print(
        "Valid percentage:",
        round(valid_pixels / total * 100, 2),
        "%"
    )

print()
print("Output:", output)
print()
print("SENTINEL-2 QUALITY MASK COMPLETE")
