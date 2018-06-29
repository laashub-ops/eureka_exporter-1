import requests
import xml.etree.ElementTree
import re
import http.client
from datetime import datetime

utc_time = datetime.utcnow()
print(utc_time)

z = 0
app_list = []
eureka_url = 'http://213.183.195.222:8761/eureka/apps'
eureka_xml = requests.get(eureka_url)
eureka_list = xml.etree.ElementTree.fromstring(eureka_xml.text)
for eureka_app in eureka_list.iter('name'):
    app_name = eureka_app.text
    if app_name != 'MyOwn':
        app_list.append(app_name)
        z = z + 1
        eureka_app_url = eureka_url + '/' + app_name
        eureka_app_xml = requests.get(eureka_app_url)
        eureka_app_instance_list = xml.etree.ElementTree.fromstring(eureka_app_xml.text)
        for instance in eureka_app_instance_list.iter('instanceId'):
            if re.search(':',instance.text):
                eureka_app_instance_url = eureka_app_url + '/' + instance.text
                eureka_app_instance_xml = requests.get(eureka_app_instance_url)
                eureka_app_instance_text = xml.etree.ElementTree.fromstring(eureka_app_instance_xml.text)
                eureka_app_instance_statusurl = eureka_app_instance_text.find('statusPageUrl').text
                try:
                    eureka_app_instance_statusurl_conn = http.client.HTTPConnection(eureka_app_instance_statusurl)
                    eureka_app_instance_statusurl_conn.request("GET", "/")
                    eureka_app_instance_statusurl_conn_response = eureka_app_instance_statusurl_conn.getresponse()
                    eureka_app_instance_statusurl_status_code = eureka_app_instance_statusurl_conn_response.status
                    eureka_app_instance_statusurl_conn.close()
                except requests.exceptions.RequestException:
                    eureka_app_instance_statusurl_status_code = '001'
                print(app_name, instance.text, eureka_app_instance_statusurl, eureka_app_instance_statusurl_status_code)

print(z)
print(len(app_list))

utc_time = datetime.utcnow()
print(utc_time)
