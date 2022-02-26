from bloxburg_cashier import *

if __name__ == "__main__":
    config = parse_json("config.json")
    debug_bool = bool(config["debug"])
    timeout = int(config["detection_timeout"])
    
    try:
        prompt_region = get_prompt_window_region()
    except ValueError as e:
        print("Bad Region Dimensions!")
    objs = setup_objects(config, prompt_region, debug=debug_bool)
    loop_locate(objs=objs, det_timeout=timeout)
