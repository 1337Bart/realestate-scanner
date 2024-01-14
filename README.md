# realestate-scanner

# Env 
## Windows
.\env\Scripts\activate

## Unix
source realeastate/bin/activate

## Start scraping. From root:
python realestate_scanner/manage.py scrape_listings


## Start calculation. From root:
python realestate_scanner/manage.py calculate_predictions


## Migrations, from root:
python realestate_scanner/manage.py makemigrations

python realestate_scanner/manage.py migrate



TODO:
1. normalize -> all strings ToSmall, removeDiacritics
2. add front