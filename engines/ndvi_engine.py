from pathlib import Path

import numpy as np
import rasterio


def calculate_ndvi(red_path, nir_path, output_path):
    print("===== GEOSHIELD NDVI ENGINE =====")

    print("Red:", red_path)
    print("NIR:", nir_path)

    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype("float32")
        profile = red_src.profile.copy()
        red_nodata = red_src.nodata

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype("float32")
        nir_nodata = nir_src.nodata

    print("Red shape:", red.shape)
    print("NIR shape:", nir.shape)
    print("CRS:", profile["crs"])

    if red.shape != nir.shape:
        raise ValueError("B04 and B08 dimensions do not match.")

    # Sentinel-2 L2A reflectance scaling.
    # Both bands use the same scale factor, so it cancels
    # mathematically in the NDVI ratio.
    red = red * 0.0001
    nir = nir * 0.0001

    valid = np.isfinite(red) & np.isfinite(nir)

    if red_nodata is not None:
        valid &= red != red_nodata

    if nir_nodata is not None:
        valid &= nir != nir_nodata

    denominator = nir + red

    valid &= denominator != 0

    ndvi = np.full(red.shape, np.nan, dtype="float32")

    ndvi[valid] = (
        (nir[valid] - red[valid])
        / denominator[valid]
    )

    # Remove physically impossible values caused by invalid pixels.
    ndvi[(ndvi < -1) | (ndvi > 1)] = np.nan

    profile.update(
        driver="GTiff",
        dtype="float32",
        count=1,
        nodata=-9999.0,
        compress="deflate",
        predictor=3,
        tiled=True,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = np.where(
        np.isfinite(ndvi),
        ndvi,
        -9999.0
    ).astype("float32")

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(output, 1)

    valid_ndvi = ndvi[np.isfinite(ndvi)]

    print()
    print("===== NDVI COMPLETE =====")
    print("Output:", output_path)
    print("Pixels:", ndvi.size)
    print("Valid pixels:", valid_ndvi.size)

    if valid_ndvi.size:
        print("Minimum:", float(valid_ndvi.min()))
        print("Maximum:", float(valid_ndvi.max()))
        print("Mean:", float(valid_ndvi.mean()))
        print("Median:", float(np.median(valid_ndvi)))

    print("GeoTIFF written successfully.")


if __name__ == "__main__":

    root = Path("data/sentinel2")

    red_files = list(root.rglob("*_B04_10m.jp2"))
    nir_files = list(root.rglob("*_B08_10m.jp2"))

    if not red_files:
        raise FileNotFoundError("B04 Red band not found.")

    if not nir_files:
        raise FileNotFoundError("B08 NIR band not found.")

    if len(red_files) > 1:
        raise RuntimeError(f"Multiple B04 files found: {red_files}")

    if len(nir_files) > 1:
        raise RuntimeError(f"Multiple B08 files found: {nir_files}")

    calculate_ndvi(
        red_files[0],
        nir_files[0],
        "data/ndvi/sentinel2_ndvi.tif",
    )