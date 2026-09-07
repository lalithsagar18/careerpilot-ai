import ipaddress
import urllib.parse
import socket
import re
import httpx

class SafeURLScraper:
    """
    Safely retrieves and extracts readable text from public job URLs
    while strictly protecting against SSRF, internal network scans,
    and prompt injection payload vectors.
    """

    BLOCKED_IPS = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
        "169.254.169.254",  # AWS/Cloud Metadata
    ]

    @classmethod
    def is_safe_url(cls, url: str) -> bool:
        try:
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme not in ["http", "https"]:
                return False
            
            hostname = parsed.hostname
            if not hostname:
                return False
                
            if hostname.lower() in cls.BLOCKED_IPS:
                return False

            # Resolve DNS and check if IP is private
            ip_str = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip_str)

            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return False

            return True
        except Exception:
            return False

    @classmethod
    async def fetch_job_text(cls, url: str) -> str:
        if not cls.is_safe_url(url):
            raise ValueError("URL is prohibited or could not be safely resolved.")

        headers = {
            "User-Agent": "CareerPilot-JobAnalyzer/1.0 (+https://careerpilot.ai/bot)"
        }
        
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, max_redirects=3) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            # Simple clean text parsing (strip HTML scripts and tags)
            html = response.text
            # Remove scripts and style elements
            cleaned = re.sub(r'<(script|style).*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
            # Remove HTML tags
            cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
            # Normalize whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned)
            return cleaned.strip()[:15000]  # truncate to 15k characters
