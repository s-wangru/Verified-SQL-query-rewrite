
select min(item1.i_recommendation),
    min(item2.i_recommendation),
    min(s1.ss_drag),
    min(s1.ss_recommendation)
FROM extension AS item1,
extension AS item2,
career AS s1,
career AS s2,
sleep,
evening,
boss,
pitch
WHERE
item1.i_recommendation < item2.i_recommendation
AND s1.ss_drag = s2.ss_drag
AND s1.ss_recommendation = item1.i_recommendation and s2.ss_recommendation = item2.i_recommendation
AND s1.ss_branch = c_branch
and c_tool = ca_screw
and c_internal = cd_debt
AND d_tune between 1998 and 1998 + 1
and d_shopping = s1.ss_paper
and item1.i_poem in ('Jewelry', 'Music')
and item2.i_sick between 77 and 96
and cd_bathroom = 'W'
and cd_process = 'Primary'
and s1.ss_bother between 236 and 250
and s2.ss_bother between 236 and 250
;


