import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_listing_data_entry(data):
    # Define expected types for each field
    field_types = {
        "listing_title": str,
        "listing_address": str,
        "price": int,
        "price_per_sqm": float,
        "rooms": int,
        "area": float,
        "url": str,
    }

    # Iterate over each expected field and its type
    for field, expected_type in field_types.items():
        # Extract the value for the field from the data
        value = data.get(field)

        # Check if the value is of the expected type
        if not isinstance(value, expected_type):
            logging.info(
                f"Invalid type for field {field}: {type(value)} expected {expected_type}"
            )
            return None  # Discard this entry

        # Check if the value is non-zero for numeric types
        if expected_type in (int, float) and value == 0:
            logging.info(f"Zero value found for field {field}")
            return None  # Discard this entry

        # Ensure string fields are non-empty
        if expected_type == str and not value.strip():
            logging.info(f"Empty string for field {field}")
            return None  # Discard this entry

    # If all fields are valid, return the original data
    return data


# And the validate_listing_data function stays mostly the same
def validate_listing_data(cleaned_data):
    logging.info(f"Starting validation on {len(cleaned_data)} element list")
    validated_data = [
        validate_listing_data_entry(entry)
        for entry in cleaned_data
        if validate_listing_data_entry(entry) is not None
    ]

    logging.info(
        f"Finished validation. {len(validated_data)} out of {len(cleaned_data)} meet the validation criteria"
    )

    return validated_data
