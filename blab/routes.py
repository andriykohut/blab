from blab import app
from blab import controllers

app.router.add_route('GET', '/', controllers.hello)
