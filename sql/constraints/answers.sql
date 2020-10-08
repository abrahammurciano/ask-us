alter table answers add
constraint check_answers_points
	check (points >= 0);