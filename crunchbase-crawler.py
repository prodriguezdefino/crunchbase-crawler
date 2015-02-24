#!/usr/bin/python

import csv
import json
import urllib
import urllib2
import datetime
import pprint
import os.path
import time
import traceback

datetime_format = '%Y-%m-%d %H:%M:%S'
user_key = '8281900a2863fe0ff65072d83d93e755'
order = 'ASC'
starting_page = 12

def format_time_in_millis(millis):
    return datetime.datetime.fromtimestamp(millis).strftime(datetime_format);

def get_org_detailed(permalink):
    org_url = 'https://api.crunchbase.com/v/2/' + permalink + '?' + urllib.urlencode({'user_key': user_key})
    request = urllib2.Request(org_url)
    data = None
    try: 
       org = json.load(urllib2.urlopen(request))
       data = org['data']
       time.sleep(1)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
    except httplib.HTTPException, e:
        print 'HTTPException' + e
    except Exception:
        print 'generic exception: ' + traceback.format_exc()
    return data 

def generate_tuple(obase):
    exploded = get_org_detailed(obase['path'].encode('utf8'))
    print obase['path'].encode('utf8')
    founder = None
    website = None
    role_company = None
    secondary_role_for_profit = None
    short_description = None
    permalink = None
    primary_role = None
    is_closed = None
    closed_on_trust_code = None
    homepage_url = None
    name = None
    founded_on = None
    founded_on_trust_code = None
    closed_on = None
    num_employees_range = None
    total_funding_usd = None
    number_of_investments = None
    local_url = None
    remote_url = None

    if exploded is not None: 
        #explore json for founders info
        if 'founders' in exploded['relationships'].keys():
            founder = exploded['relationships']['founders']['items'][0]['name'].encode('utf8')
        else:
            founder = 'Not Present'
        #explore json for image info
        if 'primary_image' in exploded['relationships'].keys():
            remote_url = 'http://images.crunchbase.com/' + exploded['relationships']['primary_image']['items'][0]['path'].encode('utf8')
            filename = remote_url.split('/')[-1].split('.')[0]
            file_ext = '.'+remote_url.split('.')[-1]
            local_url = filename+file_ext
            if not os.path.isfile('images/' + local_url):
                try:
                    urllib.urlretrieve(remote_url, 'images/' + local_url)
                except Exception:
                    print 'problem retrieving image - generic exception: ' + traceback.format_exc()

        # extract properties from json
        if 'role_company' in exploded['properties'].keys() and not exploded['properties']['role_company'] is None:
            role_company = exploded['properties']['role_company']
        if 'secondary_role_for_profit' in exploded['properties'].keys() and not exploded['properties']['secondary_role_for_profit'] is None:
            secondary_role_for_profit = exploded['properties']['secondary_role_for_profit']
        if 'short_description' in exploded['properties'].keys() and not exploded['properties']['short_description'] is None:
            short_description = exploded['properties']['short_description'].encode('utf8').replace(',','|||').replace("\r","").replace("\n","")
        if 'permalink' in exploded['properties'].keys() and not exploded['properties']['permalink'] is None:
            permalink = exploded['properties']['permalink'].encode('utf8')
        if 'primary_role' in exploded['properties'].keys() and not exploded['properties']['primary_role'] is None:
            primary_role = exploded['properties']['primary_role'].encode('utf8')
        if 'is_closed' in exploded['properties'].keys() and not exploded['properties']['is_closed'] is None:
            is_closed = exploded['properties']['is_closed']
        if 'closed_on_trust_code' in exploded['properties'].keys() and not exploded['properties']['closed_on_trust_code'] is None:
            closed_on_trust_code = exploded['properties']['closed_on_trust_code']
        if 'homepage_url' in exploded['properties'].keys() and not exploded['properties']['homepage_url'] is None:
            homepage_url = exploded['properties']['homepage_url'].encode('utf8')
        if 'founded_on' in exploded['properties'].keys() and not exploded['properties']['founded_on'] is None:
            founded_on = exploded['properties']['founded_on'].encode('utf8')
        if 'founded_on_trust_code' in exploded['properties'].keys() and not exploded['properties']['founded_on_trust_code'] is None:
            founded_on_trust_code = exploded['properties']['founded_on_trust_code']
        if 'closed_on' in exploded['properties'].keys() and not exploded['properties']['closed_on'] is None:
            closed_on = exploded['properties']['closed_on']
        if 'num_employees_range' in exploded['properties'].keys() and not exploded['properties']['num_employees_range'] is None:
            num_employees_range = exploded['properties']['num_employees_range']
        if 'total_funding_usd' in exploded['properties'].keys() and not exploded['properties']['total_funding_usd'] is None:
            total_funding_usd = exploded['properties']['total_funding_usd']
        if 'number_of_investments' in exploded['properties'].keys() and not exploded['properties']['number_of_investments'] is None:
            number_of_investments = exploded['properties']['number_of_investments']
        return [
            obase['name'].encode('utf8').replace(',','|||'), 
            obase['path'].encode('utf8'), 
            obase['type'].encode('utf8'),
            obase['created_at'],
            obase['updated_at'],
            role_company,
            secondary_role_for_profit,
            short_description,
            permalink,
            primary_role,
            is_closed,
            closed_on_trust_code,
            homepage_url,
            founded_on,
            founded_on_trust_code,
            closed_on,
            num_employees_range,
            total_funding_usd,
            number_of_investments,
            founder,
            local_url,
            remote_url
        ]
    else:
        return None


