from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

today = datetime.today().date()
engine = create_engine('sqlite:///list.db')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")


def today_tasks():
    rows = session.query(Table).filter(Table.deadline == today).all()
    print(f'\nToday {today.day} {today.strftime("%b")}:')
    if rows:
        for row in rows:
            print(f'{row.id}. {row.task}')
    else:
        print('Nothing to do!\n')


def week_tasks():
    for i in range(7):
        day = today + timedelta(days=i)
        print(f'\n{day.strftime("%A")} {day.day} {day.strftime("%b")}:')
        rows = session.query(Table).filter(Table.deadline == day).all()
        if rows:
            for row in rows:
                print(f'{row.id} - {row.task}\n')
        else:
            print('Nothing to do!\n')


def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('\nAll tasks:')
    for row in rows:
        print(f'{row.id}. {row.task}. {datetime.strftime(row.deadline, "%d %b")}\n')
    else:
        print('No tasks! \nChoose option 5 to add new task.\n')


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < today).all()
    print('\nMissed tasks:')
    if rows:
        for row in rows:
            print(f'{row.id}. {row.task}. {datetime.strftime(row.deadline, "%d %b")}')
    else:
        print('Nothing is missed!\n')


def add_task():
    while True:
        t = input('\nEnter task:\n>')
        try:
            d = datetime.strptime(input('Enter deadline:\n>'), '%Y-%m-%d')
            new_row = Table(task=t, deadline=d)
            session.add(new_row)
            session.commit()
            print('The task has been added!\n')
        except ValueError:
            print('Wrong date format, try again\n')


def del_task():
    print('Choose the number of the task you want to delete:')
    all_tasks()
    id_del = input('> ')
    session.query(Table).filter(Table.id == int(id_del)).delete()
    session.commit()
    print('The task has been deleted!\n')


while True:
    menu()
    option = input('>')
    if option == '0':
        print('\nBYE!')
        break
    elif option == '1':
        today_tasks()
    elif option == '2':
        week_tasks()
    elif option == '3':
        all_tasks()
    elif option == '4':
        missed_tasks()
    elif option == '5':
        add_task()
    elif option == '6':
        del_task()
