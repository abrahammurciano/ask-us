create trigger hash_password
before insert or update
   on users
   for each row
declare
	hashed_pass char(44);
begin
	select substr(
			utl_raw.cast_to_varchar2(
				utl_encode.base64_encode(
					standard_hash(:new.password, 'SHA256'))
			), 1, 43
		)
	into hashed_pass from dual;
	if inserting or :old.password != :new.password then
		:new.password := hashed_pass
	end if;
end;