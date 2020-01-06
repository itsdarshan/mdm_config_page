# import libraries
from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

# config setup and set secret key
app = Flask(__name__)

app.config.from_pyfile('config.py')

# database object
db = SQLAlchemy(app)


# class
class Clientinfo(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    port_url = db.Column(db.String(80))
    services = db.relationship('Service', backref='comp')

    def __init__(self,port_url):
        self.port_url = port_url


class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    cred = db.Column(db.String(100))
    comp_id = db.Column(db.Integer, db.ForeignKey('clientinfo.company_id'))

    def __init__(self, cred,comp_id):
        self.cred = cred
        self.comp_id = comp_id


@app.route('/')
def show_all():
    return render_template('temp.html')


@app.route('/update', methods=['POST', 'GET'])
def choice():
    if request.method == 'POST':
        m = request.form['id']
        ex = db.session.query(db.session.query(Service.cred).filter(Service.comp_id == m).exists()).scalar()
        if ex:
            return render_template('temp1.html', p=m)
        else:
            return render_template('temp2.html', p=m)


@app.route('/read', methods=['POST', 'GET'])
def read():
    if request.method == 'POST':
        p = request.form['URL']
        l = request.form['id']
        u = db.session.query(Service.cred).filter(Service.comp_id == l).scalar()
        return render_template('temp3.html', p=p, u=hash(u))


@app.route('/add', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        if not request.form['url']:
            return 'Enter All Fields'
        else:
            ex = exists = db.session.query(
                db.session.query(Clientinfo).filter_by(port_url=request.form['url']).exists()).scalar()
            if ex:
                p = db.session.query(Clientinfo.company_id).filter_by(port_url=request.form['url']).scalar()
                return render_template('choice.html', x=request.form['url'], p=p)
            else:
                client_info = Clientinfo(port_url=request.form['url'])
                db.session.add(client_info)
                db.session.commit()
                return render_template('temp2.html', p=client_info.company_id, u=request.form['url'])


@app.route('/unp', methods=['POST', 'GET'])
def unp():
    if request.method == 'POST':
        if not request.form['uname'] or not request.form['pwd']:
            return 'Enter All Fields'
        else:
            srv = Service(cred=request.form['uname'] + request.form['pwd'], comp_id=request.form['CI'])
            db.session.add(srv)
            db.session.commit()
    return render_template('temp.html')





@app.route('/update_info', methods=['POST', 'GET'])
def update_info():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
        cred = request.form['uname'] + request.form['pwd']
        db.session.query(Service).filter(Service.comp_id).update({Service.cred: cred})
        db.session.commit()
        return render_template('temp.html')


if __name__ == '__main__':
    app.run(debug=True)
