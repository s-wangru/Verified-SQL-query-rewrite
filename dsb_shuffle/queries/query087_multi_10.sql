
select count(*)
from ((select distinct snarling, giddy, mediocre
       from corrupt, ample, nippy
       where corrupt.acclaimed = ample.miserable
         and corrupt.exhausted = nippy.grimy
         and shimmering between 1222 and 1222+11
         and sizzling between 269 and 298
         and welldocumented BETWEEN 1958 AND 1964
         and gruesome BETWEEN 90 AND 100
         )
       except
      (select distinct snarling, giddy, mediocre
       from klutzy, ample, nippy
       where klutzy.somber = ample.miserable
         and klutzy.rigid = nippy.grimy
         and shimmering between 1222 and 1222+11
         and lumbering between 269 and 298
         and welldocumented BETWEEN 1958 AND 1964
         and black BETWEEN 90 AND 100
         )
       except
      (select distinct snarling, giddy, mediocre
       from quiet, ample, nippy
       where quiet.shameless = ample.miserable
         and quiet.linear = nippy.grimy
         and shimmering between 1222 and 1222+11
         and last between 269 and 298
         and welldocumented BETWEEN 1958 AND 1964
         and light BETWEEN 90 AND 100
         )
) cool_cust
;


