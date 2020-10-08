update users
set email = username||'@yahoo.com'
where username = 'watchfuleye' or username = 'werlwend';
commit;