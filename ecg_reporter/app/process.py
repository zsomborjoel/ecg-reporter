from ecg_reporter.app.executors import execute_sql
from ecg_reporter.app.logs import add_to_log
from ecg_reporter.app.configs import get_config
from ecg_reporter.app.emails import *
from ecg_reporter.app.ecg_visualisation import visualise_all, visualise_part
from datetime import date, timedelta


def process():

    try:
        today = date.today()

        for day in range(6):
            act_day = today - timedelta(days=day)
            sql = """
                select rn, measurement, signal from (
                    select
                        row_number() over(partition by get_body_heartget_id order by heartgetsignal_id asc) as rn,
                        dense_rank() over(partition by get_body_heartget_id order by 1) as filtr,
                        get_body_heartget_id as measurement,
                        signal
                    from withings.heartgetsignal
                    where date(created_at) = '{}'
                    order by heartgetsignal_id
                ) sub where filtr = 1;
                """.format(act_day)


            df = execute_sql(sql.strip())

            # get signals from dataframe
            signals = df.loc[:, "signal"]

            # change dataframe data to numpy_array for biosppy lib
            numpy_array = signals.to_numpy()

            if df.empty:
                pass
            else:
                visualise_part('heartgetsignal_first_half_' + str(act_day), df, 0, 4500)
                visualise_part('heartgetsignal_secound_half_' + str(act_day), df, 4500, 10000)
                visualise_all('heartgetsignal_summary_' + str(act_day) + ".png", numpy_array)


    except Exception as e:
        pass
        add_to_log('Error occurred: ' + str(e))


def main():
    add_to_log('Process started')
    print('started')
    process()
    print('finished')
    add_to_log('Process ended')
    add_to_log('====================================================================')


if __name__ == '__main__':
    main()