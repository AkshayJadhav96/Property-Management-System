-----------------Function 1(Old)
create or replace function Calculate_company_revenue(
    companyID INT,
    startDate Date,
    endDate Date
    )
returns decimal
as $$
declare
totalRevenue decimal:=0;
begin
    select coalesce(sum(P.Amount),0)
    into totalRevenue
    from Lease L
    left join Payment P using(Lease_ID)
    where L.Property_ID in (Select Property_ID from Property where Company_ID=companyID)
    and P.Payment_Date between startDate and endDate;
    return totalRevenue;
end;
$$
language plpgsql;

select Calculate_company_revenue(2,'2021-5-21','2024-4-10');

--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--

-----------------Procedure 1(Old)
CREATE OR REPLACE PROCEDURE UpdateLatePayment()
LANGUAGE plpgsql
AS $$
DECLARE 
    threshold_date DATE;
BEGIN 
    -- SELECT Lease_Start_Date + INTERVAL '14 days' INTO threshold_date
    -- FROM Lease;

    UPDATE Payment
    SET Late_Fee = Amount * 0.1
    FROM Lease
    WHERE Lease.Lease_ID = Payment.Lease_ID
    AND Lease_Start_Date+ INTERVAL '14 days' < Payment_Date;

    COMMIT;
END;
$$;

-- call 
update payment
set late_fee=Null;
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Procedure 1

