
from dateutil import parser
import requests
import pandas as pd
import matplotlib.pyplot as plt

my_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkJaS1YiLCJzdWIiOiIyM1ZCNTYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNjEwMDIyMjEwLCJpYXQiOjE2MDk0MTc0MTB9.m_vEY9pK3aVzC6cZ4353JtC23sGdzcG6FKWQ9DHpwaI"


def get_date_from_user():

    try:
        date = parser.parse(input("Enter date: "))
    except Exception:
        raise Exception("You did not enter a valid date.")
    else:
        datestr = date.strftime('%Y-%m-%d')
        return datestr


def get_data(date_str, activity='heart', detail_level='1min'):
    """returns the fitbit time series data for the activity.

    :param date_str: date string with the format of YYYY-MM-DD.  The date should be a date that is
    included within fitbit data.
    :type date_str: str
    :param activity: [description], defaults to 'heart'
    :type activity: str, optional
    :param detail_level: Number of data points to include. Either 1sec or 1min., defaults to '1min'
    :type detail_level: str, optional
    :raises Exception: If a date string with the format of YYYY-MM-DD is not entered.
    :return: JSON formatted values of activity data at the entered detail level.
    :rtype: dictionary
    """
    # TODO: CHECK IF DATE STR in fitbit format. I think this is what the fitbit class was doing.
    if date_str is None:
        raise Exception(
            "The function requires a date string in the format YYYY-MM-DD.")
    heart_rates_url = "https://api.fitbit.com/1/user/-/activities/" \
        + activity+"/date/" + date_str+"/1d/" + detail_level + ".json"
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
    hr_df = pd.DataFrame(oneDayData['activities-heart-intraday']['dataset'])
    hr_max = hr_df['value'].max()
    hr_min = hr_df['value'].min()
    hr_mean = hr_df['value'].mean()
    print(hr_df.head())
    print(f'Total HR Samples is {len(hr_df.index)}')
