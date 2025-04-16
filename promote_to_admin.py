# promote_to_admin.py
from app.db.database import SessionLocal
from app.models.user import User

def promote_to_admin(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print(f"❌ Usuario con email {email} no encontrado")
        return
    
    user.is_admin = True
    db.commit()
    print(f"✅ Usuario {email} promovido a administrador")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python promote_to_admin.py <email_del_usuario>")
        sys.exit(1)
    
    email = sys.argv[1]
    promote_to_admin(email)