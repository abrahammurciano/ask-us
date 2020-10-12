update all_posts set points = 1 where points <= 0;
update all_posts set timestamp = sysdate where id = 66;