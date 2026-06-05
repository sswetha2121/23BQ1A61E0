import requests

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyM2JxMWE2MWUwQHZ2aXQubmV0IiwiZXhwIjoxNzgwNjM4MDczLCJpYXQiOjE3ODA2MzcxNzMsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI2OTBkNmQyOS0xNGMwLTQ4MDUtYjVjZS00ZTMyZjkyNDlmOGIiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJ0dW1tYWxhIHN3ZXRoYSBjaG93ZGFyeSIsInN1YiI6IjU4YzVlMzBjLTYzNzAtNGIwZi1hNmUzLWZjMGM5YWM3ODgzYSJ9LCJlbWFpbCI6IjIzYnExYTYxZTBAdnZpdC5uZXQiLCJuYW1lIjoidHVtbWFsYSBzd2V0aGEgY2hvd2RhcnkiLCJyb2xsTm8iOiIyM2JxMWE2MWUwIiwiYWNjZXNzQ29kZSI6IlFRZEVZeSIsImNsaWVudElEIjoiNThjNWUzMGMtNjM3MC00YjBmLWE2ZTMtZmMwYzlhYzc4ODNhIiwiY2xpZW50U2VjcmV0IjoiQ2pta3dTeGJqQ1RLWXVZUiJ9.wt7GGBB7m_ciqEMglqBSK-NTwOuuOt2RU_0JiBDI2zI"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

DEPOTS_URL = "http://4.224.186.213/evaluation-service/depots"
VEHICLES_URL = "http://4.224.186.213/evaluation-service/vehicles"


def get_json(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.text)
        exit()

    return response.json()


depots = get_json(DEPOTS_URL)["depots"]
vehicles = get_json(VEHICLES_URL)["vehicles"]


def knapsack(tasks, capacity):
    n = len(tasks)

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

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

    max_impact, selected_tasks = knapsack(
        vehicles,
        capacity
    )

    print("\n" + "=" * 60)
    print(f"Depot ID: {depot['ID']}")
    print(f"Mechanic Hours: {capacity}")
    print(f"Maximum Impact: {max_impact}")

    total_duration = sum(
        task["Duration"]
        for task in selected_tasks
    )

    print(f"Total Duration Used: {total_duration}")

    print("\nSelected Tasks:")

    for task in selected_tasks:
        print(
            f"TaskID: {task['TaskID']} | "
            f"Duration: {task['Duration']} | "
            f"Impact: {task['Impact']}"
        )