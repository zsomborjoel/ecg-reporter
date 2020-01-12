import matplotlib.pyplot as plt
from biosppy.signals import ecg
from .logs import add_to_log

def visualise_part(df, begin, end):
    ax = plt.gca()
    df = df[(df['rn'] >= begin) & (df['rn'] <= end)]
    df.plot(kind='line', x='rn', y='signal', ax=ax)
    figure = plt.gcf()
    figure.set_size_inches(15, 8)
    plt.savefig('test.png')


def visualise_all(nparray):

    # load raw ECG signal
    signal = nparray

    # process it and plot (changed function in source lib)
    ecg.ecg(signal=signal, sampling_rate=300., show=False, path='C:/Users/zsomb/PycharmProjects/MyProject/fullecg.png')
