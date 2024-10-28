import heapq

def calculate_capture_probability(encounters):
    if encounters == 0:
        return 0.0
    
    probability = 0.0
    for i in range(encounters):
        probability += (9 ** i) / (10 ** (i + 1))
    return probability

def find_best_path(routes, countdown, bounty_hunters, autonomy):
    bounty_hunters_map = {}
    for bh in bounty_hunters:
        bounty_hunters_map.setdefault(bh['planet'], []).append(bh['day'])

    
    priority_queue = [(0, 0, autonomy, "Tatooine", 0, ["Start at Tatooine"])]
    best_capture_probability = 1.0 
    best_path = []
    visited = {}

    while priority_queue:
        days_spent, _, fuel, current_planet, encounters, path = heapq.heappop(priority_queue)

        if current_planet == "Endor" and days_spent <= countdown:
            capture_probability = calculate_capture_probability(encounters)
            if capture_probability < best_capture_probability:
                best_capture_probability = capture_probability
                best_path = path
            continue

        if (current_planet, days_spent, fuel) in visited and visited[(current_planet, days_spent, fuel)] <= encounters:
            continue
        visited[(current_planet, days_spent, fuel)] = encounters

    
        for route in routes:
            if route['origin'] == current_planet:
                next_planet = route['destination']
                travel_time = route['travel_time']

                
                if fuel >= travel_time:
                    next_days_spent = days_spent + travel_time
                    new_fuel = fuel - travel_time
                    new_path = path + [f"Travel from {current_planet} to {next_planet}"]

                   
                    new_encounters = encounters
                    if next_planet in bounty_hunters_map and next_days_spent in bounty_hunters_map[next_planet]:
                        new_encounters += 1 
                        new_path[-1] += f" (Encounter Bounty Hunter on day {next_days_spent})"

                    
                    if next_days_spent <= countdown:
                        heapq.heappush(priority_queue, (
                            next_days_spent,
                            len(new_path),
                            new_fuel,
                            next_planet,
                            new_encounters,
                            new_path
                        ))

        # Refuel option with encounter check
        if fuel < autonomy and days_spent + 1 <= countdown:
            new_encounters = encounters
            if current_planet in bounty_hunters_map and (days_spent + 1) in bounty_hunters_map[current_planet]:
                new_encounters += 1  
                new_path = path + [f"Refuel on {current_planet} (Encounter Bounty Hunter on day {days_spent + 1})"]
            else:
                new_path = path + [f"Refuel on {current_planet}"]

            heapq.heappush(priority_queue, (
                days_spent + 1,
                len(new_path),
                autonomy,  
                current_planet,
                new_encounters,
                new_path
            ))
        
        if current_planet in bounty_hunters_map:
            for wait_days in range(1, countdown - days_spent + 1):
                if (days_spent + wait_days) in bounty_hunters_map[current_planet]:
                    continue  
                
                new_path = path + [f"Wait for {wait_days} day(s) on {current_planet}"]

                
                heapq.heappush(priority_queue, (
                    days_spent + wait_days,
                    len(new_path),
                    fuel,
                    current_planet,
                    encounters, 
                    new_path
                ))
        
        if current_planet not in bounty_hunters_map:
            for wait_days in range(1, countdown - days_spent + 1):
                new_path = path + [f"Wait for {wait_days} day(s) on {current_planet}"]

                
                heapq.heappush(priority_queue, (
                    days_spent + wait_days,
                    len(new_path),
                    fuel,
                    current_planet,
                    encounters,  
                    new_path
                ))

    
    final_probability = (1 - best_capture_probability) * 100 if best_path else 0

    
    print(f"Best Path: {best_path}")
    print(f"Final Probability of Success: {final_probability}%")

    return final_probability
