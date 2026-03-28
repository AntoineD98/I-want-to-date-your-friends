from fastapi import FastAPI

from api.routes.network_routes import router as network_router
from api.routes.user_interaction_routes import router as interaction_router
from api.routes.user_update_routes import router as user_router


app = FastAPI()

app.include_router(network_router)
app.include_router(interaction_router)
app.include_router(user_router)

