create package user_management as
	function hash_password(
		password in users.password%type
	) return users.password%type;

	function check_password(
		uid in users.id%type,
		password in varchar
	) return boolean;

	procedure change_password(
		id users.id%type,
		old_pass varchar,
		new_pass varchar
	);
end user_management;