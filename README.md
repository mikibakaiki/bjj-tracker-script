# BJJ Kimono Tracker

Basic script to scrap a specific website and keep track of kimono prices.

The idea is to have notifications in the future, when a certain product reaches a certain price.

# Connection string:

1. Create a `.env` file with the following:

`ATLAS_URI=mongodb+srv://USERNAME:password@cluster.mongodb.net/db_name?retryWrites=true&w=majority`

or

`ATLAS_URI=mongodb+srv://USERNAME:password@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority`

# Requirements:

- Python +3.9
- virtualenv - `pip install virtualenv`

# Setup:

1. Run the script `./setup.sh`
2. Create a `.env` file with the `ATLAS_URI` string. This is needed for the connection to the database
3. Activate the virtualenv: `source bjj_venv/bin/activate`
4. Run the script `python main.py [--mode] [main, sim, noimg]`
   4.1 The options are:
   - main: the default behavior of the script. Will scrap the website and write into the DB
   - sim: simulation mode - will scrap the website and just print results, not writing to the DB
   - noimg: retrieve, from the DB, all the kimonos without an img. This is useful because i entered this information later on the dev stage, and not all kimonos have images.

## Useful commands:

- `nohup python main.py` to [run and let the process sleep](https://stackoverflow.com/questions/2975624/how-to-run-a-script-in-the-background-even-after-i-logout-ssh)

- `pip freeze > requirements.txt` for the requirements

- `pip install -r requirements.txt` to install the requirements

- `python3 -m venv my_venv` to create virtualenv, if not created

- `source ./my_venv/bin/activate` to activate virtualenv

- `(my_venv)$ pip3 install -r ./requirements.txt` to install dependencies

- `(my_venv)$ deactivate` to leave virtual environment

- `crontab -e` to run this as a cron job

- `20 10 * * * cd /path/to/bjj_kimonos_scripts && ./bin/python ./main.py` example of the job to run every day at 10h20

## Action Bumps
bump
bump
bump
another one bumps the dust
