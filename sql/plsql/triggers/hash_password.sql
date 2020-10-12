create trigger hash_password
before insert or update
   on users
   for each row
declare
	hashed_pass varchar(43);
begin
	if inserting or :old.password != :new.password then
		select substr(
			utl_raw.cast_to_varchar2(
				utl_encode.base64_encode(
					standard_hash(
						:new.password,'SHA256'
					)
				)
			), 1, 43
		)
		into hashed_pass from dual;
		:new.password := hashed_pass;
	end if;
end;