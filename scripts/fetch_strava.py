#!/usr/bin/env python3
"""Fetch Strava activities and write _data/strava.json for Jekyll build."""

import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

TOKEN_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
PER_PAGE = 200
WEEKS_BACK = 16


def get_access_token() -> str:
    client_id = os.environ["STRAVA_CLIENT_ID"]
    client_secret = os.environ["STRAVA_CLIENT_SECRET"]
    refresh_token = os.environ["STRAVA_REFRESH_TOKEN"]

    resp = requests.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_all_runs(access_token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}
    runs = []
    page = 1
    while True:
        resp = requests.get(
            ACTIVITIES_URL,
            headers=headers,
            params={"type": "Run", "per_page": PER_PAGE, "page": page},
            timeout=30,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        runs.extend(batch)
        if len(batch) < PER_PAGE:
            break
        page += 1
    return runs


def week_label(dt: datetime) -> str:
    """Return a label like 'Feb W1' for the given datetime."""
    week_of_month = math.ceil(dt.day / 7)
    return f"{dt.strftime('%b')} W{week_of_month}"


def week_start(dt: datetime) -> datetime:
    """Return Monday of the week containing dt (UTC)."""
    return (dt - timedelta(days=dt.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def build_today(runs: list[dict]) -> dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    distance_m = 0.0
    elevation_m = 0.0
    moving_time_s = 0
    count = 0
    for r in runs:
        if r["start_date_local"][:10] == today:
            distance_m += r.get("distance", 0)
            elevation_m += r.get("total_elevation_gain", 0)
            moving_time_s += r.get("moving_time", 0)
            count += 1
    return {
        "date": today,
        "runs": count,
        "distance_km": round(distance_m / 1000, 2),
        "elevation_m": round(elevation_m, 1),
        "moving_time_s": moving_time_s,
    }


def build_yearly(runs: list[dict]) -> list[dict]:
    yearly: dict[int, dict] = defaultdict(lambda: {"runs": 0, "distance_m": 0.0, "elevation_m": 0.0, "moving_time_s": 0})
    for run in runs:
        year = int(run["start_date_local"][:4])
        yearly[year]["runs"] += 1
        yearly[year]["distance_m"] += run.get("distance", 0)
        yearly[year]["elevation_m"] += run.get("total_elevation_gain", 0)
        yearly[year]["moving_time_s"] += run.get("moving_time", 0)

    result = []
    for year in sorted(yearly.keys(), reverse=True):
        y = yearly[year]
        dist_km = y["distance_m"] / 1000
        result.append({
            "year": year,
            "runs": y["runs"],
            "distance_km": round(dist_km, 2),
            "elevation_m": round(y["elevation_m"], 1),
            "moving_time_s": y["moving_time_s"],
        })
    return result


def build_weekly(runs: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc)
    cutoff = week_start(now) - timedelta(weeks=WEEKS_BACK - 1)

    weekly: dict[datetime, float] = defaultdict(float)
    for run in runs:
        dt = datetime.fromisoformat(run["start_date_local"].replace("Z", "+00:00"))
        ws = week_start(dt.replace(tzinfo=timezone.utc))
        if ws >= cutoff:
            weekly[ws] += run.get("distance", 0) / 1000  # metres → km

    # Fill all 16 weeks (including empty ones)
    result = []
    for i in range(WEEKS_BACK):
        ws = cutoff + timedelta(weeks=i)
        result.append(
            {
                "label": week_label(ws),
                "distance_km": round(weekly.get(ws, 0.0), 2),
            }
        )
    return result


def decode_polyline(encoded: str) -> list[tuple[float, float]]:
    """Decode a Google Encoded Polyline string to (lat, lon) pairs."""
    if not encoded:
        return []
    coords: list[tuple[float, float]] = []
    index, lat, lng = 0, 0, 0
    while index < len(encoded):
        for is_lng in (False, True):
            result, shift = 0, 0
            while True:
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            value = ~(result >> 1) if result & 1 else result >> 1
            if is_lng:
                lng += value
            else:
                lat += value
        coords.append((lat / 1e5, lng / 1e5))
    return coords


def polyline_to_svg_path(coords: list[tuple[float, float]], width: int = 200, height: int = 120) -> str:
    """Normalize (lat, lon) coords to an SVG path string within width×height."""
    if len(coords) < 2:
        return ""
    lats = [c[0] for c in coords]
    lngs = [c[1] for c in coords]
    lat_range = (max(lats) - min(lats)) or 1e-9
    lng_range = (max(lngs) - min(lngs)) or 1e-9
    pad = 8
    scale = min((width - 2 * pad) / lng_range, (height - 2 * pad) / lat_range)
    parts = []
    for i, (lat, lng) in enumerate(coords):
        x = pad + (lng - min(lngs)) * scale
        y = pad + (max(lats) - lat) * scale  # flip Y axis
        parts.append(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}")
    return " ".join(parts)


def build_output(runs: list[dict]) -> dict:
    total_distance = sum(r.get("distance", 0) for r in runs)
    total_time = sum(r.get("moving_time", 0) for r in runs)
    total_elevation = sum(r.get("total_elevation_gain", 0) for r in runs)

    activities = []
    for r in sorted(runs, key=lambda x: x["start_date"], reverse=True):
        dist = r.get("distance", 0)
        time = r.get("moving_time", 0)

        # Route map: decode summary polyline → SVG path
        encoded = (r.get("map") or {}).get("summary_polyline") or ""
        route_svg = polyline_to_svg_path(decode_polyline(encoded))

        # Primary photo URL (from summary activities response)
        photos = r.get("photos") or {}
        primary = photos.get("primary") or {}
        urls = primary.get("urls") or {}
        photo_url = urls.get("600") or urls.get("100") or ""

        activities.append(
            {
                "id": r["id"],
                "name": r.get("name", ""),
                "date": r["start_date_local"][:10],
                "distance_m": round(dist, 1),
                "moving_time_s": time,
                "elevation_m": round(r.get("total_elevation_gain", 0), 1),
                "avg_speed_ms": round(r.get("average_speed", 0), 3),
                "strava_url": f"https://www.strava.com/activities/{r['id']}",
                "route_svg": route_svg,
                "photo_url": photo_url,
            }
        )

    return {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "today": build_today(runs),
        "summary": {
            "total_distance_km": round(total_distance / 1000, 2),
            "total_runs": len(runs),
            "total_elevation_m": round(total_elevation, 1),
            "total_moving_time_s": total_time,
        },
        "yearly": build_yearly(runs),
        "weekly": build_weekly(runs),
        "activities": activities,
    }


def main() -> None:
    print("Fetching Strava access token…")
    token = get_access_token()

    print("Fetching all run activities…")
    runs = fetch_all_runs(token)
    print(f"  Found {len(runs)} runs.")

    output = build_output(runs)

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "_data",
        "strava.json",
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Written to {out_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyError as exc:
        print(f"ERROR: Missing environment variable {exc}", file=sys.stderr)
        sys.exit(1)
    except requests.HTTPError as exc:
        print(f"ERROR: Strava API request failed: {exc}", file=sys.stderr)
        sys.exit(1)
