-- Trigger 1
CREATE OR REPLACE FUNCTION create_role_and_grant_access()
RETURNS TRIGGER AS
$$
DECLARE
    new_company_id INT;
    new_password TEXT;
BEGIN
    -- Get the newly inserted company ID and password
    SELECT NEW.Company_ID, NEW.Password INTO new_company_id, new_password;

    -- Create a new role based on the company ID
    EXECUTE format('CREATE ROLE company_role_%s WITH LOGIN PASSWORD %L', new_company_id, new_password);

    -- Create a view specific to the company
    EXECUTE format('CREATE OR REPLACE VIEW company_employee_view_%s AS SELECT * FROM employee WHERE company_id = %s', new_company_id, new_company_id);

    -- Grant SELECT privilege on the view to the new role
    EXECUTE format('GRANT SELECT ON company_employee_view_%s TO company_role_%s', new_company_id, new_company_id);

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER after_insert_company
AFTER INSERT ON Company
FOR EACH ROW
EXECUTE FUNCTION create_role_and_grant_access()

-- Trigger 2
CREATE OR REPLACE FUNCTION enforce_lease_expiry()
RETURNS TRIGGER AS
$$
BEGIN
    -- Check if the lease end date is in the past
    IF NEW.Lease_End_Date < CURRENT_DATE THEN
        -- Update the lease status to 'Expired'
        NEW.Lease_Status := 'Expired';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER lease_expiry_trigger
BEFORE INSERT OR UPDATE ON Lease
FOR EACH ROW
EXECUTE FUNCTION enforce_lease_expiry();

--  Trigger 3

CREATE OR REPLACE FUNCTION ensure_data_consistency()
RETURNS TRIGGER AS
$$
BEGIN
    -- Check if the property has active leases
    IF EXISTS (SELECT 1 FROM Lease WHERE Property_ID = OLD.Property_ID AND Lease_Status <> 'Expired') THEN
        RAISE EXCEPTION 'Cannot delete property with active leases';
    END IF;

    -- Check if the property has pending maintenance requests
    IF EXISTS (SELECT 1 FROM MaintenanceRequest WHERE maintenance_request_id = OLD.maintenance_request_id AND Status = 'Pending') THEN
        RAISE EXCEPTION 'Cannot delete property with pending maintenance requests';
    END IF;

    RETURN OLD;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER ensure_data_consistency_trigger
BEFORE DELETE ON Property
FOR EACH ROW
EXECUTE FUNCTION ensure_data_consistency();

# Trigger 4

-- CREATE OR REPLACE FUNCTION update_late_fee()
-- RETURNS TRIGGER AS
-- $$
-- DECLARE end_date DATE;
-- DECLARE expected_due_date DATE;
-- BEGIN
--     -- Calculate the lease end date for the associated lease
    
--     SELECT Lease_End_Date INTO end_date FROM Lease WHERE Lease_ID = NEW.Lease_ID;

--     -- Calculate the expected payment due date (14 days after lease end date)
--      expected_due_date = end_date + INTERVAL '14 days';

--     -- Check if the payment date is greater than the expected due date
--     IF NEW.Payment_Date > expected_due_date THEN
--         -- Calculate the late fee (10% of the payment amount)
--         NEW.Late_Fee := 0.1 * NEW.Amount;
--     ELSE
--         -- No late fee if payment is made on or before the due date
--         NEW.Late_Fee := 0;
--     END IF;

--     RETURN NEW;
-- END;
-- $$
-- LANGUAGE plpgsql;

-- CREATE TRIGGER update_late_fee_trigger
-- BEFORE INSERT ON Payment
-- FOR EACH ROW
-- EXECUTE FUNCTION update_late_fee();

#Trigger 5

CREATE OR REPLACE FUNCTION create_employee_role_and_view()
RETURNS TRIGGER AS
$$
BEGIN
    -- Create a role for the new employee
    EXECUTE format('CREATE ROLE employee_role_%s with login password %L', NEW.Employee_ID,new.emp_password);

    -- Create a view of data in the employee table related to the particular employee only
    EXECUTE format('CREATE VIEW employee_view_%s AS SELECT * FROM Employee WHERE Employee_ID = %s', NEW.Employee_ID, NEW.Employee_ID);

    -- Grant SELECT privilege on the view to the corresponding role
    EXECUTE format('GRANT SELECT ON employee_view_%s TO employee_role_%s', NEW.Employee_ID, NEW.Employee_ID);

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER create_employee_role_and_view_trigger
AFTER INSERT ON Employee
FOR EACH ROW
EXECUTE FUNCTION create_employee_role_and_view();

# Trigger 6

CREATE OR REPLACE FUNCTION create_tenant_role_and_view()
RETURNS TRIGGER AS
$$
BEGIN
    -- Create a role for the new tenant
    EXECUTE format('CREATE ROLE tenant_role_%s with login password %L', NEW.Tenant_ID,NEW.tenant_pass);

    -- Create a view of data in the Tenant table related to the particular tenant only
    EXECUTE format('CREATE VIEW tenant_view_%s AS SELECT * FROM Tenant WHERE Tenant_ID = %s', NEW.Tenant_ID, NEW.Tenant_ID);
	
-- 	EXECUTE format('CREATE VIEW tenant_review_%s AS SELECT * FROM Review WHERE Tenant_ID = %s', NEW.Tenant_ID, NEW.Tenant_ID);
	
	EXECUTE format('CREATE VIEW tenant_lease_view_%s AS SELECT * FROM Review WHERE Tenant_ID = %s', NEW.Tenant_ID, NEW.Tenant_ID);

    -- Grant SELECT privilege on the view to the corresponding role
    EXECUTE format('GRANT SELECT ON tenant_view_%s TO tenant_role_%s', NEW.Tenant_ID, NEW.Tenant_ID);
	
	EXECUTE format('GRANT SELECT ON property_reviews TO tenant_role_%s', NEW.Tenant_ID);
	
	EXECUTE format('GRANT insert ON review TO tenant_role_%s', NEW.Tenant_ID);
	
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER create_tenant_role_and_view_trigger
AFTER INSERT ON Tenant
FOR EACH ROW
EXECUTE FUNCTION create_tenant_role_and_view();
