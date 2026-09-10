import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb+srv://subhamrath1611_db_user:xl4PM6eNPotKC3hy@atelier-cluster.lct4bvw.mongodb.net/?retryWrites=true&w=majority&appName=Atelier-cluster")
    db = client["atelier_os"]
    
    email = "subham.rath1611@gmail.com"
    user = await db.users.find_one({"email": email})
    
    if user:
        now = datetime.now(timezone.utc)
        # Update user to verified and set credits to 20
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"email_verified": True, "credit_balance": 20, "updated_at": now}}
        )
        
        # Insert ledger transaction
        prior_grant = await db.credit_transactions.find_one({
            "user_id": user["_id"],
            "type": "grant",
            "source": "system",
        })
        
        if not prior_grant:
            await db.credit_transactions.insert_one({
                "user_id": user["_id"],
                "type": "grant",
                "amount": 20,
                "source": "system",
                "job_id": None,
                "created_at": now,
            })
            print("Granted 20 credits and verified email!")
        else:
            print("Email verified, but grant already existed.")
    else:
        print("User not found.")

if __name__ == "__main__":
    asyncio.run(main())
