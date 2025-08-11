from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import initialize_connection_pool
from queries.users import register_user, register_agent, get_user_by_username, get_active_lease_for_tenant, get_rental_requests_for_tenant, get_tenant_id_by_userid, get_available_properties, get_owner_active_leases,get_owner_properties, get_owner_id_by_userid, get_user_statistics, get_property_summary, get_lease_summary,get_rental_requests_summary, get_agent_id_by_userid,get_agent_properties, get_agent_active_leases, get_agent_rental_requests, get_owner_list, save_property
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
def agent_registration():
    if 'role' not in session or session['role'] != 'admin':
        flash("⛔ Only admin can register agents.","warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']

        user_id = register_agent(name, username, email, phone, password)
        if user_id:
            flash("Agent registered successfully.","success")
            return redirect(url_for('dashboard_admin'))
        else:
            flash("Failed to register agent.","error")
        return render_template('register_agent.html')  # Separate template
    
        # Always return template for GET requests and failed POSTs
    return render_template('register_agent.html')

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
    # Get agent_id from the logged-in session
    if 'user_id' not in session or session.get('role') != 'agent':
        return redirect('/login')

    agent_id = get_agent_id_by_userid(session.get("user_id"))
    
    if not agent_id:
        return redirect(url_for("login"))

    # Fetch agent-specific data
    properties = get_agent_properties(agent_id)
    active_leases = get_agent_active_leases(agent_id)
    rental_requests = get_agent_rental_requests(agent_id)
    owners_list = get_owner_list()
    print(properties)
    print(active_leases)
    print(rental_requests)
    print(owners_list)

    return render_template(
        'dashboard_agent.html',
        properties=properties,
        active_leases=active_leases,
        rental_requests=rental_requests,
        owners = owners_list
    )

@app.route('/agent/add-property', methods=['GET', 'POST'])
def add_property():
    if 'role' not in session or session['role'] != 'agent':
        flash("⛔ Only agents can add properties.", "error")
        return redirect(url_for('login'))

    owners = get_owner_list()  # Your DB function to fetch owners
    print(owners)
    if request.method == 'POST':
        title = request.form['title']
        property_type = request.form['property_type']
        size = request.form['size']
        address = request.form['address']
        price = request.form['price']
        description = request.form['description']
        owner_id = request.form['owner_id']
        print("owner_id",owner_id)

        success = save_property(title, property_type, size, address, price, description, owner_id)
        if success:
            flash("✅ Property added successfully!", "success")
        else:
            flash("❌ Failed to add property.", "error")
        return redirect(url_for('dashboard_agent'))

    return render_template('add_property.html', owners=owners)


@app.route('/dashboard_admin',methods = ['GET','POST'])
def dashboard_admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            # Call your DB function to register agent
            register_agent(name, username, email, phone, password)
            flash('Agent registered successfully!', 'success')
            return redirect(url_for('dashboard_admin'))
        except Exception as e:
            flash(f'Error registering agent: {e}', 'danger')
        
        return render_template('dashboard_admin.html')

    # Fetch data from the views
    user_stats = get_user_statistics()
    property_summary = get_property_summary()
    lease_summary = get_lease_summary()
    rental_requests = get_rental_requests_summary()
    print(user_stats)
    print(property_summary)
    print(lease_summary)
    print(rental_requests)
    return render_template(
        'dashboard_admin.html',
        user_stats=user_stats,
        property_summary=property_summary,
        lease_summary=lease_summary,
        rental_requests=rental_requests
    )

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
