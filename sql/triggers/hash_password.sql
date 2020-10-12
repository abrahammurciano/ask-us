create trigger hash_password
before insert or update
   on users
   for each row
declare
	hashed_pass varchar(40);
begin
	select standard_hash(:new.password, 'SHA256')
	into hashed_pass from dual;
	if inserting or :old.password != :new.password then
		:new.password := substr(
			utl_raw.cast_to_varchar2(
				utl_encode.base64_encode(hashed_pass)
			), 1, 43
		);
	end if;
end;