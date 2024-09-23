
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with source_data as (

    select
        games.name as game_name,
        categories.name as categorie_name,
        release_date,
        'Windows' as plateforms
    from {{ ref('categories') }}
        join {{ ref('link_games_categories') }}
            on categories.id_categorie = link_games_categories.id_categorie
        join {{ ref('games') }}
            on link_games_categories.id_game = games.steam_id
    where games.windows <> 0

    union

    select
        games.name as game_name,
        categories.name as categorie_name,
        release_date,
        'Mac' as plateforms
    from
        {{ ref('categories') }}
            join {{ ref('link_games_categories') }}
                on categories.id_categorie = link_games_categories.id_categorie
            join {{ ref('games') }}
                on link_games_categories.id_game = games.steam_id
    where games.mac <> 0

    union

    select
        games.name as game_name,
        categories.name as categorie_name,
        release_date,
        'Linux' as plateforms
    from
        {{ ref('categories') }}
            join {{ ref('link_games_categories') }}
                on categories.id_categorie = link_games_categories.id_categorie
            join {{ ref('games') }}
                on link_games_categories.id_game = games.steam_id
    where games.linux <> 0
)

select *
from source_data
