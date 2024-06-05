from DBController import ValidatorDB

def select_validator():
    validators_online = ValidatorDB.get_all_validators_online()
    validators_percentage = calculate_percentage(validators_online)

def calculate_percentage(data, limit=20, min_percentage=0.1):
    # Calculate the total balance
    total_balance = sum(person['balance'] for person in data.values())
    initial_percentages = [(person['balance'] / total_balance) * 100 for person in data.values()]

    # Apply reductions based on flags
    percentages = []
    for (name, person), initial_percentage in zip(data.items(), initial_percentages):
        if person['flags'] == 0:
            percentages.append(initial_percentage)
        elif person['flags'] == 1:
            percentages.append(initial_percentage * 0.5)
        elif person['flags'] == 2:
            percentages.append(initial_percentage * 0.25)

    # Adjust percentages that exceed the limit and accumulate excess
    excess = 0
    for i, percentage in enumerate(percentages):
        if percentage > limit:
            excess += percentage - limit
            percentages[i] = limit

    # Redistribute the excess proportionally among those below the limit
    while excess > 0:
        total_below_limit = sum(p for p in percentages if p < limit)
        if total_below_limit == 0:
            break

        new_excess = 0
        for i in range(len(percentages)):
            if percentages[i] < limit:
                redistribution = (percentages[i] / total_below_limit) * excess
                # Ensure redistribution does not exceed the limit
                if percentages[i] + redistribution > limit:
                    new_excess += (percentages[i] + redistribution) - limit
                    percentages[i] = limit
                else:
                    percentages[i] += redistribution
        excess = new_excess

    # Ensure no percentage is below the minimum percentage
    for i, percentage in enumerate(percentages):
        if percentage < min_percentage:
            excess = min_percentage - percentage
            percentages[i] = min_percentage
            total_above_min = sum(p for p in percentages if p > min_percentage)
            if total_above_min > 0:
                for j in range(len(percentages)):
                    if percentages[j] > min_percentage:
                        percentages[j] -= (percentages[j] / total_above_min) * excess

    return {name: percentage for name, percentage in zip(data.keys(), percentages)}