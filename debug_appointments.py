# backend/debug_appointments.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

print("=== DEBUG APPOINTMENTS IMPORT ===")

try:
    print("1. Intentando importar appointments...")
    from app.routes.appointments import router
    print("✅ SUCCESS: Router imported")
    print(f"   Router: {router}")
    print(f"   Prefix: {router.prefix}")
    print(f"   Tags: {router.tags}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    print("=== FULL TRACEBACK ===")
    traceback.print_exc()
    print("======================")

print("=== DEBUG COMPLETADO ===")