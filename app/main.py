
from fastapi import FastAPI
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

from app.database.database import Base, engine
from app.api.whatsapp import router as whatsapp_router

app = FastAPI()
#Create table in the databse
Base.metadata.create_all(bind=engine)


app.include_router(whatsapp_router)







       













