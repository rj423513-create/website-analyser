import requests
import time

def get_gtmetrix_screenshot(url, api_key):
    post_url = "https://gtmetrix.com/api/2.0/tests"
    headers = {"Content-Type": "application/vnd.api+json"}
    payload = {
        "data": {
            "type": "test",
            "attributes": {
                "url": url
            }
        }
    }

    try:
        resp = requests.post(
            post_url,
            json=payload,
            auth=(api_key, ""),
            headers=headers,
            timeout=15)
        if resp.status_code != 201:
            return None, f"GTMetrix test start failed: {resp.status_code} {resp.reason}"

        test_data = resp.json()
        test_id = test_data["data"]["id"]

        # Poll up to 30 times (90 seconds total)
        for _ in range(30):
            time.sleep(3)
            status_url = f"https://gtmetrix.com/api/2.0/tests/{test_id}"
            status_resp = requests.get(
                status_url, auth=(api_key, ""), timeout=15)

            if status_resp.status_code == 200:
                status_data = status_resp.json()
                state = status_data["data"]["attributes"]["state"]

                if state == "completed":
                    report_id = status_data["data"]["attributes"].get("report")
                    if report_id:
                        screenshot_url = f"https://gtmetrix.com/api/2.0/reports/{report_id}/resources/screenshot"
                        img_resp = requests.get(
                            screenshot_url, auth=(api_key, ""), timeout=20)
                        if img_resp.status_code == 200:
                            return img_resp.content, None
                        else:
                            return None, f"Failed to download screenshot: {img_resp.status_code}"
                elif state in ["error", "canceled"]:
                    return None, f"GTMetrix test state error: {state}"
            else:
                return None, f"Failed polling status: {status_resp.status_code}"

        return None, "GTMetrix test timed out"
    except Exception as e:
        return None, f"Error: {str(e)}"
