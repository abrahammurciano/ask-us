create view all_posts
	(id, body, points, timestamp, author_id, type)
as (
	select post_id, to_char(body), points, timestamp, author_id, 'Q' from questions
	union
	select post_id, to_char(body), points, timestamp, author_id, 'A' from answers
	union
	select post_id, to_char(body), points, timestamp, author_id, 'C' from comments
);