from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ias_csm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.Enum('active', 'inactive', 'banned'), default='active')
    phone_number = db.Column(db.String(15))
    address = db.Column(db.Text)
    dob = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    password_reset_token = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))


class ClientInfo(db.Model):
    __tablename__ = 'client_info'
    client_id = db.Column(db.Integer, primary_key=True)
    client_type = db.Column(db.String(100), nullable=False)
    service_availed = db.Column(db.String(255), nullable=False)
    region_residence = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    date_transaction = db.Column(db.Date, nullable=False)

class SurveyQuestion(db.Model):
    __tablename__ = 'survey_questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Enum('short_answer', 'paragraph', 'multiple_choice', 'checkboxes', 'rating'), nullable=False)
    is_required = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.form_id'), nullable=False)  # Add this line

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    response_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client_info.client_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('survey_questions.question_id'), nullable=False)
    response_text = db.Column(db.Text)

class Form(db.Model):
    __tablename__ = 'forms'
    form_id = db.Column(db.Integer, primary_key=True)
    form_title = db.Column(db.String(255), nullable=False)
    form_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('userName')  # Get username from form
        password = request.form.get('password')

        user = AdminUser.query.filter_by(user_name=user_name, password=password).first()

        if user:
            session['user_id'] = user.user_id
            return redirect(url_for('admin_home'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        user_name = request.form['userName']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        dob = request.form.get('dob')

        # Check if user already exists
        existing_user = AdminUser.query.filter((AdminUser.user_name == user_name) | (AdminUser.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('register'))

        # Create new user
        new_user = AdminUser(
            user_name=user_name,
            f_name=f_name,
            l_name=l_name,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            dob=dob,
            status='active',  # Default status
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/admin/home')
def admin_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve all saved forms from the database
    saved_forms = Form.query.order_by(Form.created_at.desc()).all()
    return render_template('home.html', saved_forms=saved_forms)

@app.route('/admin/summary')
def summary():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('summary.html')

@app.route('/admin/questions', methods=['GET', 'POST'])
def questions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        form_title = request.form.get('form_title')
        form_description = request.form.get('form_description')

        # Save the form to the database
        new_form = Form(
            form_title=form_title,
            form_description=form_description
        )
        db.session.add(new_form)
        db.session.commit()

        # Save the questions and link them to the form
        questions = []
        for key, value in request.form.items():
            if key.startswith('question_text_'):
                index = key.split('_')[-1]
                question_text = value
                question_type = request.form.get(f'question_type_{index}')
                is_required = request.form.get(f'is_required_{index}') == 'true'

                options = []
                for opt_key, opt_value in request.form.items():
                    if opt_key.startswith(f'option_{index}_'):
                        options.append(opt_value)

                questions.append({
                    'question_text': question_text,
                    'question_type': question_type,
                    'is_required': is_required,
                    'options': options
                })

        for question in questions:
            new_question = SurveyQuestion(
                question_text=question['question_text'],
                question_type=question['question_type'],
                is_required=question['is_required'],
                form_id=new_form.form_id,  # Link to the new form
                created_at=datetime.utcnow()
            )
            db.session.add(new_question)

        db.session.commit()
        flash('Form saved successfully!', 'success')
        return redirect(url_for('admin_home'))

    return render_template('questions.html')

# Route to delete a form
@app.route('/delete_form/<int:form_id>', methods=['DELETE'])
def delete_form(form_id):
    form = Form.query.get(form_id)
    if form:
        # Delete associated questions first (if any)
        SurveyQuestion.query.filter_by(form_id=form_id).delete()

        # Delete the form
        db.session.delete(form)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Form deleted successfully!'})
    return jsonify({'success': False, 'message': 'Form not found!'}), 404

# Route to copy a form
@app.route('/copy_form/<int:form_id>', methods=['POST'])
def copy_form(form_id):
    form = Form.query.get(form_id)
    if form:
        # Create a new form with the same data
        new_form = Form(
            form_title=f"Copy of {form.form_title}",
            form_description=form.form_description,
            created_at=datetime.utcnow()
        )
        db.session.add(new_form)
        db.session.commit()

        # Copy associated questions (if any)
        questions = SurveyQuestion.query.filter_by(form_id=form_id).all()
        for question in questions:
            new_question = SurveyQuestion(
                question_text=question.question_text,
                question_type=question.question_type,
                is_required=question.is_required,
                form_id=new_form.form_id,  # Link to the new form
                created_at=datetime.utcnow()
            )
            db.session.add(new_question)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Form copied successfully!'})
    return jsonify({'success': False, 'message': 'Form not found!'}), 404

@app.route('/admin/individual')
def individual():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('individual.html')

@app.route('/client/survey')
def survey():
    return render_template('client.html')

@app.route('/client/submit_survey', methods=['POST'])
def submit_survey():
    if request.method == 'POST':
        # Handle survey submission
        client_id = request.form.get('client_id')
        question_id = request.form.get('question_id')
        response_text = request.form.get('response_text')

        new_response = SurveyResponse(client_id=client_id, question_id=question_id, response_text=response_text)
        db.session.add(new_response)
        db.session.commit()
        flash('Survey submitted successfully!', 'success')
    return redirect(url_for('survey'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Helper Functions
def format_date(date):
    """Format a date to a readable string."""
    return date.strftime('%Y-%m-%d %H:%M:%S')

def calculate_percentage(total, part):
    """Calculate the percentage of a part relative to the total."""
    return round((part / total) * 100, 2) if total > 0 else 0

if __name__ == '__main__':
    app.run(debug=True)
