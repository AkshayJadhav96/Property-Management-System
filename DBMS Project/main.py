from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required , current_user
from functools import wraps
from flask import abort


app = Flask(__name__)

app.secret_key='Aditya'


# this is for getting unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'Login'

@login_manager.user_loader
def load_user(user_id):
    return User_table.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://<username>:<password>@<host_name>:<port>/<database_name>'
db=SQLAlchemy(app)


# Define custom decorators for role-based access control
def role_required(role):
    """Decorator to allow only specific roles or admin access to the route."""
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or (current_user.role != role and current_user.role != 'admin'):
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorated_view
    return decorator
# @app.route('/admin/dashboard')
# @login_required
# def admin_dashboard():
#     if current_user.role != 'admin':
#         abort(403)  # Forbidden
#     # Render admin dashboard
#     return render_template('base.html')

# def tenant_required(func):
#     """Decorator to allow only tenants access to the route."""
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.role != 'tenant':
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('index'))
#         return func(*args, **kwargs)
#     return decorated_view


# def employee_required(func):
#     """Decorator to allow only employees access to the route."""
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.role != 'employee':
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('index'))
#         return func(*args, **kwargs)
#     return decorated_view


# def company_required(func):
#     """Decorator to allow only companies access to the route."""
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.role != 'company':
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('index'))
#         return func(*args, **kwargs)
#     return decorated_view



class Task(db.Model):
    employee_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
with app.app_context():
    db.create_all()

class User_table(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(1000))
    role = db.Column(db.String(20))
    role_id=db.Column(db.String(50))
    
class Review(UserMixin,db.Model):
    Review_ID = db.Column(db.Integer, primary_key=True)
    Tenant_ID = db.Column(db.Integer)
    Property_ID = db.Column(db.Integer)
    Rating = db.Column(db.Integer)
    Comment = db.Column(db.Text)
    Date = db.Column(db.Date)

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)  # Corrected here
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    contact_number = db.Column(db.String(20))
    ceo = db.Column(db.String(255))
    revenue_in_crores = db.Column(db.DECIMAL(18, 2))
    number_of_employees = db.Column(db.Integer)

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    contact_information = db.Column(db.String(255))
    salary = db.Column(db.DECIMAL(18, 2))
    department = db.Column(db.String(255))
    employment_start_date = db.Column(db.Date)
    employment_end_date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))  # Corrected here
    company = db.relationship('Company', backref=db.backref('employees', lazy=True))


    
@app.route("/company/<int:company_id>/employees")
def company_employees(company_id):
    company = Company.query.get_or_404(company_id)
    employees = Employee.query.filter_by(company_id=company_id).all()
    return render_template('company_employees.html', company=company, employees=employees)

