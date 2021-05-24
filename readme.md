# LambdaTest scripts using Pylenium

After installing poetry via pip3

- Run `poetry install`
- Run `poetry run pylenium init`



## Setup virtual environment
You can do this via virtualenv or poetry

### virtualenv
```
python -m venv venv
```

then run

```
# Windows 
./venv/Scripts/activate

#Mac OS
source /venv/bin/activate

```

### poetry

spawn a new shell with virtual environment. 
```
poetry shell
```

Additional info can be found here https://python-poetry.org/docs/



## Run tests

This is setup so you only need to run the sh scripts. If you want to run specific tests that are not these, refer to the documentation for pytest and pylenium. 

### Normal

```
python -m pytest path/to/file.sh

```


### Poetry

```
poetry run python path/to/your/script.sh

```