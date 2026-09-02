"""
GeoShield AI Enterprise
Temporary Master Roadmap Generator

Purpose:
    Generate ROADMAP.md from repository state.

Rules:
    [x] = milestone completed
    [ ] = milestone incomplete

The roadmap is intentionally temporary.
When GeoShield AI reaches production completion, use:

    python tools/generate_roadmap.py --delete-roadmap

to permanently remove ROADMAP.md from the repository.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "ROADMAP.md"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def has_tracked(path: str) -> bool:
    try:
        tracked = git("ls-files", path)
        return bool(tracked)
    except subprocess.CalledProcessError:
        return False


def has_commit_message(text: str) -> bool:
    try:
        log = git("log", "--oneline", "--all", "--grep", text)
        return bool(log)
    except subprocess.CalledProcessError:
        return False


def test_suite_exists() -> bool:
    return exists("tests") and has_tracked("tests")


def determine_status() -> dict[str, bool]:
    return {
        # ==========================================================
        # FOUNDATION
        # ==========================================================

        "foundation_repo": True,
        "foundation_git": True,
        "foundation_application": exists("core/application.py"),
        "foundation_configuration": exists("core/config.py"),
        "foundation_service_registry": exists("core/service_registry.py"),
        "foundation_engine_registry": exists("core/engine_registry.py"),
        "foundation_logging": exists("core/logger.py"),
        "foundation_environment": exists("core/environment.py"),

        # ==========================================================
        # GEOSPATIAL CORE
        # ==========================================================

        "geo_data_models": exists("core/data/dataset.py"),
        "geo_raster_models": exists("core/data/raster_dataset.py"),
        "geo_ingestion": exists("core/data/ingestion.py"),
        "geo_validation": exists("core/data/validator.py"),
        "geo_spatial_engine": exists("core/spatial_engine.py")
        or exists("engines/environment/environment_engine.py"),
        "geo_image_processing": exists("core/image_processing/processing_pipeline.py"),

        # ==========================================================
        # SPECTRAL INTELLIGENCE
        # ==========================================================

        "spectral_ndvi": exists("core/indices/ndvi.py"),
        "spectral_ndwi": exists("core/indices/ndwi.py"),
        "spectral_ndbi": exists("core/indices/ndbi.py"),
        "spectral_ndmi": exists("core/indices/ndmi.py"),
        "spectral_nbr": exists("core/indices/nbr.py"),
        "spectral_evi": exists("core/indices/evi.py"),
        "spectral_savi": exists("core/indices/savi.py"),
        "spectral_engine": exists("core/indices/spectral_engine.py"),
        "spectral_reporting": exists("core/indices/spectral_report.py"),

        # ==========================================================
        # HAZARD INTELLIGENCE
        # ==========================================================

        "hazard_classifier": exists("core/hazards/classifier.py"),
        "hazard_detector": exists("core/hazards/detector.py"),
        "hazard_engine": exists("core/hazards/hazard_engine.py"),
        "hazard_risk": exists("core/hazards/risk.py"),
        "hazard_severity": exists("core/hazards/severity.py"),
        "hazard_response": exists("core/hazards/hazard_response.py"),
        "multi_hazard": exists("core/hazards/multi_hazard.py"),

        # ==========================================================
        # SATELLITE ARCHITECTURE
        # ==========================================================

        "satellite_manager": exists("backend/satellite/manager.py"),
        "satellite_provider_architecture": exists(
            "backend/satellite/providers/base.py"
        ),
        "sentinel_provider": exists(
            "backend/satellite/providers/sentinel_provider.py"
        ),
        "landsat_provider": exists(
            "backend/satellite/providers/landsat_provider.py"
        ),
        "planet_provider": exists(
            "backend/satellite/providers/planet_provider.py"
        ),
        "sentinel2_engine": exists("engines/sentinel2"),
        "sentinel2_connector": exists(
            "core/connectors/sentinel2/sentinel2_connector.py"
        ),

        # ==========================================================
        # COPERNICUS
        # ==========================================================

        "copernicus_auth": exists("core/auth/copernicus.py"),
        "copernicus_client": exists("core/data/copernicus_client.py"),
        "copernicus_catalogue": exists(
            "core/connectors/sentinel2/sentinel2_catalog.py"
        ),
        "copernicus_search": exists(
            "core/connectors/sentinel2/sentinel2_search.py"
        ),
        "copernicus_downloader": exists(
            "core/connectors/sentinel2/sentinel2_downloader.py"
        ),

        # ==========================================================
        # PLANET
        # ==========================================================

        "planet_auth": exists("core/auth/planet.py"),
        "planet_search": exists("backend/satellite/planet_search.py"),
        "planet_assets": exists("backend/satellite/planet_assets.py"),
        "planet_download": exists("backend/satellite/planet_download.py"),
        "planet_service": exists("backend/satellite/planet_service.py"),

        # ==========================================================
        # DISASTER INTELLIGENCE
        # ==========================================================

        "fire_engine": exists("backend/disaster/fire_engine.py"),
        "disaster_engine": exists("backend/disaster/disaster_engine.py"),
        "firms_connector": exists("backend/connectors/firms_connector.py"),
        "wildfire_service": exists("backend/services/wildfire.py"),
        "fire_monitor": exists("backend/services/fire_monitor.py"),

        # ==========================================================
        # API / SERVICES
        # ==========================================================

        "api_satellite": exists("backend/api/satellite.py"),
        "health_api": exists("backend/routes/health.py"),
        "alerts_api": exists("backend/routes/alerts.py"),
        "county_api": exists("backend/routes/county.py"),
        "dashboard_api": exists("backend/routes/dashboard.py"),
        "resource_api": exists("backend/routes/resources.py"),

        # ==========================================================
        # INTELLIGENCE ENGINES
        # ==========================================================

        "risk_engine": exists("core/risk_engine.py"),
        "decision_engine": exists("core/decision_engine.py"),
        "workflow_engine": exists("core/workflow_engine.py"),
        "alert_engine": exists("engines/alerts/alert_engine.py"),
        "risk_intelligence": exists(
            "engines/risk_intelligence_engine.py"
        ),
        "impact_risk": exists("engines/impact_risk_engine.py"),
        "hotspot_intelligence": exists(
            "engines/hotspot_intelligence_engine.py"
        ),

        # ==========================================================
        # AGRICULTURE
        # ==========================================================

        "agriculture_engine": exists(
            "backend/satellite/ai/agriculture.py"
        ),
        "cropstress": exists(
            "backend/satellite/sentinel2/cropstress.py"
        ),
        "vegetation_engine": exists(
            "backend/satellite/sentinel2/vegetation.py"
        ),
        "drought_engine": exists("backend/satellite/ai/drought.py"),

        # ==========================================================
        # DATA
        # ==========================================================

        "kenya_boundaries": exists("data/boundaries"),
        "kenya_roads": exists("data/roads"),
        "fire_data": exists("data/fires/kenya_fires.csv"),
        "ndvi_outputs": exists("data/ndvi"),

        # ==========================================================
        # TESTING
        # ==========================================================

        "tests_directory": test_suite_exists(),
        "auth_tests": exists("tests/auth/test_copernicus_auth.py"),
        "core_tests": exists("tests/core"),
        "satellite_tests": exists("tests/satellites"),
        "integration_tests": exists("tests/integration"),

        # ==========================================================
        # PRODUCTION HARDENING
        # ==========================================================

        "production_config": False,
        "production_database": False,
        "production_auth": False,
        "production_observability": False,
        "production_security_audit": False,
        "production_load_testing": False,
        "production_failure_recovery": False,
        "production_ci_cd": False,
        "production_containerization": False,
        "production_deployment": False,

        # ==========================================================
        # AI / AUTONOMOUS INTELLIGENCE
        # ==========================================================

        "ai_reasoning_layer": False,
        "ai_event_correlation": False,
        "ai_prediction_layer": False,
        "ai_cross_domain_fusion": False,
        "ai_recommendation_engine": False,
        "ai_autonomous_alert_prioritization": False,

        # ==========================================================
        # GLOBAL SCALE
        # ==========================================================

        "global_country_support": False,
        "global_multi_region_processing": False,
        "global_scalable_data_pipeline": False,
        "global_tenant_architecture": False,

        # ==========================================================
        # FINAL PRODUCT
        # ==========================================================

        "enterprise_dashboard": False,
        "user_management": False,
        "organization_management": False,
        "audit_logging": False,
        "production_documentation": False,
        "api_documentation": False,
        "security_documentation": False,
        "deployment_documentation": False,
        "production_release": False,
    }


MILESTONES = [
    (
        "M01",
        "Repository & Engineering Foundation",
        [
            ("foundation_repo", "Professional repository structure"),
            ("foundation_git", "Git/GitHub workflow"),
            ("foundation_application", "Application factory"),
            ("foundation_configuration", "Central configuration"),
            ("foundation_service_registry", "Service registry"),
            ("foundation_engine_registry", "Engine registry"),
            ("foundation_logging", "Central logging"),
            ("foundation_environment", "Environment management"),
        ],
    ),
    (
        "M02",
        "Geospatial Data Core",
        [
            ("geo_data_models", "Data models"),
            ("geo_raster_models", "Raster data model"),
            ("geo_ingestion", "Data ingestion architecture"),
            ("geo_validation", "Data validation"),
            ("geo_image_processing", "Image processing pipeline"),
        ],
    ),
    (
        "M03",
        "Spectral Intelligence",
        [
            ("spectral_ndvi", "NDVI"),
            ("spectral_ndwi", "NDWI"),
            ("spectral_ndbi", "NDBI"),
            ("spectral_ndmi", "NDMI"),
            ("spectral_nbr", "NBR"),
            ("spectral_evi", "EVI"),
            ("spectral_savi", "SAVI"),
            ("spectral_engine", "Spectral engine"),
            ("spectral_reporting", "Spectral reporting"),
        ],
    ),
    (
        "M04",
        "Hazard & Risk Intelligence",
        [
            ("hazard_classifier", "Hazard classifier"),
            ("hazard_detector", "Hazard detector"),
            ("hazard_engine", "Hazard engine"),
            ("hazard_risk", "Risk scoring"),
            ("hazard_severity", "Severity model"),
            ("hazard_response", "Response intelligence"),
            ("multi_hazard", "Multi-hazard intelligence"),
        ],
    ),
    (
        "M05",
        "Satellite Acquisition Architecture",
        [
            ("satellite_manager", "Satellite manager"),
            ("satellite_provider_architecture", "Provider abstraction"),
            ("sentinel_provider", "Sentinel provider"),
            ("landsat_provider", "Landsat provider"),
            ("planet_provider", "Planet provider"),
            ("sentinel2_engine", "Sentinel-2 engine"),
            ("sentinel2_connector", "Sentinel-2 connector"),
        ],
    ),
    (
        "M06",
        "Copernicus / Sentinel-2 Live Pipeline",
        [
            ("copernicus_auth", "Copernicus authentication"),
            ("copernicus_client", "Copernicus client"),
            ("copernicus_catalogue", "Catalogue integration"),
            ("copernicus_search", "Sentinel-2 search"),
            ("copernicus_downloader", "Sentinel-2 downloader"),
        ],
    ),
    (
        "M07",
        "Planet Integration",
        [
            ("planet_auth", "Planet authentication architecture"),
            ("planet_search", "Planet scene search"),
            ("planet_assets", "Planet asset architecture"),
            ("planet_download", "Planet download architecture"),
            ("planet_service", "Planet service layer"),
        ],
    ),
    (
        "M08",
        "Disaster Intelligence",
        [
            ("fire_engine", "Fire engine"),
            ("disaster_engine", "Disaster engine"),
            ("firms_connector", "NASA FIRMS connector"),
            ("wildfire_service", "Wildfire service"),
            ("fire_monitor", "Fire monitoring"),
        ],
    ),
    (
        "M09",
        "API & Service Layer",
        [
            ("api_satellite", "Satellite API"),
            ("health_api", "Health API"),
            ("alerts_api", "Alerts API"),
            ("county_api", "County API"),
            ("dashboard_api", "Dashboard API"),
            ("resource_api", "Resource API"),
        ],
    ),
    (
        "M10",
        "Decision & Risk Intelligence",
        [
            ("risk_engine", "Risk engine"),
            ("decision_engine", "Decision engine"),
            ("workflow_engine", "Workflow engine"),
            ("alert_engine", "Alert engine"),
            ("risk_intelligence", "Risk intelligence engine"),
            ("impact_risk", "Impact/risk engine"),
            ("hotspot_intelligence", "Hotspot intelligence"),
        ],
    ),
    (
        "M11",
        "Agricultural Intelligence",
        [
            ("agriculture_engine", "Agriculture intelligence"),
            ("cropstress", "Crop stress analysis"),
            ("vegetation_engine", "Vegetation intelligence"),
            ("drought_engine", "Drought intelligence"),
        ],
    ),
    (
        "M12",
        "Operational Data Layer",
        [
            ("kenya_boundaries", "Kenya administrative boundaries"),
            ("kenya_roads", "Road network"),
            ("fire_data", "Fire datasets"),
            ("ndvi_outputs", "NDVI/intelligence outputs"),
        ],
    ),
    (
        "M13",
        "Automated Testing",
        [
            ("tests_directory", "Test architecture"),
            ("auth_tests", "Authentication tests"),
            ("core_tests", "Core unit tests"),
            ("satellite_tests", "Satellite tests"),
            ("integration_tests", "Integration tests"),
        ],
    ),
    (
        "M14",
        "Production Hardening",
        [
            ("production_config", "Production configuration"),
            ("production_database", "Production database"),
            ("production_auth", "Production authentication"),
            ("production_observability", "Observability"),
            ("production_security_audit", "Security audit"),
            ("production_load_testing", "Load testing"),
            ("production_failure_recovery", "Failure recovery"),
            ("production_ci_cd", "CI/CD"),
            ("production_containerization", "Containerization"),
            ("production_deployment", "Production deployment"),
        ],
    ),
    (
        "M15",
        "AI Intelligence Layer",
        [
            ("ai_reasoning_layer", "AI reasoning"),
            ("ai_event_correlation", "Cross-event correlation"),
            ("ai_prediction_layer", "Prediction"),
            ("ai_cross_domain_fusion", "Cross-domain fusion"),
            ("ai_recommendation_engine", "Recommendations"),
            ("ai_autonomous_alert_prioritization", "Autonomous alert prioritization"),
        ],
    ),
    (
        "M16",
        "Global Scale",
        [
            ("global_country_support", "Multi-country support"),
            ("global_multi_region_processing", "Multi-region processing"),
            ("global_scalable_data_pipeline", "Scalable data pipeline"),
            ("global_tenant_architecture", "Multi-tenant architecture"),
        ],
    ),
    (
        "M17",
        "Enterprise Product",
        [
            ("enterprise_dashboard", "Enterprise dashboard"),
            ("user_management", "User management"),
            ("organization_management", "Organization management"),
            ("audit_logging", "Audit logging"),
            ("production_documentation", "Production documentation"),
            ("api_documentation", "API documentation"),
            ("security_documentation", "Security documentation"),
            ("deployment_documentation", "Deployment documentation"),
            ("production_release", "GeoShield AI production release"),
        ],
    ),
]


def render(status: dict[str, bool]) -> str:
    lines = []

    lines.append("# GeoShield AI Enterprise — Master Roadmap")
    lines.append("")
    lines.append("> **Temporary project-control document.**")
    lines.append(">")
    lines.append("> This roadmap exists only during GeoShield AI development.")
    lines.append("> Completed milestones are marked automatically from repository evidence.")
    lines.append("> When the final production milestone is complete, this roadmap is permanently deleted.")
    lines.append("")
    lines.append("## Status Legend")
    lines.append("")
    lines.append("- 🟩 `[x]` Completed")
    lines.append("- ⬜ `[ ]` Not completed")
    lines.append("")
    lines.append("## Current Reality")
    lines.append("")
    lines.append(
        "Planet acquisition is currently treated as an implemented integration "
        "architecture, not an active production data dependency, because the "
        "Planet service entitlement has expired."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    completed = 0
    total = 0

    for milestone_id, title, tasks in MILESTONES:
        milestone_done = all(status[key] for key, _ in tasks)

        lines.append(
            f"## {milestone_id} — "
            f"{'🟩' if milestone_done else '⬜'} {title}"
        )
        lines.append("")

        for key, description in tasks:
            done = status[key]
            total += 1

            if done:
                completed += 1

            mark = "x" if done else " "
            icon = "🟩" if done else "⬜"

            lines.append(
                f"- [{mark}] {icon} {description}"
            )

        lines.append("")

    percentage = (completed / total * 100) if total else 0

    lines.append("---")
    lines.append("")
    lines.append("## Overall Progress")
    lines.append("")
    lines.append(
        f"**{completed}/{total} tracked objectives completed "
        f"({percentage:.1f}%).**"
    )
    lines.append("")
    lines.append("## Completion Rule")
    lines.append("")
    lines.append(
        "A milestone must have implementation evidence in the repository "
        "and corresponding tests before it is considered production-complete."
    )
    lines.append("")
    lines.append("## Git Workflow")
    lines.append("")
    lines.append("For every completed milestone:")
    lines.append("")
    lines.append("1. Implement.")
    lines.append("2. Test.")
    lines.append("3. Run the relevant test suite.")
    lines.append("4. Generate this roadmap.")
    lines.append("5. Review the changed roadmap.")
    lines.append("6. Commit.")
    lines.append("7. Push.")
    lines.append("8. Continue to the next milestone.")
    lines.append("")
    lines.append("## Final Deletion")
    lines.append("")
    lines.append(
        "After GeoShield AI reaches its final production milestone, execute:"
    )
    lines.append("")
    lines.append(
        "```powershell\n"
        "python tools/generate_roadmap.py --delete-roadmap\n"
        "git add -A\n"
        'git commit -m "chore: remove temporary development roadmap"\n'
        "git push\n"
        "```"
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    if "--delete-roadmap" in sys.argv:
        if ROADMAP.exists():
            ROADMAP.unlink()
            print("ROADMAP.md permanently deleted.")
        else:
            print("ROADMAP.md does not exist.")
        return

    status = determine_status()
    ROADMAP.write_text(
        render(status),
        encoding="utf-8",
    )

    print("=" * 60)
    print("GEOSHIELD AI ROADMAP GENERATED")
    print("=" * 60)
    print(f"File: {ROADMAP}")

    completed = sum(status.values())
    total = len(status)

    print(f"Completed objectives: {completed}")
    print(f"Total objectives:     {total}")
    print(
        f"Progress:             "
        f"{completed / total * 100:.1f}%"
    )


if __name__ == "__main__":
    main()