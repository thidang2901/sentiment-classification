--1) Write a query to return all employees still working for the company with last names starting with "Smith" sorted by last name then first name.
select 
	*
from 
	employees e 
where 
	e.lastname like 'Smith%' and
	terminationdate is null
order by 
	e.lastname asc,
	e.firstname asc
;

--2) Given the `Employee` and `AnnualReviews` tables, write a query to return all employees who have never had a review sorted by HireDate.
select 
	*
from 
	employees e
where 
	e.id not in (select ar.empid from annual_reviews ar)
order by 
	e.hiredate asc
;

--3) Write a query to calculate the difference (in days) between the most and least tenured employee still working for the company
select 
	CURRENT_DATE - min(hiredate) as most_tenured, 
	CURRENT_DATE - max(hiredate) as least_tenured
FROM 
	employees e
where 
	e.terminationdate is null
;

--4) Given the employee table above, write a query to calculate the longest period (in days) that the company has gone without a hiring or firing anyone
select max(period_since_last_hiring_and_firing) as the_longest_period_since_last_hiring_and_firing
from (
	select 
		id, hire_date, last_hiring_and_firing, hire_date - last_hiring_and_firing as period_since_last_hiring_and_firing
	from (
		select 
			id, hire_date, 
			CASE
			    WHEN last_firing_since_last_hiring is null THEN last_hiring
			    ELSE last_firing_since_last_hiring
			END AS last_hiring_and_firing
		from (
			select 
				id, hire_date, last_hiring, 
				(select max(e3.terminationdate) from employees e3 where e3.terminationdate < hire_date and e3.terminationdate > last_hiring) as last_firing_since_last_hiring
			from (
				select 
					e.id as id, 
					e.hiredate as hire_date, 
					e.terminationdate as termination_date,
					(select max(e2.hiredate) from employees e2 where e2.hiredate < e.hiredate) as last_hiring
				from 
					employees e
			) as find_last_dates
		) as merged_last_dates
	) as calc_period
) as find_longest_period

--5) Write a query that returns each employee and for each row/employee include the greatest number of employees that worked for the company at any time during their tenure and the first date that maximum was reached. Extra points for not using cursors