CREATE OR REPLACE PROCEDURE AddEmployee(
    p_employee_id INT,
    p_name VARCHAR(255),
    p_position VARCHAR(255),
    p_contact_information VARCHAR(255),
    p_salary DECIMAL(18, 2),
    p_department VARCHAR(255),
    p_employment_start_date DATE,
    p_employment_end_date DATE,
    p_company_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Employee(Employee_ID, Name, Position, Contact_Information, Salary, Department, Employment_Start_Date, Employment_End_Date, Company_ID)
    VALUES (p_employee_id, p_name, p_position, p_contact_information, p_salary, p_department, p_employment_start_date, p_employment_end_date, p_company_id);
    
    COMMIT;
END;
$$;

--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Procedure 2
CREATE OR REPLACE PROCEDURE UpdateLeaseStatus()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Update leases based on conditions
    UPDATE Lease
    SET Lease_Status = 
        CASE
            WHEN Lease_End_Date < CURRENT_DATE THEN 'Expired'
            WHEN Lease_End_Date >= CURRENT_DATE AND Lease_Status = 'Active' THEN 'Active'
            WHEN Lease_End_Date >= CURRENT_DATE AND Lease_Status = 'Expired' THEN 'Active' -- If lease was expired but now renewed
            ELSE Lease_Status
        END;
    
    COMMIT;
END;
$$;
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Procedure 3
CREATE OR REPLACE PROCEDURE GenerateMaintenanceReport()
LANGUAGE plpgsql
AS $$
DECLARE
    pending_requests INT;
    completed_requests INT;
BEGIN
    -- Count pending maintenance requests
    SELECT COUNT(*)
    INTO pending_requests
    FROM MaintenanceRequest
    WHERE Status = 'Pending';

    -- Count completed maintenance requests
    SELECT COUNT(*)
    INTO completed_requests
    FROM MaintenanceRequest
    WHERE Status = 'Completed';

    -- Print report
    RAISE NOTICE 'Maintenance Report:';
    RAISE NOTICE '------------------';
    RAISE NOTICE 'Pending Requests: %', pending_requests;
    RAISE NOTICE 'Completed Requests: %', completed_requests;

    COMMIT;
END;
$$;

--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Function1

CREATE OR REPLACE FUNCTION GetLeaseDuration(p_lease_id INT)
RETURNS text AS $$
DECLARE
    lease_duration INT;
	a int;
	b int;
BEGIN
    -- Calculate lease duration in months
    SELECT lease_end_Date - lease_start_Date
    INTO lease_duration
    FROM lease
    WHERE lease_ID = p_lease_id;

	return lease_duration||' '||'days';
	
END;
$$ LANGUAGE plpgsql;

select GetLeaseDuration(17);

select * from lease;
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Function2
CREATE OR REPLACE FUNCTION CalculateTotalLateFeesCollected()
RETURNS DECIMAL(18, 2) AS $$
DECLARE
    total_late_fees DECIMAL(18, 2);
BEGIN
    -- Calculate total late fees collected
    SELECT SUM(Late_Fee)
    INTO total_late_fees
    FROM Payment;

    RETURN COALESCE(total_late_fees, 0);
END;
$$ LANGUAGE plpgsql;
select CalculateTotalLateFeesCollected()
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Function3
CREATE OR REPLACE FUNCTION GetPropertyMaintenanceCost(p_property_id INT)
RETURNS DECIMAL(18, 2) AS $$
DECLARE
    total_maintenance_cost DECIMAL(18, 2);
BEGIN
    -- Calculate total maintenance cost for the property
    SELECT SUM(Cost)
    INTO total_maintenance_cost
    FROM MaintenanceRequest
    WHERE Maintenance_Request_ID IN (
        SELECT Maintenance_Request_ID
        FROM Property
        WHERE Property_ID = p_property_id
    );

    RETURN COALESCE(total_maintenance_cost, 0);
END;
$$ LANGUAGE plpgsql;

select GetPropertyMaintenanceCost(4)

--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--
-----------------Function4 @@@@@@@@@@
CREATE OR REPLACE FUNCTION GetEmployeeDetails(employ_id INT)
RETURNS TABLE (
    emplo_id INT,
    employ_name VARCHAR(255),
    pos VARCHAR(255),
    contact_information VARCHAR(255),
    salary DECIMAL(18, 2),
    department VARCHAR(255),
    employment_start_date DATE,
    employment_end_date DATE,
	comp_id int,
    company_name VARCHAR(255)
)
AS $$
BEGIN
    RETURN QUERY
        SELECT
            e.*,
            c.name AS company_name
        FROM
            Employee e
            LEFT JOIN Company c ON e.company_id = c.company_id
        WHERE
            employ_id=e.employee_id;
END;
$$ LANGUAGE plpgsql;


select GetEmployeeDetails(1)
select * from employee; 


CREATE OR REPLACE FUNCTION CalculateTotalRentDue(ten_id INT)
RETURNS DECIMAL(18, 2) 
AS $$
DECLARE 
    total_rent DECIMAL(18, 2);
BEGIN
    SELECT SUM(rent_due)
    INTO total_rent
    FROM (
        SELECT (rent_amount+coalesce(sum(late_fee),0) - COALESCE(SUM(amount), 0)) AS rent_due
        FROM Lease
        LEFT JOIN Payment ON Lease.lease_id = Payment.lease_id
        WHERE Lease.tenant_id = ten_id
        GROUP BY Lease.lease_id
    ) AS rent_due_per_lease;

    RETURN total_rent;
END
$$ 
LANGUAGE plpgsql;

drop function CalculateTotalRentDue

select CalculateTotalRentDue(4);


CREATE OR REPLACE FUNCTION GetAvailableProperties(size_x INT, property_type VARCHAR(255), min_price DECIMAL(18, 2), max_price DECIMAL(18, 2))
RETURNS TABLE (
  property_id INT,
  address VARCHAR(255),
  size INT,
  type VARCHAR(255),
  market_value DECIMAL(18, 2),
  landlord_name VARCHAR(255)
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.property_id as property_id,p.address as address,p.size as size,p.type as type,p.market_value as market_value,l.name AS landlord_name
  FROM Property p
  LEFT JOIN Landlord l ON p.landlord_id = l.landlord_id
  WHERE p.size >= $1
    AND p.type = $2
    AND p.market_value BETWEEN $3 AND $4
    AND NOT EXISTS (
      SELECT 1
      FROM Lease
      WHERE Lease.property_id = p.property_id
      AND Lease.lease_end_date > CURRENT_DATE
    );
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION AverageRatingForProperty(prop_id INT)
RETURNS DECIMAL(18, 2)
AS $$
DECLARE avg_rating DECIMAL(18, 2);
BEGIN
    SELECT AVG(rating) INTO avg_rating
    FROM Review
    WHERE property_id = $1;
    RETURN avg_rating;
END
$$ 
LANGUAGE plpgsql;

select AverageRatingForProperty(4);
