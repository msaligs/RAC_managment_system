from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Scholar(db.Model):
    scholar_id = db.Column(db.Integer(),primary_key = True, nullable = False)
    name = db.Column(db.String(50),nullable = False)
    roll_no = db.Column(db.String(15),nullable = False,unique = True)
    year_of_admission = db.Column(db.String(10),nullable = False)
    research_topic = db.Column(db.String(150))
    full_time = db.Column(db.Boolean,nullable= False)
    status = db.Column(db.String(10),nullable = False)
    date_of_award = db.Column(db.String(15))
    
    supervisor_id = db.Column(db.Integer,db.ForeignKey("supervisor.supervisor_id"))
    hod_nominee_id = db.Column(db.Integer,db.ForeignKey("supervisor.supervisor_id"))
    supervisor_nominee_id = db.Column(db.Integer,db.ForeignKey("supervisor.supervisor_id"))
    
    supervisor = db.relationship("Supervisor",backref = 'scholar',foreign_keys=[supervisor_id])
    hod_nominee = db.relationship("Supervisor",backref = 'hod_nominee_scholar', foreign_keys=[hod_nominee_id])
    supervisor_nominee = db.relationship("Supervisor",backref = 'supervisor_nominee_scholar',foreign_keys=[supervisor_nominee_id])

class Supervisor(db.Model):
    supervisor_id = db.Column(db.Integer(),primary_key = True, nullable = False)
    salutation = db.Column(db.String(20),nullable = False)
    name = db.Column(db.String(50),nullable = False)
    designation = db.Column(db.String(50),nullable = False)
    department = db.Column(db.String(50),nullable = False)
    university = db.Column(db.String(50),nullable = False)
    
    
    
class Rac_report(db.Model):
    rac_report_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    scholar_id = db.Column(db.Integer, db.ForeignKey('scholar.scholar_id'), nullable=False)
    rac_no = db.Column(db.Integer, nullable=False)
    date_of_presentation = db.Column(db.String(20), nullable=False)
    
    recommendation = db.relationship('Recommendation')  
    review = db.relationship('Review')
    
    __table_args__ = (
        db.UniqueConstraint('rac_no', 'date_of_presentation', name='uq_rac_no_date_of_presentation'),
    )
    
class Recommendation(db.Model):
    Recommendation_id = db.Column(db.Integer(),primary_key = True, nullable = False)
    rac_report_id = db.Column(db.Integer,db.ForeignKey('rac_report.rac_report_id'),nullable = False)
    recommendation = db.Column(db.String(250),nullable = False)
    
class Review(db.Model):
    review_id = db.Column(db.Integer(),primary_key = True, nullable = False)
    rac_report_id = db.Column(db.Integer,db.ForeignKey('rac_report.rac_report_id'),nullable = False)
    review = db.Column(db.String(250),nullable = False)
    