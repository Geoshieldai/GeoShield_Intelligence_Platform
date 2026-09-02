"""
Tests for the GeoShield core kernel.
"""

from pathlib import Path

from core.kernel import GeoShieldKernel


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIRE_DATASET = PROJECT_ROOT / "data" / "fires" / "kenya_fires.csv"


def test_kernel_can_be_created() -> None:
    """The GeoShield kernel should initialize successfully."""

    kernel = GeoShieldKernel()

    assert kernel is not None
    assert kernel.fire_engine is not None


def test_kernel_has_fire_pipeline() -> None:
    """The kernel should expose the fire pipeline."""

    kernel = GeoShieldKernel()

    assert callable(kernel.run_fire_pipeline)


def test_fire_dataset_exists() -> None:
    """The fire dataset required by the kernel test should exist."""

    assert FIRE_DATASET.exists(), (
        f"Required fire dataset not found: {FIRE_DATASET}"
    )


def test_kernel_fire_pipeline() -> None:
    """The kernel should process the Kenya fire dataset."""

    kernel = GeoShieldKernel()

    results = kernel.run_fire_pipeline(str(FIRE_DATASET))

    assert isinstance(results, list)