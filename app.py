from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json 
import mining

with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = parameters["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parameters["track_modifications"]
app.config['SECRET_KEY'] = parameters["secret_key"] 

db = SQLAlchemy(app)


class Blockchain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prev_hash = db.Column(db.String(512), nullable=False)
    sender_id = db.Column(db.String(512), nullable=False)
    reciver_id = db.Column(db.String(512), nullable=False)
    transaction_amt = db.Column(db.String(256), nullable=False)
    new_hash = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return str(self.id) + " " + self.prev_hash 


class Blockchain_Waiting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prev_hash = db.Column(db.String(512), nullable=False)
    sender_id = db.Column(db.String(512), nullable=False)
    reciver_id = db.Column(db.String(512), nullable=False)
    transaction_amt = db.Column(db.String(256), nullable=False)
    nonce = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.id) + " " + self.prev_hash 

    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    public_key = db.Column(db.String(10), nullable=False)
    private_key = db.Column(db.String(10, nullable=False))
    current_balance = db.Column(db.string(10, nullable=False))
    dob = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return self.id + ' : ' + self.name


class Miner(db.Mode):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    public_key = db.Column(db.String(10), nullable=False)
    private_key = db.Column(db.String(10, nullable=False))
    current_mine = db.Column(db.string(10, nullable=False))
    dob = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return self.id + ' : ' + self.name


@login_manager.user_loader
def load_user(id):
    return User().query.get(int(id))



@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender_id = request.form.get('sender_id')
        reciver_id = request.form.get('reciver_id')
        transaction_amt = request.form.get('transaction_amt')
        prev_block = Blockchain.query.all()[-1]
        blockchain_Waiting = Blockchain_Waiting(prev_hash = prev_block.prev_hash, sender_id = sender_id, reciver_id = reciver_id, transaction_amt = transaction_amt, nonce = 1)
        print(blockchain_Waiting)
        db.session.add(blockchain_Waiting)
        db.session.commit()
    blockchain = Blockchain.query.all()
    return render_template('index.html', blockchain = blockchain)


@app.route('/mine', methods = ['GET', 'POST'])
def mine():
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        id_block = request.form.get('id_block')
        block_tobe_mined = Blockchain_Waiting.query.all()[0]
        print(block_tobe_mined)
        x, new_hash = mining.set_mine(block_tobe_mined)
        block = Blockchain(prev_hash = x.prev_hash, sender_id = x.sender_id, reciver_id = x.reciver_id, transaction_amt = x.transaction_amt, new_hash = new_hash)
        db.session.add(block)
        db.session.delete(block_tobe_minedxc )
        db.session.commit()
    all_pending_block = Blockchain_Waiting.query.all()
    return render_template('yo.html', all_pending_block = all_pending_block)


@app.route('/genesis', methods = ['GET', 'POST'])
def genesis():
    block = Blockchain(prev_hash = "0x0", sender_id = "Not me", reciver_id = "Not me", transaction_amt = "Lot of money", new_hash = mining.SHA256("ABCD"))
    db.session.add(block)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True, threaded = True)