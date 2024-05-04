
import re


def is_valid_ip(ip):
    """Validate an IP address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None