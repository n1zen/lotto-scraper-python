from playwright.sync_api import Playwright, sync_playwright

def convert_date_string_to_tuple(date_string: str) -> tuple:
    """
    Convert a date string in the format "Month Day, Year" to a tuple (month, day, year).
    Example: "January 4, 2021" -> ("January", "4", "2021")
    """
    month, day_year = date_string.split(" ", 1)
    day, year = day_year.split(", ")
    return month, day, year

def set_starting_date(page, start_date: str) -> None:
    month, day, year = convert_date_string_to_tuple(start_date)
    page.locator("#cphContainer_cpContent_ddlStartMonth").select_option(month)
    page.locator("#cphContainer_cpContent_ddlStartDate").select_option(day)
    page.locator("#cphContainer_cpContent_ddlStartYear").select_option(year)

def set_ending_date(page, end_date: str) -> None:
    month, day, year = convert_date_string_to_tuple(end_date)
    page.locator("#cphContainer_cpContent_ddlEndMonth").select_option(month)
    page.locator("#cphContainer_cpContent_ddlEndDay").select_option(day)
    page.locator("#cphContainer_cpContent_ddlEndYear").select_option(year)

def set_date_range(page, start_date: str, end_date: str) -> None:
    set_starting_date(page, start_date)
    set_ending_date(page, end_date)
    
def set_game_name(page, game_name: str) -> None:
    if game_name.lower() == "all":
        return
    page.locator("#cphContainer_cpContent_ddlSelectGame").select_option(game_name)

def get_table_data(page, game_name: str, start_date: str, end_date: str) -> list:
    table_data = []
    set_game_name(page, game_name)
    set_date_range(page, start_date, end_date)
    page.get_by_role("button", name="Search").click()
    rows = page.get_by_role("row").all()
    for row in rows:
        cells = row.get_by_role("cell").all_text_contents()
        if cells:  # Only add rows that have data
            table_data.append(cells)
    return table_data

def print_table_data(table_data: list, headers: list) -> None:
    print("Headers:\n", headers)
    print("Table Data:\n")
    for row in table_data:
        print(row)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pcso.gov.ph/SearchLottoResult.aspx")

    # ---------------------

    # Input game name
    game_name = input("Enter the game name (if you want to see all the games, type 'all'): ")
    # Input starting date
    start_date = input("Enter the starting date (e.g., January 4, 2021): ")
    # Input ending date
    end_date = input("Enter the ending date (e.g., January 4, 2021): ")

    # Get the Headers
    headers = page.get_by_role("columnheader").all_text_contents()

    # Get the data from the table
    table_data = get_table_data(page, game_name, start_date, end_date)

    # Print the data
    print_table_data(table_data, headers)
    
    context.close()
    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()