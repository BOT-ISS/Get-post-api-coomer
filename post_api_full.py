import requests
import json


#full obtiene los archivos en post.son


url_base = "https://coomer.su/api/v1/posts"
cookie = "eyJfcGVybWFuZW50Ijp0cnVlLCJhY2NvdW50X2lkIjo3MjEwODR9.Zfjphw.zkkHYEE7EfT_IRjFqzZOo3F_jo0"
headers = {
    "accept": "application/json",
    "Cookie": cookie
}

offset = 0
posts_per_page = 50
total_posts_to_fetch = 1000  # Cambiar aquí para obtener más o menos publicaciones
all_posts = []

while len(all_posts) < total_posts_to_fetch:
    # Construye la URL con el desplazamiento actual
    url = f"{url_base}?o={offset}"

    # Realiza la solicitud GET con la cookie de sesión
    response = requests.get(url, headers=headers)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Convierte la respuesta JSON en un diccionario de Python
        posts = response.json()

        # Si no hay más publicaciones, sal del bucle
        if not posts:
            break

        # Calcula cuántas publicaciones se pueden agregar sin exceder el límite total
        remaining_posts = total_posts_to_fetch - len(all_posts)
        posts_to_add = min(remaining_posts, len(posts))

        # Agrega las publicaciones actuales al resultado final
        all_posts.extend(posts[:posts_to_add])

        # Aumenta el desplazamiento para obtener el siguiente conjunto de publicaciones
        offset += posts_per_page
    else:
        print("Error al obtener las publicaciones:", response.status_code)
        break

# Guarda las publicaciones en un archivo JSON
with open("posts.json", "w") as file:
    json.dump(all_posts, file, indent=4)

print("Los resultados se han guardado en el archivo 'posts.json'")
