import requests
import random

def get_random_anime_character():
    # AniList API URL
    url = "https://graphql.anilist.co"

    # Erweiterte GraphQL Query für zusätzliche Informationen
    query = '''
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        characters {
          name {
            full
          }
          image {
            large
          }
          description
          media {
            nodes {
              title {
                romaji
                english
              }
            }
          }
        }
      }
    }
    '''

    # Variablen für die GraphQL-Abfrage
    variables = {
        'page': random.randint(1, 154705),  # Zufällige Seite auswählen
        'perPage': 1  # Nur einen zufälligen Charakter pro Anfrage
    }

    try:
        # Anfrage an die AniList API senden
        response = requests.post(url, json={'query': query, 'variables': variables})
        
        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            data = response.json()

            # Charakterdaten extrahieren
            character = data['data']['Page']['characters'][0]  # Hier ändern, um den ersten Charakter zu nehmen
            character_name = character['name']['full']
            character_image = character['image']['large']
            
            # Anime-Titel extrahieren (Romaji und Englisch)
            anime_titles = character['media']['nodes'][0]['title']
            anime_title_romaji = anime_titles['romaji']
            anime_title_english = anime_titles.get('english', 'Kein englischer Titel verfügbar')

            return {
                "name": character_name,
                "image": character_image,
                "anime_title_romaji": anime_title_romaji,
                "anime_title_english": anime_title_english,
                "description": character['description'] or 'Keine Beschreibung verfügbar'
            }
        else:
            print(f"Fehler beim Abrufen der Daten: {response.status_code}")
            return None
    except Exception as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        return None
