from flask import Flask, session, render_template,request, redirect,flash,send_file
from model import *
from datetime import datetime
from sqlalchemy import extract

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RAC_database.sqlite3'
db.init_app(app)


app.app_context().push()
session = db.session

import os

# Generate a random secret key
app.secret_key = os.urandom(24)
###############################################################
###############################################################

import plotly.express as px
import pandas as pd


@app.route('/')
def index():
    # Query scholars and group by year of admission and status
    results = db.session.query(
        extract('year', Scholar.date_of_admission).label('year'),
        Scholar.status,
        db.func.count('*').label('count')
    ).group_by('year', Scholar.status).all()

    # Convert the query results to a DataFrame
    df = pd.DataFrame(results, columns=['year', 'status', 'count'])

    # Filter the DataFrame to include only the desired statuses
    desired_statuses = ['awarded', 'in_progress']  # Replace with the actual statuses you want to visualize
    filtered_df = df[df['status'].isin(desired_statuses)]
    # Create a Plotly figure for the stacked bar chart
    # fig = px.bar(df, x='year', y='count', color='status', barmode='stack',
    #              labels={'count': 'Number of Scholars'}, title='Scholars by Year of Admission and Status')
    fig = px.line(filtered_df,x='year', y='count',color='status', title='Year wise new scholar')

    # Update the layout of the chart
    fig.update_xaxes(title='Year of Admission')
    fig.update_yaxes(title='Number of Scholars')

    # Convert the Plotly figure to HTML
    chart_html = fig.to_html(full_html=False)
    return render_template('index.html', chart_html=chart_html)



###############################################################
###############################################################



# to rendered all the scholars
@app.route('/scholars', methods=['GET', 'POST'])
def scholar():
    if request.method == 'GET':
        scholars = session.query(Scholar).filter(extract('year', Scholar.date_of_admission) == datetime.now().year).all()
        return render_template('scholar.html', scholars=scholars)

    # for scholar search
    elif request.method == 'POST':
        search_criteria = request.form.get('search_criteria')
        if search_criteria == 'name':

            q = request.form.get('name_input')
            if q.isalpha():
                query = '%'+q+'%'
                scholars = Scholar.query.filter(Scholar.name.like(query)).all()
                flash(f"Scholar with name '{q}'",'success')
                return render_template('scholar.html', scholars=scholars)
            else:
                flash(f"Please search with valid name",'danger')
                return redirect('/scholars')

        elif search_criteria == 'roll_no':
            roll_no = request.form.get('roll_no_input')
            scholars = session.query(Scholar).filter(Scholar.roll_no == roll_no).all()
            flash(f"Scholar with roll no '{roll_no}'",'success')
            return render_template('scholar.html', scholars=scholars)

        elif search_criteria == 'status':
            status = request.form.get('status_input')
            scholars = session.query(Scholar).filter(Scholar.status == status).all()
            flash(f"Scholar with status '{status}'",'success')
            return render_template('scholar.html', scholars=scholars)

        elif search_criteria == 'date_of_admission':
            date_of_admission = request.form.get('year_of_admission_input')
            scholars = session.query(Scholar).filter(extract('year', Scholar.date_of_admission) == date_of_admission).all()
            flash(f"Scholar of Year '{date_of_admission}'",'success')
            return render_template('scholar.html', scholars=scholars)
        
        elif search_criteria == 'supervisor':
            q = request.form.get('supervisor_input')
            if q.isalpha():
                query = '%' + q + '%'
                # scholars = session.query(Scholar).filter(Scholar.supervisor.name.like(query)).all()
                scholars = session.query(Scholar).join(Scholar.supervisor).filter(Supervisor.name.like(query)).all()
                flash(f"Scholar Under supervisor with name '{q}'",'success')
                return render_template('scholar.html', scholars=scholars)
            else:
                return redirect('/scholars')

    return render_template('scholar.html')
    
    
# to show scholar card
@app.route('/scholar_card/<int:id>')
def scholar_card(id):
    scholar = session.query(Scholar).get(id)
    # scholar = Scholar.query.get(id)

    return render_template('scholar_card.html',scholar = scholar)


# to rendered all the supervisors
@app.route('/supervisors',methods=['GET','POST'])
def delete():
    supervisors = session.query(Supervisor).all()
    return render_template('supervisors.html',supervisors = supervisors)

