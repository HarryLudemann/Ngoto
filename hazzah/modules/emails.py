import requests

def get_email_info(target_email):
    r = requests.get('https://emailrep.io/' + target_email ).json()
    context = {
        'email': r['email'],
        'reputation': r['reputation'],
        'suspicious': r['suspicious'],
        'references': r['references'],
        'blacklisted': r['details']['blacklisted'],
        'malicious_activity': r['details']['malicious_activity'],
        'malicious_activity_recent': r['details']['malicious_activity_recent'],
        'credentials_leaked': r['details']['credentials_leaked'],
        'credentials_leaked_recent': r['details']['credentials_leaked_recent'],
        'data_breach': r['details']['data_breach'],
        'first_seen': r['details']['first_seen'],
        'last_seen': r['details']['last_seen'],
        'domain_exists': r['details']['domain_exists'],
        'domain_reputation': r['details']['domain_reputation'],
        'new_domain': r['details']['new_domain'],
        'days_since_domain_creation': r['details']['days_since_domain_creation'],
        'suspicious_tld': r['details']['suspicious_tld'],
        'spam': r['details']['spam'],
        'free_provider': r['details']['free_provider'],
        'disposable': r['details']['disposable'],
        'deliverable': r['details']['deliverable'],
        'accept_all': r['details']['accept_all'],
        'valid_mx': r['details']['valid_mx'],
        'primary_mx': r['details']['primary_mx'],
        'spoofable': r['details']['spoofable'],
        'spf_strict': r['details']['spf_strict'],
        'dmarc_enforced': r['details']['dmarc_enforced'],
        'profiles': r['details']['profiles'],
    }
    return context