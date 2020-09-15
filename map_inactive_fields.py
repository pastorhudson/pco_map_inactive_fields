import pypco
from dotenv import load_dotenv, find_dotenv
import os
import csv

load_dotenv(find_dotenv(filename='secrets.env'))

# Put your API secrets in the .env file
pco = pypco.PCO(os.environ.get('APP_ID'), os.environ.get('APP_SECRET'))

# Edit this map to change set the old Reason to the new PCO reason.
# Use https://api.planningcenteronline.com/people/v2/inactive_reasons to get the reason id's.
# Anything you want to map to "No Reason provided" set to None
# Make sure you include your own Planning Center Inactive Reasons
# https://people.planningcenteronline.com/customize#tab=personal look for "Membership Inactive Reason"
reason_map = {'Not attending': {
    "type": "InactiveReason",
    "id": "4473896"
},
    'Deceased': {
        "type": "InactiveReason",
        "id": '4426198'
    },
    'Moved': {
        "type": "InactiveReason",
        "id": '4426196'
    },
    'Death': {
        "type": "InactiveReason",
        "id": '4426198'
    },
    'Inactivity': {
        "type": "InactiveReason",
        "id": '4473897'
    },
    'Transferred': {
        "type": "InactiveReason",
        "id": '4426197'
    },
    'Joined elsewhere': {
        "type": "InactiveReason",
        "id": '4426197'
    },
    'Requested removal': {
        "type": "InactiveReason",
        "id": '5393074'
    },
    'DELETION': None,
    'Requested Removal': {
        "type": "InactiveReason",
        "id": '5393074'
    },
    'Transfer': {
        "type": "InactiveReason",
        "id": '4426197'
    },
    'Not Attending': {
        "type": "InactiveReason",
        "id": '4473896'
    },
    'Other': None,
    'Moved to new church': {
        "type": "InactiveReason",
        "id": '4426197'
    }}

# Create a list of people that have your two inactive custom fields populated
list_result = pco.iterate('https://api.planningcenteronline.com/people/v2/lists/<LIST_ID>/people')

# A CSV file will be created with all the updated profiles.
with open('people_maped.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_NONE)
    writer.writerow(['pco_id', 'name', 'current_inactive_date', 'current_inactive_reason_id', 'current_inactive_reason', 'removed_by_date', 'removed_by_reason', 'link'])
    for r in list_result:
        person = pco.get(f'/people/v2/people/{r["data"]["id"]}?include=field_data,inactive_reason')
        removed_by_date = ""
        rbd_split = ""
        link = ""
        for d in person['included']:
            link = f"https://people.planningcenteronline.com/people/AC{person['data']['id']}"
            try:
                # Set the correct ID for your custom field_definition's Inactive Date
                if d['relationships']['field_definition']['data']['id'] == '364583':
                    removed_by_date = d['attributes']['value']
                    rbd_split = "/".join(
                        [removed_by_date.split('/')[1], removed_by_date.split('/')[0], removed_by_date.split('/')[2]])
                # Set the correct ID for your custom field_definition's Inactive Reason
                if d['relationships']['field_definition']['data']['id'] == '364582':
                    removed_by_reason = d['attributes']['value']
            except Exception as e:
                pass

        inactive_reason_id = "None"
        inactive_reason = "None"
        try:
            inactive_reason_id = person['data']['relationships']['inactive_reason']['data']['id']
            inactive_reason = pco.get(f'/people/v2/inactive_reasons/{inactive_reason_id}')['data']['attributes']['value']
        except Exception as e:
            pass

        person_payload = {
            "data": {
                "attributes": {'status': 'inactive', 'inactivated_at': rbd_split, },
                "relationships": {
                    "inactive_reason": {
                        "data": reason_map[removed_by_reason]
                    }
                }
            }
        }

        row = [person['data']['id'],
               person['data']['attributes']['name'],
               person['data']['attributes']['inactivated_at'],
               inactive_reason_id,
               inactive_reason,
               removed_by_date,
               removed_by_reason,
               link]
        writer.writerow(row)

        print(person_payload)
        print(row)
        pco.patch(f'/people/v2/people/{person["data"]["id"]}', person_payload)
