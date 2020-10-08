update users
set password = substr(
	UTL_RAW.CAST_TO_VARCHAR2(
		UTL_ENCODE.BASE64_ENCODE(
			STANDARD_HASH(
				substr(
					email,
					1,
					instr(email, '@') - 1
				),
				'SHA256'
			)
		)
	), 1, 43
)
where mod(id, 2) != 0;
commit;