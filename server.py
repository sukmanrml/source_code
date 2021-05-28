from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
import json
import datetime
from json import JSONEncoder
from pengolahan import proses_jawaban
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
#config for db
app.secret_key = "mys3cr3tk3y"
app.static_folder = 'static'
db = Database()

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chatbot'

# Intialize MySQL
mysql = MySQL(app)

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

fac = StemmerFactory()
stemmer = fac.create_stemmer()

#memuat dataset
# dataset = open('warkop.txt', 'r', errors = 'Ignore')
dataset = db.readjawab(None)
data = ''
for i in dataset:
    data = data + i['jawaban'] + '\n'
# data = dataset.read()
data = data.lower()

token_kalimat = sent_tokenize(data)
token_kata = word_tokenize(data)

#melakukan tokenisasi
for i in range(len(token_kata)):
  token_kata[i] = stemmer.stem(token_kata[i])

#config for flask-mail
dataserver = db.readsmtp(None)
app.config['MAIL_SERVER'] = next(filter(lambda x:x['konfigurasi_key']=='server', dataserver))['value']
app.config['MAIL_PORT'] = next(filter(lambda x:x['konfigurasi_key']=='mail_port', dataserver))['value']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = next(filter(lambda x:x['konfigurasi_key']=='email', dataserver))['value']
app.config['MAIL_PASSWORD'] = next(filter(lambda x:x['konfigurasi_key']=='password', dataserver))['value']
mail= Mail(app)

def sensor():
    email_user = next(filter(lambda x:x['konfigurasi_key']=='email', dataserver))['value']
    server = next(filter(lambda x:x['konfigurasi_key']=='server', dataserver))['value']
    port = next(filter(lambda x:x['konfigurasi_key']=='port_smtp', dataserver))['value']
    password = next(filter(lambda x:x['konfigurasi_key']=='password', dataserver))['value']
    server = smtplib.SMTP (server, port)
    server.starttls()
    server.login(email_user, password)

    #EMAIL
    message = 'Terdapat pesan yang belum terjawab di HALO WARKOP'
    server.sendmail(email_user, email_user, message)
    server.quit()

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',days=1)
sched.start()

def hapus():
    db.deletestat()


sched = BackgroundScheduler(daemon=True)
sched.add_job(hapus,'interval',days=1)
sched.start()


@app.route("/chatbot")
def home():
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return render_template("chatbot.html", title="chatbot", waktu=current_time)

