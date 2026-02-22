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


def pace_seconds(distance_m: float, moving_time_s: float) -> float:
    """Return pace in seconds-per-km, or 0 if distance is 0."""
    if distance_m <= 0:
        return 0.0
    return moving_time_s / (distance_m / 1000)


def build_output(runs: list[dict]) -> dict:
    total_distance = sum(r.get("distance", 0) for r in runs)
    total_time = sum(r.get("moving_time", 0) for r in runs)
    total_elevation = sum(r.get("total_elevation_gain", 0) for r in runs)

    activities = []
    for r in sorted(runs, key=lambda x: x["start_date"], reverse=True):
        dist = r.get("distance", 0)
        time = r.get("moving_time", 0)
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
            }
        )

    return {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
