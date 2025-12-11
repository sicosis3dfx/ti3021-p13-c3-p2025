import bcrypt 

# Paso 1. Obtener contraseña en plano
incoming_password = input("Ingrese su contraseña: ").encode("UTF-8")
# Paso 2. Crear un pedazo de sal
salt = bcrypt.gensalt(rounds=12)
# Paso 3. Hashear la contraseña en plano y dar una sal al hasheo
hashed_password = bcrypt.hashpw(password=incoming_password, salt=salt)
print("Contraña hasheada", hashed_password)
# Paso 4. Ingresar de nuevo la contraseña
confirm_password = input("Ingrese nuevamente la contraseña: ").encode("UTF-8")
if bcrypt.checkpw(confirm_password, hashed_password):
    print("Contraseña correcta")
else:
    print("Contraseña Incorrecta")