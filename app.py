from flask import Flask, session, render_template,request, redirect
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RAC_database.sqlite3'
db.init_app(app)


app.app_context().push()
session = db.session
        
# for Home page
@app.route('/')
def index():    
    return render_template('index.html')


# to rendered all the scholars
@app.route('/scholars', methods=['GET', 'POST'])
def scholar():
    if request.method == 'GET':
        scholars = session.query(Scholar).filter(Scholar.year_of_admission == '2022').all()
        return render_template('scholar.html', scholars=scholars)

    elif request.method == 'POST':
        search_criteria = request.form.get('search_criteria')
        if search_criteria == 'name':
            search_value = request.form.get('name_input')
            scholars = session.query(Scholar).filter(Scholar.name == search_value).all()
            return render_template('scholar.html', scholars=scholars)

        elif search_criteria == 'roll_no':
            roll_no = request.form.get('roll_no_input')
            scholars = session.query(Scholar).filter(Scholar.roll_no == roll_no).all()
            return render_template('scholar.html', scholars=scholars)

        elif search_criteria == 'status':
            status = request.form.get('status_input')
            scholars = session.query(Scholar).filter(Scholar.status == status).all()
            return render_template('scholar.html', scholars=scholars)

        elif search_criteria == 'year_of_admission':
            year_of_admission = request.form.get('year_of_admission_input')
            scholars = session.query(Scholar).filter(Scholar.year_of_admission == year_of_admission).all()
            return render_template('scholar.html', scholars=scholars)
        # elif search_criteria == 'supervisor':
        #     supervisor_input = request.form.get('supervisor_input')
        #     print(supervisor_input)
        #     scholars = session.query(Scholar).filter(Scholar.supervisor.name == supervisor_input).all()
        #     return render_template('scholar.html', scholars=scholars)

    return render_template('scholar.html')
    # return "nothong"

    
    
    
# to show scholar card
@app.route('/scholar_card/<int:id>')
def scholar_card(id):
    scholar = session.query(Scholar).get(id)
    return render_template('scholar_card.html',scholar = scholar)


# to rendered all the supervisors
@app.route('/supervisors',methods=['GET','POST'])
def delete():
    supervisors = session.query(Supervisor).all()
    return render_template('supervisors.html',supervisors = supervisors)

# to add new scholars
@app.route('/new_scholar',methods=['GET','POST'])
def add_scholars():
    if request.method == 'GET':
        supervisor = session.query(Supervisor).all()
        return render_template('/new_scholar.html',supervisor=supervisor)
    
    elif request.method == 'POST':
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        year_of_admission = request.form.get('year_of_admission')
        research_topic = request.form.get('research_topic')
        full_time = request.form.get('full_time')
        if full_time == 'true':
            full_time = True
        else:
            full_time = False
        supervisor_id = request.form.get('supervisor_id')
        hod_nominee_id = request.form.get('hod_nominee_id')
        supervisor_nominee_id = request.form.get('supervisor_nominee_id')
        
        scholar = Scholar(name = name,roll_no = roll_no,year_of_admission =year_of_admission,research_topic= research_topic,full_time = full_time,supervisor_id = supervisor_id,hod_nominee_id=hod_nominee_id,supervisor_nominee_id = supervisor_nominee_id)
        db.session.add(scholar)
        try:
            db.session.commit()
            return redirect('/scholars')
        except Exception as e:
            print("can not be added",e)
            return redirect('/')
    
    
# to add new supervisor
@app.route('/new_supervisor',methods = ['GET','POST'])
def add_scholar():
    if request.method == 'GET':
        return render_template('/new_supervisor.html') 
    elif request.method == 'POST':
        salutation = request.form.get('salutation')
        name = request.form.get('name')
        designation = request.form.get('designation')
        department = request.form.get('department')
        university = request.form.get('university')
        supervisor = Supervisor(name=name,salutation =salutation,designation =designation,department =department,university =university)
        db.session.add(supervisor)
        try:
            db.session.commit()
            return redirect('/supervisors')
        except Exception as e:
            print("can not be added",e)
            return render_template('/new_supervisor.html')


