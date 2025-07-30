from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import initialize_connection_pool
from queries.users import register_user, register_agent, get_user_by_username, get_active_lease_for_tenant, get_rental_requests_for_tenant, get_tenant_id_by_userid, get_available_properties, get_owner_active_leases,get_owner_properties, get_owner_id_by_userid
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# -------------------------
# Init DB pool at startup
# -------------------------
if not initialize_connection_pool():
    raise Exception("❌ Failed to initialize DB connection pool.")

# -------------------------
# Home redirects to login
# -------------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# -------------------------
# Owner/Tenant Registration
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']
        role = request.form['role'].lower()

        if role not in ['tenant', 'owner']:
            flash("❌ Only tenants and owners can self-register.")
            return redirect(url_for('register'))

        user_id = register_user(name, username, email, phone, password, role)
        if user_id:
            flash("✅ Registration successful. Please log in.")
            return redirect(url_for('login'))
        else:
            flash("❌ Registration failed. Try a different username/email.")

    return render_template('register.html')

# -------------------------
# Admin registers Agent
# -------------------------
@app.route('/admin/agent', methods=['GET', 'POST'])
def register_agent():
    if 'role' not in session or session['role'] != 'admin':
        flash("⛔ Only admin can register agents.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']

        user_id = register_agent(name, username, email, phone, password)
        if user_id:
            flash("✅ Agent registered successfully.")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("❌ Failed to register agent.")

    return render_template('register_agent.html')  # Separate template

# -------------------------
# Login Route
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and user['password_hash'] == password:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            print(f"✅ User {username} logged in with role {user['role']}")
            dashboard_routes = {
                'tenant': 'dashboard_tenant',
                'owner': 'dashboard_owner',
                'agent': 'dashboard_agent',
                'admin': 'dashboard_admin'
            }
            print(dashboard_routes.get(user['role'], 'login'))
            return redirect(url_for(dashboard_routes.get(user['role'], 'login')))
        else:
            flash("❌ Invalid username or password.")

    return render_template('login.html')

# -------------------------
# Logout
# -------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------------
# Dashboards
# -------------------------
@app.route('/dashboard_tenant')
def dashboard_tenant():
    # Ensure user is logged in and is a tenant
    if 'user_id' not in session or session.get('role') != 'tenant':
        return redirect(url_for('login'))

    tenant_id = get_tenant_id_by_userid(session['user_id'])

    active_lease = get_active_lease_for_tenant(tenant_id)
    rental_requests = get_rental_requests_for_tenant(tenant_id)
    # print(rental_requests)
    available_properties = get_available_properties()
    # print(available_properties)
    return render_template(
        'dashboard_tenant.html',
        leases=active_lease,
        requests=rental_requests,
        properties = available_properties
    )

@app.route('/dashboard_owner')
def dashboard_owner():
    if 'user_id' not in session or session.get('role') != 'owner':
        return redirect('/login')
    
    owner_id = get_owner_id_by_userid(session['user_id'])

    # Fetch data using stored functions
    properties = get_owner_properties(owner_id)
    leases = get_owner_active_leases(owner_id)
    print(properties)
    print(leases)
    print(owner_id,session['user_id'])
    return render_template('dashboard_owner.html', properties=properties, leases=leases)

@app.route('/dashboard_agent')
def dashboard_agent():
    return render_template('dashboard_agent.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
