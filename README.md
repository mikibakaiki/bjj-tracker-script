# BJJ Kimono Tracker

Basic script to scrap a specific website and keep track of kimono prices. The idea is to have notifications in the future, when a certain product reaches a certain price.

## Useful commands:

- `crontab -e` to run this as a cron job

- `20 10 * * * cd /path/to/bjj_kimonos_scripts && ./bin/python ./main.py` example of the job to run every day at 10h20

- `pip freeze > requirements.txt` for the requirements

- `pip install -r requirements.txt` to install the requirements

- `python3 -m venv my_venv` to create virtualenv, if not created

- `source ./my_venv/bin/activate` to activate virtualenv

- `(my_venv)$ pip3 install -r ./requirements.txt` to install dependencies

- `(my_venv)$ deactivate` to leave virtual environment
