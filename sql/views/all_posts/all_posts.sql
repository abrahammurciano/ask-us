create or replace view all_posts
	(id, body, points, timestamp, type)
as (
	select post_id, to_char(body), points, timestamp, 'Q' from questions
	union
	select post_id, to_char(body), points, timestamp, 'A' from answers
	union
	select post_id, to_char(body), points, timestamp, 'C' from comments
);