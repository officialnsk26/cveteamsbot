import os
import requests
import datetime
import json
import logging
import sys
import pathlib

# API URLs and API Key
CIRCL_LU_URL = "https://cve.circl.lu/api/query"

# Path and time settings
CVES_JSON_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/output/cve-notif.json"
LAST_NEW_CVE = datetime.datetime.now() - datetime.timedelta(days=1)
LAST_MODIFIED_CVE = datetime.datetime.now() - datetime.timedelta(days=1)
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query_circl(time_filter, time_value):
    ''' Query CIRCL for CVEs based on a time filter and value '''
    params = {
        'time_modifier': 'from',
        'time_start': time_value.strftime(TIME_FORMAT),
        'time_type': time_filter
    }
    response = requests.get(CIRCL_LU_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch data from CIRCL using time filter {time_filter} starting from {time_value}")
        return None

def search_exploits(cve_id):
    ''' Mock function to search for public exploits based on CVE ID. '''
    return []  # Placeholder for actual exploit search logic

def generate_new_cve_message(cve_data: dict) -> str:
    ''' Generate new CVE message for sending to Teams '''
    message = f"🚨 *{cve_data['id']}* 🚨\n"
    message += f"🔮 *CVSS*: {cve_data.get('cvss', 'N/A')}\n"
    message += f"📅 *Published*: {cve_data.get('Published', 'N/A')}\n"
    message += "📓 *Summary*: "
    message += cve_data["summary"] if len(cve_data["summary"]) < 500 else cve_data["summary"][:500] + "..."
    if cve_data.get("vulnerable_configuration"):
        message += f"\n🔓 *Vulnerable*: " + ", ".join(cve_data["vulnerable_configuration"][:10])
    message += "\n\n🟢 ℹ️ *More information*\n" + "\n".join(cve_data.get("references", [])[:5])
    return message

def generate_modified_cve_message(cve_data: dict) -> str:
    ''' Generate modified CVE message for sending to Teams '''
    return f"📣 *{cve_data['id']}* was modified on {cve_data.get('last-modified', 'N/A').split('T')[0]} (originally published on {cve_data.get('Published', 'N/A').split('T')[0]})"

def send_msteams_message(message: str, public_expls_msg: str, title: str, color: str="000000"):
    ''' Send a message to Microsoft Teams channel '''
    webhook_url = "YOUR'S MS TEAMS WEBHOOK URL"
    full_message = message + "\n" + public_expls_msg if public_expls_msg else message
    response = requests.post(
        url=webhook_url,
        headers={"Content-Type": "application/json"},
        json={
            "themeColor": color,
            "summary": title,
            "sections": [{"activityTitle": title, "activitySubtitle": full_message.replace('\n', '<br>')}],
        }
    )
    if response.status_code == 200:
        logging.info("Message sent to Microsoft Teams successfully")
    else:
        logging.error(f"Failed to send message to Microsoft Teams. Status code: {response.status_code}")

def generate_public_expls_message(public_expls: list) -> str:
    ''' Generate the message for public exploits '''
    if public_expls:
        return "😈 *Public Exploits* (_limit 20_) 😈\n" + "\n".join(public_expls[:20])
    return ""

def main():
    print('CVE Notification Bot v1.0')
    query_results = query_circl('Published', LAST_NEW_CVE)
    if query_results:
        for cve_data in query_results['results']:
            cve_id = cve_data['id']
            message = generate_new_cve_message(cve_data)
            exploits = search_exploits(cve_id)
            exploits_message = generate_public_expls_message(exploits)
            send_msteams_message(message, exploits_message, "New CVE Alert", "0078D7")

if __name__ == "__main__":
    main()