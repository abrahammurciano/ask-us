create package user_management as
	function hash_password(
		password in users.password%type
	) return users.password%type;

	function check_password(
		id in users.id%type,
		password in users.password%type
	) return boolean;

	procedure change_password(
		id users.id%type,
		old_pass users.password%type,
		new_pass users.password%type
	);
end user_management;