@app.route("/company/<int:company_id>/employees/add", methods=['POST','GET'])
def add_employee(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        contact_information = request.form.get('contactInformation')
        salary = request.form.get('salary')
        department = request.form.get('department')
        employment_start_date = request.form.get('startDate')

        # Create a new Employee object and add it to the database
        new_employee = Employee(
            name=name,
            position=position,
            contact_information=contact_information,
            salary=salary,
            department=department,
            employment_start_date=employment_start_date,
            company_id=company_id
        )
        db.session.add(new_employee)
        db.session.commit()

        flash('Employee added successfully', 'success')
        return redirect(url_for('company_employees', company_id=company_id))

    return render_template('add_employee.html', company_id=company_id, company=company)  # Corrected here


    # company = Company.query.get_or_404(company_id)
    # employee = Employee.query.get_or_404(employee_id)

# @app.route('/company/<int:company_id>/employee/<int:employee_id>/update', methods=['GET'])
# def update_employee(company_id, employee_id):
#     # Retrieve employee from the database based on company_id and employee_id
#     employee = Employee.query.filter_by(company_id=company_id, employee_id=employee_id).first()
#     if not employee:
#         flash('Employee not found', 'error')
#         return redirect(url_for('company_employees', company_id=company_id))
    
#     return render_template('update_employee.html', company_id=company_id, employee=employee)

@app.route("/company/<int:company_id>/employees/<int:employee_id>/update", methods=['GET', 'POST'])
def update_employee(company_id, employee_id):
    company = Company.query.get_or_404(company_id)
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'POST':
        # Update employee details
        employee.name = request.form.get('name')
        employee.position = request.form.get('position')
        employee.contact_information = request.form.get('contactInformation')
        employee.salary = request.form.get('salary')
        employee.department = request.form.get('department')
        employee.employment_start_date = request.form.get('startDate')
        db.session.commit()
        flash('Employee updated successfully', 'success')
        return redirect(url_for('company_employees', company_id=company_id))
    return render_template('update_employee.html', company=company, employee=employee)

@app.route("/company/<int:company_id>/employees/<int:employee_id>/delete", methods=['POST'])
def delete_employee(company_id, employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully', 'success')
    return redirect(url_for('company_employees', company_id=company_id))

@app.route("/")
def index():
    return render_template('index.html')
    


@app.route("/companies")
@login_required
@role_required('company')
def companies():
    
    return render_template('companies.html')

    # company = Company.query.get_or_404(company_id)
    # employees = Employee.query.filter_by(Company_ID=company_id).all()
    # return render_template('companies.html', company=company, employees=employees)




@app.route('/tenants', methods=['POST','GET'])
@login_required
@role_required('tenant')
def Tenants():
    if request.method == 'POST':
        # review_id = request.form['review_id']
        tenant_id = request.form.get('tenantId')
        property_id = request.form.get('propertyId')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        date = request.form.get('date')
       

        with db.engine.connect() as conn:
            new_user = conn.execute(text(f"INSERT INTO Review(Tenant_ID, Property_ID, Rating, Comment, Date) VALUES ({tenant_id},{property_id},{rating},'{comment}','{date}');"))
            conn.commit()
        # new_review = Review( Tenant_ID=tenant_id, Property_ID=property_id,
        #                     Rating=rating, Comment=comment, Date=date)
        # db.session.add(new_review)
        # db.session.commit()
        flash("Review submitted successfully","success")

    return render_template('tenants.html')


@app.route("/bookings")
@login_required
def Bookings():
        
    return render_template('bookings.html')



@app.route('/function_1', methods=['GET', 'POST'])
@login_required
@role_required('company')
def function_1():
    if request.method == 'POST':
        # Retrieve inputs from the form
        company_id = request.form.get('companyID')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')

        # Call the function to calculate revenue
        try:
            revenue = Calculate_company_revenue(company_id, start_date, end_date)
            return render_template('revenue_output.html',revenue = revenue)
        except Exception as e:
            return jsonify({'error': str(e)})

    # Handle GET request to render the form
    return render_template('comp_revenue.html')

        

def Calculate_company_revenue(company_id, start_date, end_date):
    conn = db.engine.connect()
    result = conn.execute(text(f"SELECT Calculate_company_revenue({company_id}, '{start_date}', '{end_date}')")).scalar()
    conn.close()

    return result

@app.route('/signup',methods =['POST','GET'])
def Signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        user = User_table.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        
        encpassword = generate_password_hash(password)
        # this is method 1 to save data in database
        # with db.engine.connect() as conn:
        #     new_user = conn.execute(text(f"INSERT INTO User_table(username,email,password) VALUES ('{username}','{email}','{encpassword}');"))
        #     conn.commit()

        # this is method 2 to save data in database
        new_user = User_table(username = username , email = email , password = encpassword,role = role,role_id=role)
        db.session.add(new_user)
        db.session.commit()
        with db.engine.connect() as conn:
            new_user = conn.execute(text(f"update User_table set role_id='{new_user.role + str(new_user.id)}' where id = {new_user.id}"))
            conn.commit()
        
        flash("Signup Success Please Login","success")
        return render_template('login.html')
        



    return render_template('signup.html')

@app.route('/login', methods = ['POST','GET'])
def Login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        
        user = User_table.query.filter_by(email = email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            if user.role == 'admin':
                # If the user is an admin, redirect to admin panel
                login_user(user)
                return redirect(url_for('index'))
            if user.role == 'tenant':
                return redirect(url_for('Tenants'))
            elif user.role == 'employee':
                return redirect(url_for('index'))
            elif user.role == 'company':
                return redirect(url_for('companies'))
            else:
                flash('Unknown role. Please contact support.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/logout")
@login_required
def Logout():
    logout_user()
    flash("Logout Successfull","warning")
    return redirect(url_for('Login'))


@app.route('/test')
def test():
    try:
        Task.query.all()
        return 'My database is connected'
    except:
        return 'not coonected'
    

@app.route('/home')
def home():
    return 'this is our home page'


# functions

# function no 1

@app.route('/get_lease_duration', methods=['POST','GET'])
@login_required
@role_required('tenant')
def get_lease_duration():
    if request.method == 'POST':
        lease_id = request.form.get('leaseId')

        lease_duration = get_lease_duration_from_db(lease_id)
        if lease_duration is not None:
            return jsonify({'lease_duration': lease_duration})
        else:
            return jsonify({'error': 'No lease duration found for the provided lease ID.'})
    
    return render_template('f_lease_duration.html')

def get_lease_duration_from_db(lease_id):
    try:
        conn = db.engine.connect()
        result = conn.execute(text(f"SELECT GetLeaseDuration({lease_id})"))
        lease_duration = result.fetchone()[0]
        conn.close()
        return lease_duration
    except Exception as e:
        print("Error:", e)
        return None


# function no 2

@app.route('/get_property_maintenance_cost', methods=['POST','GET'])
@login_required
def get_property_maintenance_cost():
    if request.method == 'POST':
        property_id = request.form.get('propertyId')

        maintenance_cost = get_property_maintenance_cost_from_db(property_id)

        return jsonify({'maintenance_cost': maintenance_cost})
    
    return render_template('f_prop_maintain_cost.html')

def get_property_maintenance_cost_from_db(property_id):
    try:
       
        conn = db.engine.connect()

      
        result = conn.execute(text(f"SELECT GetPropertyMaintenanceCost({property_id})"))
        maintenance_cost = result.fetchone()[0]

        conn.close()

        return maintenance_cost
    except Exception as e:
        print("Error:", e)
        return None
    

# function no 3

@app.route('/get_employee_details', methods=['POST','GET'])
@login_required
@role_required('employee')
def get_employee_details():
    if request.method == 'POST':
        employee_id = request.form.get('employeeId')

        employee_details = get_employee_details_from_db(employee_id)

        return render_template('output_emp_det.html',employee_details = employee_details)
    
    return render_template('f_employee_det.html')

def get_employee_details_from_db(employee_id):
    try:
        conn = db.engine.connect()

        result = conn.execute(text(f"SELECT * from GetEmployeeDetails({employee_id})"))

        r=conn.execute(text(f"select column_name from information_schema.columns where table_schema='public' and table_name='employee';"))
        
        t=result.fetchall()[0]
        p=r.fetchall()

    
        
        employee_details = {p[j][0]:t[j] for j in range(len(t)-1)}
        employee_details['company_name']=t[-1]
        
        conn.close()

        return employee_details
    except Exception as e:
        print("Error:", e)
        return None


# function no - 4

@app.route('/calculate_total_rent_due', methods=['POST','GET'])
@login_required
@role_required('tenant')
@role_required('company')
def calculate_total_rent_due():
    if request.method == 'POST':
        tenant_id = request.form.get('tenantId')

        # Execute the PostgreSQL function
        with db.engine.connect() as conn:
            result = conn.execute(text(f"SELECT CalculateTotalRentDue({tenant_id})"))
            total_rent_due = result.fetchone()[0]

        return jsonify({'total_rent_due': total_rent_due})
    
    return render_template('f_due_rent.html')


# function no - 5


@app.route('/get_available_properties', methods=['POST','GET'])
@login_required
def get_available_properties():
    if request.method == 'POST':
        size = request.form.get('size')
        property_type = request.form.get('propertyType')
        min_price = request.form.get('minPrice')
        max_price = request.form.get('maxPrice')

        with db.engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM GetAvailableProperties({size}, '{property_type}', {min_price}, {max_price})"))
            t=result.fetchall()

            # print(t)
            r=conn.execute(text(f"select column_name from information_schema.columns where table_schema='public' and table_name='property';"))
            p=r.fetchall()
            # print(p)

            properties = {}
            i=0
            for row in t:
                d={}
                i+=1
                for j in range(len(row)-1):
                    d[p[j][0]]=row[j]
                d['LandLord_Name']=row[-1]
                properties[i]=d
 

        return render_template('output_avail_prop.html', properties = properties)
    
    return render_template('f_avail_prop.html')
    
    

    
    
# function no - 6


@app.route('/average_rating', methods=['POST','GET'])
@login_required
def average_rating():
    if request.method == 'POST':
        property_id = request.form.get('propertyId')

        # Execute the PostgreSQL function
        with db.engine.connect() as conn:
            result = conn.execute(text(f"SELECT AverageRatingForProperty({property_id})"))
            avg_rating = result.fetchone()[0]

        return render_template('f_avg_rating.html', avg_rating=avg_rating)
    
    return render_template('f_avg_rating.html')

if __name__ == '__main__':
    app.run(debug = True)
