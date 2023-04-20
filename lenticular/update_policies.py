import yaml

def update_policies():
    # Load YAML file
    with open('policies.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Prompt user for input for each key
    for key in config:
        current_val = config[key]
        if isinstance(current_val, dict):
            for subkey in current_val:
                subcurrent_val = current_val[subkey]
                subnew_val = input(f"Enter a new value for {subkey} (default is {subcurrent_val}): ")
                if subnew_val == '':
                    current_val[subkey] = subcurrent_val
                else:
                    current_val[subkey] = subnew_val

        else:
            new_val = input(f"Enter a new value for {key} (default is {current_val}): ")
        
            # Use default value if user doesn't enter anything
            if new_val == '':
                config[key] = current_val
            else:
                config[key] = new_val

    # Save updated values back to YAML file
    with open('policies.yaml', 'w') as file:
        yaml.dump(config, file)

if __name__ == '__main__':
    update_policies()   