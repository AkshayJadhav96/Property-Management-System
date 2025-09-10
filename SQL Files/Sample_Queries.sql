-- Q1)
-- select name,rent_amount from tenant,lease
-- where tenant.tenant_id=lease.tenant_id and
-- tenant.employment_status='Student' and 
-- lease.rent_amount>=1300 and lease.rent_amount<=1700;

-- Q2)
-- select name,specialization from contractor,maintenancerequest
-- where contractor.contractor_id=maintenancerequest.assigned_contractor_id and
-- maintenancerequest.status!='Completed'

-- Q3)
-- select address,market_value,name
-- from property,landlord,insurancepolicy 
-- where property.landlord_id=landlord.landlord_id and
-- insurancepolicy.property_id=property.property_id and
-- insurancepolicy.expiry_date<current_date;

-- Q4)
-- select name,property.address,market_value,rent_amount
-- from company,property,lease
-- where company.company_id=property.company_id and 
-- property.property_id=lease.property_id and
-- property.built_year<2000 and
-- lease.rent_amount>1500

-- Q5)
-- select tenant.name,company.name,amount
-- from tenant,lease,payment,company,property
-- where 
-- tenant.tenant_id=lease.tenant_id and
-- lease.lease_id=payment.lease_id and
-- property.property_id=lease.property_id and
-- company.company_id=property.company_id and
-- (payment_method='Bank Transfer' or payment_method='Credit Card'); 

-- select lease_id,lease_start_date from lease ;

-- update payment 
-- set payment_date='2023-10-17'
-- where lease_id=10
