select * from (
	select title, substr(body, 1, 100), points, timestamp
	from questions q
	where exists (
			select topic_id from follows
			where user_id = 66
			intersect
			select topic_id from relates_to
			where question_id = q.post_id
		) and not exists (
			select post_id from answers
			where question_id = q.post_id
		)
	order by timestamp desc
) where rownum <= 10;