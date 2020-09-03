create table comments(
	post_id number(8) primary key references posts(id),
	parent_post_id number(8) references posts(id),
	body clob not null,
	points number(10) default 0 not null,
	timestamp date default sysdate not null
);