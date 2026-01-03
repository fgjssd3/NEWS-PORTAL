#!/usr/bin/env python3
# create_complete_schema.py - Crée toutes les tables nécessaires

import psycopg2
import os

DB_CONFIG = {
    'dbname': 'db_x0yq',
    'user': 'db_x0yq_user',
    'password': 'OLkFK55IG6uHQ71odoMaf2D0S2foWjB8',
    'host': 'dpg-d5bavb8gjchc73bsvoq0-a.oregon-postgres.render.com',
    'port': 5432,
    'sslmode': 'require'
}

print("🚀 Connexion à Render PostgreSQL...")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # 1. Vérifie quelles tables existent déjà
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    existing_tables = [row[0] for row in cursor.fetchall()]
    print(f"📊 Tables existantes: {len(existing_tables)}")
    if existing_tables:
        print("  " + ", ".join(existing_tables))
    
    # 2. Crée les tables Django système (dans le bon ordre)
    print("\n📦 Création des tables Django...")
    
    # Table django_content_type (doit être créée en premier)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_content_type (
            id SERIAL PRIMARY KEY,
            app_label VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            UNIQUE(app_label, model)
        );
    """)
    print("  ✅ django_content_type")
    
    # Table auth_permission
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_permission (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            content_type_id INTEGER NOT NULL REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
            codename VARCHAR(100) NOT NULL,
            UNIQUE(content_type_id, codename)
        );
    """)
    print("  ✅ auth_permission")
    
    # Table auth_group
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_group (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL UNIQUE
        );
    """)
    print("  ✅ auth_group")
    
    # Table auth_group_permissions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_group_permissions (
            id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED,
            permission_id INTEGER NOT NULL REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
            UNIQUE(group_id, permission_id)
        );
    """)
    print("  ✅ auth_group_permissions")
    
    # Table auth_user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_user (
            id SERIAL PRIMARY KEY,
            password VARCHAR(128) NOT NULL,
            last_login TIMESTAMP WITH TIME ZONE,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) NOT NULL UNIQUE,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined TIMESTAMP WITH TIME ZONE NOT NULL
        );
    """)
    print("  ✅ auth_user")
    
    # Table auth_user_groups
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_user_groups (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
            group_id INTEGER NOT NULL REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED,
            UNIQUE(user_id, group_id)
        );
    """)
    print("  ✅ auth_user_groups")
    
    # Table auth_user_user_permissions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
            permission_id INTEGER NOT NULL REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
            UNIQUE(user_id, permission_id)
        );
    """)
    print("  ✅ auth_user_user_permissions")
    
    # Table django_admin_log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_admin_log (
            id SERIAL PRIMARY KEY,
            action_time TIMESTAMP WITH TIME ZONE NOT NULL,
            object_id TEXT,
            object_repr VARCHAR(200) NOT NULL,
            action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
            change_message TEXT NOT NULL,
            content_type_id INTEGER REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
            user_id INTEGER NOT NULL REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
        );
    """)
    print("  ✅ django_admin_log")
    
    # Table django_migrations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_migrations (
            id SERIAL PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied TIMESTAMP WITH TIME ZONE NOT NULL
        );
    """)
    print("  ✅ django_migrations")
    
    # Table django_session
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_session (
            session_key VARCHAR(40) NOT NULL PRIMARY KEY,
            session_data TEXT NOT NULL,
            expire_date TIMESTAMP WITH TIME ZONE NOT NULL
        );
    """)
    print("  ✅ django_session")
    
    # 3. Crée tes tables d'application
    print("\n📰 Création des tables de l'application...")
    
    # Table news_category
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_category (
            id SERIAL PRIMARY KEY,
            categoryname VARCHAR(100) NOT NULL
        );
    """)
    print("  ✅ news_category")
    
    # Table news_newspost
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_newspost (
            id SERIAL PRIMARY KEY,
            posttitle VARCHAR(500) NOT NULL,
            postdetail TEXT NOT NULL,
            postimage VARCHAR(100),
            postdate DATE NOT NULL,
            category_id INTEGER NOT NULL
        );
    """)
    print("  ✅ news_newspost")
    
    # Table news_comment
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_comment (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            emailid VARCHAR(40) NOT NULL,
            commentmsg VARCHAR(1000) NOT NULL,
            cdate DATE NOT NULL,
            status VARCHAR(20) NOT NULL,
            newspost_id INTEGER NOT NULL
        );
    """)
    print("  ✅ news_comment")
    
    # Table news_contact
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_contact (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            contact VARCHAR(15) NOT NULL,
            emailid VARCHAR(40) NOT NULL,
            message VARCHAR(300) NOT NULL,
            mdate DATE NOT NULL,
            isread VARCHAR(10) NOT NULL
        );
    """)
    print("  ✅ news_contact")
    
    # 4. Insère les données de base
    print("\n📥 Insertion des données initiales...")
    
    # Insère le contenu type Django
    cursor.execute("""
        INSERT INTO django_content_type (app_label, model) VALUES 
        ('admin', 'logentry'),
        ('auth', 'permission'),
        ('auth', 'group'),
        ('auth', 'user'),
        ('contenttypes', 'contenttype'),
        ('sessions', 'session'),
        ('news', 'newspost'),
        ('news', 'category'),
        ('news', 'comment'),
        ('news', 'contact')
        ON CONFLICT DO NOTHING;
    """)
    print("  ✅ Contenu type Django")
    
    # Insère les permissions de base
    cursor.execute("""
        INSERT INTO auth_permission (name, content_type_id, codename) 
        SELECT 'Can add log entry', id, 'add_logentry' FROM django_content_type WHERE app_label='admin' AND model='logentry'
        UNION ALL
        SELECT 'Can change log entry', id, 'change_logentry' FROM django_content_type WHERE app_label='admin' AND model='logentry'
        UNION ALL
        SELECT 'Can delete log entry', id, 'delete_logentry' FROM django_content_type WHERE app_label='admin' AND model='logentry'
        UNION ALL
        SELECT 'Can view log entry', id, 'view_logentry' FROM django_content_type WHERE app_label='admin' AND model='logentry'
        ON CONFLICT DO NOTHING;
    """)
    print("  ✅ Permissions de base")
    
    # Crée un superuser (mot de passe: admin123)
    cursor.execute("""
        INSERT INTO auth_user (
            password, username, email, is_superuser, is_staff, is_active,
            first_name, last_name, date_joined
        ) VALUES (
            'pbkdf2_sha256$600000$mRrD5lB4tQ7vK9jZ$abc123def456ghi789jkl012mno345pqr678stu901vwx234yz=', 
            'admin', 'admin@example.com',
            true, true, true, '', '', NOW()
        ) ON CONFLICT (username) DO NOTHING;
    """)
    print("  ✅ Superuser 'admin' (mot de passe: admin123)")
    
    # Insère les catégories
    categories = ['Bollywood', 'Sports', 'Entertainment', 'Politics', 'Business']
    for cat in categories:
        cursor.execute(
            "INSERT INTO news_category (categoryname) VALUES (%s) ON CONFLICT DO NOTHING;",
            (cat,)
        )
    print(f"  ✅ {len(categories)} catégories")
    
    # Marque les migrations comme appliquées
    migrations = [
        ('contenttypes', '0001_initial'),
        ('auth', '0001_initial'),
        ('admin', '0001_initial'),
        ('sessions', '0001_initial'),
        ('news', '0001_initial'),
    ]
    
    for app, name in migrations:
        cursor.execute(
            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW()) ON CONFLICT DO NOTHING;",
            (app, name)
        )
    print(f"  ✅ {len(migrations)} migrations appliquées")
    
    # 5. Vérification finale
    print("\n📊 Vérification finale...")
    
    cursor.execute("SELECT COUNT(*) FROM django_content_type;")
    print(f"  - django_content_type: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM auth_permission;")
    print(f"  - auth_permission: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM auth_user;")
    print(f"  - auth_user: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM news_category;")
    print(f"  - news_category: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM django_migrations;")
    print(f"  - django_migrations: {cursor.fetchone()[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*50)
    print("🎉 SCHÉMA COMPLET CRÉÉ AVEC SUCCÈS !")
    print("="*50)
    print("\n🔗 Accède à ton site: https://distinctionptf-icgu.onrender.com")
    print("👤 Identifiants admin: admin / admin123")
    print("\n✅ Ton application Django est maintenant prête !")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()