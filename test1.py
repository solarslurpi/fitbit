# Sleep logs - https://dev.fitbit.com/build/reference/web-api/sleep/
# Two kinds of sleep data:
#   stages : Levels data is returned with 30-second granularity.
#   - deep, light, rem, wake
#   classic : Levels data returned with 60-second granularity.
# - asleep, restless, awake
import json

with open('postman_json/sleep-dateRange.json') as f:
    data = json.load(f)
# I see a loop through as being the time to use vectors
# in this case a pandas apply to create a table based
# on passing in the data
for s in data['sleep']:
    print(s['dateOfSleep'])
    print(s['type'])
    print(s['timeInBed'])
    print(s['minutesAfterWakeup'])
    print(s['minutesAsleep'])
    print(s['minutesAwake'])
    print(s['minutesToFallAsleep'])
    print(json.dumps(s['levels']['summary'], indent=4))


print(json.dumps(data['sleep'], indent=4))
print('hello')
