alter table users add (
	constraint check_users_email
		check (email like '_%@_%._%'),
	constraint check_users_points
		check (points >= 0)
);