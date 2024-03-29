import time
import random
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

base_url = "https://www.otodom.pl"
cookie = "laquesis=euads-4306@b#remd-1201@a#remd-1298@b#see-1753@b#see-1767@c#see-1768@b#see-1795@a#see-1832@b#seore-490@b#sfs-572@b#smr-1204@b#smr-1912@a#smr-1927@a#smr-2032@a#smr-2130@b#smr-2237@b#smr-2267@b; laquesisff=gre-12226#rer-165#rer-166#rst-73#rst-74; laquesissu=522@my_observed_ads|0; lang=pl; dfp_user_id=46482139-9e38-4864-94b7-82bca03df28a; PHPSESSID=houertfcvm7m475q9lbukbeiav; mobile_default=desktop; ninja_user_status=unlogged; observed5_id_clipboard=64cf515115ac7; observed5_sec_clipboard=nkIDds%2BJBOza357Eyehga5f6lAS6a5Z5; optimizelyEndUserId=oeu1691308369872r0.13259982167197792; lqstatus=1691352958|189cc6c9d46x14695e8b|see-1753#seore-490#remd-1201#see-1795#see-1832#smr-1927||; ldTd=true; onap=189c4fc2da5x44dd65e3-8-189cc6c9d46x14695e8b-22-1691354654"


class Scraper:
    base_url = "https://www.otodom.pl"

    def __init__(self):
        self.driver = webdriver.Chrome()

    def build_search_url(
        self,
        building_type: str = "mieszkanie",
        transaction_type: str = "sprzedaz",
        region: Optional[str] = None,
        page: int = 1,
        limit: int = 72,
    ) -> str:
        mandatory_url = f"/pl/wyniki/{transaction_type}/{building_type}/{region}"
        params = {
            "page": page,
            "limit": limit,
            "viewType": "listing",
            "ownerTypeSingleSelect": "ALL",
            "direction": "DESC",
        }
        url = urljoin(self.base_url, mandatory_url)
        url += "?" + urlencode(params)
        logging.info(url)
        return url

    def scrape_listing_pages(
        self,
        building_type: str,
        region: str,
        transaction_type: str,
        max_pages: int = 1,
    ) -> List[Dict]:
        self.driver = webdriver.Chrome()
        all_raw_data = []

        try:
            url = self.build_search_url(
                building_type=building_type,
                region=region,
                transaction_type=transaction_type,
            )
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)
            accept_cookies = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_cookies.click()
        except Exception as e:
            logging.error("Could not find or click the 'Accept cookies' button: %s", e)
            self.driver.quit()
            return []

        page = 1
        while page <= max_pages:
            delay = random.uniform(0.01, 0.5)
            time.sleep(delay)

            page_content = self.driver.page_source
            listings_data = self.get_listings(page_content)
            all_raw_data.extend(listings_data)

            try:
                # Wait until the 'Next' button is clickable
                wait = WebDriverWait(self.driver, 10)
                next_page = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[@data-cy="pagination.next-page"]')
                    )
                )
                next_page.click()
            except Exception as e:
                logging.error("Could not find or click the 'Next' button: %s", e)
                break

            page += 1
            url = self.build_search_url(
                building_type=building_type,
                region=region,
                transaction_type=transaction_type,
                page=page,
            )
            logging.info("Now getting details from URL: %s", url)
            self.driver.get(url)

            time.sleep(random.uniform(0.01, 0.5))

        self.driver.quit()
        return all_raw_data

    def get_listings(self, page_content: str) -> List[Dict]:
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
                details = self.get_listing_details(listing)
                if details:
                    all_details.append(details)
            except Exception as e:
                logging.error("An error occurred while getting listing details: %s", e)
                continue

        return all_details

    def get_listing_details(self, listing) -> Optional[Dict]:
        try:
            a_tag = listing.find("a", {"data-cy": "listing-item-link"})
            listing_url = a_tag["href"] if a_tag is not None else "URL not found"

            listing_details = listing.find("article", class_="css-1dzw04n e1n06ry50")
            if listing_details is None:
                logging.warning("Listing details not found.")
                return None

            listing_title = listing_details.find(
                "div", class_="css-gg4vpm e1n06ry51"
            ).text
            listing_address = listing_details.find(
                "p", class_="css-19dkezj e1n06ry53"
            ).text

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


# scraper = Scraper()
# raw_data = scraper.scrape_listing_pages(
#     building_type="mieszkanie",
#     region="slaskie",
#     transaction_type="sprzedaz",
#     max_pages=3,
# )

# cleaned_listings = DataPrepare.prepare_listing_data(raw_data)
# validated_listings = Validator.validate_listing_data(cleaned_listings)


# if validated_listings:
#     Saver.save_listings(validated_listings)
