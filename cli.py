import argparse
import os
import json
import logging

def parse_args():
    parser = argparse.ArgumentParser(description="Organize files by extensions into folders.")
    parser.add_argument("--config",required=True,help="The path to .json with directory or list of directories")

    return parser.parse_args()

def parse_config(config_path):
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path,'r',encoding='utf-8') as jfile:
            config = json.load(jfile)

        if "directories" not in config or not isinstance(config["directories"],list):
            logging.error("Config file must contain a 'directories' list.")
            return None
        if "dry_run" not in config or not isinstance(config["dry_run"],bool):
            logging.error("Config file must contain a boolean 'dry_run' field.")
            return None
        return config
    except Exception as e:
        logging.error("Failed to parse config: {}".format(e))
        return None
    
def load_config(config_file):
    try:
        with open(config_file,"r") as f:
            return json.load(f)
    except Exception as e:
        logging.error("Failed to load config file: {}".format(e))
        return None