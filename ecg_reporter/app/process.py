from ecg_reporter.app.executors import execute_sql
from ecg_reporter.app.logs import add_to_log
from ecg_reporter.app.pdf_creation import add_to_pdf
from ecg_reporter.app.emails import send_mail
from ecg_reporter.app.ecg_visualisation import visualise_all, visualise_part
from ecg_reporter.app.clear import clear_images_directory
from ecg_reporter.app.clear import get_config
from datetime import date, timedelta
import sys

number_of_days = 7
password = sys.argv[1]
from_address = get_config("from_address")
to_address = get_config("to_address")
subject = "Heti ECG kimutatás"

def process():

    try:
        today = date.today()

        for day in range(number_of_days):
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

            str_act_day = str(act_day)
            str_day = str(day)

            if df.empty:
                pass
            else:
                visualise_part(str_day + 'heart_signal_first_half_' + str_act_day, df, 0, 4500)
                visualise_part(str_day + 'heart_signal_second_half_' + str_act_day, df, 4500, 10000)
                visualise_all(str_day + 'heart_signal_summary_' + str_act_day + ".png", numpy_array)

        pdf_path, filename = add_to_pdf(str(today - timedelta(number_of_days)), str(today))

        send_mail(
            from_address,
            to_address,
            subject,
            filename,
            pdf_path,
            password
        )

    except Exception as e:
        pass
        add_to_log('Error occurred: ' + str(e))
    finally:
        clear_images_directory()



def main():
    add_to_log('Process started')
    print('started')
    process()
    print('finished')
    add_to_log('Process ended')
    add_to_log('====================================================================')


if __name__ == '__main__':
    main()