from fastapi import APIRouter, HTTPException, Request
from database import get_db
from auth.password_utils import verify_password
from auth.jwt_utils import create_token

# 🔹 Import behavior layer
from behavior.metadata_collector import collect_login_metadata
from behavior.behaviorhistory_logger import log_successful_login
from behavior.userbaseline_builder import build_user_baseline

router = APIRouter()


@router.post("/api/login")
def login(data: dict, request: Request):
    db = get_db()

    user = db.execute(
        "SELECT id, username, password_hash, role FROM users WHERE email=?",
        (data["email"],)
    ).fetchone()

    # ❌ Invalid user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ❌ Wrong password
    if not verify_password(data["password"], user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ===============================
    # ✅ SUCCESSFUL LOGIN STARTS HERE
    # ===============================

    # 1️⃣ Generate JWT (identity only)Create JWT after successful verification
    token = create_token({
        "sub": user[0],
        "username": user[1],
        "role": user[3]
    })

    # 2️⃣ Collect FULL metadata
    metadata = collect_login_metadata(
        request,
        user_id=user[0],
        username=user[1]
    )

    # 3️⃣ Store login into behavior_logs
    log_id = log_successful_login(metadata)

    # 4️⃣ Rebuild baseline from last 30 logins
    build_user_baseline(user[0])

    # ===============================
    # ✅ RETURN TOKEN TO CLIENT
    # ===============================

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Login successful"
    }
