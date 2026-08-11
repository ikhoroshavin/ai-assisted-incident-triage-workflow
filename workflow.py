import anthropic, json
from config.config import MODEL, client, alert
from info_collector import collect
from datetime import datetime

#the models first call (analysis of timing, affected instances etc)
def extract_params(user_prompt: str) -> dict:
    instruction = """You are a Tech Ops engineer on the APM (Alternative Payment Methods) team.
    Read the ALERT below and extract the following fields: incident_time, instances (list of strings), 
    domains (list of strings, e.g. payment method and provider, lowercased), component (string)
    Return ONLY a VALID JSON object with exactly these fields. No explanations, no markdown code fences.
    Expected shape: {"incident_time": "...", "instances": ["..."], "domains": ["..."], "component": "..."}"""

    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": instruction + "\n\nALERT:\n" + user_prompt}],
    )

    return _extract_json(resp.content[0].text)

#the models second call (analysis of info_collector.py result)
def rank_relevance(alert: str, collected: dict) -> dict:
    instruction = """You're a Tech Ops Engineer on the APM (Alternative Payment Methods) Team. You're investigating an incident with the ALERT parameters below
    and list of data from different sources. Using the all know information about THIS EXACTLY incident, look into the data in COLLECTED list
    and assess the degree of relevance for each message to the incident, based on time of the incident, relevance of instances, endpoints, semantic sense.
    Sort all messages by source and degree of relevance and return a VALID JSON that includes the source, the time, the message text, the link to the message.
    The messages with the highest degree of relevance should be on top, the messages with moderate degree of relevance mark as POSIBLY RELEVANT,
    the messages with lowest degree of relevant (0.6 and below) should be excluded from the output.
    All errors of response should be noticed in the output."""
    payload = json.dumps(collected, ensure_ascii=False)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user",
                   "content": instruction + "\n\nALERT:\n" + alert + "\n\nCOLLECTED:\n" + payload}],
    )
    return _extract_json(resp.content[0].text)

#I had to add this helper because the model returned json in markdown formatting and the script fall
def _extract_json(text: str):
    start = text.find("{")
    end = text.rfind("}")  
    return json.loads(text[start:end + 1])

#Simple logging. Includes the alert, the model, the payload collected by info_collector and timing params
def write_logs(alert, params, collected, result):
    now = datetime.now()
    record = {
        "run_at": now.isoformat(),
        "model": MODEL,
        "alert": alert,
        "params": params,
        "collected": collected,
        "result": result,
    }
    with open(f"logs.json", "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    params = extract_params(alert)          
    collected = collect(params)             
    result = rank_relevance(alert, collected)
    write_logs(alert, params, collected, result)
    print(json.dumps(result, indent=2, ensure_ascii=False))