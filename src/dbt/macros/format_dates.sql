{% macro format_date(date, month_mapping) %}

-- Les dates de sortie Steam arrivent dans des dizaines de formats/locales
-- ("21 Aug 2012", "Oct 2014", "Q1 2015", "2014年5月", "Oca 2016"…). Tenter de
-- parser le mois de façon exhaustive est fragile (cf. erreur « invalid value "Oc"
-- for "MM" »). Le rapport n'agrège que par ANNÉE : on extrait donc l'année de
-- façon robuste (jamais d'erreur) et on la ramène au 1er janvier. Les valeurs
-- sans année identifiable deviennent NULL.
CASE
    WHEN release_date_date ~ '\d{4}'
    THEN (SUBSTRING(release_date_date FROM '(\d{4})') || '-01-01')::DATE
    ELSE NULL
END AS release_date
{% endmacro %}
