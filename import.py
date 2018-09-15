# a file that imports chevron.xlsx to db
import sys
import xlrd

from models import *
from application import app

# you can give args to clear db
if len(sys.argv) > 1:
    if sys.argv[1] == 'cleardb':
        with app.app_context():
            db.drop_all()
            db.create_all()
        print("database dropped")

# read in data
workbook = xlrd.open_workbook("data/chevron.xlsx")

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
        db.session.add(worker)

        # give certification
        for cert in cols[2].split(','):
            print(cert)
            add_certification(worker.id, cert.strip().lower())

        db.session.commit()

# work on facilities
f_sheet = workbook.sheet_by_index(3)

# loop every column of facility sheet
for row in range(f_sheet.nrows):
    cols = f_sheet.row_values(row)

    if row != 0:
        print(cols)

        facility = Facility(float(cols[2]), float(cols[3]))
        db.session.add(facility)

db.session.commit()



def add_certification(worker_id, certification):
    # looks if type in db
    query = EquipmentType.query.filter_by(name=certification).first()

    # creates one
    if query is None:
        e_type = EquipmentType(certification)
        db.session.add(e_type)

        # give certification
        cert = Certification(e_type.id, worker_id)
        db.session.add(cert)

    else:
        cert_2 = Certification(query.id, worker_id)
        db.session.add(cert_2)

    db.session.commit()

