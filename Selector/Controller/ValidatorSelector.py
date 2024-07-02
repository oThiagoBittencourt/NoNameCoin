from Controller.DBController import ValidatorDB
import random
import threading
import time

db = ValidatorDB()

def select_validator():
    validators_online = db.get_all_validators_online()
    print(f"1:{validators_online}")
    validators_percentage = calculate_percentage(validators_online)
    print(f"2:{validators_percentage}")
    selected_validators = choice_validators(validators_percentage, 3)
    print(f"3:{selected_validators}")
    result_container = {}
    if not selected_validators:
        pass
        #thread = threading.Thread(target=choice_validators_thread, args=(3, 60, result_container, validators_percentage))
        #thread.start()
        #thread.join()
        #selected_validators = result_container.get('selected_users', [])
    for validator in selected_validators:
        # Adicionar Sequencia
        db.update_sequence(validator)
        # Definir Status como "working"
        db.change_status(validator, "working")
    # Limpar de todos os outros que não foram selecionados
    validators_timeout = db.get_all_validators_timeout()
    for validator_timeout in validators_timeout:
        db.update_sequence(validator_timeout, True)
    return selected_validators

def choice_validators_thread(num_selections, timeout, result_container, validators_percentage):
    start_time = time.time()
    while time.time() - start_time < timeout:
        selected_users = choice_validators(validators_percentage, num_selections)
        if selected_users:
            result_container['selected_users'] = selected_users
            return
        if time.time() - start_time + 10 >= timeout :
            return
        time.sleep(10)
    result_container['selected_users'] = []

def choice_validators(validators, num_selections):
    if num_selections > len(validators):
        return []
    
    names = list(validators.keys())
    weights = list(validators.values())

    # Ensures that the selected users are unique
    selected = set()
    while len(selected) < num_selections:
        selected.update(random.choices(names, weights=weights, k=num_selections))
        if len(selected) > num_selections:
            selected = set(list(selected)[:num_selections])

    return list(selected)

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