# to update  scholar details
@app.route('/update_scholar/<int:id>',methods=['GET','POST'])
def update_scholar(id):
    scholar = session.query(Scholar).get(id)
    if request.method == 'GET':
        supervisor = session.query(Supervisor).all()
        return render_template('/update_scholar.html',scholar = scholar,supervisor = supervisor)
    
    elif request.method == 'POST':
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        y_o_admission = request.form.get('year_of_admission')
        
        if name != None:
            scholar.name = name.strip().title()
        
        if roll_no != None:
            scholar.roll_number = roll_no.strip()
        if y_o_admission != None:
            scholar.year_of_admission = y_o_admission
            
        scholar.research_topic = request.form.get('research_topic')
        full_time = request.form.get('full_time')
        
        if full_time =='true':
            scholar.full_time = True
        elif full_time == 'false':
            scholar.full_time = False
        scholar.supervisor_id = request.form.get('supervisor_id')
        scholar.hod_nominee_id = request.form.get('hod_nominee_id')
        scholar.supervisor_nominee_id = request.form.get('supervisor_nominee_id')
        
        try:            
            db.session.commit()
            # return redirect('/scholar_card/id')
            return redirect('/scholar_card/{}'.format(id))
        except Exception as e:
            print("something went wrong",e)
            return redirect('/scholar_card/{}'.format(id))
            
            
# to update supervisor details
@app.route("/update_supervisor/<int:id>", methods=['POST','GET'])
def update_supervisor(id):
    supervisor = session.query(Supervisor).get(id)
    if request.method == 'GET':
        return render_template('/update_supervisor.html',supervisor = supervisor)
    
    elif request.method == 'POST':
        salutation = request.form.get("salutation")
        name = request.form.get("name")
        designation = request.form.get("designation")
        department = request.form.get("department")
        university = request.form.get("university")
        supervisor.salutation = salutation
        supervisor.name = name
        supervisor.designation =designation
        supervisor.department = department
        supervisor.university = university
        
        try:
            db.session.commit()
            return redirect('/supervisors')
        except Exception as e:
            print("something went wrong",e)


@app.route('/supervisor_scholar/<int:id>')
def supervisor_scholar(id):
    supervisor = session.query(Supervisor).get(id)
    return render_template('/supervisor_scholar.html',supervisor = supervisor)


# to save individual scholar report details
@app.route('/scholar_report',methods=['GET','POST'])
def scholar_report():
    
    if request.method == 'GET':
        scholars = session.query(Scholar).all()
        return render_template('/report_form.html',scholars = scholars)

    elif request.method == 'POST':
        scholar_id = request.form.get('scholar_id')
        date_of_presentation = request.form.get('date')
        rac_no = request.form.get('rac_no')
        reviews = request.form.getlist('review')
        recommendations = request.form.getlist('recommendation')
        
        rr = Rac_report(scholar_id = scholar_id,
                       rac_no = rac_no,
                       date_of_presentation = date_of_presentation)

        db.session.add(rr)
        
        try:
            db.session.commit()
            rac_report_id = Rac_report.query.filter_by(date_of_presentation=date_of_presentation, rac_no=rac_no).first()
            for recom in recommendations:
                re = Recommendation(rac_report_id=rac_report_id.rac_report_id, recommendation=recom)

                db.session.add(re)
                
            for rev in reviews:
                re = Review(rac_report_id=rac_report_id.rac_report_id, review=rev)

                db.session.add(re)
            try:
                db.session.commit()
                return redirect('/scholar_report')
            except Exception as e:
                print("something went wrong",e)
            
        except Exception as e:
            print("something went wrong",e)
        
        
    return redirect('/')


# to view individual scholar reports
@app.route('/view_report/<int:id>', methods = ['GET','POST'])
def view_report(id):
    rac_reports = session.query(Rac_report).filter_by(scholar_id = id).all()
    scholar = session.query(Scholar).get(id)
    return render_template('/view_report.html', rac_reports = rac_reports, scholar = scholar)





if __name__ == "__main__":
    app.run(debug= True)