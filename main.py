from fastapi import FastAPI, HTTPException

from models import User

app = FastAPI()

VALID_CREDENTIALS = {
    "email": "pierre@palenca.com",
    "password": "MyPwdChingon123",
    "access_token": "cTV0aWFuQ2NqaURGRE82UmZXNVBpdTRxakx3V1F5",
}

PROFILE = {
    "country": "mx",
    "city_name": "Ciudad de México",
    "worker_id": "34dc0c89b16fd170eba320ab186d08ed",
    "first_name": "Pierre",
    "last_name": "Delarroqua",
    "email": "pierre@palenca.com",
    "phone_prefix": "+52",
    "phone_number": "5576955981",
    "rating": "4.8",
    "lifetime_trips": 1254,
}


@app.get("/")
async def root():
    return {"message": "Hello Palenca"}


@app.post("/uber/login")
async def login(user: User):
    if (
        user.email == VALID_CREDENTIALS["email"]
        and user.password == VALID_CREDENTIALS["password"]
    ):
        return {"message": "SUCCESS", "access_token": VALID_CREDENTIALS["access_token"]}

    raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/uber/profile/{access_token}")
async def get_profile(access_token):
    if access_token == VALID_CREDENTIALS["access_token"]:
        return {"message": "SUCCESS", "platform": "uber", "profile": PROFILE}
    raise HTTPException(
        status_code=401,
        detail={"message": "CREDENTIALS_INVALID", "details": "Incorrect token"},
    )
