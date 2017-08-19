import json

from modules.google_finance import GoogleFinance

"""
This module creates a database listing all instruments by fetching data from official source.
"""

sources = [
        GoogleFinance()
    ]

data = []
for source in sources:
    data.extend(source.fetch())

with open('output/database.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, sort_keys=True)
