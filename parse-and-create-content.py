import xml.etree.ElementTree as ET
import os
from slugify import slugify

# Parse XML file
tree = ET.parse('mobile-broadband-provider-info/serviceproviders.xml')
root = tree.getroot()

# Specify the Hugo content directory
hugo_content_dir = 'web/content/'

# Iterate through countries and providers
for country in root.findall('.//country'):
    country_code = country.get('code')
    country_name = slugify(country.find('name').text)

    # Create a directory for the country if it doesn't exist
    country_dir = os.path.join(hugo_content_dir, country_name)
    os.makedirs(country_dir, exist_ok=True)

    for provider in country.findall('.//provider'):
        provider_name = provider.find('name').text

        # Create a slugified version of the provider name for the directory and content file name
        provider_slug = slugify(provider_name)

        # Generate provider directory path
        provider_dir = os.path.join(country_dir, provider_slug)
        os.makedirs(provider_dir, exist_ok=True)

        # Generate content file path (index.md)
        content_path = os.path.join(provider_dir, 'index.md')

        networkid_element = provider.find('.//network-id')
        networkid_mcc = networkid_element.get('mcc') if networkid_element is not None else ""
        networkid_mnc = networkid_element.get('mnc') if networkid_element is not None else ""
        

        # Create front matter for the content file
        front_matter = f'''---
title: "{provider_name}"
country_code: "{country_code}"
country_name: "{country_name}"
networkid_mcc: "{networkid_mcc}"
networkid_mnc: "{networkid_mnc}"
apns:
'''

        # Iterate through APNs and add them to the front matter
        for apn in provider.findall('.//apn'):
            # Check if the 'name' element exists
            name_element = apn.find('name')
            apn_name = name_element.text if name_element is not None else ""

            apn_value = apn.get('value')

            plan_element = apn.find('.//plan')
            plan_type = plan_element.get('type') if plan_element is not None else ""

            usage_element = apn.find('.//usage')
            usage_type = usage_element.get('type') if usage_element is not None else ""
            
            gateway_element = apn.find('gateway')
            gateway = gateway_element.text if gateway_element is not None else ""
            
            username_element = apn.find('username')
            username = username_element.text if username_element is not None else ""

            password_element = apn.find('password')
            # need to replace due a possible typo/bug in Telekom Srbija password data
            password = password_element.text.replace('"', '\\"') if password_element is not None and password_element.text is not None else ""
            
            authentication_element = apn.find('authentication')
            authentication = authentication_element.text if authentication_element is not None else ""
            
            dns_elements = apn.findall('dns')
            dns_values = [dns.text for dns in dns_elements]
            
            mmsc_element = apn.find('mmsc')
            mmsc = mmsc_element.text if mmsc_element is not None else ""
            
            mmsproxy_element = apn.find('mmsproxy')
            mmsproxy = mmsproxy_element.text if mmsproxy_element is not None else ""
            
            mmsattachmentsize_element = apn.find('mmsattachmentsize')
            mmsattachmentsize = mmsattachmentsize_element.text if mmsattachmentsize_element is not None else ""
 
            front_matter += f'''  - name: "{apn_name}"
    value: "{apn_value}"
    plan_type: "{plan_type}"
    usage_type: "{usage_type}"
    gateway:    "{gateway}"
    username: "{username}"
    password: "{password}"
    authentication: "{authentication}"
    dns: "{dns_values}"
    mmsc: "{mmsc}"
    mmsproxy: "{mmsproxy}"
    mmsattachmentsize: "{mmsattachmentsize}"
'''

        front_matter += '---\n'

        # Write front matter to the content file (index.md)
        with open(content_path, 'w') as content_file:
            content_file.write(front_matter)


