import sys
sys.path.append('./components')

import os
import random
import yaml
import click

from experiment import Experiment
from db import create_engine

def run(config_file='./components/config/experiment.yaml'):

    click.echo(f"Using the config file {config_file}")

    with open(config_file) as f:
        loaded_config = yaml.load(f)

    db_u = loaded_config['db_user']
    db_p = loaded_config['db_password']

    db_url = 'postgresql://{}:{}@localhost:5432/localhost'.format(db_u, db_p )
    print(db_url)
    experiment = Experiment(
        config=loaded_config,
        db_engine=create_engine(db_url),
        project_path='./'
    )

if __name__ == '__main__':
        run()