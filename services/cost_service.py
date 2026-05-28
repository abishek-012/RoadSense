def estimate_repair_cost(severity):

    cost_table = {
        "low": 1000,
        "medium": 3000,
        "high": 7000
    }

    return cost_table.get(severity, 1000)