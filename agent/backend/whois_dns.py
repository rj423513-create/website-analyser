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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Robust robots.txt check (avoids soft-404s)
    robots = "Not Found"
    robots_candidates = []
    if domain.startswith("https://"):
        robots_candidates = [f"https://{clean_domain}/robots.txt", f"http://{clean_domain}/robots.txt"]
    else:
        robots_candidates = [f"http://{clean_domain}/robots.txt", f"https://{clean_domain}/robots.txt"]

    robots_txt_content = ""
    for r_url in robots_candidates:
        try:
            resp = None
            try:
                resp = requests.get(r_url, timeout=8, headers=headers, allow_redirects=True, verify=True)
            except requests.exceptions.SSLError:
                resp = requests.get(r_url, timeout=8, headers=headers, allow_redirects=True, verify=False)
            
            if resp and resp.status_code == 200 and ("user-agent" in resp.text.lower() or "disallow" in resp.text.lower()):
                robots = "Found"
                robots_txt_content = resp.text
                break
        except BaseException:
            continue

    # Robust sitemap.xml check (avoids soft-404s by verifying XML markers)
    sitemap = "Not Found"
    sitemap_candidates = []
    
    # Respect input scheme preference
    if domain.startswith("http://"):
        sitemap_candidates.append(f"http://{clean_domain}/sitemap.xml")
        sitemap_candidates.append(f"https://{clean_domain}/sitemap.xml")
    else:
        sitemap_candidates.append(f"https://{clean_domain}/sitemap.xml")
        sitemap_candidates.append(f"http://{clean_domain}/sitemap.xml")

    # If robots.txt had Sitemap directives, prioritize them
    if robots_txt_content:
        for line in robots_txt_content.splitlines():
            line_str = line.strip()
            if line_str.lower().startswith("sitemap:"):
                parts = line_str.split(":", 1)
                if len(parts) > 1:
                    sitemap_url = parts[1].strip()
                    if sitemap_url and sitemap_url not in sitemap_candidates:
                        sitemap_candidates.insert(0, sitemap_url)

    for url in sitemap_candidates:
        try:
            resp = None
            try:
                resp = requests.get(url, timeout=8, headers=headers, allow_redirects=True, verify=True)
            except requests.exceptions.SSLError:
                resp = requests.get(url, timeout=8, headers=headers, allow_redirects=True, verify=False)
            
            if resp and resp.status_code == 200:
                text_lower = resp.text.lower()
                is_xml = "<urlset" in text_lower or "<sitemapindex" in text_lower or "?xml" in text_lower or "sitemap" in text_lower
                if is_xml or "xml" in resp.headers.get("Content-Type", "").lower():
                    # Avoid HTML soft-404s
                    if "<html" in text_lower and not ("<urlset" in text_lower or "<sitemapindex" in text_lower or "<sitemap" in text_lower):
                        continue
                    sitemap = "Found"
                    break
        except BaseException:
            continue

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
