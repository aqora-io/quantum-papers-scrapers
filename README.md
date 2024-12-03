# Scrapers for Quantum Papers

Here, you can find various scrapers used to automatically gather the latest news articles related to quantum computing and quantum physics.

## Overview

Each scraper in this directory is a Python script designed to extract links to new articles from specific websites. These links are then posted to Quantum News, keeping the community updated with the latest in quantum technology.

## Existing Scrapers

- `phys_org.py`: Scrapes articles from [phys.org](https://phys.org/tags/quantum+computing/sort/date/1d/)
- `quantum_insider.py`: Scrapes from Quantum Insider
- `hpc_wire.py`: Scrapes from HPC Wire
- `quanta_magazine.py`: Scrapes from Quanta Magazine
- *(Additional scrapers as they are added)*

## Adding Your Own Scraper

To contribute a new scraper:

1. **Copy an existing scraper** as a template. For example, you can use `phys_org.py` as a starting point.

2. **Modify the scraper** to target a new website. Update the URL, headers, and parsing logic as needed to extract the relevant article links.

3. **Integrate your scraper** into `scrape.py`. Add a new function for your scraper and update the `all_scrapers` dictionary.

4. **Test your scraper** by running:
   ```bash
   python scrape.py NAME_OF_NEW_SCRAPER testtest testtest
   ```
   This command will execute your scraper and attempt to post stories to [https://aqora.io/discussions/research-papers](https://aqora.io/discussions/research-papers). Make sure to replace `NAME_OF_NEW_SCRAPER` with the key you added to the `all_scrapers` dictionary.
