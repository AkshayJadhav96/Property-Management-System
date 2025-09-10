CREATE TABLE Company (
    Company_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Contact_Number TEXT,
    CEO VARCHAR(255),
    Revenue_in_Crores DECIMAL(18, 2),
    Number_of_Employees INT
);
 

CREATE TABLE Landlord (
    Landlord_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Contact_Information VARCHAR(255),
    Bank_Account VARCHAR(255),
    Tax_ID VARCHAR(255)
);


-- Employee table
CREATE TABLE Employee (
    Employee_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Position VARCHAR(255),
    Contact_Information VARCHAR(255),
    Salary DECIMAL(18, 2),
    Department VARCHAR(255),
    Employment_Start_Date DATE,
    Employment_End_Date DATE,
    Company_ID INT,
    FOREIGN KEY (Company_ID) REFERENCES Company(Company_ID)
);

-- Contractor table
CREATE TABLE Contractor (
    Contractor_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Contact_Information VARCHAR(255),
    Specialization VARCHAR(255),
    Hourly_Rate DECIMAL(18, 2)
);

CREATE TABLE Workers (
    Worker_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Contact_Information VARCHAR(255),
    Salary DECIMAL(18, 2),
    Contractor_ID INT,
    FOREIGN KEY (Contractor_ID) REFERENCES Contractor(Contractor_ID)
);

CREATE TABLE MaintenanceRequest (
    Maintenance_Request_ID INT PRIMARY KEY,
    Description TEXT,
    Request_Date DATE,
    Status VARCHAR(255),
    Assigned_Contractor_ID INT,
    Completion_Date DATE,
    Cost DECIMAL(18, 2),
    FOREIGN KEY (Assigned_Contractor_ID) REFERENCES Contractor(Contractor_ID)
);

CREATE TABLE Property (
    Property_ID INT PRIMARY KEY,
    Address VARCHAR(255),
    Size INT,
    Type VARCHAR(255),
    Market_Value DECIMAL(18, 2),
    Built_Year INT,
    Company_ID INT,
    Landlord_ID INT,
    Maintenance_Request_ID INT,
    FOREIGN KEY (Company_ID) REFERENCES Company(Company_ID),
    FOREIGN KEY (Landlord_ID) REFERENCES Landlord(Landlord_ID),
    FOREIGN KEY (Maintenance_Request_ID) REFERENCES MaintenanceRequest(Maintenance_Request_ID)
);


-- Tenant table
CREATE TABLE Tenant (
    Tenant_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT,
    Gender VARCHAR(50),
    Contact_Information VARCHAR(255),
    Employment_Status VARCHAR(255),
    Background_Check VARCHAR(255)
);


-- Lease table
CREATE TABLE Lease (
    Lease_ID INT PRIMARY KEY,
    Property_ID INT,
    Tenant_ID INT,
    Lease_Start_Date DATE,
    Lease_End_Date DATE,
    Rent_Amount DECIMAL(18, 2),
    Payment_History TEXT,
    Lease_Status VARCHAR(255),
    Renewal_Terms VARCHAR(255),
    FOREIGN KEY (Property_ID) REFERENCES Property(Property_ID),
    FOREIGN KEY (Tenant_ID) REFERENCES Tenant(Tenant_ID)
);


-- Payment table
CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY,
    Lease_ID INT,
    Payment_Date DATE,
    Amount DECIMAL(18, 2),
    Payment_Method VARCHAR(255),
    Late_Fee DECIMAL(18, 2),
    FOREIGN KEY (Lease_ID) REFERENCES Lease(Lease_ID)
);


-- Review table
CREATE TABLE Review (
    Review_ID INT PRIMARY KEY,
    Tenant_ID INT,
    Property_ID INT,
    Rating INT,
    Comment TEXT,
    Date DATE,
    FOREIGN KEY (Tenant_ID) REFERENCES Tenant(Tenant_ID),
    FOREIGN KEY (Property_ID) REFERENCES Property(Property_ID)
);


-- InsurancePolicy table
CREATE TABLE InsurancePolicy (
    Policy_ID INT PRIMARY KEY,
    Property_ID INT,
    Coverage_Amount DECIMAL(18, 2),
    Premium DECIMAL(18, 2),
    Expiry_Date DATE,
    Coverage_Type VARCHAR(255),
    FOREIGN KEY (Property_ID) REFERENCES Property(Property_ID)
);


