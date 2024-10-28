import argparse
import json
from config import load_config
from routes import load_routes
from utils import find_best_path 

def main():
    parser = argparse.ArgumentParser(description="Calculate the odds of the Millennium Falcon reaching Endor.")
    parser.add_argument("millennium_falcon", help="Path to the millennium-falcon.json file")
    parser.add_argument("empire_data", help="Path to the empire.json file")
    
    args = parser.parse_args()
    
    millennium_data = load_config(args.millennium_falcon)
    
    routes = load_routes(millennium_data['routes_db'])
    
    with open(args.empire_data) as f:
        empire_data = json.load(f)

    probability = find_best_path(  
        routes,
        empire_data['countdown'],
        empire_data['bounty_hunters'],
        millennium_data['autonomy']
    )
    
    print(f"Millennium Falcon Autonomy: {millennium_data['autonomy']}")
    print(f"Empire Countdown: {empire_data['countdown']}")
    
    print(f"The Millennium Falcon has a {probability:.2f}% chance of reaching Endor in time!")

if __name__ == "__main__":
    main()
