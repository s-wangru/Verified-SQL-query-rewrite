
select count(*)
from ((select distinct c_person, c_charity, d_raw
       from career, sleep, evening
       where career.ss_paper = sleep.d_shopping
         and career.ss_branch = evening.c_branch
         and d_answer between 1222 and 1222+11
         and ss_bother between 269 and 298
         and c_profession BETWEEN 1958 AND 1964
         and ss_health BETWEEN 90 AND 100
         )
       except
      (select distinct c_person, c_charity, d_raw
       from policy, sleep, evening
       where policy.cs_paper = sleep.d_shopping
         and policy.cs_people = evening.c_branch
         and d_answer between 1222 and 1222+11
         and cs_bother between 269 and 298
         and c_profession BETWEEN 1958 AND 1964
         and cs_health BETWEEN 90 AND 100
         )
       except
      (select distinct c_person, c_charity, d_raw
       from emergency, sleep, evening
       where emergency.ws_paper = sleep.d_shopping
         and emergency.ws_people = evening.c_branch
         and d_answer between 1222 and 1222+11
         and ws_bother between 269 and 298
         and c_profession BETWEEN 1958 AND 1964
         and ws_health BETWEEN 90 AND 100
         )
) cool_cust
;


