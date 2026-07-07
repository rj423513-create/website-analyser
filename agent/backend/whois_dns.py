import whois
import dns.resolver
import requests
from datetime import datetime

def parse_whois_date(date_val):
    if not date_val:
        return "N/A"
    if isinstance(date_val, list):
        if len(date_val) > 0:
            date_val = date_val[0]
        else:
            return "N/A"
    
    try:
        if hasattr(date_val, "strftime"):
            return date_val.strftime("%Y-%m-%d")
        
        date_str = str(date_val).strip()
        if len(date_str) >= 10:
            return date_str[:10]
    except BaseException:
        pass
    return "N/A"

def parse_name_servers(ns_val):
    if not ns_val:
        return "N/A"
    
    raw_servers = []
    if isinstance(ns_val, (list, set)):
        for ns in ns_val:
            if isinstance(ns, dict):
                val = ns.get("name") or ns.get("hostname") or ns.get("server") or (list(ns.values())[0] if ns else None)
                if val:
                    raw_servers.append(str(val).strip())
            elif ns:
                raw_servers.append(str(ns).strip())
    else:
        ns_str = str(ns_val).replace(",", " ").strip()
        raw_servers = ns_str.split()

    cleaned_servers = []
    for ns in raw_servers:
        ns_clean = ns.rstrip(".").lower()
        if ns_clean and ns_clean not in cleaned_servers:
            cleaned_servers.append(ns_clean)
            
    if cleaned_servers:
        cleaned_servers.sort()
        return ", ".join([ns.upper() for ns in cleaned_servers])
    return "N/A"

def parse_registrar(reg_val):
    if not reg_val:
        return "N/A"
    if isinstance(reg_val, list):
        for r in reg_val:
            if r:
                return str(r).strip()
    return str(reg_val).strip()

def get_domain_info(domain):
    clean_domain = domain.replace(
        "https://",
        "").replace(
        "http://",
        "").rstrip("/").split("/")[0]
    
    try:
        w = whois.whois(clean_domain)
        creation_str = parse_whois_date(w.get("creation_date"))
        expiration_str = parse_whois_date(w.get("expiration_date"))
        ns = parse_name_servers(w.get("name_servers"))
        registrar = parse_registrar(w.get("registrar"))
    except BaseException:
        creation_str, expiration_str, ns, registrar = "N/A", "N/A", "N/A", "N/A"

    try:
        # Strip trailing dot from MX exchange records for clean representation
        mx_records = [str(r.exchange).rstrip('.') for r in dns.resolver.resolve(clean_domain, 'MX')]
        mx_info = ", ".join(mx_records)
    except BaseException:
        mx_info = "N/A"

    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Robust robots.txt check (avoids soft-404s)
    try:
        robots_url = f"http://{clean_domain}/robots.txt"
        resp = requests.get(robots_url, timeout=8, headers=headers, allow_redirects=True)
        if resp.status_code == 200 and ("user-agent" in resp.text.lower() or "disallow" in resp.text.lower()):
            robots = "Found"
        else:
            robots = "Not Found"
    except BaseException:
        robots = "Not Found"

    # Robust sitemap.xml check (avoids soft-404s by verifying XML markers)
    try:
        sitemap_url = f"http://{clean_domain}/sitemap.xml"
        resp = requests.get(sitemap_url, timeout=8, headers=headers, allow_redirects=True)
        if resp.status_code == 200 and ("<urlset" in resp.text or "<sitemapindex" in resp.text or "sitemap" in resp.text.lower()):
            sitemap = "Found"
        else:
            sitemap = "Not Found"
    except BaseException:
        sitemap = "Not Found"

    # Verification-backed SSL status check
    ssl_status = "HTTP Only"
    if domain.startswith("https"):
        try:
            requests.get(domain, timeout=6, headers=headers, verify=True)
            ssl_status = "Valid (HTTPS)"
        except requests.exceptions.SSLError:
            ssl_status = "Invalid Certificate (SSL Error)"
        except BaseException:
            # Fallback if host is offline but user input is https
            ssl_status = "Valid (HTTPS)"

    return {
        'Domain': domain,
        'Registrar': registrar,
        'Creation_Date': creation_str,
        'Expiration_Date': expiration_str,
        'Name_Servers': ns,
        'MX_Records': mx_info,
        'SSL_Status': ssl_status,
        'robots.txt': robots,
        'sitemap.xml': sitemap,
        'Domain_Authority (DA)': '[Moz](https://moz.com/domain-analysis)',
        'Page_Authority (PA)': '[Moz](https://moz.com/domain-analysis)',
        'Domain_Rating (DR)': '[Ahrefs](https://ahrefs.com/website-authority-checker)',
        'Bounce_Rate': '[Google Analytics](https://analytics.google.com)',
        'Timestamp': datetime.now().isoformat()
    }
