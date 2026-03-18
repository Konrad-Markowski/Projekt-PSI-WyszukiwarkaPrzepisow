# Projekt PSI – Wyszukiwarka Przepisów

### Opis projektu

**Wyszukiwarka Przepisów** to serwerowa aplikacja napisana w **FastAPI**, która udostępnia REST API do:
- **rejestracji i logowania użytkowników** (JWT),
- **dodawania, edytowania i usuwania własnych przepisów**,
- **wyszukiwania przepisów** po:
  - nazwie dania,
  - kategorii (np. `Main`, `Dessert`),
  - kuchni / obszarze pochodzenia (np. `Italian`, `Polish`),
  - składniku (np. `chicken`, `cheese`),
- **przechowywania ulubionych przepisów** użytkownika,
- **losowych rekomendacji posiłków**.

Dane trzymane są w bazie **PostgreSQL** (tabele `users` oraz `meals`) z użyciem **SQLAlchemy** i biblioteki **databases** (tryb asynchroniczny).

---

### Stos technologiczny

- **Python 3.12**
- **FastAPI** – warstwa HTTP / REST
- **Uvicorn** – ASGI server
- **PostgreSQL 17**
- **SQLAlchemy 2** + **databases[asyncpg]**
- **Pydantic 2** i **pydantic-settings**
- **dependency-injector** – wstrzykiwanie zależności
- **python-jose** – JWT
- Docker + docker-compose

Struktura katalogów backendu:
- `fastApiProjectPSI/src/main.py` – punkt wejścia FastAPI
- `fastApiProjectPSI/src/api/routers/meal.py` – endpointy dotyczące posiłków
- `fastApiProjectPSI/src/api/routers/user.py` – endpointy użytkownika i ulubionych
- `fastApiProjectPSI/src/core/domain/` – modele domenowe (`User`, `Meal`, itp.)
- `fastApiProjectPSI/src/core/repositories/` – interfejsy repozytoriów
- `fastApiProjectPSI/src/infrastructure/repositories/` – implementacje repozytoriów (dostęp do DB)
- `fastApiProjectPSI/src/infrastructure/services/` – logika biznesowa
- `fastApiProjectPSI/src/infrastructure/dto/` – obiekty DTO zwracane przez API
- `fastApiProjectPSI/src/infrastructure/utils/` – narzędzia (hasła, tokeny, stałe)
- `fastApiProjectPSI/src/db.py` – konfiguracja bazy danych i definicje tabel
- `fastApiProjectPSI/src/config.py` – konfiguracja aplikacji z env
- `fastApiProjectPSI/src/dane_startowe.sql` – przykładowe dane startowe

---

### Uruchomienie z Docker / docker-compose (zalecane)

Wymagania:
- zainstalowany **Docker** i **docker-compose**.

1. Przejdź do katalogu projektu backendu:
   ```bash
   cd fastApiProjectPSI
   ```
2. Zbuduj i uruchom kontenery:
   ```bash
   docker-compose up --build
   ```
3. Aplikacja będzie dostępna pod adresem:
   - API: `http://localhost:8000`
   - dokumentacja OpenAPI / Swagger: `http://localhost:8000/docs`

Domyślne dane połączenia do bazy (ustawione w `docker-compose.yml` oraz `config.py`):
- `DB_HOST=db`
- `DB_NAME=app`
- `DB_USER=postgres`
- `DB_PASSWORD=pass`

#### Wgranie danych startowych

Po pierwszym uruchomieniu możesz wgrać przykładowe dane z pliku `src/dane_startowe.sql`:

1. Wejdź do kontenera bazy:
   ```bash
   docker exec -it db psql -U postgres
   ```
2. Połącz się z bazą `app`:
   ```sql
   \c app;
   ```
3. Skopiuj i wykonaj polecenia INSERT z pliku `fastApiProjectPSI/src/dane_startowe.sql`
   (pliku nie można wprost uruchomić, ponieważ zawiera też komendę `docker exec`).

---

### Uruchomienie lokalne (bez Dockera)

Wymagania:
- Python 3.12,
- działający serwer PostgreSQL,
- skonfigurowane zmienne środowiskowe.

1. Zainstaluj zależności:
   ```bash
   cd fastApiProjectPSI
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

2. Ustaw zmienne środowiskowe (przykład dla Linux/macOS):
   ```bash
   export DB_HOST=localhost
   export DB_NAME=app
   export DB_USER=postgres
   export DB_PASSWORD=pass
   ```

3. Uruchom serwer:
   ```bash
   uvicorn src.main:app --reload
   ```

4. Wejdź na:
   - `http://127.0.0.1:8000/docs` – Swagger UI

---

### Model danych (wysoki poziom)

- **users**
  - `id` – UUID (klucz główny, generowany w Postgresie przez `gen_random_uuid()`)
  - `email` – unikalny e‑mail
  - `password` – hasło użytkownika (w produkcji powinno być hashowane)
  - `favourites` – tablica stringów z ID ulubionych posiłków

- **meals**
  - `id` – int (klucz główny)
  - `strMeal` – nazwa dania
  - `strInstructions` – opis przygotowania
  - `ingredients` – tablica stringów (składniki)
  - `measures` – tablica stringów (miary składników)
  - `strCategory` – nazwa kategorii (np. Main, Dessert)
  - `strArea` – kuchnia / kraj (np. Italian, Polish)
  - `strMealThumb` – URL miniaturki
  - `strTags` – tagi tekstowe
  - `strYoutube` – link do filmu na YouTube
  - `user_id` – UUID użytkownika, który dodał przepis (FK do `users.id`)

