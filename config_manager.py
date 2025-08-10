import configparser
import json
import os
import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify

CONFIG_FILE = "config.ini"

# === FUNCTION: Read config file ===
def read_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    config = configparser.ConfigParser()
    config.read(file_path)

    if "Database" not in config:
        raise ValueError("Missing 'Database' section in config file.")

    db_config = {
        "host": config["Database"].get("host"),
        "port": int(config["Database"].get("port", 3306)),
        "user": config["Database"].get("username"),
        "password": config["Database"].get("password"),
        "database": config["Database"].get("database"),
    }

    # Extract other sections to save as JSON
    config_data = {}
    for section in config.sections():
        config_data[section] = dict(config[section])

    return db_config, config_data

# === FUNCTION: Save config data to MySQL ===
def save_to_mysql(db_config, config_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data JSON NOT NULL
            )
        """)
        json_data = json.dumps(config_data)
        cursor.execute("INSERT INTO config_data (data) VALUES (%s)", (json_data,))
        conn.commit()
        conn.close()
        print("Configuration saved to MySQL database.")
    except Error as e:
        print(f"MySQL error: {e}")
        raise

# === FUNCTION: Fetch latest config from MySQL ===
def fetch_from_mysql(db_config):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM config_data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return {}
    except Error as e:
        raise RuntimeError(f"MySQL fetch error: {e}")

# === Read config and initialize DB ===
try:
    db_connection_info, full_config_data = read_config(CONFIG_FILE)
    save_to_mysql(db_connection_info, full_config_data)
except Exception as e:
    print(f"Error during setup: {e}")

# === FLASK API ===
app = Flask(__name__)

@app.route("/config", methods=["GET"])
def get_config():
    try:
        db_connection_info, _ = read_config(CONFIG_FILE)
        data = fetch_from_mysql(db_connection_info)
        return jsonify({"status": "success", "config": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
