from app import *
print ("deleting old database" )
db.drop_all()
print ("creating new database" )
db.create_all()



# # ============================== Scholar ===============================


print ("Entering the data in Scholar\n")
print("....................................\n")

f =open("Scholars.csv","r")
f.readline()

for c in f.readlines():
    c = c.split(',')
    
    flag = False
    if c[7] == "Full Time":
        flag = True
    t = Scholar(name =c[0],
                roll_no=c[1],
                year_of_admission=c[2],
                research_topic=c[6],
                full_time = flag,
                supervisor_id=c[3],
                hod_nominee_id = c[4],
                supervisor_nominee_id=c[5],
                status = c[8],
                date_of_award = c[9]
                )

    db.session.add(t)

f.close()
print("commiting the scholar database")
print("....................................\n")
try:
    db.session.commit()
    print("data successfully entered into Scholar table\n\n")
except Exception as e:
    print(e)


# ============================== Supervisor ===============================
print ("Entering the data in Supervisor\n")
print("....................................\n")

f =open("Supervisor.csv","r")
f.readline()
# Salutation,Name,Designation,Department,University
for c in f.readlines():
    c = c.split(',')
    t = Supervisor(salutation = c[0], name=c[1], designation=c[2],department=c[3],university=c[4])
    db.session.add(t)

f.close()
print("commiting the database")
print("....................................\n")
try:
    db.session.commit()
    print("data successfully entered into Supervisor table\n\n")
except Exception as e:
    print(e)