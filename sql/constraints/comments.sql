alter table comments add
constraint check_comments_points
	check (points >= 0);