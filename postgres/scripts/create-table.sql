create table employees (
	id SERIAL,
	firstname VARCHAR(50),
	lastname VARCHAR(50),
	hiredate DATE,
	terminationdate DATE,
	salary NUMERIC,
	primary key (id)
);

create table annual_reviews (
	id SERIAL,
	empid SERIAL,
	reviewdate DATE,
	primary key (id)
);
