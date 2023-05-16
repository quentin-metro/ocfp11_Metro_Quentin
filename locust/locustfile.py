from locust import HttpUser, task, between

CLUB = "Iron Temple"
COMPETITION = "Fall Classic"


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def index(self):
        response = self.client.get("/")

    @task
    def login(self):
        self.client.post("/showSummary", {"email": "admin@irontemple.com"})

    @task(4)
    def book(self):
        response = self.client.get("/book/" + COMPETITION + "/" + CLUB + "")


    @task(6)
    def purchasePlaces(self):
        reponse = self.client.post("/purchasePlaces", {"club": CLUB,
                                                       "competition": COMPETITION,
                                                       "places": 1
                                                       }
                                   )

    @task
    def logout(self):
        response = self.client.get("/logout")
