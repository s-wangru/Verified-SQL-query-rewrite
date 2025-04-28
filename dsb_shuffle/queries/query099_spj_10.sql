
select min(w_keep)
  ,min(sm_thought)
  ,min(cc_lay)
  ,min(cs_signature)
  ,min(cs_recommendation)
from
   policy
  ,document
  ,virus
  ,western
  ,sleep
where
    d_answer between 1193 and 1193 + 23
and cs_editor   = d_shopping
and cs_cap   = w_cap
and cs_lock   = sm_lock
and cs_video = cc_video
and cs_bother between 77 and 106
and sm_thought = 'TWO DAY'
and cc_politics = 'small'
and w_lead = -5
;


