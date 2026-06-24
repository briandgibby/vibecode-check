# Example 3 — adding error handling — an already‑clear prompt (restraint)

## The original prompt
What a newer programmer might actually type:

> in my app.py i have a function get_weather(city) that calls the openweathermap api. can you add error handling so if the api call fails it returns 'weather unavailable' instead of crashing? im on python 3.11 using the requests library

---

## Without the skill
A coding agent takes the prompt at face value and runs with it:

Here's how to add error handling to your `get_weather` function so it returns `'weather unavailable'` instead of crashing:

```python
import requests

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": "YOUR_API_KEY",
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # raises an exception for 4xx/5xx status codes
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to weather service.")
        return "weather unavailable"
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out.")
        return "weather unavailable"
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return "weather unavailable"
    except requests.exceptions.RequestException as e:
        print(f"Error: An unexpected error occurred: {e}")
        return "weather unavailable"
```

**What each exception handles:**

- `ConnectionError` — network is down, DNS failure, or the server refused the connection
- `Timeout` — the request took too long (the `timeout=10` argument is what triggers this; always set a timeout or your app can hang indefinitely)

> _…baseline truncated — the full no‑skill response ran 58 lines (it just started building)._

---

## With Vibecode Check

## Clarifying questions

None warranted. The prompt names the file, the function, the library, the Python version, and the desired behavior. The one open point — which failure modes count as "fails" — has a safe, conventional default I can state and flag for veto rather than block on.

---

## 1. The cleaned-up prompt

```
In `app.py`, add error handling to the existing `get_weather(city)` function so
that any failure during the OpenWeatherMap API call returns the string
`'weather unavailable'` instead of raising an exception.

**Stack:** Python 3.11, `requests` library.

**What counts as failure — handle all of these:**
- Network/connection errors (`requests.exceptions.ConnectionError`, `requests.exceptions.Timeout`)
- Any non-2xx HTTP status code (check `response.raise_for_status()`)
- Malformed or missing JSON in the response body

Wrap only the internals of `get_weather(city)` — do not change its signature or
touch any other function in the file.

When done, show me a quick manual test: call `get_weather("London")` with the
network disconnected (or with a bad API key) and confirm the function returns
`'weather unavailable'` rather than raising.
```

---

## 2. What I changed & corrected — and the convention behind it

**Changes:**

- **Named the failure modes explicitly.** "If the api call fails" is ambiguous — `requests` distinguishes network errors, timeouts, HTTP error codes, and bad response bodies, and a coding agent might handle only one category unless told otherwise. The rewrite lists all three common categories so the agent handles each. The conventional idiom is `try/except requests.exceptions.RequestException` (the base class for all `requests` errors) plus `response.raise_for_status()` for HTTP-level failures and a `try/except` around JSON parsing.

- **Added a scope guard.** "Do not change its signature or touch any other function in the file" makes the boundary explicit. Without this, an agent sometimes helpfully refactors neighboring code or adds a helper function — which can introduce unintended changes.

- **Added a verification step.** The original prompt ends at "instead of crashing," giving the agent no way to confirm it worked. Adding "show me a quick manual test" closes the loop so the agent demonstrates the behavior rather than just asserting it works.

No terminology corrections needed — everything in the original was standard.

---

## 3. Assumptions & possible misunderstandings — are we still in sync?

- I assumed "if the api call fails" means *all* common failure categories (connection error, timeout, non-2xx HTTP status, bad JSON) — not just one. Correct me if you only want to catch network errors, for example.
- I assumed the existing function does not already have a `try/except` block. If it does, the agent will need to extend it rather than wrap from scratch — pointing the agent at the existing block with a comment would help.
- I assumed `'weather unavailable'` (lowercase, with a space) is the exact return string you want. If your calling code checks against a specific casing, make sure the prompt matches.

---

## 4. Prompt tips for next time

**Define what "failure" means.** The phrase "if it fails" reads clearly in conversation but is ambiguous to a coding agent, because a library like `requests` surfaces failures in several distinct ways (network down, server returns 404, response isn't valid JSON). Listing the failure modes — even briefly — removes that ambiguity and means you get error handling that actually covers the cases you care about.

**End with a verification step.** Notice I added "show me a quick manual test." Agents stop when the code *looks* done; a verification step gives them a concrete check to run, so they catch their own mistakes before handing back to you. For error handling especially, it's worth asking the agent to demonstrate the fallback path, not just the happy path.
