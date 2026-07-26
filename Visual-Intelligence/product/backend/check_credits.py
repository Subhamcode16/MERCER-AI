import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb+srv://subhamrath1611_db_user:xl4PM6eNPotKC3hy@atelier-cluster.lct4bvw.mongodb.net/?retryWrites=true&w=majority&appName=Atelier-cluster")
    db = client["atelier_os"]
    
    users = await db.users.find({}).to_list(length=10)
    for u in users:
        print(f"User: {u.get('email')}, tier: {u.get('tier')}, credits: {u.get('credit_balance')}, verified: {u.get('email_verified')}")
        
    grants = await db.credit_transactions.find({"source": "system"}).to_list(length=10)
    print("\nGrants:")
    for g in grants:
        print(g)

if __name__ == "__main__":
    asyncio.run(main())
