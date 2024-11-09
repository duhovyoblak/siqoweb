

-- Najprv musis vlozit userov
insert into PM_USER select * from SUSER where USER_ID not in  ('SIQO', 'Anonymous');

-- Nizke ID maju root items 
insert into pm_forum select * from sitem where ITEM_ID > 5;

select * from SUSER where USER_ID not in  ('SIQO', 'Anonymous');