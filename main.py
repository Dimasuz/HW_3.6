import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, load_tables, Publisher

print('Для подключения к БД,')
base_name = input('введите название БД: ')
if base_name == '':
    base_name = 'model'
host = input('введите host: ')
if host == '':
    host = 'localhost'
port = input('введите port: ')
if port == '':
    port = '5432'
username = input('введите username: ')
if username == '':
    username = 'postgres'
password = input('введите пароль: ')

DSN = 'postgresql://' + username + ':' + password + '@' + host + ':' + port + '/' + base_name
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

load_tables('tests_data.json', session)

pub = input('Для поиска имени издателя введите его id или нажмите Enter: ')
if pub != '':
    for c in session.query(Publisher).filter(Publisher.id == int(pub)).all():
        print(f'Имя издателя с id={c.id} - {c.name}.')

pub = input('Для поиска id издателя введите его имя или нажмите Enter: ')
if pub != '':
   for c in session.query(Publisher).filter(Publisher.name == pub).all():
        print(f'Id издателя с именем"{c.name}" - {c.id}.')

session.close()

print('Конец программы.')

