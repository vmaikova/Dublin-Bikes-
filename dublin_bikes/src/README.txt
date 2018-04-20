**Programs run in src use mysql.connector and require Python 2.7**
This is run separately of functioning website and will require a different environment to scrape and query data independently form DataRetrieval.py, to schedule it from main.py, or to make graphs from graphing.py

**Please follow process below:**
1. conda create --name dublinbikes2018 python=2.7
2. y
3. source activate dublinbikes2018
4. pip install -r requirements.txt

**To Run Scraper that scrapes data from Dublinbikes API every 300 seconds, or 10 minutes:**
python main.py

**To create graphs for each station:**
python graphing.py

**To deactivate from python 2.7 environment:**
source deactivate