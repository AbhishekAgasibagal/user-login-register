import streamlit as st
import sqlite3
import os

# --- DATABASE LOGIC ---
class Database:
    def __init__(self, db_name="vault.db"):
        # Local storage for the database
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return cursor.fetchone() is not None

# --- STREAMLIT UI ---
def main():
    st.set_page_config(page_title="Elite Vault", page_icon="👤")
    db = Database()

    # Custom CSS to match your Dark/Gold theme
    st.markdown("""
        <style>
        .stApp { background-color: #10141d; color: white; }
        .stButton>button { width: 100%; border-radius: 12px; background-color: #d4af37; color: black; font-weight: bold; border: none; }
        .stTextInput>div>div>input { background-color: #1e2433; color: white; border: 2px solid #d4af37; border-radius: 12px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛡️ Nexus Guard Terminal")
    
    # Sidebar for Navigation
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Identity Management", menu)

    if choice == "Login":
        st.subheader("WAITING FOR IDENTITY 👤")
        
        user = st.text_input("Username", placeholder="Enter Username")
        # Interactive "Watcher" logic for Web
        if user:
            st.info("🧐 The Guard is watching your input...")
            
        password = st.text_input("Password", type="password", placeholder="Enter Password")

        if st.button("INITIALIZE LOGIN"):
            if db.validate_login(user, password):
                st.success(f"Welcome back, {user}. Access Granted. ✅")
                st.balloons()
            else:
                st.error("🚫 Identity Verification Failed.")

    elif choice == "Register":
        st.subheader("IDENTITY REGISTRATION 📝")
        
        new_user = st.text_input("Choose Username")
        new_password = st.text_input("Choose Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("REGISTER IDENTITY"):
            if new_password != confirm_password:
                st.warning("Passwords do not match!")
            elif new_user and new_password:
                if db.register_user(new_user, new_password):
                    st.success("Identity Saved Successfully! You can now login.")
                else:
                    st.error("Identity already exists in the vault.")
            else:
                st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()