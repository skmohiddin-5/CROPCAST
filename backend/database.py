import sqlite3
from pathlib import Path
from datetime import datetime


# Database folder
DATABASE_FOLDER = Path(__file__).parent.parent / "database"

# Create database folder if it does not exist
DATABASE_FOLDER.mkdir(exist_ok=True)

# Database file
DATABASE_PATH = DATABASE_FOLDER / "rainfall.db"


def create_database():
    """
    Creates the rainfall_predictions table
    if it does not already exist.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rainfall_predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            village TEXT NOT NULL,
            state TEXT,
            country TEXT,

            latitude REAL,
            longitude REAL,

            temperature REAL,
            humidity REAL,
            pressure REAL,
            wind_speed REAL,
            precipitation REAL,

            rain_probability REAL,
            prediction TEXT,

            language TEXT,

            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(
    village,
    state,
    country,
    latitude,
    longitude,
    temperature,
    humidity,
    pressure,
    wind_speed,
    precipitation,
    rain_probability,
    prediction,
    language
):
    """
    Saves one rainfall prediction into the database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO rainfall_predictions (
            village,
            state,
            country,
            latitude,
            longitude,
            temperature,
            humidity,
            pressure,
            wind_speed,
            precipitation,
            rain_probability,
            prediction,
            language,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        village,
        state,
        country,
        latitude,
        longitude,
        temperature,
        humidity,
        pressure,
        wind_speed,
        precipitation,
        rain_probability,
        prediction,
        language,
        created_at
    ))

    connection.commit()
    connection.close()


# Create database when this file is run
if __name__ == "__main__":
    create_database()
    print("Database created successfully!")
    print(f"Database location: {DATABASE_PATH}")


def get_prediction_history():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM rainfall_predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    history = [dict(row) for row in rows]

    connection.close()

    return history