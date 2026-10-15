from uuid import uuid4


def generate_user_data():
    """Return a complete, unique account payload for the practice API."""
    unique_id = uuid4().hex

    return {
        "name": "API Test User",
        "email": f"api-test-{unique_id}@example.com",
        "password": "TestPassword123!",
        "title": "Mr",
        "birth_date": "15",
        "birth_month": "6",
        "birth_year": "1990",
        "firstname": "API",
        "lastname": "Tester",
        "company": "Test Company",
        "address1": "123 Test Street",
        "address2": "Suite 456",
        "country": "Canada",
        "zipcode": "M5V 1A1",
        "state": "Ontario",
        "city": "Toronto",
        "mobile_number": "4165550100",
    }


def generate_payment_data():
    """Return non-sensitive test card data accepted by the practice site."""
    return {
        "name_on_card": "API Test User",
        "card_number": "4111111111111111",
        "cvc": "123",
        "expiry_month": "12",
        "expiry_year": "2030",
    }
