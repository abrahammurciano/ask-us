create table topics(
	id number(8) primary key generated always as identity,
	label varchar(20) unique not null,
	description varchar(255) not null
);