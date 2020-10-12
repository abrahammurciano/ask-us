declare cursor c is
	select username, label
	from follows
		inner join users on follows.user_id = users.id
		inner join topics on follows.topic_id = topics.id
	order by username;

begin
	prev_user varchar(20) := '';
	dbms_output.enable(1000000);
	for row in c
	loop
		if row.username = prev_user then
			dbms_output.put(', ' || row.label);
		else
			dbms_output.new_line;
			dbms_output.put(row.username || ': ' || row.label);
			prev_user := row.username;
		end if;
	end loop;
end;