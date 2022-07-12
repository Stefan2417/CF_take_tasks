import requests
import json
import random
from collections import Counter


def search(arr, key):
    l = 0
    r = len(arr) - 1
    ans = -1
    while l <= r:
        c = (l + r) // 2
        if arr[c] <= key:
            ans = c
            l = c + 1
        else:
            r = c - 1
    if ans == -1 or arr[ans] != key:
        return False
    else:
        return True


URL_PROBLEMSET = 'https://codeforces.com/api/problemset.problems'
URL_USER_SUBMISSONS = 'https://codeforces.com/api/user.status'
URL_PROBLEM = 'https://codeforces.com/contest'

f = open('input.json')
data = json.load(f)
f.close()
tags = ''
for i in data['tags']:
    tags = tags + i + ';'
tags = tags[:-1]
headers_tags = {'tags': tags}
ban = []

for i in range(len(data['handles'])):
    headers_user = {'handle': data['handles'][i]}
    submissions = requests.get(URL_USER_SUBMISSONS, params=headers_user).json()
    if submissions['status'] != 'OK':
        print('USER ' + data['handles'][i] + ' NOT FOUND\n')
    else:
        submissions = submissions['result']
        for j in range(len(submissions)):
            if submissions[j].get('problem') != None and submissions[j]['problem'].get('contestId') != None:
                ban.append([submissions[j]['problem']['contestId'], submissions[j]['problem']['index']])
ban.sort()

problems = requests.get(URL_PROBLEMSET, params=headers_tags).json()

if problems['status'] != 'OK':
    print('BEDA')
    exit(0)

problems = problems['result']['problems']

good_problems = []

for i in range(len(problems) - 1):
    if problems[i].get('rating') == None:
        continue
    if problems[i]['contestId'] >= data['minimum_contestId'] and len(problems[i]['tags']) > 0 and problems[i][
        'rating'] >= data['plot'][0] and problems[i]['rating'] <= \
            data['plot'][1] and search(ban, [
        problems[i]['contestId'], problems[i]['index']]) == False and (
            len(list((Counter(problems[i]['tags']) & Counter(data['ban_tags'])).elements())) == 0):
        good_problems.append(problems[i])

if len(good_problems) == 0:
    print("sorry, there are no problems matching your criteria")
    exit(0)

ans = []

for i in range(min(len(good_problems), data['number_of_problems'])):
    id = random.randint(0, len(good_problems) - 1)
    ans.append(good_problems[id])

for i in range(len(ans)):
    if data['output_tags'] == True:
        print(ans[i]['tags'])
    print(URL_PROBLEM + '/' + str(ans[i]['contestId']) + '/problem/' + ans[i]['index'])
