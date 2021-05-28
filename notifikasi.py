# from flask_mail import Mail, Message
# import schedule
# import time
# from server import app

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'sukmanirmaladewi.sn@gmail.com'
# app.config['MAIL_PASSWORD'] = '14Januari2000'

# def notifikasi ():
#     email = '221710021@stis.ac.id'
#     psn = 'cek'
#     msg = Message('Pertanyaan baru di HALO PUSDIKLAT', sender='sukmanirmaladewi.sn@gmail.com', recipients=[email])
#     msg.body = psn
#     try:
#         mail= Mail(app)
#         mail.connect()
#         mail.send(msg)
#     except Exception as e:
#         return print(e)

# schedule.every().day.at("22:53").do(notifikasi)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())