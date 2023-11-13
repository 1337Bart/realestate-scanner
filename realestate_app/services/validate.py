import logging
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Validator:
    @staticmethod
    def validate_listing_data_entry(
        data: Dict[str, Optional[str]]
    ) -> Optional[Dict[str, Optional[str]]]:
        expected_field_types = {
            "listing_title": str,
            "price": int,
            "price_per_sqm": float,
            "rooms": int,
            "area": float,
            "url": str,
            "street": (str, type(None)),
            "district": (str, type(None)),
            "city": str,
            "voivodeship": str,
        }

        for field, expected_types in expected_field_types.items():
            if not isinstance(expected_types, tuple):
                expected_types = (expected_types,)

            value = data.get(field)

            if not isinstance(value, expected_types):
                return None

            if isinstance(value, (int, float)) and value == 0:
                return None

        return data

    @staticmethod
    def validate_listing_data(
        cleaned_data: List[Dict[str, Optional[str]]]
    ) -> List[Dict[str, Optional[str]]]:
        validated_data = []
        for entry in cleaned_data:
            validated_entry = Validator.validate_listing_data_entry(entry)
            if validated_entry:
                validated_data.append(validated_entry)

        logging.info(
            f"Finished validation. {len(validated_data)} out of {len(cleaned_data)} meet the validation criteria"
        )
        return validated_data