---

### Autoryzacja i JWT

System autoryzacji oparty jest o **tokeny JWT**:
- rejestracja użytkownika tworzy rekord w `users`,
- logowanie (`/user/token`) zwraca obiekt `TokenDTO`:
  - `access_token` – token JWT,
  - `token_type` – zawsze `"Bearer"`.
- token należy przekazywać w nagłówku:
  ```http
  Authorization: Bearer <ACCESS_TOKEN>
  ```

Token jest generowany w `src/infrastructure/utils/token.py`:
- algorytm: `HS256`,
- sekret: `SECRET_KEY` z `src/infrastructure/utils/consts.py`,
- domyślny czas życia: `EXPIRATION_MINUTES = 60`.

Endpointy, które wymagają autoryzacji (nagłówek Bearer):
- tworzenie, edycja i usuwanie posiłków (`POST /meal/create`, `PUT /meal/{id}`, `DELETE /meal/{id}`),
- zarządzanie ulubionymi (`POST /user/favourites/{uuid}/add`, `DELETE /user/favourites/{uuid}/remove`).

---

### Przykładowe endpointy API

#### Użytkownicy (`/user`)

- **POST `/user/register`**
  - Rejestracja nowego użytkownika.
  - Body (JSON):
    ```json
    {
      "email": "user@example.com",
      "password": "haslo123"
    }
    ```

- **POST `/user/token`**
  - Logowanie i zwrócenie tokenu JWT.

- **GET `/user/{uuid}`**
  - Dane użytkownika po UUID.

- **GET `/user/user/email/{email}`**
  - Wyszukanie użytkownika po e‑mailu.

- **POST `/user/user/favourites/{uuid}/add?meal_id={id}`**
  - Dodanie posiłku do ulubionych użytkownika (wymaga Bearer tokenu).

- **DELETE `/user/user/favourites/{uuid}/remove?meal_id={id}`**
  - Usunięcie posiłku z ulubionych użytkownika (wymaga Bearer tokenu).

- **GET `/user/user/favourites/{uuid}`**
  - Lista ulubionych posiłków użytkownika.

- **GET `/user/users`**
  - Lista wszystkich użytkowników.

> Uwaga: ścieżki zawierają dodatkowe segmenty `user/...` ponieważ w routerze użyto prefiksu `app.include_router(user_router, prefix="/user")` oraz własnych ścieżek w dekoratorach.

#### Posiłki (`/meal`)

Router `meal` jest podpięty z prefiksem `/meal`, więc:

- **POST `/meal/create`**
  - Dodanie nowego posiłku (wymaga Bearer tokenu).
  - Body (JSON):
    ```json
    {
      "strMeal": "Spaghetti Carbonara",
      "strInstructions": "Opis przygotowania...",
      "ingredients": ["spaghetti", "pancetta"],
      "measures": ["200g", "100g"],
      "strCategory": "Main",
      "strArea": "Italian",
      "strMealThumb": "https://example.com/spaghetti.jpg",
      "strTags": "pasta,Italian",
      "strYoutube": "https://www.youtube.com/..."
    }
    ```

- **GET `/meal/all`**
  - Lista wszystkich posiłków.

- **GET `/meal/category/{category}`**
  - Posiłki z wybranej kategorii (case‑insensitive).

- **GET `/meal/area/{area}`**
  - Posiłki z wybranego obszaru / kuchni.

- **GET `/meal/name/{name}`**
  - Wyszukiwanie posiłków po fragmencie nazwy (`ILIKE %name%`).

- **GET `/meal/user/{user_id}`**
  - Posiłki dodane przez wskazanego użytkownika (UUID).

- **GET `/meal/meals/recommendations?n=3`**
  - Losowe rekomendacje `n` posiłków (domyślnie 3).

- **GET `/meal/{meal_id}`**
  - Szczegóły pojedynczego posiłku po ID.

- **GET `/meal/ingredient/{ingredient_name}`**
  - Posiłki zawierające podany składnik (sprawdzane w tablicy `ingredients`).

- **PUT `/meal/{meal_id}`**
  - Aktualizacja posiłku (wymaga Bearer tokenu; tylko właściciel przepisu może modyfikować).

- **DELETE `/meal/{meal_id}`**
  - Usunięcie posiłku (wymaga Bearer tokenu; tylko właściciel przepisu).

---

### Testowanie API

W katalogu `fastApiProjectPSI` znajduje się plik `test_main.http`, którego można użyć w IDE (np. VS Code, IntelliJ / PyCharm) do ręcznego wywoływania endpointów HTTP.

Najwygodniejszym sposobem eksploracji API jest jednak wejście na:
- `http://localhost:8000/docs` (Swagger UI),
- lub `http://localhost:8000/redoc` (jeśli dostępne).

---

### Rozszerzenia i możliwe kierunki rozwoju

- dodanie frontendu (np. React / Vue) korzystającego z istniejącego API,
- poprawa bezpieczeństwa (hashowanie haseł, rotacja klucza JWT, konfiguracja przez zmienne środowiskowe zamiast stałych),
- paginacja i sortowanie wyników wyszukiwania,
- filtrowanie po wielu kryteriach naraz (np. kategoria + składnik + czas przygotowania),
- system ocen / komentarzy do przepisów.