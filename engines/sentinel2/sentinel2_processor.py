from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import rasterio


# ============================================================
# GEOSHIELD SENTINEL-2 PROCESSOR
# ============================================================
#
# Current capability:
#   Sentinel-2 L2A SAFE
#        ?
#   B04 (Red) + B08 (NIR)
#        ?
#   NDVI
#        ?
#   GeoTIFF
#
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SENTINEL2_ROOT = PROJECT_ROOT / "data" / "sentinel2"
EXTRACTED_ROOT = SENTINEL2_ROOT / "extracted"
OUTPUT_ROOT = SENTINEL2_ROOT / "processed"

NDVI_OUTPUT = OUTPUT_ROOT / "ndvi.tif"


# ============================================================
# FIND SAFE PRODUCT
# ============================================================

def find_safe_product() -> Path:
    """Find the first Sentinel-2 SAFE product in the extracted directory."""

    if not EXTRACTED_ROOT.exists():
        raise FileNotFoundError(
            f"Sentinel-2 extraction directory does not exist: "
            f"{EXTRACTED_ROOT}"
        )

    safe_products = sorted(EXTRACTED_ROOT.glob("*.SAFE"))

    if not safe_products:
        raise FileNotFoundError(
            f"No Sentinel-2 .SAFE product found in: "
            f"{EXTRACTED_ROOT}"
        )

    return safe_products[0]


# ============================================================
# FIND BAND
# ============================================================

def find_band(safe_product: Path, band: str) -> Path:
    """Find a specific Sentinel-2 JP2 band."""

    matches = list(
        safe_product.rglob(f"*_{band}_10m.jp2")
    )

    if not matches:
        raise FileNotFoundError(
            f"Could not find {band} 10 m band in {safe_product}"
        )

    return matches[0]


# ============================================================
# READ RASTER
# ============================================================

def read_band(path: Path):
    """Read a single raster band."""

    with rasterio.open(path) as src:

        data = src.read(1).astype(np.float32)

        profile = src.profile.copy()

        transform = src.transform

        crs = src.crs

        nodata = src.nodata

    return data, profile, transform, crs, nodata


# ============================================================
# CALCULATE NDVI
# ============================================================

def calculate_ndvi(
    red: np.ndarray,
    nir: np.ndarray,
) -> np.ndarray:
    """Calculate NDVI from Sentinel-2 B04 and B08."""

    denominator = nir + red

    ndvi = np.full(
        red.shape,
        np.nan,
        dtype=np.float32,
    )

    valid = denominator != 0

    ndvi[valid] = (
        (nir[valid] - red[valid])
        / denominator[valid]
    )

    return ndvi


# ============================================================
# SAVE NDVI
# ============================================================

def save_ndvi(
    ndvi: np.ndarray,
    profile: dict,
    output_path: Path,
) -> None:
    """Save NDVI as a GeoTIFF."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_profile = profile.copy()

    output_profile.update(
        driver="GTiff",
        dtype="float32",
        count=1,
        compress="deflate",
        nodata=-9999.0,
    )

    output = np.where(
        np.isfinite(ndvi),
        ndvi,
        -9999.0,
    ).astype(np.float32)

    with rasterio.open(
        output_path,
        "w",
        **output_profile,
    ) as dst:

        dst.write(
            output,
            1,
        )


# ============================================================
# STATISTICS
# ============================================================

def print_statistics(ndvi: np.ndarray) -> None:
    """Print useful NDVI statistics."""

    valid = ndvi[np.isfinite(ndvi)]

    if valid.size == 0:
        print("No valid NDVI pixels found.")
        return

    print()
    print("===== NDVI STATISTICS =====")

    print(
        "Valid pixels:",
        f"{valid.size:,}",
    )

    print(
        "Minimum:",
        f"{float(np.min(valid)):.4f}",
    )

    print(
        "Maximum:",
        f"{float(np.max(valid)):.4f}",
    )

    print(
        "Mean:",
        f"{float(np.mean(valid)):.4f}",
    )

    print(
        "Median:",
        f"{float(np.median(valid)):.4f}",
    )

    print(
        "============================"
    )


# ============================================================
# MAIN PROCESSING PIPELINE
# ============================================================

def process_sentinel2() -> Path:

    print()
    print("===== GEOSHIELD SENTINEL-2 PROCESSOR =====")

    # --------------------------------------------------------
    # Locate SAFE product
    # --------------------------------------------------------

    safe_product = find_safe_product()

    print()
    print("SAFE product:")
    print(safe_product)

    # --------------------------------------------------------
    # Locate B04 and B08
    # --------------------------------------------------------

    red_path = find_band(
        safe_product,
        "B04",
    )

    nir_path = find_band(
        safe_product,
        "B08",
    )

    print()
    print("Red band (B04):")
    print(red_path)

    print()
    print("NIR band (B08):")
    print(nir_path)

    # --------------------------------------------------------
    # Read bands
    # --------------------------------------------------------

    print()
    print("Reading B04...")

    red, red_profile, red_transform, red_crs, _ = read_band(
        red_path
    )

    print(
        "B04 shape:",
        red.shape,
    )

    print()
    print("Reading B08...")

    nir, nir_profile, nir_transform, nir_crs, _ = read_band(
        nir_path
    )

    print(
        "B08 shape:",
        nir.shape,
    )

    # --------------------------------------------------------
    # Validate geometry
    # --------------------------------------------------------

    if red.shape != nir.shape:
        raise ValueError(
            f"B04 and B08 dimensions do not match: "
            f"{red.shape} vs {nir.shape}"
        )

    if red_transform != nir_transform:
        raise ValueError(
            "B04 and B08 have different geotransforms."
        )

    if red_crs != nir_crs:
        raise ValueError(
            "B04 and B08 have different coordinate reference systems."
        )

    # --------------------------------------------------------
    # Sentinel-2 reflectance scaling
    # --------------------------------------------------------
    #
    # Sentinel-2 L2A image values are normally scaled
    # integers. Dividing both bands by the same scale factor
    # does not change the NDVI ratio.
    #
    # Therefore the NDVI calculation can safely use the
    # original values directly.
    #
    # --------------------------------------------------------

    print()
    print("Calculating NDVI...")

    ndvi = calculate_ndvi(
        red,
        nir,
    )

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    print()
    print("Saving NDVI GeoTIFF...")

    save_ndvi(
        ndvi,
        red_profile,
        NDVI_OUTPUT,
    )

    print(
        "NDVI output:",
        NDVI_OUTPUT,
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print_statistics(ndvi)

    print()
    print("GeoShield Sentinel-2 processing: HEALTHY")
    print("==========================================")

    return NDVI_OUTPUT


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        output = process_sentinel2()

        print()
        print("PROCESSING COMPLETE.")
        print("Output file:", output)

    except Exception as exc:

        print()
        print("===== SENTINEL-2 PROCESSING FAILED =====")
        print("Error type:", type(exc).__name__)
        print("Error:", str(exc))
        print("========================================")

        raise
