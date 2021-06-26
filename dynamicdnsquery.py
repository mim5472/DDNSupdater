# ------------------- python3.7 ----------------#
import dns.message
import dns.query
import argparse
import requests
import logging
import sys

# logging settings and format - Timestamp - log message.
logging.basicConfig(filename='ddnsquery.log', format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


# Query your domain name using Public DNS server. Exit the script if fails.
def querydnsserver(fqdn, ns):
    dnsdata = dns.message.make_query(fqdn, dns.rdatatype.A)
    try:
        query = dns.query.udp(dnsdata, ns, timeout=5)
        answer = query.answer[0].to_text()
        return answer.split()[-1:][0]
    except Exception as e:
        logging.info(e)
        sys.exit(1)


# Check your router's Public IP address using ipfy.com API. Exit the script if fails.
def ipfyquery():
    try:
        req = requests.get('https://api.ipify.org/?format=json', timeout=10)
        data = req.json()
        return data['ip']
    except Exception as e:
        logging.info(e)
        sys.exit(1)


# Function to send update to DDNS provider using their API. Change the username/password.
# Example below is using DYNU.com DDNS provider.
def ddnsupdate():
    try:
        payload = {'username': 'XXXX', 'password': 'MD5hash'}
        apiurl = 'http://api.dynu.com/nic/update'
        updaterequest = requests.get(apiurl, params=payload, timeout=10)
        if updaterequest.status_code == 200:
            logging.info('Send request to update IP address.')
            print('Request send to DDNS provider.')
        else:
            logging.info('Unable to update IP address.')
    except Exception as e:
        logging.info(e)
        sys.exit(1)


# -------------- Main script starts here.------------------------#
# Supply 2 arguments to the script: FQDN and DNS Server.
parser = argparse.ArgumentParser()
parser.add_argument('fqdn', help='Enter Fully Qualified Domain Name.')
parser.add_argument('nsserver', help='Enter a DNS server.')
args = parser.parse_args()

# If Public DNS result is equal to IPFY result, do nothing. Log the query.
# If the the result is different, the send update to your DDNS provider using requests module.
if ipfyquery() == querydnsserver(args.fqdn, args.nsserver):
    logging.info('Query Sent to IPFY: {}, Public DNS: {}. Update: No.'.format(ipfyquery(),
                                                                  querydnsserver(args.fqdn, args.nsserver)))
else:
    logging.info('Query Sent to IPFY: {}, Public DNS: {}. Update: Yes.'.format(ipfyquery(),
                                                                  querydnsserver(args.fqdn, args.nsserver)))
    # Run the ddnsupdate function.
    ddnsupdate()

