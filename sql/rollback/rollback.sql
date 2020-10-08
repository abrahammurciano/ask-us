-- 1. Select the data
select * from users where username like 'a%';

-- 2. Update email endings
update users
set email = substr(email, 1, instr(email, '@') - 1) || '@aol.com'
where username like 'a%';

-- 3. Select the updated data
select * from users where username like 'a%';

-- 4. Undo the changes
rollback;

-- 5. Select the rolled back data
select * from users where username like 'a%';