# to add new scholars
@app.route('/new_scholar',methods=['GET','POST'])
def add_scholars():
    supervisor = session.query(Supervisor).all()
    if request.method == 'GET':
        return render_template('/new_scholar.html',supervisor=supervisor)
    
    elif request.method == 'POST':
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        email = request.form.get('email')
        gender = request.form.get('gender')
        date_of_admission = request.form.get('date_of_admission')
        print(date_of_admission,type(date_of_admission))
        research_topic = request.form.get('research_topic')
        full_time = request.form.get('full_time')
        if full_time == 'true':
            full_time = True
        else:
            full_time = False

        supervisor_id = request.form.get('supervisor_id')
        hod_nominee_id = request.form.get('hod_nominee_id')
        supervisor_nominee_id = request.form.get('supervisor_nominee_id')
        
        scholar = Scholar(
            name = name,
            roll_no = roll_no,
            email = email,
            gender = gender,
            research_topic= research_topic,
            full_time = full_time,
            date_of_admission =datetime.strptime(date_of_admission,'%Y-%m-%d'),
            supervisor_id = supervisor_id,
            hod_nominee_id=hod_nominee_id,
            supervisor_nominee_id = supervisor_nominee_id)
        db.session.add(scholar)
        try:
            db.session.commit()
            flash(f"New scholar record created Successfully'",'success')
            scholars = session.query(Scholar).filter(Scholar.roll_no == roll_no)
            return redirect('/scholar_card/'+str(scholar.scholar_id))
        except Exception as e:
            flash("something goes wrong,Please try again","danger")
            return redirect('/new_scholar.html',supervisor=supervisor)
    
    
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
        scholar.name = request.form.get('name')
        scholar.roll_no = request.form.get('roll_no')
        scholar.email = request.form.get('email')
        scholar.gender = request.form.get('gender')
        scholar.research_topic = request.form.get('research_topic')
        full_time = request.form.get('full_time')
        if full_time =='true':
            scholar.full_time = True
        elif full_time == 'false':
            scholar.full_time = False
        scholar.status = request.form.get('status')

        date_of_admission = request.form.get('date_of_admission')
        if date_of_admission != '':
            scholar.date_of_admission = datetime.strptime(date_of_admission,'%Y-%m-%d')
        else:
            scholar.date_of_admission = None

        pre_submission_date = request.form.get('pre_submission_date')
        if pre_submission_date != '':
            scholar.pre_submission_date = datetime.strptime(pre_submission_date,'%Y-%m-%d')
        else:
            scholar.pre_submission_date = None

        thesis_submission_date = request.form.get('thesis_submission_date')
        if thesis_submission_date != '':
            scholar.thesis_submission_date = datetime.strptime(thesis_submission_date,'%Y-%m-%d')
        else:
            scholar.thesis_submission_date = None
        viva_voce_date = request.form.get('viva_voce_date')
        if viva_voce_date != '':
            scholar.viva_voce_date = datetime.strptime(viva_voce_date,'%Y-%m-%d')
        else:
            scholar.viva_voce_date = None
        date_of_award = request.form.get('date_of_award')
        if date_of_award != '':
            scholar.date_of_award = datetime.strptime(date_of_award,'%Y-%m-%d')
        else:
            scholar.date_of_award = None
        # if name != None:
        #     scholar.name = name.strip().title()
        
        # if roll_no != None:
        #     scholar.roll_number = roll_no.strip()
        # if y_o_admission != None:
        #     scholar.date_of_admission = y_o_admission
            
        scholar.supervisor_id = request.form.get('supervisor_id')
        scholar.hod_nominee_id = request.form.get('hod_nominee_id')
        scholar.supervisor_nominee_id = request.form.get('supervisor_nominee_id')
        
        try:            
            db.session.commit()
            # return redirect('/scholar_card/id')
            flash("Details Updated successfully","success")
            return redirect('/scholar_card/{}'.format(id))
        except Exception as e:
            flash("something went wrong",'danger')
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



@app.route('/view_reports/<int:id>',methods = ['GET','POST'])
def view_reports(id):
    scholar = Scholar.query.get(id)
    rac_reports = Rac_report.query.filter_by(scholar_id = id).all()
    return render_template('view_report.html',scholar = scholar,rac_reports =rac_reports)

####################################################
# from flask_weasyprint import HTML, render_pdf

# @app.route('/download_report/<int:rac_id>')
# def download_report(rac_id):
#     rac_report = session.query(Rac_report).get(rac_id)
#     scholar = session.query(Scholar).get(rac_report.scholar_id)
#     # return render_template('report.html', rac_report = rac_report, scholar=scholar)
#     html = render_template('report.html', rac_report = rac_report, scholar=scholar)

#     # Generate PDF using WeasyPrint
#     pdf_path = f'temp_report_{scholar.roll_no}.pdf'
#     HTML(string=html).write_pdf(pdf_path)

#     # Send the generated PDF as a response for download
#     return render_pdf(HTML(string=html))
#     # return send_file(pdf_path, as_attachment=True, download_name=f'RAC_{scholar.roll_no}.pdf')


# @app.route('/attendence',methods = ['GET','POST'])
# def attendence():
#     if request.method == 'GET':
#         supervisors = session.query(Supervisor).all()
#         return render_template('attendence.html',supervisors = supervisors)
#     elif request.method =='POST':
#         status = request.form.get('status')
#         supervisor_id = request.form.get('supervisor_id')
#         full_time = request.form.get('full_time')
#         year = request.form.get('year')
#         # forming the query

#         query = Scholar.query.filter_by(status = status,full_time=full_time)
#         if supervisor_id:
#             query = query.filter_by(supervisor_id = supervisor_id)
#         if year:
#             query = query.filter(extract('year', Scholar.date_of_admission) == year)
#         scholars = query.all()
#         if len(scholars) == 0:
#             flash("No scholar found","info")
#             return redirect('/attendence')
#         else:
#             # Add a timestamp to make the pdf_path unique
#             # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             pdf_path = f'AttendenceSheet.pdf'

#             # return render_template('attendence_sheet.html', scholars=scholars)
#             html = render_template('attendence_sheet.html', scholars=scholars)
#             HTML(string=html).write_pdf(pdf_path)
#             return send_file(pdf_path, as_attachment=True, download_name=f'Attendence_{status}_{full_time}.pdf')
#             # return render_pdf(HTML(string=html))



if __name__ == "__main__":
    app.run(debug= True,host='0.0.0.0')