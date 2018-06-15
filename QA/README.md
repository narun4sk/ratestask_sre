In this section we will provide a description of a largely extended
version of the service implemented above. Provide answers at a
high-level, using a couple of paragraphs for each question.

## Service definition

Imagine that for this service you need to receive and insert big
batches of new prices, ranging within tens of thousands of items,
conforming to a similar format. Each batch of items needs to be
processed together, either all items go in, or none of them does.

Both the incoming data updates and requests for data can be highly
sporadic - there might be large periods without much activity,
followed by periods of heavy activity.

Being a paid service, high availability is very much a requirement.

1. How would you design the system?
2. What parts of the system do you expect to become the bottlenecks as the load grows?
3. How can those bottlenecks be addressed in the future?

Provide a high-level diagram, along with a few paragraphs describing the choices you've made and what factors do you need to take into consideration.

```
DIAGRAM                   XXXXXXXXXXXXX
                         XX            XXXXXX
                        XX                  XX  XXXXX
                      XXX                    XXX     XXX
                      X     INTERNET                   XX
                    XXX                                 XX
                    XXXXXXXX                             XX
                           XXXXX+XXXX^XXXXX        XXXXXXXX
                                |    |     XXXXXXXXX
                                |    |
                                |    |
          Traffic flow   +------v----+-------------+
       +----------------->                         |
       |                 |  LOAD BALANCER          |
       |    +--------------------------------------+
       |    |            |  CACHING SERVER         |
       |    |            +-------------------------+
       |    |
+------+----v--------------------+        +----------------------------------+
|      GREEN SERVERS             |        |      BLUE SERVERS                |
+--------------------------------+        +----------------------------------+
|SRV_1    |SRV_2       |SRV_N    |        |SRV_1     |SRV_2       |SRV_N     |
|         |            |         |        |          |            |          |
+-----^---+---+--------+---------+        +----------+------------+----------+
      |       |
      |       |
      |       |       +----------------------------------+
      |       |       |     DATABASE CLUSTER             |
      |       |       +----------------+-----------------+
      |       +------->  READ/WRITE    | READ/WRITE      |
      +---------------+  REPLICA/SHARD | REPLICA/SHARD   |
                      +----------------+-----------------+
```

### Answers

1. I would try to implement the system similar to what's shown in the diagram, namely a *blue/green deployment*.
   One copy of the application (green) would be deployed alongside the existing version (blue). Then the *load
   balancer* is updated to switch to the new version (green). The most part of the traffic to the app changes to
   the new version all at once, however often it's important to wait for the old (blue) version to finish serving
   the requests sent to it.

   Similar strategy applies to the *database*. Often data is the most valuable asset of the bussines, therefore
   DB also should be replicated on at least 2 servers. Dependant on the amount of the write ingress traffic - 
   perhaps also sharded.

   Load Balancer here would ensure not only high throughput, but also seamles application updates.

2. The most likely bottleneck is the time spent in the DB, therefore database replicas may serve not only for data
   protection but also to spread the read requests. For write requests sharding is necessary.

   It's unlikely that the modern website would survive just with one application server, therefore it's important
   to keep in mind modular designs when developing apps, so that the apps may be easily spread accross multiple 
   servers and share the load.

3. Most bottlenecks arise from the bad decission in the code, therefore code revisions, profiling and similar well 
   know good practices is a must. Just as important is to always keep in mind, that the app one day will grow too
   big to fit on just one server, therfore it's better if the app is modular from the very begining, as breaking
   the monoliths may prove very difficult.

## Additional questions

Here are a few possible scenarios where the system requirements change or the new functionality is required:

1. The batch updates have started to become very large, but the
   requirements for their processing time are strict.

2. Code updates need to be pushed out frequently. This needs to be
   done without the risk of stopping a data update already being
   processed, nor a data response being lost.

3. For development and staging purposes, you need to start up a number
   of scaled-down versions of the system.

Please address *at least* one of the situations. Please describe:

- Which parts of the system are the bottlenecks or problems that might make it incompatible with the new requirements?
- How would you restructure and scale the system to address those?

### More Answers

1.

2.

3.
