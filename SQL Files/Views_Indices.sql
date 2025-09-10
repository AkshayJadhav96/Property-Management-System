-------------Views-------------------


--111-- PropertyDetailsView:
CREATE VIEW PropertyDetailsView AS
SELECT p.Property_ID, p.Address, p.Size, p.Type, p.Market_Value,
       c.Name AS Company_Name, l.Name AS Landlord_Name
FROM Property p
INNER JOIN Company c ON p.Company_ID = c.Company_ID
INNER JOIN Landlord l ON p.Landlord_ID = l.Landlord_ID;
select * from PropertyDetailsView;

--112-- EmployeeDetailsView:
CREATE VIEW EmployeeDetailsView AS
SELECT e.Employee_ID, e.Name AS Employee_Name, e.Position, e.Contact_Information,
       e.Salary, e.Department, e.Employment_Start_Date, e.Employment_End_Date,
       c.Name AS Company_Name
FROM Employee e
INNER JOIN Company c ON e.Company_ID = c.Company_ID;
select * from EmployeeDetailsView

--113-- LeaseDetailsView:
CREATE VIEW LeaseDetailsView AS
SELECT l.Lease_ID, p.Address AS Property_Address, t.Name AS Tenant_Name,
       l.Lease_Start_Date, l.Lease_End_Date, l.Rent_Amount, l.Payment_History,
       l.Lease_Status
FROM Lease l
INNER JOIN Property p ON l.Property_ID = p.Property_ID
INNER JOIN Tenant t ON l.Tenant_ID = t.Tenant_ID;
select * from LeaseDetailsView

--114-- MaintenanceRequestOverview:
CREATE VIEW MaintenanceRequestOverview AS
SELECT mr.Maintenance_Request_ID, p.Address AS Property_Address,
       mr.Description, mr.Request_Date, mr.Status,
       c.Name AS Contractor_Name, mr.Completion_Date, mr.Cost
FROM MaintenanceRequest mr
INNER JOIN Contractor c ON mr.Assigned_Contractor_ID = c.Contractor_ID
INNER JOIN Property p ON mr.Maintenance_Request_ID = p.Maintenance_Request_ID;
select * from MaintenanceRequestOverview

--115-- TenantReviews:
CREATE VIEW TenantReviews AS
SELECT r.Review_ID, t.Name AS Tenant_Name, t.Age, t.Gender,
       p.Address AS Property_Address, r.Rating, r.Comment, r.Date
FROM Review r
INNER JOIN Tenant t ON r.Tenant_ID = t.Tenant_ID
INNER JOIN Property p ON r.Property_ID = p.Property_ID;
select * from TenantReviews





----------------Indices---------------------

--121--Company table
CREATE INDEX idx_company_name ON Company (Name);

--122--Employee table
CREATE INDEX idx_employee_company_id ON Employee (Company_ID);
CREATE INDEX idx_employee_name ON Employee (Name);

--123--Contractor table
CREATE INDEX idx_contractor_name ON Contractor (Name);
CREATE INDEX idx_contractor_specialization ON Contractor (Specialization);

--124--MaintenanceRequest table
CREATE INDEX idx_maintenance_request_status ON MaintenanceRequest (Status);
CREATE INDEX idx_maintenance_request_completion_date ON MaintenanceRequest (Completion_Date);

--125--Property table
CREATE INDEX idx_property_address ON Property (Address);
CREATE INDEX idx_property_type ON Property (Type);


--126--Lease table
CREATE INDEX idx_lease_property_id ON Lease (Property_ID);
CREATE INDEX idx_lease_tenant_id ON Lease (Tenant_ID);
CREATE INDEX idx_lease_status ON Lease (Lease_Status);

--127--Tenant table
CREATE INDEX idx_tenant_name ON Tenant (Name);

--128--Payment table
CREATE INDEX idx_payment_lease_id ON Payment (Lease_ID);
CREATE INDEX idx_payment_date ON Payment (Payment_Date);

--129--Review table
CREATE INDEX idx_review_property_id ON Review (Property_ID);
CREATE INDEX idx_review_tenant_id ON Review (Tenant_ID);

--130--InsurancePolicy table
CREATE INDEX idx_insurance_policy_property_id ON InsurancePolicy (Property_ID);
CREATE INDEX idx_insurance_policy_expiry_date ON InsurancePolicy (Expiry_Date);
