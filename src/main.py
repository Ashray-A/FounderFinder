from wikipedia_scraper import scrape_wikipedia
import pandas as pd
import os
import time

def process_company(company_name):
    result = scrape_wikipedia(company_name)
    print(f"Company: {result['company']}")
    print(f"Founder(s): {result['founder']}")
    print()

def main():
    while True:
        print("\nChoose an option:")
        print("1. Search for a single company")
        print("2. Process companies from CSV file")
        print("3. Exit")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        
        if choice == '1':
            company_name = input("Enter the company name: ")
            process_company(company_name)
        
        elif choice == '2':
            input_file = input("Enter the path to your CSV file (or press Enter for default 'data/input_companies.csv'): ")
            if not input_file:
                input_file = os.path.join('data', 'input_companies.csv')
            
            if not os.path.exists(input_file):
                print(f"File not found: {input_file}")
                continue
            
            print(f"Reading input CSV from {input_file}...")
            input_df = pd.read_csv(input_file)
            print(f"Found {len(input_df)} companies in the input file.")
            
            results = []
            for company in input_df['company_name']:
                result = scrape_wikipedia(company)
                results.append(result)
                print(f"Processed: {company}")
                print(f"Founder(s): {result['founder']}")
                print()
                time.sleep(1)  # Be nice to Wikipedia
            
            output_file = os.path.join('data', 'founder_results.csv')
            pd.DataFrame(results).to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")
        
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()