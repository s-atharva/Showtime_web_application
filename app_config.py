import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(basedir, "app_config.yaml")

with open(config_path) as fp:
    config = yaml.safe_load(fp)
    db_schema = config["db_schema"]
