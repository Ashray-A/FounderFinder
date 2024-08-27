# Company Founder Scraper

This script scrapes Wikipedia to find the founders of given companies.

## Script Usage Instructions

1. Ensure you have Python 3.7+ installed on your system.
2. Install the required packages by running:
pip install pandas requests
Copy3. Place the `main.py` and `wikipedia_scraper.py` files in the same directory.
4. Run the script by executing:
python src/main.py
Copy5. Follow the prompts in the terminal to either:
- Search for a single company's founder
- Process multiple companies from a CSV file

When processing from a CSV file, ensure your file has a column named 'company_name'.

## Resources Used

- Python 3.7+
- Libraries: pandas, requests, re, time, os
- Wikipedia API for searching and retrieving page content

## Challenges Faced

1. Wikipedia Data Inconsistency: The format and location of founder information in Wikipedia pages are not standardized, making it challenging to extract consistently.

2. Company Name Variations: Companies often have multiple name formats (e.g., "Apple" vs "Apple Inc."), requiring the script to handle various aliases.

3. Founder Name Cleaning: Extracted founder names often include titles, suffixes, or extra information that needed to be cleaned for consistency.

4. API Rate Limiting: To avoid overloading Wikipedia's servers and potential IP blocking, I implemented delays between requests.

5. Crunchbase API Limitations: The free version of the Crunchbase API wasn't sufficient for this project due to limited access and query restrictions, which is why we focused solely on Wikipedia as a data source.

## Future Improvements

1. Implement more sophisticated natural language processing techniques to improve founder name extraction accuracy.

2. Expand the search to include other reliable online sources beyond Wikipedia.

3. Develop a machine learning model to identify founder information in unstructured text more accurately.

4. Create a user interface for easier interaction with the script.

5. Implement caching to store already searched companies and reduce API calls.

6. Add support for multi-threading to process multiple companies simultaneously, improving overall speed.

7. Integrate with a database for storing and retrieving results more efficiently.

8. Implement more robust error handling and logging for better debugging and maintenance.