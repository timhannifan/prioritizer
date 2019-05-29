## Purpose
This is a simplified version of the [triage](https://github.com/dssg/triage) package written by DSSG at UChicago. The tools contained are intended to be used as generalized framework for experimenting with machine learning models for prediction, risk analysis, and resource prioritization.

A command line interface provides access the modular components, or an entire experiment can be run using a preconfigured file. Utilities are available for label/feature generation, time series splits, pipeline execution, and model evaluation.

The following dependencies are required to run the project:
- Python 3.6.0,
- PostgreSQL server running on localhost
- Some interesting binary event data, preferrably with some time and geospacial features

## Usage
After cloning the repository, create a new virtualenv and load from requirements file:
```
git clone https://github.com/timhannifan/prioritizer.git
cd prioritizer
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```
Add a configuration file to `/config`. See example file included.

Run `src/prioritizer/readstoreraw.py` on your data, changing SQL commands as necessary. This will bulk load your data to your local db.

Run prioritizer from command line:
```
cd src
ipython3
> from prioritizer.cli import Experiment
> experiment = Experiment()
> experiment.run('absolute/path/to/data.csv')
```
## License
The MIT License (MIT)
