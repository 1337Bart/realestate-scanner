from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlencode, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import random
import logging

from validator import validate_listing_data


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

base_url = "https://www.otodom.pl"
cookie = "laquesis=euads-4306@b#remd-1201@a#remd-1298@b#see-1753@b#see-1767@c#see-1768@b#see-1795@a#see-1832@b#seore-490@b#sfs-572@b#smr-1204@b#smr-1912@a#smr-1927@a#smr-2032@a#smr-2130@b#smr-2237@b#smr-2267@b; laquesisff=gre-12226#rer-165#rer-166#rst-73#rst-74; laquesissu=522@my_observed_ads|0; lang=pl; dfp_user_id=46482139-9e38-4864-94b7-82bca03df28a; PHPSESSID=houertfcvm7m475q9lbukbeiav; mobile_default=desktop; ninja_user_status=unlogged; observed5_id_clipboard=64cf515115ac7; observed5_sec_clipboard=nkIDds%2BJBOza357Eyehga5f6lAS6a5Z5; optimizelyEndUserId=oeu1691308369872r0.13259982167197792; lqstatus=1691352958|189cc6c9d46x14695e8b|see-1753#seore-490#remd-1201#see-1795#see-1832#smr-1927||; ldTd=true; onap=189c4fc2da5x44dd65e3-8-189cc6c9d46x14695e8b-22-1691354654"


# TODO sprawdzic czy da sie to ograc endpointami otodom albo jakos inaczej, mniej podatnie na zmiany
# TODO dopisać enumy
def build_search_url(
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

    logging.info(url)
    return url


def scrape_listing_pages(building_type, region, transaction_type, max_pages=2):
    driver = webdriver.Chrome()
    page = 1
    all_raw_data = []

    # Wait for the 'Accept' button of the cookie consent pop-up to be clickable, and click it
    try:
        url = build_search_url(
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
        logging.error("Could not find or click the 'Accept cookies' button: %s", e)
        driver.quit()
        return []

    while page <= max_pages:
        delay = random.uniform(0.01, 0.5)
        time.sleep(delay)

        page_content = driver.page_source
        listings_data = get_listings(page_content)
        all_raw_data.extend(listings_data)

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
            logging.error("Could not find or click the 'Next' button: %s", e)
            break  # Break out of the loop if we can't go to the next page

        page += 1
        url = build_search_url(
            building_type=building_type,
            region=region,
            transaction_type=transaction_type,
            page=page,
        )
        logging.info("Now getting details from URL: %s", url)
        driver.get(url)

        time.sleep(random.uniform(0.01, 0.5))

    driver.quit()
    return all_raw_data


def get_listings(page_content):
    logging.info("Entered get_listings...")
    soup = BeautifulSoup(page_content, "lxml")
    main = soup.find("div", class_="css-1i02l4 egbyzpx3")

    if not main:
        logging.error("Main content div not found in the page.")
        return []

    listings = main.find_all("li", class_="css-o9b79t e1dfeild0")
    all_details = []

    for listing in listings:
        try:
            details = get_listing_details(listing)
            if details:
                all_details.append(details)
        except Exception as e:
            logging.error("An error occurred while getting listing details: %s", e)
            continue

    return all_details


def get_listing_details(listing):
    try:
        a_tag = listing.find("a", {"data-cy": "listing-item-link"})
        listing_url = a_tag["href"] if a_tag is not None else "URL not found"

        listing_details = listing.find("article", class_="css-1dzw04n e1n06ry50")
        if listing_details is None:
            logging.warning("Listing details not found.")
            return None

        listing_title = listing_details.find("div", class_="css-gg4vpm e1n06ry51").text
        listing_address = listing_details.find("p", class_="css-19dkezj e1n06ry53").text

        listing_overview = listing_details.find(
            "div", class_="e1jyrtvq0 css-1tjkj49 ei6hyam0"
        )
        if listing_overview is None:
            logging.warning("Listing overview not found.")
            return None

        listing_overview_spans = listing_overview.find_all("span")
        price = listing_overview_spans[0].text.strip(" ")
        price_per_sqm = listing_overview_spans[1].text
        rooms = listing_overview_spans[2].text[0]
        area = listing_overview_spans[3].text
        url = base_url + listing_url

        print(
            f"""
        Listing title: {listing_title}
        Listing address: {listing_address}
        Price: {price}
        Price per square meter: {price_per_sqm}
        Rooms: {rooms}
        Area in square meters: {area}
        URL: {url}
        """
        )

        # print format:
        # Listing title: Luksusowy Penthouse z nadzwyczanym widokiem !!
        # Listing address: Tychy, śląskie
        # Price: 949 900 zł
        # Price per square meter: 8466 zł/m²
        # Rooms: 4
        # Area in square meters: 112,2 m²
        # URL: https://www.otodom.pl/pl/oferta/luksusowy-penthouse-z-nadzwyczanym-widokiem-ID4mIj8

        return {
            "listing_title": listing_title,
            "listing_address": listing_address,
            "price": price,
            "price_per_sqm": price_per_sqm,
            "rooms": rooms,
            "area": area,
            "url": url,
        }

    except AttributeError as e:
        logging.error("Attribute error in get_listing_details: %s", e)
        return None
    except Exception as e:
        logging.error("An error occurred in get_listing_details: %s", e)
        return None


def clean_listing_data(raw_data):
    cleaned_data = []

    for data in raw_data:
        logging.info("now processing data: ", data)
        cleaned_entry = {}
        cleaned_entry["listing_title"] = data["listing_title"].strip()
        cleaned_entry["listing_address"] = data["listing_address"].strip()

        # Clean the price and handle cases where the result is an empty string
        price_cleaned = re.sub(r"[^\d]", "", data["price"])
        cleaned_entry["price"] = int(price_cleaned) if price_cleaned else 0

        # Clean the price per square meter similarly
        price_per_sqm_cleaned = re.sub(r"[^\d]", "", data["price_per_sqm"])
        cleaned_entry["price_per_sqm"] = (
            float(price_per_sqm_cleaned) if price_per_sqm_cleaned else 0
        )

        cleaned_entry["rooms"] = int(data["rooms"])
        cleaned_entry["area"] = float(data["area"].replace(" m²", "").replace(",", "."))
        cleaned_entry["url"] = str(data["url"])
        logging.info(f"cleaned_data: {str(cleaned_entry)}")
        cleaned_data.append(cleaned_entry)

    return cleaned_data


raw_data = scrape_listing_pages(
    building_type="mieszkanie", region="slaskie", transaction_type="sprzedaz"
)

cleaned_data = clean_listing_data(raw_data)

validated_data = validate_listing_data(cleaned_data)


# if validated_data:
#     # If the data is valid, proceed to save it to the database
#     # This will be implemented in the next step
#     pass
# else:
#     # If the data is invalid, print a message or handle it accordingly
#     print("Invalid data, skipping entry.")
