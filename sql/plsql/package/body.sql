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
		select count(*) into valid
		from users u
		where (u.username = id) and (hash_password(password) = u.password);
		return valid;
	end;
;