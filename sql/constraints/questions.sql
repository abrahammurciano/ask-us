alter table questions add
constraint check_questions_points
	check (points >= 0);