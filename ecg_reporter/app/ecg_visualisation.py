import matplotlib.pyplot as plt
from biosppy.signals import ecg
from ecg_reporter.app.logs import add_to_log
from ecg_reporter.app.configs import get_config

path = get_config('images_path')

def visualise_part(filename, df, begin, end):
    """
    :param filename: str, filename to save the plot
    :param df: dataframe, input dataframe from pandas sql read
    :param begin: int, filter begin
    :param end: int, filter end
    :return: None
    """

    full_path = path + '/' + filename
    ax = plt.gca()

    # filter dataframe
    df = df[(df['rn'] >= begin) & (df['rn'] <= end)]

    # set elements
    df.plot(kind='line', x='rn', y='signal', ax=ax)
    figure = plt.gcf()

    # set to 1500 x 800 and save it
    figure.set_size_inches(15, 8)
    plt.savefig(full_path)

    # clears figure to separate plots
    plt.clf()

    add_to_log('Partial plot saved at {}'.format(full_path))


def visualise_all(filename, nparray):
    """
    :param filename: str, filename to save the plot
    :param nparray: nparray, input numpy array what biosppy lib use
    :return: None
    """

    # load raw ECG signal
    signal = nparray

    # process it and save the plot (changed function in source lib)
    full_path = path + '/' + filename
    ecg.ecg(signal=signal, sampling_rate=300., show=False, path=full_path)

    add_to_log('Complex plot saved at {}'.format(full_path))
