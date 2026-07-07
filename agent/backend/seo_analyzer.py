import whois
import dns.resolver
import requests
from bs4 import BeautifulSoup
import time
import uuid
from datetime import datetime
from config import RATE_LIMIT_DELAY
from .whois_dns import parse_whois_date, parse_name_servers, parse_registrar

def safe_request(url, timeout=10):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DomainSEOAgent/1.0)"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp
    except BaseException:
        return None


def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        creation_str = parse_whois_date(w.get("creation_date"))
        expiration_str = parse_whois_date(w.get("expiration_date"))
        ns = parse_name_servers(w.get("name_servers"))
        registrar = parse_registrar(w.get("registrar"))
            
        return {
            "Registrar": registrar,
            "Creation_Date": creation_str,
            "Expiration_Date": expiration_str,
            "Name_Servers": ns,
        }
    except BaseException:
        return {"Registrar": "N/A"}


def get_dns_records(domain):
    records = {"A": [], "MX": [], "NS": [], "TXT": []}
    for rtype in records.keys():
        try:
            answers = dns.resolver.resolve(domain, rtype, lifetime=5)
            for rdata in answers:
                records[rtype].append(str(rdata))
        except BaseException:
            pass
    return {k: ", ".join(v) if v else "N/A" for k, v in records.items()}


def get_builtwith_info(domain):
    try:
        resp = safe_request(f"https://builtwith.com/{domain}")
        if resp:
            soup = BeautifulSoup(resp.text, 'html.parser')
            techs = [t.get_text(strip=True)
                     for t in soup.select(".techLink, a")[:12]]
            return {"Tech_Stack": ", ".join(techs)[:800] or "N/A"}
    except BaseException:
        pass
    return {"Tech_Stack": "N/A"}


def generate_seo_issues(domain):
    issues = []
    # Generate sample SEO issues for demo
    issue_types = [
        "Missing Meta Title",
        "Slow Loading Speed",
        "Broken Internal Links",
        "No HTTPS",
        "Duplicate Content"]
    for i in range(3):  # Generate 3 issues per domain
        issue = {
            "Issue_ID": str(uuid.uuid4())[:8],
            "Issue_Name": issue_types[i % len(issue_types)],
            "Issue_Type": "Error" if i % 2 == 0 else "Warning",
            "Issue_Category": "On-Page SEO" if i == 0 else "Performance",
            "Priority": "High" if i == 0 else "Medium",
            "Severity_Score": 85 - i * 10,
            "URL": f"https://{domain}",
            "Affected_URLs_Count": 1,
            "Page_Title": f"Home | {domain}",
            "Status_Code": 200,
            "Issue_Description": f"Detected issue on {domain}",
            "Impact": "Affects search rankings",
            "Recommendation": "Fix recommended action",
            "Detection_Method": "Automated Crawl",
            "First_Seen": datetime.now().strftime("%Y-%m-%d"),
            "Last_Seen": datetime.now().strftime("%Y-%m-%d"),
            "Assigned_To": "Team",
            "Fix_Status": "Open",
            "Estimated_Effort": "Medium",
            "Confidence_Score": 90,
            "Crawl_Depth": 1,
            "Internal_Links_Count": 45,
            "External_Links_Count": 12,
            "Canonical_URL": f"https://{domain}",
            "Robots_Status": "Indexable",
            "Meta_Robots": "index, follow",
            "Hreflang_Status": "Valid",
            "Mobile_Friendly": "Yes",
            "Core_Web_Vitals_Impact": "LCP affected",
            "Screenshot_Evidence": f"https://image.thum.io/get/https://{domain}"
        }
        issues.append(issue)
    return issues


def analyze_domain(domain: str):
    time.sleep(RATE_LIMIT_DELAY)
    whois_data = get_whois_info(domain)
    dns_data = get_dns_records(domain)
    built_data = get_builtwith_info(domain)
    seo_issues = generate_seo_issues(domain)

    base = {"Domain": domain}
    base.update(whois_data)
    base.update(dns_data)
    base.update(built_data)

    # Return both base + SEO issues (flattened for Excel)
    return base, seo_issues
