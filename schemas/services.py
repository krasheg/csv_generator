from faker import Faker


def fake_data(column_type, value_range=(0, 10)):
    faker = Faker()
    allowed_methods = {
        'Full name': faker.name(),
        'Job': faker.job(),
        'Email': faker.safe_email(),
        'Company': faker.company(),
        'Integer': faker.random_int(*value_range),
        'Address': faker.address()
    }
    return allowed_methods[column_type]
