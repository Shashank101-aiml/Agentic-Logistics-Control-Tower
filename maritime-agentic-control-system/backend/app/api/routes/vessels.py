from fastapi import APIRouter

router = APIRouter()


@router.get("/vessels")
def get_vessels():
    return [
        {
            "id": "MV-OCEAN-STAR",
            "name": "MV Ocean Star",
            "type": "Container Ship (14,000 TEU)",
            "speed": "18.4 kts",
            "heading": "240° SW",
            "corridor": "Corridor Beta (Southern Bypass)",
            "status": "MITIGATING RISK",
            "lat": 15.2,
            "lng": 64.5,
            "risk": "ELEVATED"
        },
        {
            "id": "MV-TITAN-EXPRESS",
            "name": "MV Titan Express",
            "type": "VLCC Crude Tanker",
            "speed": "14.1 kts",
            "heading": "285° WNW",
            "corridor": "Corridor Alpha (Direct)",
            "status": "HIGH HAZARD ALERT",
            "lat": 12.5,
            "lng": 45.3,
            "risk": "CRITICAL"
        },
        {
            "id": "MV-PACIFIC-CARRIER",
            "name": "MV Pacific Carrier",
            "type": "Bulk Carrier",
            "speed": "12.0 kts",
            "heading": "110° ESE",
            "corridor": "Corridor Gamma (Coastal)",
            "status": "PORT DELAYED",
            "lat": 1.35,
            "lng": 103.8,
            "risk": "NORMAL"
        },
        {
            "id": "MV-NEPTUNE-VOYAGER",
            "name": "MV Neptune Voyager",
            "type": "LNG Tanker",
            "speed": "19.8 kts",
            "heading": "320° NW",
            "corridor": "Corridor Beta (Southern Bypass)",
            "status": "ON SCHEDULE",
            "lat": 26.5,
            "lng": 56.4,
            "risk": "NORMAL"
        },
        {
            "id": "MV-EASTERN-HORIZON",
            "name": "MV Eastern Horizon",
            "type": "Container Ship (8,500 TEU)",
            "speed": "21.2 kts",
            "heading": "045° NE",
            "corridor": "Corridor Alpha (Direct)",
            "status": "ON SCHEDULE",
            "lat": 12.0,
            "lng": 114.0,
            "risk": "NORMAL"
        },
        {
            "id": "MV-POLARIS-LEADER",
            "name": "MV Polaris Leader",
            "type": "Ro-Ro Vehicle Carrier",
            "speed": "17.5 kts",
            "heading": "180° S",
            "corridor": "Corridor Beta (Southern Bypass)",
            "status": "ON SCHEDULE",
            "lat": 8.5,
            "lng": 76.2,
            "risk": "NORMAL"
        }
    ]