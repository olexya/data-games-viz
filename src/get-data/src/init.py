from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, Float
import dotenv
import os

dotenv.load_dotenv()

def create(engine):
    metadata = MetaData()

    Table(
        "games_info", metadata,
        Column("success", Boolean),
        Column("type", String),
        Column("name", String),
        Column("steam_appid", Integer, primary_key=True),
        Column("fullgame_appid", String),
        Column("demos", String),
        Column("fullgame_name", String),
        Column("required_age", Integer),
        Column("is_free", Boolean),
        Column("controller_support", String),
        Column("detailed_description", String),
        Column("metacritic_score", String),
        Column("metacritic_url", String),
        Column("about_the_game", String),
        Column("short_description", String),
        Column("supported_languages", String),
        Column("header_image", String),
        Column("capsule_image", String),
        Column("capsule_imagev5", String),
        Column("website", String),
        Column("pc_requirements_minimum", String),
        Column("pc_requirements_recommended", String),
        Column("mac_requirements_minimum", String),
        Column("mac_requirements_recommended", String),
        Column("linux_requirements_minimum", String),
        Column("linux_requirements_recommended", String),
        Column("legal_notice", String),
        Column("drm_notice", String),
        Column("developers", String),
        Column("publishers", String),
        Column("price_overview_currency", String),
        Column("price_overview_initial", String),
        Column("price_overview_final", Float),
        Column("price_overview_discount_percent", String),
        Column("price_overview_initial_formatted", String),
        Column("price_overview_final_formatted", String),
        Column("packages", String),
        Column("package_groups", String),
        Column("dlc", String),
        Column("platforms_windows", Boolean),
        Column("platforms_mac", Boolean),
        Column("platforms_linux", Boolean),
        Column("categories", String),
        Column("genres", String),
        Column("screenshots", String),
        Column("movies", String),
        Column("recommendations_total", Integer),
        Column("achievements_total", String),
        Column("achievements_highlighted", String),
        Column("release_date_coming_soon", Boolean),
        Column("release_date_date", String),
        Column("support_info_url", String),
        Column("support_info_email", String),
        Column("background", String),
        Column("background_raw", String),
        Column("reviews", String),
        Column("content_descriptors_ids", String),
        Column("content_descriptors_notes", String),
        Column("ratings", String),
        Column("ext_user_account_notice", String),
        schema=os.getenv("SCHEMA")
    )

    Table(
        "games_metadata", metadata,
        Column("id", Integer),
        Column("name", String),
        Column("value", String),
        schema=os.getenv("SCHEMA")
    )

    metadata.create_all(engine)
