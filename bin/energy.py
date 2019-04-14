from datetime import datetime
import pandas as pd
from timer import timeit


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


@timeit(repeat=3, number=10)
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


@timeit(repeat=3, number=10)
def apply_tariff_iterrows(df):
    """
    Use pandas iterrows generator method to get energy cost per hour
    :param df: dateframe to update
    :return: updated dataframe
    """
    energy_cost_list = []
    for index, row in df.iterrows():
        energy_used = row['energy_kwh']
        hour = row['date_time'].hour
        energy_cost = apply_tariff(energy_used, hour)
        energy_cost_list.append(energy_cost)
    df['cost_cents'] = energy_cost_list
    return df


@timeit(repeat=3, number=10)
def apply_tariff_apply(df):
    """
    Use apply() method to add third column with energy cost per hour
    :param df: dateframe to update
    :return: updated dataframe
    """
    df['cost_cents'] = df.apply(
        lambda row: apply_tariff(
            kwh=row['energy_kwh'],
            hour=row['date_time'].hour
        ), axis=1
    )
    return df


@timeit(repeat=3, number=10)
def apply_tariff_isin(df):
    """
    Use isin() to select appropriate rows to apply appropriate tariff in a vectorized operation
    :param df: dataframe to update
    :return: updated dataframe
    """
    # define hour range boolean arrays
    peak_hours = df.index.hour.isin(range(17, 24))
    shoulder_hours = df.index.hour.isin(range(7, 17))
    off_peak_hours = df.index.hour.isin(range(0, 7))

    # apply tariffs to hour ranges
    df.loc[peak_hours, 'cost_cents'] = df.loc[peak_hours, 'energy_kwh'] * 28
    df.loc[shoulder_hours, 'cost_cents'] = df.loc[shoulder_hours, 'energy_kwh'] * 20
    df.loc[off_peak_hours, 'cost_cents'] = df.loc[off_peak_hours, 'energy_kwh'] * 12
    return df


#@timeit(repeat=3, number=10)
def apply_tariff_cut(df):
    """
    Use cut() to split up rows
    :param df: dataframe to update
    :return: updated dataframe
    """
    # cut() returns ndarray with appropriate rate for row
    cents_per_kwh = pd.cut(
        x=df.index.hour,
        bins=[0, 7, 17, 24],
        include_lowest=True,
        labels=[12, 20, 28]
    ).astype(int)
    df['cost_cents'] = cents_per_kwh * df['energy_kwh']
    return df


if __name__ == '__main__':
    file = 'data/demand_profile.csv'
    df = import_file(file)
    apply_tariff_loop(df)
    apply_tariff_iterrows(df)
    apply_tariff_apply(df)

    df.set_index('date_time', inplace=True)
    apply_tariff_isin(df)
    apply_tariff_cut(df)

    data_store = pd.HDFStore('processed_data.h5')
    data_store['preprocessed_df'] = df
    data_store.close()
