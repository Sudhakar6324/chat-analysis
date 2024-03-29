import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message':messages, 'message_date': dates})

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    return df