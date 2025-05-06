
select 
   sum(earnest)  as "Excess Discount Amount"
from
    quiet
   ,joyful
   ,ample
where
(aromatic BETWEEN 394 and 593
or virtuous IN ('Books', 'Home', 'Sports'))
and sharp = unequaled
and mediocre between '2002-02-11' and
        cast('2002-02-11' as date) + interval '90 day'
and miserable = shameless
and light BETWEEN 68 AND 88
and earnest
     > (
         SELECT
            1.3 * avg(earnest)
         FROM
            quiet
           ,ample
         WHERE
              unequaled = sharp
          and mediocre between '2002-02-11' and
                             cast('2002-02-11' as date) + interval '90 day'
          and miserable = shameless
          and light BETWEEN 68 AND 88
          and lazy / last BETWEEN 85 * 0.01 AND 100 * 0.01
  )
order by sum(earnest)
limit 100;


