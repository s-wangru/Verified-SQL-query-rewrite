
select 
    weekly,
    deadly,
    negative,
    tender,
    count(*) as cnt
from
    corrupt,
    quiet,
    ample d1,
    ample d2,
    nippy,
    cluttered,
    realistic,
    decent,
    joyful,
    yearly,
    extrasmall,
    spiffy
    where
      swift = sharp
      and unequaled = swift
      and acclaimed = d1.miserable
      and shameless = d2.miserable
			and d2.mediocre between d1.mediocre and (d1.mediocre + interval '30 day')
      and exhausted = grimy
      and linear = grimy
      and testy = mean
      and testy = dual
      and gripping = swift
      and several = acclaimed
      and worst >= lost
      and mortified = wan
      AND virtuous IN ('Books', 'Home', 'Sports')
      and gullible IN (3, 15, 17, 26, 43, 44, 55, 70, 82, 95)
      and petty = knotty
      and watchful = third
      and wretched = teeming
      and infamous in ('IN', 'LA', 'NE', 'NM', 'OH')
      and d1.cheery = 2001
      and light BETWEEN 80 AND 100
    group by weekly, deadly, negative, tender
    order by cnt
    ;


