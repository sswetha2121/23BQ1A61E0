import os
import requests

TOKEN = os.getenv(
    "EVAL_SERVICE_TOKEN",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aXNlIiwiZW1haWwiOiIyM2JxMWE2MWUwQHZ2aXQubmV0IiwiZXhwIjoxNzgwNjM1MjM5LCJpYXQiOjE3ODA2MzQzMzksImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiIyMTc4MTI2Ny1mNTMzLTQ5NjktODMwZC1mNGNjZWVlNTg1MWUiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJ0dW1tYWxhIHN3ZXRoYSBjaG93ZGFyeSIsInN1YiI6IjU4YzVlMzBjLTYzNzAtNGIwZi1hNmUzLWZjMGM5YWM3ODgzYSJ9LCJlbWFpbCI6IjIzYnExYTYxZTBAdnZpdC5uZXQiLCJuYW1lIjoidHVtbWFsYSBzd2V0aGEgY2hvd2RhcnkiLCJyb2xsTm8iOiIyM2JxMWE2MWUwIiwiYWNjZXNzQ29kZSI6IlFRZEVZeSIsImNsaWVudElEIjoiNThjNWUzMGMtNjM3MC00YjBmLWE2ZTMtZmMwYzlhYzc4ODNhIiwiY2xpZW50U2VjcmV0IjoiQ2pta3dTeGJqQ1RLWXVZUiJ9.sVJRqDHWnVrK4TMYBlqY_p0RBgsDhkCcttf1RbkB92c"
)

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

depots_url = "http://4.224.186.213/evaluation-service/depots"
vehicles_url = "http://4.224.186.213/evaluation-service/vehicles"

def fetch_json(url, name):
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        raise SystemExit(
            f"Authorization failed for {name}: {response.status_code} {response.reason}. "
            "Update the token in EVAL_SERVICE_TOKEN or refresh the hard-coded token."
        )
    if response.status_code != 200:
        raise SystemExit(
            f"Failed to fetch {name}: {response.status_code} {response.reason}. Body: {response.text}"
        )
    try:
        return response.json()
    except ValueError:
        raise SystemExit(f"Failed to parse JSON from {name} endpoint: {response.text}")

print("Fetching data from evaluation service...")
depots_data = fetch_json(depots_url, "depots")
vehicles_data = fetch_json(vehicles_url, "vehicles")

if "depots" not in depots_data:
    raise SystemExit(f"Unexpected depots response shape: {depots_data}")
if "vehicles" not in vehicles_data:
    raise SystemExit(f"Unexpected vehicles response shape: {vehicles_data}")

depots = depots_data["depots"]
vehicles = vehicles_data["vehicles"]

def knapsack(tasks, capacity):
    n = len(tasks)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        duration = tasks[i - 1]["Duration"]
        impact = tasks[i - 1]["Impact"]

        for w in range(capacity + 1):
            if duration <= w:
                dp[i][w] = max(
                    impact + dp[i - 1][w - duration],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(tasks[i - 1])
            w -= tasks[i - 1]["Duration"]

    return dp[n][capacity], selected

for depot in depots:
    capacity = depot["MechanicHours"]

    best_score, selected_tasks = knapsack(
        vehicles,
        capacity
    )

    print("\n" + "=" * 50)
    print("Depot:", depot["ID"])
    print("Mechanic Hours:", capacity)
    print("Maximum Impact:", best_score)

    print("\nSelected Tasks:")
    for task in selected_tasks:
        print(
            task["TaskID"],
            "Duration:", task["Duration"],
            "Impact:", task["Impact"]
        )