def get_org_page(url, url_suffix, latest_update):
    orgs_url = url + url_suffix + urllib.urlencode({'user_key': user_key}) + '&' + urllib.urlencode({'order': 'updated_at ' + order})
    print orgs_url
    request = urllib2.Request(orgs_url)
    response = None
        
    try: 
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
    except httplib.HTTPException, e:
        print 'HTTPException' + e
    except Exception:
        import traceback
        print 'generic exception: ' + traceback.format_exc()

    if response != None:
        orgs = json.load(response)
        # strip elements with updated_at lower or equals to the actual one
        filtered = []
        for item in orgs['data']['items']:
            if float(item['updated_at']) > float(latest_update):
                filtered.append(item)
        #just for testing purposes
        #filtered = filtered[:100]
        tuples = map(generate_tuple, filtered)
        return { 'tuples' : tuples, 'paging' :  orgs['data']['paging'] }
    else:
        return None

print 'checking for file...'

file_name = 'crunchbase.csv'

latest_update = 0
if os.path.isfile(file_name):
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            latest_update = row['Updated Date']
            break
    print 'latest update: ' + str(latest_update)

print 'Getting crunchbase organizations...'

url = 'https://api.crunchbase.com/v/2/organizations?page=' + str(starting_page)
tuples = []

payload = get_org_page(url, '&', latest_update)
if payload != None:
    tuples.extend(filter(None,payload['tuples']))
    count = 0 
    while (payload != None) and (payload['paging']['next_page_url'] != None) and (count < 3):
        next_url = payload['paging']['next_page_url']
        payload = get_org_page(next_url, '&', latest_update)
        tuples.extend(filter(None,payload['tuples']))
        count = count + 1;
        with open(file_name + '.' + str(count), 'w') as itf:
            writer = csv.writer(itf, delimiter=',')
            writer.writerows(tuples)

    with open(file_name + '.new', 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(tuples)

    timestamp = time.time()
    copyTmp = 'cp crunchbase.csv crunchbase.csv-' + str(timestamp)
    stripHeaderCmd = 'tail -n +2 crunchbase.csv > crunchbase.csv.old'
    mergeCmd = 'cat crunchbase.csv.old crunchbase.csv.new > merged.csv'
    cleanCmd = 'sort -t , --key=1,5 -r merged.csv | sort -t , --key=1,1 --unique | sort -t , -k 5 -r > clean.csv'
    addHeaderCmd = 'echo "Name,Path,Type,Created Date,Updated Date,Role Company,Secondary role for profit,Short description,Permalink,Primary role,Is closed,Closed on trust code,Website,Founded on,Founded on trust code,Closed on,Num employees range,Total funding usd,Number of investments,Founders,Local url,Remote url" > crunchbase.csv'
    moveCmd = 'cat clean.csv >> crunchbase.csv' 
    removeCmd = 'rm merged.csv crunchbase.csv.new crunchbase.csv.old clean.csv' 
    os.system(copyTmp)
    os.system(stripHeaderCmd)
    os.system(mergeCmd)
    os.system(cleanCmd)
    os.system(addHeaderCmd)
    os.system(moveCmd)
    os.system(removeCmd)
    print 'file processing in ' + str(time.time() - timestamp) + ' seconds.'
else:
    print 'no data acquired'
print 'finished.'

