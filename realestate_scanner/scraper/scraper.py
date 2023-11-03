from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlencode, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


base_url = "https://www.otodom.pl"

cookie = "laquesis=euads-4306@b#remd-1201@a#remd-1298@b#see-1753@b#see-1767@c#see-1768@b#see-1795@a#see-1832@b#seore-490@b#sfs-572@b#smr-1204@b#smr-1912@a#smr-1927@a#smr-2032@a#smr-2130@b#smr-2237@b#smr-2267@b; laquesisff=gre-12226#rer-165#rer-166#rst-73#rst-74; laquesissu=522@my_observed_ads|0; lang=pl; dfp_user_id=46482139-9e38-4864-94b7-82bca03df28a; PHPSESSID=houertfcvm7m475q9lbukbeiav; mobile_default=desktop; ninja_user_status=unlogged; observed5_id_clipboard=64cf515115ac7; observed5_sec_clipboard=nkIDds%2BJBOza357Eyehga5f6lAS6a5Z5; optimizelyEndUserId=oeu1691308369872r0.13259982167197792; lqstatus=1691352958|189cc6c9d46x14695e8b|see-1753#seore-490#remd-1201#see-1795#see-1832#smr-1927||; ldTd=true; onap=189c4fc2da5x44dd65e3-8-189cc6c9d46x14695e8b-22-1691354654"


# dopisać enumy
def build_url(
    building_type="mieszkanie",
    transaction_type="sprzedaz",
    region=None,
    page=1,
    limit=72,
):
    base_url = "https://www.otodom.pl"

    mandatory_url = f"/pl/wyniki/{transaction_type}/{building_type}/{region}"

    params = {}

    params["page"] = page
    params["limit"] = limit

    params["viewType"] = "listing"
    params["ownerTypeSingleSelect"] = "ALL"
    params["direction"] = "DESC"

    url = urljoin(base_url, mandatory_url)
    url += "?" + urlencode(params)

    print(url)
    return url


def get_listing_page_content(building_type, region, transaction_type):
    driver = webdriver.Chrome()
    page = 1

    # Wait for the 'Accept' button of the cookie consent pop-up to be clickable, and click it
    try:
        url = build_url(
            building_type=building_type,
            region=region,
            transaction_type=transaction_type,
        )
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        accept_cookies = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies.click()
    except Exception as e:
        print("Could not find or click the 'Accept cookies' button:", e)

    while True:
        delay = random.uniform(0.01, 0.5)
        time.sleep(delay)

        page_content = driver.page_source
        get_listings(page_content)

        try:
            # Wait until the 'Next' button is clickable
            wait = WebDriverWait(driver, 10)
            next_page = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@data-cy="pagination.next-page"]')
                )
            )
            next_page.click()
        except Exception as e:
            print(
                "Could not find or click the 'Next' button using Selenium. Trying with JavaScript...",
                e,
            )
            try:
                # Try clicking the 'Next' button using JavaScript
                next_page = driver.find_element(
                    By.XPATH, '//button[@data-cy="pagination.next-page"]'
                )  # find 'Next' button
                driver.execute_script("arguments[0].click();", next_page)
            except Exception as e:
                print("Could not find or click the 'Next' button using JavaScript:", e)
                break

        page += 1
        url = build_url(
            building_type=building_type,
            region=region,
            transaction_type=transaction_type,
            page=page,
        )
        print("Now getting details from url: ", url)
        driver.get(url)

        time.sleep(random.uniform(0.01, 0.5))

    driver.quit()


def get_listings(page_content):
    print("entered get_listings...")
    soup = BeautifulSoup(page_content, "lxml")
    main = soup.find("div", class_="css-1i02l4 egbyzpx3")
    listings = main.find_all("li", class_="css-o9b79t e1dfeild0")

    count = 0
    for listing in listings:
        count += 1
        if count == 1:
            print("listing: ", listing)
        get_listings_details(listing)


def get_listings_details(listing):
    print("Starting to fetch details...")
    # Extract the href value
    a_tag = listing.find("a", {"data-cy": "listing-item-link"})
    listing_url = a_tag["href"] if a_tag is not None else "URL not found"

    listing_details = listing.find("article", class_="css-1dzw04n e1n06ry50")
    listing_title = listing_details.find("div", class_="css-gg4vpm e1n06ry51").text
    listing_address = listing_details.find("p", class_="css-19dkezj e1n06ry53").text

    listing_overview = listing_details.find(
        "div", class_="e1jyrtvq0 css-1tjkj49 ei6hyam0"
    )
    listing_overview_spans = listing_overview.find_all("span")

    price = listing_overview_spans[0].text.strip(" ")
    price_per_sqm = listing_overview_spans[1].text
    rooms = listing_overview_spans[2].text[0]
    area = listing_overview_spans[3].text

    print(
        f"""
    Listing title: {listing_title}
    Listing address: {listing_address}
    Price: {price}
    Price per square meter: {price_per_sqm}
    Rooms: {rooms}
    Area in square meters: {area}
    URL: {base_url + listing_url}
    """
    )


get_listing_page_content(
    building_type="mieszkanie", region="slaskie", transaction_type="sprzedaz"
)
