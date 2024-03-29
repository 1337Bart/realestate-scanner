import re
from typing import Dict, List, Optional


class DataPrepare:
    @staticmethod
    def prepare_listing_entry(entry: Dict[str, str]) -> Optional[Dict[str, str]]:
        if not isinstance(entry, dict):
            print("Warning: Entry is not a dictionary. Skipping... Entry:", entry)
            return None
        if entry:
            cleaned_entry = {}
            cleaned_entry["listing_title"] = (
                entry["listing_title"].strip()
                if "listing_title" in entry and entry["listing_title"]
                else "missing"
            )

            price_cleaned = re.sub(r"[^\d]", "", entry["price"])
            cleaned_entry["price"] = int(price_cleaned) if price_cleaned else 0

            price_per_sqm_cleaned = re.sub(r"[^\d]", "", entry["price_per_sqm"])
            cleaned_entry["price_per_sqm"] = (
                float(price_per_sqm_cleaned) if price_per_sqm_cleaned else 0
            )

            cleaned_entry["rooms"] = int(entry["rooms"])
            cleaned_entry["area"] = float(
                entry["area"].replace(" m²", "").replace(",", ".")
            )
            cleaned_entry["url"] = str(entry["url"])

            granular_address_details = DataPrepare.extract_listing_address(
                entry["listing_address"].strip()
            )
            cleaned_entry.update(granular_address_details)

            return cleaned_entry

    @staticmethod
    def extract_listing_address(address: str) -> Dict[str, Optional[str]]:
        address_parts = address.split(", ")
        street, district, city, voivodeship = (None, None, None, None)

        if len(address_parts) == 4:
            street, district, city, voivodeship = address_parts
        elif len(address_parts) == 3:
            district, city, voivodeship = address_parts
        elif len(address_parts) == 2:
            city, voivodeship = address_parts
        elif len(address_parts) == 1:
            voivodeship = address_parts[0]

        return {
            "street": street,
            "district": district,
            "city": city,
            "voivodeship": voivodeship,
        }

    @staticmethod
    def prepare_listing_data(raw_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        cleaned_data = []

        for data_entry in raw_data:
            cleaned_entry = DataPrepare.prepare_listing_entry(data_entry)
            if cleaned_entry:
                cleaned_data.append(cleaned_entry)
            else:
                continue

        return cleaned_data
