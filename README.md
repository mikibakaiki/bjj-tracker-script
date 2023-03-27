# BJJ Kimono Tracker

Basic script to scrap a specific website and keep track of kimono prices. The idea is to have notifications in the future, when a certain product reaches a certain price.

# Connection string:

1. Create a `.env` file with the following:

`ATLAS_URI=mongodb+srv://username:password@cluster.mongodb.net/db_name?retryWrites=true&w=majority`

## Useful commands:

- `nohup python main.py` to [run and let the process sleep](https://stackoverflow.com/questions/2975624/how-to-run-a-script-in-the-background-even-after-i-logout-ssh)

- `pip freeze > requirements.txt` for the requirements

- `pip install -r requirements.txt` to install the requirements

- `python3 -m venv my_venv` to create virtualenv, if not created

- `source ./my_venv/bin/activate` to activate virtualenv

- `(my_venv)$ pip3 install -r ./requirements.txt` to install dependencies

- `(my_venv)$ deactivate` to leave virtual environment
