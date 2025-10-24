# Monitoring Web Scraper

## > Purpose:
Scraping websites to monitor changes in prices, and buy at the desired price or taking action for competitive causes.

## > Process:
1- Used jupyter lab to try and test my code before making the web scraper script.
2- Made a class to make the request and handle cookies if not provided.
3- Wrote two functions to save the data after scraping:
  - First one to save to json.
  - Second one to save to duckdb database.
4- Built the scraper in main.py file and run it once every day for around a week.
5- Made a script to make sure if data is saved into the database.

## > Tools:
1- curl_cffi
2- selectolax
3- duckdb
4- jupyterlab

## > To Run main.py:
1- First install uv:
```bash 
pip install uv 
```

2- Then run the following command:
```bash
uv run main.py 
```

## > To View Jupter Lab:
1- First install dependencies:
```bash 
uv sync
```

2- Second, change virtual environment:
```bash 
source .venv/bin/activate
```

3- Finally, start jupyter lab:
```bash
jupyter lab
```

