import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)


def calculate_stats(df):
    mean = df.mean().to_dict()
    std = df.std().to_dict()
    return mean, std


def detect_anomalies(data_array, mean, std, num_std_dev=3):
    features = ['Voltage', 'Current', 'TruePower', 'ApparentPower']
    data_point = dict(zip(features, data_array))
    anomalies = []
    cnt = 0
    for feature, value in data_point.items():
        lower_bound = mean[feature] - num_std_dev * std[feature]
        upper_bound = mean[feature] + num_std_dev * std[feature]
        if value < lower_bound or value > upper_bound:
                cnt = cnt + 1

    if cnt > 0:
        return "Abnormal Detected!"
    else:
        return "No Abnormal Detected"

file_path = 'data_training1.csv'
df = load_data(file_path)
mean_values, std_values = calculate_stats(df)


# new_data_array = [400,2200,900,300]
# alert = detect_anomalies(new_data_array, mean_values, std_values)
# print(alert)
