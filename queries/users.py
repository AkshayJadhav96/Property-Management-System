from db import execute_query

# ----------------------------------
# Call register_user() SQL function
# ----------------------------------
def register_user(name, username, email, phone, password, role):
    query = """
        SELECT register_user(%s, %s, %s, %s, %s, %s);
    """
    result = execute_query(query, (name, username, email, phone, password, role))
    return result[0][0] if result else None  # Assuming it returns user_id

# ----------------------------------
# Call register_agent() SQL function
# ----------------------------------
def register_agent(name, username, email, phone, password):
    query = """
        SELECT register_agent(%s, %s, %s, %s, %s);
    """
    result = execute_query(query, (name, username, email, phone, password))
    return result[0][0] if result else None

# ----------------------------------
# Used during login
# ----------------------------------

def check_username_exists(username):
    query = """
        SELECT check_user_exists(%s);
    """
    result = execute_query(query, (username,))
    return result[0][0] if result else False

def get_user_by_username(username):
    query = """
        SELECT user_id, name, username, email, phone, password_hash, role
        FROM users
        WHERE username = %s;
    """
    result = execute_query(query, (username,))
    return result[0] if result else None

def get_active_lease_for_tenant(tenant_id):
    query = """
        select * from get_tenant_active_lease(%s);
    """
    return execute_query(query, (tenant_id,))


def get_rental_requests_for_tenant(tenant_id):
    query = """
        select * from get_tenant_rental_requests(%s)
    """
    return execute_query(query, (tenant_id,))

def get_tenant_id_by_userid(user_id):
    query = """
        select tenant_id from tenants where user_id = %s
    """
    res =  execute_query(query, (user_id,))
    return res[0][0] if res else None

def get_owner_id_by_userid(user_id):
    query = """
        select owner_id from owners where user_id = %s
    """
    res =  execute_query(query, (user_id,))
    return res[0][0] if res else None

def get_available_properties():
    query = """
        select * from available_properties_view
    """
    return execute_query(query)

def get_owner_properties(owner_id):
    query = """
        select * from get_owner_properties(%s)
    """
    res = execute_query(query,(owner_id,))
    return res

def get_owner_active_leases(owner_id):
    query = """
        select * from get_owner_active_leases(%s)
    """
    res = execute_query(query,(owner_id,))
    return res

def get_user_statistics():
    query = """
        SELECT * FROM user_statistics_view;
    """
    return execute_query(query)

def get_property_summary():
    query = """
        SELECT * FROM property_summary_view;
    """
    return execute_query(query)

def get_lease_summary():
    query = """
        SELECT * FROM lease_summary_view;
    """
    return execute_query(query)

def get_rental_requests_summary():
    query = """
        SELECT * FROM rental_requests_summary_view;
    """
    return execute_query(query)

def get_agent_id_by_userid(user_id):
    query = """
        select agent_id from agents where user_id = %s
    """
    res =  execute_query(query, (user_id,))
    return res[0][0] if res else None

def get_agent_properties(agent_id):
    query = "SELECT * FROM get_agent_properties(%s);"
    return execute_query(query, (agent_id,))

def get_agent_active_leases(agent_id):
    query = "SELECT * FROM get_agent_active_leases(%s);"
    return execute_query(query, (agent_id,))

def get_agent_rental_requests(agent_id):
    query = "SELECT * FROM get_agent_rental_requests(%s);"
    return execute_query(query, (agent_id,))

def get_owner_list():
    query = "SELECT * FROM VIEW_OWNERS"
    return execute_query(query)

def save_property(title, property_type, size, address, price, description, owner_id):
    query = ""
    return execute_query(query)
