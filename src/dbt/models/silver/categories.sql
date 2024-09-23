{{ config(materialized='table') }}

with source_data as (
    select
        categories.id_categorie,
        ANY_VALUE(categories.name) as name,
        DATE_TRUNC('year', min(release_date)) as create_date,
        count(*) as nb_games,
        sum(platforms_windows::int) as windows,
        sum(platforms_mac::int) as mac,
        sum(platforms_linux::int) as linux
    from (
        select
            id_categorie,
            ANY_VALUE(description) as name
        from (
            select
                id || '-' || SUBSTRING(name, 12, POSITION('_' in SUBSTRING(name, 12)) - 1) as index,
                value as id_categorie
            from {{ env_var('SCHEMA') }}.games_metadata
            where name like '%categories%id%'
        ) as categorie_id
        join (
            select
                id || '-' || SUBSTRING(name, 12, POSITION('_' in SUBSTRING(name, 12)) - 1) as index,
                value as description
            from {{ env_var('SCHEMA') }}.games_metadata
            where name like '%categories%description%'
        ) as categorie_name
        on categorie_id.index=categorie_name.index
        group by id_categorie
    ) as categories
        join {{ ref('link_games_categories') }}
            on categories.id_categorie = link_games_categories.id_categorie
        join {{ ref('games') }}
            on link_games_categories.id_game = games.steam_id
        join {{ env_var('SCHEMA') }}.games_info
            on link_games_categories.id_game = games_info.steam_appid
    group by categories.id_categorie
)

select *
from source_data
where id_categorie is not null
