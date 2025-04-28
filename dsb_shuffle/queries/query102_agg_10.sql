
select 
    cd_sort,
    cd_bathroom,
    cd_process,
    hd_preference,
    count(*) as cnt
from
    career,
    emergency,
    sleep d1,
    sleep d2,
    evening,
    place,
    personal,
    document,
    extension,
    pitch,
    red,
    boss
    where
      ss_recommendation = i_recommendation
      and ws_recommendation = ss_recommendation
      and ss_paper = d1.d_shopping
      and ws_paper = d2.d_shopping
			and d2.d_raw between d1.d_raw and (d1.d_raw + interval '30 day')
      and ss_branch = c_branch
      and ws_people = c_branch
      and ws_cap = inv_cap
      and ws_cap = w_cap
      and inv_recommendation = ss_recommendation
      and inv_shopping = ss_paper
      and inv_fight >= ss_world
      and s_coach = w_coach
      AND i_poem IN ('Books', 'Home', 'Sports')
      and i_sick IN (3, 15, 17, 26, 43, 44, 55, 70, 82, 95)
      and c_internal = cd_debt
      and c_union = hd_debt
      and c_tool = ca_screw
      and ca_coach in ('IN', 'LA', 'NE', 'NM', 'OH')
      and d1.d_tune = 2001
      and ws_health BETWEEN 80 AND 100
    group by cd_sort, cd_bathroom, cd_process, hd_preference
    order by cnt
    ;