@app.route("/get", methods=['GET', 'POST'])
def get_bot_response():
    userText = request.args.get('pesan') ##model (?)
    hasil = proses_jawaban(userText, token_kalimat, token_kata)
    return hasil

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_admin'] = account['id_admin']
            session['email'] = account['email']
            # Redirect to home page
            flash('Selamat datang admin !', 'success')
            return redirect(url_for('indexadmin'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!')
    # Show the login form with message (if any)
    return render_template('login.html', title='Login')

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/cari/')
def cari():
    return render_template('cari.html', title='Cari')

@app.route('/addquest', methods = ['POST', 'GET'])
def addquest():
    if request.method == 'POST' and request.form['savecari']:
        if db.insertquest(request.form):
            flash("Pertanyaan dan jawaban berhasil dikirimkan")
        else:
            flash("Pertanyaan dan jawaban tidak berhasil dikirimkan")

        return redirect(url_for('cari'))
    else:
        return redirect(url_for('cari'))

@app.route('/indexadmin')
def indexadmin():
    if 'loggedin' in session:
        data = db.read(None)
        return render_template('index.html', data = data)
    flash("Silakan login terlebih dahulu")
    return redirect(url_for('login'))

@app.route('/updatestathps/<int:id>/')
def updatestathps(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('indexadmin'))
    else:
        session['update'] = id
        return render_template('stathps.html', data = data)

@app.route('/updatehps', methods = ['POST'])
def updatehps():
    if request.method == 'POST' and request.form['update']:

        if db.statushapus(session['update']):
            flash('Pertanyaan dan jawaban berhasil dihapus')
        else:
            flash('Pertanyaan dan jawaban tidak berhasil dihapus')

        session.pop('update', None)

        return redirect(url_for('indexadmin'))
    else:
        return redirect(url_for('indexadmin'))

@app.route('/updatestataktv/<int:id>/')
def updatestataktv(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('sampah'))
    else:
        session['update'] = id
        return render_template('stataktv.html', data = data)

@app.route('/updateaktv', methods = ['POST'])
def updateaktv():
    if request.method == 'POST' and request.form['update']:

        if db.statusaktif(session['update']):
            flash('Pertanyaan dan jawaban berhasil dipulihkan')
        else:
            flash('Pertanyaan dan jawaban tidak berhasil dipulihkan')

        session.pop('update', None)

        return redirect(url_for('sampah'))
    else:
        return redirect(url_for('sampah'))


@app.route('/email')
def email():
    if 'loggedin' in session:
        dataemail = db.reademail(None)
        return render_template('email.html', dataemail = dataemail)
    flash("Silakan login terlebih dahulu")
    return redirect(url_for('login'))

@app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    if request.method == 'POST':
        to = request.form['email'] 
        subjek = request.form['subjek']
        message = request.form['pesan']
        mail = request.form['email'] 

        msg = Message(subjek, sender='sukmanirmaladewi.sn@gmail.com', recipients=[mail])
        msg.body = message

        try:
            mail= Mail(app)
            mail.connect()
            mail.send(msg)
            # return render_template('kirim_sukses.html', to=to)
            flash("Pesan Anda telah terkirim.")
            return redirect(url_for('email'))
        except Exception as e:
            # print(e)
            return render_template('kirim_gagal.html', e=e)
            # flash("Pesan Anda gagal dikirim.")
            return redirect(url_for('email'))
    return render_template('form.html')

@app.route('/write/<int:id>/', methods = ['POST', 'GET'])
def write(id):
    dataemail = db.reademail(id);
    if len(dataemail) == 0:
        return redirect(url_for('indexadmin'))

    else:      
        session['write'] = id
        if request.method == 'POST':
            subjek = request.form['subjek']
            pesan = request.form['pesan']

            msg = Message(subjek, sender='sukmanirmaladewi.sn@gmail.com', recipients=dataemail[email])
            msg.body = pesan

            try:
                mail.connect()
                mail.send(msg)
                # return render_template('kirim_sukses.html', to=to)
                flash("Pesan Anda telah terkirim ke {{ email }}.")
                # return redirect(url_for('email'))
            except Exception as e:
                # print(e)
                # return render_template('kirim_gagal.html', e=e)
                flash("Pesan Anda gagal dikirim.")
                # return redirect(url_for('email'))
            return redirect(url_for('email'))
        return render_template('write.html', dataemail = dataemail)

@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/addquestadmin', methods = ['POST', 'GET'])
def addquestadmin():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("Pertanyaan dan jawaban berhasil ditambahkan")
        else:
            flash("Pertanyaan dan jawaban tidak berhasil ditambahkan")

        return redirect(url_for('indexadmin'))
    else:
        return redirect(url_for('indexadmin'))

@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('indexadmin'))
    else:
        session['update'] = id
        return render_template('update.html', data = data)

@app.route('/updatequest', methods = ['POST'])
def updatequest():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('Pertanyaan dan jawaban berhasil diperbarui')

        else:
            flash('Pertanyaan dan jawaban tidak berhasil diperbarui')

        session.pop('update', None)

        return redirect(url_for('indexadmin'))
    else:
        return redirect(url_for('indexadmin'))

@app.route('/sampah')
def sampah():
    if 'loggedin' in session:
        data = db.readstatus(None)
        return render_template('sampah.html', data = data)
    flash("Silakan login terlebih dahulu")
    return redirect(url_for('login'))

@app.route('/konfigurasi')
def konfigurasi():
    if 'loggedin' in session:
        data = db.readsmtp(None)
        email_user = next(filter(lambda x:x['konfigurasi_key']=='email', data))['value']
        smtp_server = next(filter(lambda x:x['konfigurasi_key']=='server', data))['value']
        mail_port = next(filter(lambda x:x['konfigurasi_key']=='mail_port', data))['value']
        tls = next(filter(lambda x:x['konfigurasi_key']=='tls', data))['value']
        ssl = next(filter(lambda x:x['konfigurasi_key']=='ssl', data))['value']
        return render_template('konfigurasi.html', data = data, email_user = email_user, smtp_server = smtp_server, mail_port = mail_port, tls = tls, ssl = ssl)
    flash("Silakan login terlebih dahulu")
    return redirect(url_for('login'))

@app.route('/pengunjung')
def pengunjung():
    if 'loggedin' in session:
        datachart = db.chart(None)
        datapengunjung = db.jumlah(None)
        datapengunjung = datapengunjung[0]['jumlah']
        class DateTimeEncoder(JSONEncoder):
            #Override the default method
            def default(self, obj):
                if isinstance(obj, (datetime.date, datetime.datetime)):
                    return obj.isoformat()
        chartJSONData = json.dumps(datachart, indent=4, cls=DateTimeEncoder)
        return render_template('pengunjung_.html', datachart = datachart, datapengunjung = datapengunjung, chartJSONData = chartJSONData)
    flash("Silakan login terlebih dahulu")
    return redirect(url_for('login'))

@app.route('/ubahkonf')
def ubahkonf():
    data = db.readsmtp(None)
    email_user = next(filter(lambda x:x['konfigurasi_key']=='email', data))['value']
    smtp_server = next(filter(lambda x:x['konfigurasi_key']=='server', data))['value']
    mail_port = next(filter(lambda x:x['konfigurasi_key']=='mail_port', data))['value']
    password = next(filter(lambda x:x['konfigurasi_key']=='password', data))['value']
    return render_template('ubahkonf.html', email_user = email_user, password = password, smtp_server = smtp_server, mail_port = mail_port)

@app.route('/updatesmtp', methods = ['POST'])
def updatesmtp():
    if request.method == 'POST' and request.form['update']:

        if db.updatekonf(request.form):
            flash('Konfigurasi berhasil diperbarui')

        else:
            flash('Konfigurasi tidak berhasil diperbarui')

        session.pop('update', None)

        return redirect(url_for('konfigurasi'))
    else:
        return redirect(url_for('konfigurasi'))

@app.route('/')
def index():
    return render_template('awal.html')

@app.route('/addawal', methods = ['POST', 'GET'])
def addawal():
    if request.method == 'POST' and request.form['saveawal']:
        if db.insertpengguna(request.form):
            flash("Pertanyaan dan jawaban berhasil dikirimkan")
        else:
            flash("Nama dan email salah, silahkan masukkan kembali")

        return redirect(url_for('home'))
    else:
        return redirect(url_for('awal'))


@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('admin'))
    else:
        session['delete'] = id
        return render_template('delete.html', data = data)

@app.route('/deletequest', methods = ['POST'])
def deletequest():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('Pertanyaan dan jawaban berhasil dihapus')

        else:
            flash('Pertanyaan dan jawaban tidak berhasil dihapus')

        session.pop('delete', None)

        return redirect(url_for('indexadmin'))
    else:
        return redirect(url_for('indexadmin'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
