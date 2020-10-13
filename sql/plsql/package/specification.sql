create package user_management as
	function hash_password(
		password in users.password%type
	) return users.password%type;

	function check_password(
		id in users.id%type,
		password in varchar(255)
	) return boolean;

	procedure change_password(
		id users.id%type,
		old_pass varchar(255),
		new_pass varchar(255)
	);
end user_management;