from fastapi import APIRouter, Query
from datetime import datetime, timedelta

router = APIRouter()

LIVE_CAMERAS = [
    {
        "id": "cam_nbi_01",
        "name": "Nairobi - Uhuru Highway / Kenyatta Ave",
        "county": "Nairobi",
        "lat": -1.2864,
        "lng": 36.8172,
        "status": "LIVE",
        "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "resolution": "Sub-meter Ground Precision",
        "type": "Traffic & Incident Feed"
    },
    {
        "id": "cam_nbi_02",
        "name": "Thika Superhighway - Muthaiga Interchange",
        "county": "Nairobi",
        "lat": -1.2581,
        "lng": 36.8344,
        "status": "LIVE",
        "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "resolution": "Sub-meter Ground Precision",
        "type": "Flood & Highway Monitor"
    },
    {
        "id": "cam_msa_01",
        "name": "Mombasa - Likoni Ferry Crossing",
        "county": "Mombasa",
        "lat": -4.0815,
        "lng": 39.6642,
        "status": "LIVE",
        "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "resolution": "Sub-meter Coastal Optical",
        "type": "Maritime & Ferry Patrol"
    },
    {
        "id": "cam_ksm_01",
        "name": "Kisumu - Oginga Odinga Street",
        "county": "Kisumu",
        "lat": -0.1022,
        "lng": 34.7617,
        "status": "LIVE",
        "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "resolution": "Sub-meter Ground Precision",
        "type": "Urban Surveillance"
    }
]

@router.get("/cameras")
def get_live_cameras():
    return {"status": "success", "count": len(LIVE_CAMERAS), "cameras": LIVE_CAMERAS}

@router.get("/recordings")
def get_recordings_history(date: str = Query(None, description="Format YYYY-MM-DD")):
    today = datetime.now()
    recordings = []
    for i in range(7):
        rec_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        if not date or date == rec_date:
            recordings.append({
                "archive_id": f"OSIRI_REC_{rec_date}",
                "filename": f"OSIRI_KENYA_STREAM_{rec_date}.mp4",
                "date": rec_date,
                "duration": "24h 00m 00s",
                "size": "14.2 GB",
                "status": "ARCHIVED" if i > 0 else "RECORDING_ACTIVE"
            })
    return {"status": "success", "query_date": date, "recordings": recordings}
