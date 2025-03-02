import re
import pandas as pd

def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{4}, \d{2}:\d{2}\s-\s'

    msg = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_msg': msg, 'msg_date': dates})
    # convert message_date type
    df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'msg_date': 'date'}, inplace=True)

    users = []
    msgs = []
    for msg in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:  # user name
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['msg'] = msgs
    df.drop(columns=['user_msg'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df