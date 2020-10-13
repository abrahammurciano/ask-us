create package body user_management as
	function hash_password(
		password in varchar(255)
	) return char(43) is hashed_pass char(43)
	begin

	end;
;