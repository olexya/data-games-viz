{% macro format_date(date, month_mapping) %}

CASE
    WHEN release_date_date ~ '^\d{1,2} [a-zA-Zéа-я]{3,} \d{4}'
    THEN TO_DATE(
        COALESCE((SELECT mapping->>(SUBSTRING(release_date_date FROM '\s(\w+)\s')) FROM month_mapping), SUBSTRING(release_date_date FROM '\s(\w+)\s')) || 
        SUBSTRING(release_date_date FROM '(\d{1,2})') || 
        SUBSTRING(release_date_date FROM '(\d{4})$'),
        'MMDDYYYY'
    )

    WHEN release_date_date ~ '^[a-zA-Z]{3} \d{1,2}, \d{4}'
    THEN TO_DATE(
        COALESCE((SELECT mapping->>(SUBSTRING(release_date_date FROM '^(\w+)')) FROM month_mapping), SUBSTRING(release_date_date FROM '^(\w+)')) || 
        SUBSTRING(release_date_date FROM '\s(\d{1,2}),') || 
        SUBSTRING(release_date_date FROM '(\d{4})$'),
        'MMDDYYYY'
    )

    WHEN release_date_date ~ '^Q[1-4] \d{4}'
    THEN (SUBSTRING(release_date_date FROM '(\d{4})$')::INT || '-' || 
            (SUBSTRING(release_date_date FROM 'Q(\d)')::INT * 3)::TEXT || '-01')::DATE

    WHEN release_date_date ~ '^[a-zA-Z]+ \d{4}'
    THEN TO_DATE(
        COALESCE((SELECT mapping->>(SUBSTRING(release_date_date FROM '^(\w+)')) FROM month_mapping), SUBSTRING(release_date_date FROM '^(\w+)')) || '01' || 
        SUBSTRING(release_date_date FROM '(\d{4})$'),
        'MMDDYYYY'
    )

    WHEN release_date_date ~ '^\d{4}$'
    THEN (release_date_date || '-01-01')::DATE

    WHEN release_date_date ~ '^\d{4}年\d{1,2}月\d{1,2}日$'
    THEN TO_DATE(
        SUBSTRING(release_date_date FROM '(\d{4})年') || '-' ||
        SUBSTRING(release_date_date FROM '年(\d{1,2})月') || '-' ||
        SUBSTRING(release_date_date FROM '月(\d{1,2})日'),
        'YYYY-MM-DD'
    )

    ELSE '2025-01-01'::DATE
END AS release_date
{% endmacro %}
