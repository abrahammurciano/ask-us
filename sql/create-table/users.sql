create table users(
	id number(8) generated always as identity primary key,
	username varchar(20) unique not null,
	email varchar(320) unique not null,
	password varchar(255) not null,   -- base64 sha256 hash of password
	points number(10) default 0 not null
);