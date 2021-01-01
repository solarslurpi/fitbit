
from dateutil import parser
import requests
import pandas as pd

my_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkJaS1YiLCJzdWIiOiIyM1ZCNTYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNjEwMDIyMjEwLCJpYXQiOjE2MDk0MTc0MTB9.m_vEY9pK3aVzC6cZ4353JtC23sGdzcG6FKWQ9DHpwaI"


def get_date_from_user():

    try:
        date = parser.parse(input("Enter date: "))
    except Exception:
        raise Exception("You did not enter a valid date.")
    else:
        datestr = date.strftime('%Y-%m-%d')
        return datestr


def get_data(date_str, activity='heart'):
    # TODO: CHECK IF DATE STR in fitbit format. I think this is what the fitbit class was doing.
    if date_str is None:
        raise Exception(
            "The function requires a date string in the format YYYY-MM-DD.")
    heart_rates_url = "https://api.fitbit.com/1/user/-/activities/" \
        + activity+"/date/" + date_str+"/1d/1sec.json"
    header = {'Authorization': 'Bearer {}'.format(my_access_token)}
    response = requests.get(heart_rates_url, headers=header).json()
    # If the request was successful, there should be an KeyError exception when asking for the errors list.
    try:
        failed_response = response['errors'][0]
        raise Exception(failed_response['message'])
    except KeyError:
        return response


try:
    data_date_in_fitbit_fmt = get_date_from_user()
    oneDayData = get_data(data_date_in_fitbit_fmt)
except Exception as error:
    print(error)
else:
    df = pd.DataFrame(oneDayData['activities-heart-intraday']['dataset'])
    print(df.head())
