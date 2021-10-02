from sqlalchemy import Column, Integer, String, Float, create_engine,  ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template, request

engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()

class Firm(Base):
    __tablename__ = 'firm'
    id = Column(Integer, primary_key=True)
    firm = Column(String, unique=True)

    def __init__(self,  firm):
        self.firm = firm

    def __str__(self):
       return f'{self.firm}'

class Sale(Base):
    __tablename__ = 'sale'
    id  =  Column(Integer, primary_key = True)
    firm = Column(Integer, ForeignKey('firm.id'))
    sale = Column(Float)

    def __init__(self,  firm, sale):

        self.firm = firm
        self.sale = sale

    def __str__(self):
       return f'{self.firm}:  {self.sale}'

class Mobil(Base):
    __tablename__ = 'mobil'
    id = Column(Integer, primary_key=True)
    firm = Column(Integer, ForeignKey('firm.id'))
    model = Column(Integer)
    price = Column(Integer)

    def __init__(self, firm, model, price):
        self.firm = firm
        self.model = model
        self.price = price

    def __str__(self):
        return f'{self.firm} - {self.model}: {self.price}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_firm(nam):
    id = session.query(Firm).filter(Firm.firm == nam).first().id
    if id == None:
        fm =Firm(nam)
        session.add(fm)
        session.commit()

def add_sale(firm, sale):
    id = session.query(Firm).filter(Firm.firm == firm).first().id
    sl = Sale(id, sale)
    session.add(sl)
    session.commit()

def add_mobil(firm, model, price):
    id = session.query(Firm).filter(Firm.firm == firm).first().id
    mb = Mobil(id, model, price)
    session.add(mb)
    session.commit()

#****************************************************************#

# запускаем flask
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/date')
def date():
    return render_template('date.html')

@app.route('/date', methods = ['POST'])
def date_form():
    global cur
    global id_m
    fir = request.form['firm']
    mod = request.form['model']
    prc = request.form['price']
    print(f'{fir},{mod},{prc}')
    # добавляем запись
    add_firm(fir)
    add_mobil(fir,mod,prc)

    # передаем на страницу
    data = {
             'firm' : fir,
             'model': mod,
             'price': prc}
    return render_template('date.html', **data)


if __name__ == "__main__":
    app.run(debug = True)