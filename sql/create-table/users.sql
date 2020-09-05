create table users(
	id number(8) generated always as identity primary key,
	username varchar(20) unique not null,
	email varchar(320) unique not null,
	password char(44) not null,   -- base64 sha256 is 44 chars
	points number(10) default 0 not null
);