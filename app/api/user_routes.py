from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any
from app.models.models import UserCreate, UserUpdate
from app.services.user_service import UserService
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

# Response Model
class SuccessResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

router = APIRouter(prefix="/users", tags=["users"])

# Dependency to get UserService instance
def get_user_service():
    return UserService.get_instance()

@router.post("/", 
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Bad request - Invalid data or duplicate username/email"},
        422: {"description": "Validation Error"}
    }
)
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.create_user(user_data.dict())
        return SuccessResponse(
            status="success",
            message="User created successfully",
            data=user.dict()
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Username or email already exists",
                "code": "DUPLICATE_VALUE"
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": str(e),
                "code": "INTERNAL_SERVER_ERROR"
            }
        )

@router.get("/{user_id}", 
    response_model=SuccessResponse,
    responses={
        200: {"description": "User found successfully"},
        404: {"description": "User not found"}
    }
)
def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "User not found",
                "code": "USER_NOT_FOUND"
            }
        )
    return SuccessResponse(
        status="success",
        message="User retrieved successfully",
        data=user.dict()
    )

@router.put("/{user_id}", 
    response_model=SuccessResponse,
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Bad request - Invalid data or duplicate username/email"},
        404: {"description": "User not found"},
        422: {"description": "Validation Error"}
    }
)
def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        update_data = user_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "No valid update data provided",
                    "code": "INVALID_UPDATE_DATA"
                }
            )
        
        updated_user = user_service.update_user(user_id, update_data)
        return SuccessResponse(
            status="success",
            message="User updated successfully",
            data=updated_user.dict()
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Username or email already exists",
                "code": "DUPLICATE_VALUE"
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": str(e),
                "code": "INTERNAL_SERVER_ERROR"
            }
        )

@router.delete("/{user_id}", 
    response_model=SuccessResponse,
    responses={
        200: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user_service.delete_user(user_id)
        return SuccessResponse(
            status="success",
            message="User deleted successfully"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": str(e),
                "code": "INTERNAL_SERVER_ERROR"
            }
        )

@router.get("/", 
    response_model=SuccessResponse,
    responses={
        200: {"description": "Users retrieved successfully"},
        400: {"description": "Invalid pagination parameters"}
    }
)
def get_users(
    skip: int = 0,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service)
):
    if skip < 0 or limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Invalid pagination parameters",
                "code": "INVALID_PAGINATION"
            }
        )
    
    try:
        users = user_service.get_users(skip=skip, limit=limit)
        return SuccessResponse(
            status="success",
            message="Users retrieved successfully",
            data={"users": [user.dict() for user in users]}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": str(e),
                "code": "INTERNAL_SERVER_ERROR"
            }
        )
