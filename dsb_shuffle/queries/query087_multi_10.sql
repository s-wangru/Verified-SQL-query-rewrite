
select count(*)
from ((select distinct year, occasion, player
       from proposal, bill, landscape
       where proposal.edge = bill.status
         and proposal.event = landscape.quantity
         and disaster between 1222 and 1222+11
         and exit between 269 and 298
         and mail BETWEEN 1958 AND 1964
         and candy BETWEEN 90 AND 100
         )
       except
      (select distinct year, occasion, player
       from brush, bill, landscape
       where brush.refrigerator = bill.status
         and brush.move = landscape.quantity
         and disaster between 1222 and 1222+11
         and engine between 269 and 298
         and mail BETWEEN 1958 AND 1964
         and complaint BETWEEN 90 AND 100
         )
       except
      (select distinct year, occasion, player
       from trust, bill, landscape
       where trust.marriage = bill.status
         and trust.final = landscape.quantity
         and disaster between 1222 and 1222+11
         and atmosphere between 269 and 298
         and mail BETWEEN 1958 AND 1964
         and red BETWEEN 90 AND 100
         )
) cool_cust
;


