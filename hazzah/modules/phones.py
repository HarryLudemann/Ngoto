import requests

def get_phone_info(target_phone, NUM_VERIFY_API_KEY):
    r = requests.get(f"http://apilayer.net/api/validate?access_key={NUM_VERIFY_API_KEY}&number={target_phone } ").json()
    context = {
        'valid': r['valid'],
        'number': r['number'],
        'local_format': r['local_format'],
        'international_format': r['international_format'],
        'country_prefix': r['country_prefix'],
        'country_code': r['country_code'],
        'country_name': r['country_name'],
        'location': r['location'],
        'carrier': r['carrier'],
        'line_type': r['line_type'],
    }
    return context