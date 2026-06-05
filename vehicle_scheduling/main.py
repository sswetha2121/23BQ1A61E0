import requests

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyM2JxMWE2MWUwQHZ2aXQubmV0IiwiZXhwIjoxNzgwNjM1MjM5LCJpYXQiOjE3ODA2MzQzMzksImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiIyMTc4MTI2Ny1mNTMzLTQ5NjktODMwZC1mNGNjZWVlNTg1MWUiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJ0dW1tYWxhIHN3ZXRoYSBjaG93ZGFyeSIsInN1YiI6IjU4YzVlMzBjLTYzNzAtNGIwZi1hNmUzLWZjMGM5YWM3ODgzYSJ9LCJlbWFpbCI6IjIzYnExYTYxZTBAdnZpdC5uZXQiLCJuYW1lIjoidHVtbWFsYSBzd2V0aGEgY2hvd2RhcnkiLCJyb2xsTm8iOiIyM2JxMWE2MWUwIiwiYWNjZXNzQ29kZSI6IlFRZEVZeSIsImNsaWVudElEIjoiNThjNWUzMGMtNjM3MC00YjBmLWE2ZTMtZmMwYzlhYzc4ODNhIiwiY2xpZW50U2VjcmV0IjoiQ2pta3dTeGJqQ1RLWXVZUiJ9.sVJRqDHWnVrK4TMYBlqY_p0RBgsDhkCcttf1RbkB92c"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

depots_url = "http://4.224.186.213/evaluation-service/depots"
vehicles_url = "http://4.224.186.213/evaluation-service/vehicles"

depots = requests.get(depots_url, headers=headers).json()["depots"]
vehicles = requests.get(vehicles_url, headers=headers).json()["vehicles"]

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