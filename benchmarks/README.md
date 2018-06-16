In average *252 req/sec* with *200 concurrent clients* - IMHO not too bad :)

```
$ locust -f ratestask.py --no-web -c 200 -r 50 -n 10000 --logfile=ratestask.log --print-stats --only-summary
 Name                                                          # reqs      # fails     Avg     Min     Max  |  Median   req/s
--------------------------------------------------------------------------------------------------------------------------------------------
 GET /get?date_from=2016-01-1&date_to=2016-01-05&origin=CNQIN&destination=NOKRS    2029     0(0.00%)     628      83   37811  |     170   50.10
 GET /get?date_from=2016-01-1&date_to=2016-01-05&origin=cnGGz&destination=eEtll    2061     0(0.00%)     537      85   37804  |     170   50.70
 GET /get?date_from=2016-01-1&date_to=2016-01-10&origin=CNQIN&destination=NOKRS    2031     0(0.00%)     613      90   37779  |     170   51.80
 GET /get?date_from=2016-01-1&date_to=2016-01-10&origin=cnGGz&destination=eEtll    2045     0(0.00%)     433      87   37765  |     170   49.10
 POST /put                                                       2033     0(0.00%)     523      86   37511  |     160   50.40
--------------------------------------------------------------------------------------------------------------------------------------------
 Total                                                          10199     0(0.00%)                                     252.10

Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 GET /get?date_from=2016-01-1&date_to=2016-01-05&origin=CNQIN&destination=NOKRS     2029    170    180    190    200    220    290    530  36000  37811
 GET /get?date_from=2016-01-1&date_to=2016-01-05&origin=cnGGz&destination=eEtll     2061    170    180    190    200    220    310    520    740  37804
 GET /get?date_from=2016-01-1&date_to=2016-01-10&origin=CNQIN&destination=NOKRS     2031    170    180    190    200    220    330    530  36000  37779
 GET /get?date_from=2016-01-1&date_to=2016-01-10&origin=cnGGz&destination=eEtll     2045    170    180    200    200    220    280    550    730  37765
 POST /put                                                        2033    160    180    190    200    220    350    630    770  37511
--------------------------------------------------------------------------------------------------------------------------------------------
```
