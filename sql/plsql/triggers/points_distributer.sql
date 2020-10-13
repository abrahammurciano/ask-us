create or replace trigger points_distributer
after insert on votes
for each row
begin
	update users
	set points = points + 1
	where id = (
		select author_id
		from all_posts
		where id = :new.post_id
	);

	update questions
	set points = points + 1
	where post_id = :new.post_id;

	update answers
	set points = points + 1
	where post_id = :new.post_id;

	update comments
	set points = points + 1
	where post_id = :new.post_id;
end;