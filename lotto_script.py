import re
from playwright.sync_api import Playwright, sync_playwright, expect

def get_table_data(page) -> list:
    table_data = []
    rows = page.get_by_role("row").all()
    for row in rows:
        cells = row.get_by_role("cell").all_text_contents()
        if cells:  # Only add rows that have data
            table_data.append(cells)
    return table_data


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pcso.gov.ph/SearchLottoResult.aspx")

    # ---------------------

    # Get the Headers
    headers = page.get_by_role("columnheader").all_text_contents()
    print("Headers:", headers)

    # Get the data from the table
    table_data = get_table_data(page)

    print("Table Data:")
    for row in table_data:
        print(row)

    
    context.close()
    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()