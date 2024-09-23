
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with source_data as (
    select
        id as id_game,
        value as id_categorie
    from {{ env_var('SCHEMA') }}.games_metadata
    where name like '%categories%id%'
)

select *
from source_data
where id_game is not null
