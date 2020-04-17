import os
import smtplib
import socket
import time
import re
import logging
import requests
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def parse_config():
    pattern = re.compile('.*?\${(\w+)}.*?')
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    email_config = config['email']
    for key in ['password', 'from', 'to']:
        match = pattern.findall(email_config[key])
        if match:
            email_config[key] = os.environ.get(match[0])
    return email_config

def get_current_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return hostname, ip

def get_old_ip(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.readline()
    else:
        return '0.0.0.0'

def update(filename, current_ip):
    with open(filename, 'w') as f:
        f.write(current_ip)

def internet_on():
    try:
        requests.get('http://www.baidu.com')
        return True
    except requests.exceptions.ConnectionError as err: 
        return False

def send_email(email_config, hostname, ip_address):
    if email_config['computer_name']:
        hostname = email_config['computer_name']
    smtp_server = email_config.get('server')
    smtp_server_port = email_config.get('port')
    from_address = email_config.get('from')
    to_address = email_config.get('to')
    password = email_config.get('password')
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Server IP address changed"

    body = "The new IP address of {host} is: {ip}".format(host=hostname, ip=ip_address)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_server_port, timeout=60) 
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()


def main():
    filename = 'lastip.txt'
    email_config = parse_config()
    logging.basicConfig(filename='log.txt', level=logging.INFO,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    logger = logging.getLogger("Notify_IP_Change")

    while True:
        host, current_ip = get_current_ip()
        old_ip = get_old_ip(filename)
        if internet_on() and current_ip != old_ip:
            try:
                send_email(email_config, host, current_ip)
                update(filename, current_ip)
            except Exception as e:
                logger.error(e)       
        time.sleep(300)        
        

if __name__ == "__main__":
    main()
