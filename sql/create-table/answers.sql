create table answers(
	post_id number(8) primary key references posts(id),
	accepted number(1) default 0 not null,
	question_id number(8) references questions(post_id) not null,
	body clob not null,
	points number(10) default 0 not null,
	timestamp date default sysdate not null,
	author_id number(8) references users(id) not null
);