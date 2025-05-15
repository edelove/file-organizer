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

        include_subdirs = config.get("include_subdirs", False)

        for directory in config["directories"]:
            if not validate_input_directory(directory, include_subdirs):
                continue
            organize_files(directory, config["dry_run"], include_subdirs)

    else:
        args = parse_args()

        if not hasattr(args, "directory"):
            logging.error("Directory argument missing.")
            sys.exit(1)

        if not validate_input_directory(args.directory, args.include_subdirs):
            sys.exit(1)

        organize_files(args.directory, args.dry_run, args.include_subdirs)



if __name__ == "__main__":
    main()

