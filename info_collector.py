import json
from datetime import datetime, timedelta, timezone
from config.config import WINDOW_MINUTES, TIME_KEYS, mockpath

#extract time form the different source - each source have it's own field for time
def _get_time(item: dict):
    for key in TIME_KEYS:
        if key in item:
            return datetime.fromisoformat(item[key])
    return None

#filtering the messages in the mock by time. Actually, for this demo could be replaced with simple 
# "with open(mock_path) as file: return json.load(file)", but I decided to leave the model of production logic 
# as an illustration of divide between determinated logic and AI-part
def collect(params: dict, mock_path=mockpath) -> dict:
    incident_time = datetime.fromisoformat(params["incident_time"])
    window_from = incident_time - timedelta(minutes=WINDOW_MINUTES) #incident time was mocked for demo
    window_to   = incident_time + timedelta(minutes=WINDOW_MINUTES) #incident time was mocked for demo

    with open(mock_path, encoding="utf-8") as f:
        data = json.load(f)

    filtered = {}
    for source, items in data["results"].items():
        output = []
        for item in items:
            t = _get_time(item)
            if t is not None and window_from <= t <= window_to:
                output.append(item)
        filtered[source] = output

    return {
        "collection_meta": {
            "window_from": window_from.isoformat(),
            "window_to": window_to.isoformat(),
            "incident_time": params["incident_time"],
        },
        "results": filtered,
        "collection_errors": data.get("collection_errors", []),
    }


if __name__ == "__main__":
    test_params = {"incident_time": "2026-08-11T14:12:07Z"}
    result = collect(test_params)
    print(json.dumps(result))