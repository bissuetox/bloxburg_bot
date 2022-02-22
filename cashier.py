from bloxburg_cashier import *

if __name__ == "__main__":
    prompt_region = get_prompt_window_region()
    bbimg.prompt_region = prompt_region
    # screenshot(prompt_region)

    objs = setup_objects(prompt_region)
    loop_locate(objs=objs, det_timeout=200, debug=False)
