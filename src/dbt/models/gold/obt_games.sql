{{ config(materialized='table') }}

with source_data as (

    select
        steam_id as steam_id,
        name as name_game,
        DATE_TRUNC('year', release_date) AS release_game,
        recommendations as notes,
        windows * 1 + mac * 2 + linux * 4 as plateforms,
        price
    from
        {{ ref('games') }}
)

select *
from source_data
where steam_id is not null and name_game is not null and release_game is not null
