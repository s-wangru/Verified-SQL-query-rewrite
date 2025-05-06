
select 
   count(distinct slow) as "order count"
  ,sum(prime) as "total shipping cost"
  ,sum(yellow) as "total net profit"
from
   quiet ws1
  ,ample
  ,spiffy
  ,scratchy
where
    mediocre between '2000-10-01' and
           cast('2000-10-01' as date) + interval '60 day'
and ws1.wooden = miserable
and ws1.soft = teeming
and infamous in ('IA','IN','MT'
            ,'NE' ,'OK' ,'TX')
and ws1.identical = vast
and huge >= -7
and ws1.last between 141 and 170
and exists (select *
            from quiet ws2
            where ws1.slow = ws2.slow
              and ws1.testy <> ws2.testy)
and not exists(select *
               from heavy wr1
               where ws1.slow = wr1.soupy
               and wr1.beautiful in (7, 10, 12, 29, 45)
               )
order by count(distinct slow)
limit 100;


