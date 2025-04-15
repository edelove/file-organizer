import sys
import logging
from log_config import setup_logging
from utils import validate_input_directory
from cli import parse_args, load_config
from core import organize_files

def main(config_file=None):
    setup_logging()
    
    if config_file:
        config = load_config(config_file)
        
        if not config or "directories" not in config or "dry_run" not in config:
            logging.error("Invalid config file")
            sys.exit(1)

        for directory in config["directories"]:
            if not validate_input_directory(directory):
                continue
            organize_files(directory, config["dry_run"])

    else:
        args = parse_args()
        checking_dir = args.directory
        dry_run = args.dry_run

        if not validate_input_directory(checking_dir):
            sys.exit(1)
        organize_files(checking_dir, dry_run)


if __name__ == "__main__":
    main()
