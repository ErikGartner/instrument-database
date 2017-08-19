# Mimir Instrument Database
*A tool for creating a large dump of stocks available on Google Finance.*

This tool can fetch lists of all stock available on Google Finance. It also supports fetching more data for each stock though this is
currently disabled due to Google's rate limiting.

The database can be loaded into Mimir's database to provide a list of available Stocks.

## Usage

1. Create a virtual env for Python 3.
2. Install all dependencies in `requirements.txt`
3. Run using `python database-creator.py`
