import os
import random
import yaml
import click

from prioritizer.components.experiment import Experiment
from prioritizer.components.db import create_engine


class Prioritizer():
    def __init__(self):
        self.foo = 'foo'

    def run(self, config_path):
        click.echo(f"Using the config file {config_path}")

        with open(config_path) as f:
            loaded_config = yaml.load(f)

        db_u = loaded_config['db_user']
        db_p = loaded_config['db_password']
        db_n = loaded_config['db_name']

        db_url = 'postgresql://{}:{}@localhost:5432/{}'.format(db_u,
                                                               db_p,
                                                               db_n )
        print(db_url)
        experiment = Experiment(
            config=loaded_config,
            db_engine=create_engine(db_url),
            project_path='/output'
        )

# if __name__ == '__main__':
#         run()
