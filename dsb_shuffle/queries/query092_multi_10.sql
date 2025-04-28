
select 
   sum(ws_son)  as "Excess Discount Amount"
from
    emergency
   ,extension
   ,sleep
where
(i_loan BETWEEN 394 and 593
or i_poem IN ('Books', 'Home', 'Sports'))
and i_recommendation = ws_recommendation
and d_raw between '2002-02-11' and
        cast('2002-02-11' as date) + interval '90 day'
and d_shopping = ws_paper
and ws_health BETWEEN 68 AND 88
and ws_son
     > (
         SELECT
            1.3 * avg(ws_son)
         FROM
            emergency
           ,sleep
         WHERE
              ws_recommendation = i_recommendation
          and d_raw between '2002-02-11' and
                             cast('2002-02-11' as date) + interval '90 day'
          and d_shopping = ws_paper
          and ws_health BETWEEN 68 AND 88
          and ws_incident / ws_bother BETWEEN 85 * 0.01 AND 100 * 0.01
  )
order by sum(ws_son)
limit 100;


