import re


def prepare_listing_entry(entry):
    cleaned_entry = {}
    cleaned_entry["listing_title"] = entry["listing_title"].strip()

    price_cleaned = re.sub(r"[^\d]", "", entry["price"])
    cleaned_entry["price"] = int(price_cleaned) if price_cleaned else 0

    price_per_sqm_cleaned = re.sub(r"[^\d]", "", entry["price_per_sqm"])
    cleaned_entry["price_per_sqm"] = (
        float(price_per_sqm_cleaned) if price_per_sqm_cleaned else 0
    )

    cleaned_entry["rooms"] = int(entry["rooms"])
    cleaned_entry["area"] = float(entry["area"].replace(" m²", "").replace(",", "."))
    cleaned_entry["url"] = str(entry["url"])

    granular_address_details = extract_listing_address(entry["listing_address"].strip())
    cleaned_entry.update(granular_address_details)

    return cleaned_entry


def extract_listing_address(address):
    address_parts = address.split(", ")
    # Initialize all parts as None
    street, district, city, voivodeship = (None, None, None, None)

    # Assign based on the number of components
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


def prepare_listing_data(raw_data):
    cleaned_data = []

    for data_entry in raw_data:
        cleaned_entry = prepare_listing_entry(data_entry)
        cleaned_data.append(cleaned_entry)

    return cleaned_data
