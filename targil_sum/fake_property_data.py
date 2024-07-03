"""written and submitted by David Koplev 208870279 and Rotem Kashani 209073352"""

from faker import Faker
import json
from decimal import Decimal

# Initialize Faker with en_US locale
fake = Faker('en_US')

# Create a list of 185,000 fake property data records
fake_data = []
for _ in range(185000):
    property_data = {
        "transaction_id": str(fake.uuid4()),
        "price": str(fake.pydecimal(left_digits=6, right_digits=2, positive=True)),
        "transfer_date": str(fake.date_between(start_date='-10y', end_date='today')),
        "property_type": fake.random_element(elements=('D', 'S', 'T', 'F', 'O')),
        "old_new": fake.random_element(elements=('Y', 'N')),
        "duration": fake.random_element(elements=('F', 'L')),
        "town_city": fake.city(),
        "district": fake.state_abbr(),
        "county": fake.state(),
        "ppd_category_type": fake.random_element(elements=('A', 'B')),
        "record_status": fake.random_element(elements=('A', 'C', 'D'))
    }
    fake_data.append(property_data)

# Save the fake data to a JSON file
with open('fake_property_data.json', 'w') as f:
    json.dump(fake_data, f, indent=4)

print("185,000 unique property records have been generated and saved to 'fake_property_data.json'.")