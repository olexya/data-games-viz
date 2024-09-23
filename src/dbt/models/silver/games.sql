{{ config(materialized='table') }}

with month_mapping as (
    select jsonb_build_object(
        'giu', 6, 'déc', 12, 'фев', 2, 'мая', 5, 'maj', 8, 'dic', 12,
        'Kas', 11, 'févr', 2, 'maja', 5, 'Oca', 1, 'апр', 4, 'июл', 7,
        'stycznia', 1, 'Jun', 6, 'Ap', 4
    ) as mapping
),

source_data as (

    select
        steam_appid as steam_id,
        name as name,
        {{ format_date(release_date_date, month_mapping) }},
        recommendations_total as recommendations,
        platforms_windows::int as windows,
        platforms_mac::int as mac,
        platforms_linux::int as linux,
        price_overview_final as price,
        about_the_game as about
    from
        {{ env_var('SCHEMA') }}.games_info
)

select *
from source_data
where steam_id is not null and price is not null
