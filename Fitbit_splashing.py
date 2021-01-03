
"""Learning how the fitbit web apis work.  They are documented
    https://dev.fitbit.com/build/reference/web-api/

    :raises Exception: [description]
    :raises Exception: [description]
    :raises Exception: [description]
    :return: [description]
    :rtype: [type]
    """
from dateutil import parser
import json
import requests
import pandas as pd


# I am using implicit oauth2 access.
# see https://dev.fitbit.com/build/reference/web-api/oauth2/
# for fitbit's doc on the different oauth2 access grant flows.


# TODO: Unclear how these apis should be factored out.


def get_date_from_user():

    try:
        date = parser.parse(input("Enter date: "))
    except Exception:
        raise Exception("You did not enter a valid date.")
    else:
        datestr = date.strftime('%Y-%m-%d')
        return datestr


def get_data(date_str, activity='heart', detail_level='1sec'):
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
    # TODO: The location and actually getting the access token should be more robust.
    with open('config.json') as f:
        secret_dict = json.load(f)
    access_token = secret_dict['ACCESS_TOKEN']
    heart_rates_url = "https://api.fitbit.com/1/user/-/activities/" + \
        activity+"/date/" + date_str+"/1d/" + detail_level + ".json"
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(heart_rates_url, headers=header).json()
    # If the request was successful, there should be an KeyError exception when asking for the errors list.
    try:
        failed_response = response['errors'][0]
        raise Exception(failed_response['message'])
    except KeyError:
        return response


try:
    data_date_in_fitbit_fmt = get_date_from_user()
    print(
        f'The date you entered (converted to Fitbit format): {data_date_in_fitbit_fmt}')
    oneDayData = get_data(data_date_in_fitbit_fmt)
except Exception as error:
    print(error)
else:
    hr_df = pd.DataFrame(oneDayData['activities-heart-intraday']['dataset'])
    if hr_df.empty:
        print(
            f'No entries found for the date {data_date_in_fitbit_fmt}')
    else:
        hr_max = hr_df['value'].max()
        hr_min = hr_df['value'].min()
        hr_mean = hr_df['value'].mean()
        print(hr_df.head())
        print(f'min: {hr_min} max: {hr_max} average: {hr_mean}')
        print(f'Total HR Samples is {len(hr_df.index)}')
