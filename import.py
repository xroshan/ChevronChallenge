# a file that imports chevron.xlsx to db
import sys
import xlrd

from models import *
from application import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(os.getenv("DATABASE_URL"))
session = Session(engine)

# you can give args to clear db
if len(sys.argv) > 1:
    if sys.argv[1] == 'cleardb':
        with app.app_context():
            db.drop_all()
            db.create_all()
        print("database dropped")

# read in data
workbook = xlrd.open_workbook("data/chevron.xlsx")

def add_facilities():
    # work on facilities
    f_sheet = workbook.sheet_by_index(3)

    # loop every column of facility sheet
    for row in range(f_sheet.nrows):
        cols = f_sheet.row_values(row)

        if row > 1:
            print(cols)

            facility = Facility(float(cols[2]), float(cols[3]))
            session.add(facility)

    session.commit()

def add_equipment_types():
    type_sheet = workbook.sheet_by_index(1)

    for row in range(type_sheet.nrows):
        cols = type_sheet.row_values(row)

        if row > 1:
            hrange = cols[3].split('-')
            print(cols, hrange)

            e_type = EquipmentType(cols[1].strip().lower(), float(2), int(hrange[0]), int(hrange[1]))
            session.add(e_type)

    session.commit()

def add_certification(worker_id, certification):
    # looks if type in db
    query = session.query(EquipmentType).filter_by(name=certification).first()

    # creates one
    if query is None:
        print("ERROR: cert not added")

    else:
        cert_2 = Certification(query.id, worker_id)
        session.add(cert_2)

    session.commit()

def add_workers():
    # first work on worker sheet
    worker_sheet = workbook.sheet_by_index(2)

    # loop every column of worker sheet
    for row in range(worker_sheet.nrows):
        cols = worker_sheet.row_values(row)
        
        # except label row
        if row != 0:
            print(cols)
            # db object
            worker = Worker(cols[1].strip(), cols[3].strip().lower())
            session.add(worker)
            session.commit()

            print("ID: ", worker.id)

            # give certification
            for cert in cols[2].split(','):
                print(cert)
                add_certification(worker.id, cert.strip().lower())

def add_equipment(tname, fid):
    # looks if type in db
    query = session.query(EquipmentType).filter_by(name=tname).first()

    # creates one
    if query is None:
        print("ERROR: equipment not added")
        return -1

    equipment = Equipment(query.id, fid)
    session.add(equipment)
    session.commit()

    return equipment.id


def add_work_orders():
    order_sheet = workbook.sheet_by_index(4)

    for row in range(order_sheet.nrows):
        cols = order_sheet.row_values(row)

        if row > 1:
            f_id = int(cols[2][3])

            e_id = add_equipment(cols[3].strip().lower(), f_id)
            
            print(cols, f_id)

            if e_id != -1:
                order = Order(int(cols[5]), int(cols[6]), f_id, e_id)
                session.add(order)
                session.commit()

if __name__ == '__main__':
    add_facilities()
    add_equipment_types()
    add_workers()
    add_work_orders()