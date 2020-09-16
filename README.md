# pco_map_inactive_fields
This is a basic script to use information imported into Custom Fields to update inactive status Reason, and Date in Planning Center Online.

### Why This Exists
A client had imported inactive reason, and inactive date to custom people fields from their previous ChMS "Shephard Staff".
Upon import they realized they needed to mark profiles as "Inactive" and set the inactive reason. This was close to 2000 records so it wasn't a quick easy task.
They graciously allowed me to post this as open source incase another church needs it.

### Instructions
- Edit secrets.env Adding your own Personal Access Tokens from https://api.planningcenteronline.com/oauth/applications
- Update the reasons_map at the top of map_inactive_fields.py
    - Use https://api.planningcenteronline.com/people/v2/inactive_reasons to get the reason id's.
    - Anything you want to map to "No Reason provided" set to None
    - If you need to edit Inactive Reasons do so here https://people.planningcenteronline.com/customize#tab=personal look for "Membership Inactive Reason".
- Create a list of people that have your two inactive custom fields populated
- Add that list id in the line: `list_result = pco.iterate('https://api.planningcenteronline.com/people/v2/lists/<LIST_ID>/people')
`
- Set the correct ID for your custom field_definition's Inactive Date on line 84:
`                if d['relationships']['field_definition']['data']['id'] == '<FIELD_DEFINITION_ID>':`
- Set the correct ID for your custom field_definition's Inactive Reason on line 89:
`                if d['relationships']['field_definition']['data']['id'] == '<FIELD_DEFINITION_ID>':`
- Comment out line 128 `pco.patch(f'/people/v2/people/{person["data"]["id"]}', person_payload)` to do a dry run.
- Examine the newly created `people_maped.csv` to see if the data looks correct.
- If all looks good uncomment line 128 and run the script again.
- Correct output should look like this:
    - The first line is the update payload.
    - The second line is the current information.
```
{'data': {'attributes': {'status': 'inactive', 'inactivated_at': '13/08/2013'}, 'relationships': {'inactive_reason': {'data': {'type': 'InactiveReason', 'id': '4454896'}}}}}
['75417445', 'John Doe', 'None', 'None', 'None', '09/13/2011', 'Not attending', 'https://people.planningcenteronline.com/people/AC760000']
```
I hope this helps you and your church in some way.
Thanks to Christ Lutheran Church for allowing me to share this.


