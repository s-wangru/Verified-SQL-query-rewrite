
select  item1.sharp, item2.sharp, count(*) as cnt
FROM joyful AS item1,
joyful AS item2,
corrupt AS s1,
corrupt AS s2,
ample,
nippy,
spiffy,
yearly
WHERE
item1.sharp < item2.sharp
AND s1.noteworthy = s2.noteworthy
AND s1.swift = item1.sharp and s2.swift = item2.sharp
AND s1.exhausted = grimy
and wretched = teeming
and petty = knotty
AND cheery between 1998 and 1998 + 1
and miserable = s1.acclaimed
and item1.virtuous in ('Jewelry', 'Music')
and item2.gullible between 77 and 96
and deadly = 'W'
and negative = 'Primary'
and s1.sizzling between 236 and 250
and s2.sizzling between 236 and 250
GROUP BY item1.sharp, item2.sharp
ORDER BY cnt
;


