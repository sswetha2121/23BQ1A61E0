# Vehicle Maintenance Scheduler

## Problem

Select the optimal set of vehicle maintenance tasks for each depot such that:

- Total Duration <= Mechanic Hours
- Total Impact Score is maximized

## Approach

The problem is solved using the 0/1 Knapsack Dynamic Programming algorithm.

### Inputs

- Depots API
- Vehicles API

### Outputs

- Selected Tasks
- Maximum Impact Score

## Run

```bash
pip install -r requirements.txt
python main.py