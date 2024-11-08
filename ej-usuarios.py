import requests
import json
import os

def datosUsuario():
    while True:
        n = int(input("Ingrese la cantidad de usuarios que desea obtener (entre 1 y 10): "))
        if 1 <= n <= 10:
            return n
        else:
            print("Error: La cantidad debe estar entre 1 y 10.")

def obtenerUsuarios(n):
    response = requests.get(f'https://jsonplaceholder.typicode.com/users?_limit={n}')
    response.raise_for_status() 
    return response.json()

def filtrarUsuarios(usuarios):
    vocales = ["a","e","i","o","u","A","E","I","O","U"]
    usuarioVocal = []
    usuarioConsonante = []
    
    for usuario in usuarios:
        if usuario['name'][0] in vocales:
            usuarioVocal.append(usuario)
        else:
            usuarioConsonante.append(usuario)
    
    return usuarioVocal, usuarioConsonante

def guadarJson(datos, archivo):
    directorio = "UsersData"
    os.makedirs(directorio, exist_ok=True)
    
    rutaArchivo = os.path.join(directorio, archivo)
    
    with open(rutaArchivo, 'w') as archivo:
        json.dump(datos, archivo, indent=4)
    
    print(f"Datos guardados en el archivo: {rutaArchivo}")

def filtrarUbicacion(usuarios, ubicacion):
    usuariosFiltrados = [
        usuario for usuario in usuarios 
        if ubicacion.lower() in usuario['address']['city'].lower() 
        or ubicacion.lower() in usuario['address']['street'].lower()
    ]
    
    if usuariosFiltrados:
        print(f"Se encontraron {len(usuariosFiltrados)} usuarios que coinciden con la ubicación '{ubicacion}'.")
    else:
        print(f"No se encontraron usuarios con la ubicación '{ubicacion}'.")
    
    return usuariosFiltrados

def main():
    n = datosUsuario()
    usuarios = obtenerUsuarios(n)
    
    if usuarios is not None: 
        usuarioVocal, usuarioConsonante = filtrarUsuarios(usuarios)
        guadarJson(usuarioVocal, "usersVowels.json")
        guadarJson(usuarioConsonante, "usersConsonants.json")
        
        ubicacion = input("Ingrese la ubicación (ciudad o calle) para filtrar los usuarios: ")
        usuarios_filtrados = filtrarUbicacion(usuarios, ubicacion)
        
        if usuarios_filtrados:
            guadarJson(usuarios_filtrados, "filteredUsers.json")

if __name__ == "__main__":
    main()