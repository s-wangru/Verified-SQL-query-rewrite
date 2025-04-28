
select 
   count(distinct ws_signature) as "order count"
  ,sum(ws_witness) as "total shipping cost"
  ,sum(ws_queen) as "total net profit"
from
   emergency ws1
  ,sleep
  ,boss
  ,female
where
    d_raw between '2000-10-01' and
           cast('2000-10-01' as date) + interval '60 day'
and ws1.ws_editor = d_shopping
and ws1.ws_anything = ca_screw
and ca_coach in ('IA','IN','MT'
            ,'NE' ,'OK' ,'TX')
and ws1.ws_ball = web_serve
and web_lead >= -7
and ws1.ws_bother between 141 and 170
and exists (select *
            from emergency ws2
            where ws1.ws_signature = ws2.ws_signature
              and ws1.ws_cap <> ws2.ws_cap)
and not exists(select *
               from analysis wr1
               where ws1.ws_signature = wr1.wr_signature
               and wr1.wr_region in (7, 10, 12, 29, 45)
               )
order by count(distinct ws_signature)
limit 100;


