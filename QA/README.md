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

1 How would you design the system?
2 What parts of the system do you expect to become the bottlenecks as the load grows?
3 How can those bottlenecks be addressed in the future?

Provide a high-level diagram, along with a few paragraphs describing the choices you've made and what factors do you need to take into consideration.

### Answers

```
                          XXXXXXXXXXXXX
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
       |    +------------+-------------------------|
       |    |            |  CACHING SERVER         |
       |    |            +-------------------------+
       |    |
+------+----v--------------------+        +----------------------------------+
|      GREEN SERVERS             |        |      BLUE SERVERS                |
+--------------------------------+        +----------------------------------+
|SRV_1    |SRV_2       |SRV_N    |        |SRV_1     |SRV_2       |SRV_N     |
|         |            |         |        |          |            |          |
+---------+------------+---------+        +----------+------------+----------+
```

1 answer
2 answer
3 answer


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
