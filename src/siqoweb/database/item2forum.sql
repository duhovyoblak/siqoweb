

-- Najprv musis vlozit userov
insert into PM_USER select * from SUSER where USER_ID not in  ('SIQO', 'Anonymous');

insert into pm_forum select * from sitem;

select * from SUSER where USER_ID not in  ('SIQO', 'Anonymous');