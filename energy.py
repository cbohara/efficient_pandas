import pandas as pd


def import_file(file_name):
    """
    Imports a csv file into a pandas dataframe
    :param file_name: local directory filename
    :return: pandas dataframe
    """
    return pd.read_csv(file_name, parse_dates=[0], infer_datetime_format=True)

def apply_tariff(kwh, hour):
    """
    Calculates cost of electricity for a given hour
    :param kwh: energy used in kilowatts per hour
    :param hour: hour of the day
    :return: cost in cents

    Type	    Cents per kWh	Time Range
    Peak	    28	            17:00 to 24:00
    Shoulder	20	            7:00 to 17:00
    Off-Peak    12              0:00 to 7:00
    """
    if 0 <= hour < 7:
        rate = 12
    elif 7 <= hour < 17:
        rate = 20
    elif 17 <= hour < 24:
        rate = 28
    else:
        raise ValueError(f'Invalid hour: {hour}')
    return rate * kwh

def apply_tariff_loop(df):
    """
    Use loop to add third column that provides energy cost per hour
    :param df: dataframe to update
    :return: updated dataframe
    """
    energy_cost_list = []
    for i in range(len(df)):
        energy_used = df.iloc[i]['energy_kwh']
        hour = df.iloc[i]['date_time'].hour
        energy_cost = apply_tariff(energy_used, hour)
        energy_cost_list.append(energy_cost)
    df['cost_cents'] = energy_cost_list
    return df


if __name__ == '__main__':
    file1 = 'demand_profile.csv'
    df1 = import_file(file1)
    updated_df1 = apply_tariff_loop(df1)