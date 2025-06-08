from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.user_schemas import UserCreate, UserLogin, UserOut, Token
from src.services.user_service import login_user, register_user

router = APIRouter(tags=["auth"])


@router.post(
    "/registration", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def route_registration(user_reg: UserCreate):
    new_user = await register_user(user_reg.login, user_reg.password)
    print(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def route_login_swagger(login_form: OAuth2PasswordRequestForm = Depends()):
    user_data = await login_user(login_form.username, login_form.password)
    return user_data


@router.post("/login_by_body", response_model=Token)
async def route_login(user_login_data: UserLogin):
    user_data = await login_user(user_login_data.login, user_login_data.password)
    return user_data
