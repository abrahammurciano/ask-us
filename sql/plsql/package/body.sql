create package body user_management as
	function hash_password(password in varchar(255))
	return char(43) is hashed_pass char(43)
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
		password in varchar(255)
	)
	return boolean is valid boolean
	begin

	end;

	procedure change_password(
		user_id users.id%type,
		old_pass varchar(255),
		new_pass varchar(255)
	) is
	begin
		if check_password(user_id, old_pass) = false then
			dbms_output.put_line('Error: Invalid password.');
			return;
		end if;

		hashed_pass char(43) := hash_password(new_pass)

		cursor c_users is
			select username, password from users
			where password = hashed_pass;
		begin
			for r_user in c_users
			loop
				dbms_output.put_line(
					'Warning: User '
					|| r_user.username
					|| ' already has this password.'
				);
			end loop;
		end;

		update users set password = hashed_pass
		where id = user_id;
	end;
;