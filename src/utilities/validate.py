import re

def is_valid_ip_or_domain(address):
    """Validate an IP address or a domain name."""
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    domain_pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    
    if re.match(ip_pattern, address):
        # Check if all octets are between 0 and 255
        parts = address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    elif re.match(domain_pattern, address):
        return True
    else:
        return False
