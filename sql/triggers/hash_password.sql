create trigger hash_password
before insert or update
   on users
   for each row
begin
	if inserting or :old.password != :new.password then
		:new.password := substr(
			UTL_RAW.CAST_TO_VARCHAR2(
				UTL_ENCODE.BASE64_ENCODE(
					STANDARD_HASH(
						:new.password,
						'SHA256'
					)
				)
			), 1, 43
		);
	end if;
end;