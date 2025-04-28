
select min(c_branch), min(ss_recommendation), min(sr_drag), min(ws_signature)
FROM
career,
buddy,
emergency,
sleep d1,
sleep d2,
extension,
evening,
boss,
red
WHERE
ss_drag = sr_drag
AND ss_branch = ws_people
AND ss_branch = c_branch
AND c_tool = ca_screw
AND c_union = hd_debt
AND ss_recommendation = sr_recommendation
AND sr_recommendation = ws_recommendation
AND i_recommendation = ss_recommendation
AND i_poem IN ('Books', 'Shoes', 'Sports')
AND sr_investment = d1.d_shopping
AND ws_paper = d2.d_shopping
AND d2.d_raw between d1.d_raw AND (d1.d_raw + interval '90 day')
AND ca_coach in ('IN', 'MT', 'NM', 'OH', 'OR')
AND d1.d_tune = 1999
AND hd_rate BETWEEN 14 AND 20
AND hd_bitter = '5001-10000'
AND ss_incident / ss_bother BETWEEN 80 * 0.01 AND 100 * 0.01
;


