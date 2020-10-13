create package body user_management as
	function hash_password(password in users.password%type)
	return users.password%type is hashed_pass users.password%type;
	begin
		select substr(
			utl_raw.cast_to_varchar2(
				utl_encode.base64_encode(
					standard_hash(
						password, 'SHA256'
					)
				)
			), 1, 43
		)
		into hashed_pass from dual;
		return hashed_pass;
	end;

	function check_password(
		id in users.id%type,
		password in varchar
	) return boolean is
		valid number;
	begin
		select (
			case when exists (
				select * from users u
				where (u.username = id)
				and (hash_password(password) = u.password)
			) then 1 else 0 end
		) into valid from dual;

		if valid = 1 then
			return true;
		else
			return false;
		end if;
	end;

	procedure change_password(
		id users.id%type,
		old_pass varchar,
		new_pass varchar
	) is
		hashed_pass users.password%type := hash_password(new_pass);
		cursor c_users is
			select username, password from users
			where password = hashed_pass;
	begin
		if check_password(id, old_pass) = false then
			dbms_output.put_line('Error: Invalid password.');
			return;
		end if;

		for r_user in c_users
		loop
			dbms_output.put_line(
				'Warning: User '
				|| r_user.username
				|| ' already has this password.'
			);
		end loop;

		update users u set password = hashed_pass
		where u.id = id;
	end;
end user_management;