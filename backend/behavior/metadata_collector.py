import uuid
import hashlib
from datetime import datetime
from ipaddress import ip_network


def extract_ip_prefix(ip_address: str):
    try:
        return str(ip_network(ip_address + "/24", strict=False))
    except:
        return None


def generate_device_fingerprint(user_agent: str, ip: str):
    raw = user_agent + ip
    return hashlib.sha256(raw.encode()).hexdigest()


def collect_login_metadata(request, user_id: int, username: str):
    now = datetime.utcnow()

    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    metadata = {
        "user_id": user_id,
        "username": username,
        "timestamp": now.isoformat(),
        "hour": now.hour,
        "day_of_week": now.weekday(),
        "ip_address": ip,
        "ip_prefix": extract_ip_prefix(ip),
        "location_country": None,  # integrate GeoIP later
        "location_city": None,
        "device_fingerprint": generate_device_fingerprint(user_agent, ip),
        "device_type": "desktop",  # can parse user-agent
        "os": "Unknown",
        "browser": "Unknown",
        "resource": "login",
        "action": "login_success",
        "session_id": str(uuid.uuid4()),
        "session_duration": 0,
        "vpn_detected": 0,
        "proxy_detected": 0
    }

    return metadata
