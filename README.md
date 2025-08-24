# 🏠 Property Management System  

A **Property Management System** built using **Flask** (backend) and **PostgreSQL** (hosted on Supabase) for managing properties, tenants, owners, agents, and rental workflows.  

The system provides **role-based dashboards** for Admin, Agent, Owner, and Tenant, enabling seamless property listings, rental requests, and lease management.  

---

## 🚀 Features  

### 🔑 User Management  
- User registration and login with roles (`admin`, `agent`, `owner`, `tenant`)  
- Secure authentication using session-based login  
- Admin can register **new agents** directly from the dashboard  

### 🧑‍💼 Agent Dashboard  
- View and manage listed properties  
- Track and handle rental requests related to their properties
- List new Properties
- Monitor active leases  

### 👤 Owner Dashboard  
- View owned properties  
- Track rental requests on owned properties  
- Monitor active leases with tenants  

### 🏘 Tenant Dashboard  
- Browse available properties  
- Request rentals by submitting **start and end dates**  
- Track status of rental requests  
- View active leases  

### 🛠 Admin Dashboard  
- Register new agents  
- Manage all users and roles  
- Monitor entire system data  

---

## 🗄 Database Design  

The database schema is designed to separate **user roles** from **role-specific details**:  

- **users** → stores common info (`user_id`, `name`, `email`, `phone`, `username`, `password`, `role`)  
- **agents** → (`agent_id`, `user_id`, `date_joined`, `salary`)  
- **owners** → (`owner_id`, `user_id`)  
- **tenants** → (`tenant_id`, `user_id`)  
- **properties** → (`property_id`, `listed_by`, `title`, `type`, `size`, `description`,`created_at`,`owner_id`,`status` etc.)  
- **rental_requests** → (`request_id`, `tenant_id`, `property_id`, `status`, `start_date`, `end_date`, `request_date`)  
- **leases** → (`lease_id`, `property_id`, `tenant_id`, `start_date`, `end_date`, `rent_amount`, `status`)  

👉 **Triggers (in progress):**  
- Automatically insert into `agents`, `owners`, or `tenants` when a user is created with that role.  
- Keep audit logs for property and lease updates.  

👉 **Indexes (planned):**  
- Indexes on `property_id`, `tenant_id`, and `agent_id` for faster queries.  

---

## 🔐 Security & DB Access  

- Secure connection pooling implemented in `db.py`  
- Role-based connection handling using PostgreSQL `SET ROLE`  
- Parameterized queries used throughout to prevent SQL injection  

---

## 🖼 Sample Screens  

- **Admin Dashboard** → register agents, manage users  
- **Agent Dashboard** → view listed properties, manage rental requests  
- **Tenant Dashboard** → browse properties, request rentals  
- **Owner Dashboard** → monitor properties & leases  

---

## ⚙️ Tech Stack  

- **Backend:** Flask (Python)  
- **Frontend:** Flask templates (Jinja2, TailwindCSS for styling)  
- **Database:** PostgreSQL (Supabase)  
- **ORM:** None (direct SQL with `execute_query` utility)  

---

## 📌 Future Enhancements  

- Complete trigger-based automation for rental requests and for maintainance request
- Add indexes for query optimization  
- Lease renewal & termination workflows  
- Property search & filtering  
- Notification system for rental status updates  

---

## 🏁 How to Run  

1. Clone this repo:  
   ```bash
   git clone https://github.com/AkshayJadhav96/Property-Management-System.git
   cd property-management
    ```
    
2. Install Dependencies
    ```bash
    uv sync
    ```

3. Set up .env with your database credentials:
    ```bash
    DB_HOST=...
    DB_NAME=...
    DB_USER=...
    DB_PASS=...
    DB_PORT=...
    ```

4 Run the Flask App:
    ```bash
    uv run app.py
    ```
