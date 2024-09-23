{{ config(materialized='table') }}

with source_data as (
    select
        id_categorie as id,
        name as name_categorie,
        create_date as release_date,
        nb_games,
        windows as value,
        'Windows' as plateforms
    from
        {{ ref('categories') }}
    where windows <> 0

    union

    select
        id_categorie as id,
        name as name_categorie,
        create_date as release_date,
        nb_games,
        mac as value,
        'Mac' as plateforms
    from
        {{ ref('categories') }}
    where mac <> 0

    union

    select
        id_categorie as id,
        name as name_categorie,
        create_date as release_date,
        nb_games,
        linux as value,
        'Linux' as plateforms
    from
        {{ ref('categories') }}
    where linux <> 0
)

select *
from source_data
where id is not null and name_categorie is not null and release_date is not null
