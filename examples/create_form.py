#!/usr/bin/env python3

from __future__ import print_function
import argparse
import rspace_client


def print_forms(response):
    for form in response['forms']:
        print(form['globalId'], form['name'])


# Parse command line parameters
parser = argparse.ArgumentParser()
parser.add_argument("server", help="RSpace server URL (for example, https://community.researchspace.com)", type=str)
parser.add_argument("apiKey", help="RSpace API key can be found on 'My Profile'", type=str)
args = parser.parse_args()

client = rspace_client.Client(args.server, args.apiKey)

print('Listing all forms:')
response = client.get_forms()
print_forms(response)
# Get the remaining forms if the response is paginated
while client.link_exists(response, 'next'):
    response = client.get_link_contents(response, 'next')
    print_forms(response)

# Creates a new form
print('Creating a new form...')
fields = [
    {
      "name": "A String Field",
      "type": "String",
      "defaultValue": "An optional default value"
    },
    {
      "name": "text FormField Example",
      "type": "Text",
      "defaultValue": "Some placeholder text,can be simple <em>HTML</em>"
    },
    {
      "name": "Number FormField Example",
      "type": "Number",
      "defaultValue": 23,
      "min": 0
    },
    {
      "name": "Choice FormField Example",
      "type": "Choice",
      "multipleChoice": True,
      "options": [
        "antibody1",
        "antibody2",
        "antibody3"
      ],
      "defaultOptions": [
        "antibody2",
        "antibody3"
      ]
    },
    {
      "name": "Radio FormField Example",
      "type": "Radio",
      "options": [
        "antibody1",
        "antibody2",
        "antibody3"
      ],
      "defaultOption": "antibody2"
    },
    {
      "name": "date FormField Example",
      "type": "Date",
      "defaultValue": "2018-03-21",
      "min": "2018-02-21",
      "max": "2018-04-21"
    }
]
response = client.create_form('Test Form', tags=['testing', 'example'], fields=fields)
print('Newly created form info:', response['globalId'], response['name'])

# Get form details (these are also returned when creating a new form)
print('Getting details about a form:', response['globalId'])
response = client.get_form(response['globalId'])
print('Retrieved information about a form:', response['globalId'], response['name'])
print('Fields:')
for field in response['fields']:
    print(field['type'], field['name'])

# Publish the form
print('Publishing form:', response['globalId'])
client.publish_form(response['globalId'])

# Share the form
print('Sharing form:', response['globalId'])
client.share_form(response['globalId'])

# Unshare the form
print('Unsharing form:', response['globalId'])
client.unshare_form(response['globalId'])

# Unpublish the form
print('Unpublishing form:', response['globalId'])
client.unpublish_form(response['globalId'])