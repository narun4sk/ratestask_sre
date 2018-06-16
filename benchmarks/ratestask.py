from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    params = dict(
        date_from='2016-01-1',
        date_to='2016-01-10',
        origin='cnGGz',
        destination='eEtll')

    @task
    def rates_get1(self):
        params = self.params.copy()
        self.client.get("/get", params=params)

    @task
    def rates_get2(self):
        params = self.params.copy()
        params['date_to'] = '2016-01-05'
        self.client.get("/get", params=params)

    @task
    def rates_get3(self):
        params = self.params.copy()
        params['origin'] = 'CNQIN'
        params['destination'] = 'NOKRS'
        self.client.get("/get", params=params)

    @task
    def rates_get4(self):
        params = self.params.copy()
        params['date_to'] = '2016-01-05'
        params['origin'] = 'CNQIN'
        params['destination'] = 'NOKRS'
        self.client.get("/get", params=params)

    @task
    def rates_post(self):
        data = dict(
            date_from='2016-01-1',
            date_to='2016-01-10',
            origin_code='cnGGz',
            destination_code='eEtll',
            price=1234)
        self.client.post("/put", data=data)

class WebsiteUser(HttpLocust):
    host = 'http://127.0.0.1:8888'
    task_set = WebsiteTasks
    min_wait = 30
    max_wait = 300
