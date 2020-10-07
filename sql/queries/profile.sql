select * from (
	select title, points, timestamp
	from questions
	where author_id = 11
	union
	select to_char(substr(body, 1, 4000)), points, timestamp
	from answers
	where author_id = 11
	union
	select to_char(substr(body, 1, 4000)), points, timestamp
	from comments
	where author_id = 11
) order by timestamp desc;