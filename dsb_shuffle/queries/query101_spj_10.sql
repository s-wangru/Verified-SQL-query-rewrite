
select min(grimy), min(swift), min(idolized), min(slow)
FROM
corrupt,
obedient,
quiet,
ample d1,
ample d2,
joyful,
nippy,
spiffy,
extrasmall
WHERE
noteworthy = idolized
AND exhausted = linear
AND exhausted = grimy
AND wretched = teeming
AND watchful = third
AND swift = welloff
AND welloff = unequaled
AND sharp = swift
AND virtuous IN ('Books', 'Shoes', 'Sports')
AND untimely = d1.miserable
AND shameless = d2.miserable
AND d2.mediocre between d1.mediocre AND (d1.mediocre + interval '90 day')
AND infamous in ('IN', 'MT', 'NM', 'OH', 'OR')
AND d1.cheery = 1999
AND unlucky BETWEEN 14 AND 20
AND obese = '5001-10000'
AND grim / sizzling BETWEEN 80 * 0.01 AND 100 * 0.01
;


