-- Select the data
select * from users where username like 'a%';

-- Update email endings
update users
set email = substr(email, 1, instr(email, '@') - 1) || '@aol.com'
where username like 'a%';

-- Select the updated data
select * from users where username like 'a%';

-- Undo the changes
rollback;

-- Select the rolled back data
select * from users where username like 'a%';