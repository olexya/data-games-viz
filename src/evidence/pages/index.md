---
title: "Gaming : étude de marché"
description: "Statistiques des jeux Steam — jeux, catégories et plateformes."
---

Analyse du catalogue **Steam** : volumétrie, prix, catégories et répartition par
plateforme. Utilisez les filtres ci-dessous pour affiner l'analyse.

<Dropdown name=plateforme title="Plateformes">
    <DropdownOption value="(1, 3, 5, 7)" valueLabel="Windows"/>
    <DropdownOption value="(2, 3, 6, 7)" valueLabel="Mac"/>
    <DropdownOption value="(3, 4, 5, 7)" valueLabel="Linux"/>
    <DropdownOption value="(1, 2, 3, 4, 5, 6, 7)" valueLabel="Toutes les plateformes"/>
</Dropdown>
<Dropdown title="Année" data={list_year} name=year value=year>
    <DropdownOption value="%" valueLabel="Toutes les années"/>
</Dropdown>

```sql list_year
    SELECT year(release_game) as year
    FROM data_games_viz.obt_games
    WHERE release_game is not null
    GROUP BY 1
    ORDER BY 1 DESC
```

```sql games_count
    SELECT count() as nb_games FROM data_games_viz.obt_games
```

```sql categories_count
    SELECT count(DISTINCT name_categorie) as nb_categories FROM data_games_viz.obt_categories
```

```sql plateforms_count
    SELECT count(DISTINCT plateforms) as value FROM data_games_viz.obt_plateforms
```

## Vue d'ensemble

<Grid cols=3>
    <BigValue data={games_count} value=nb_games title="Jeux référencés" fmt="#,##0"/>
    <BigValue data={categories_count} value=nb_categories title="Catégories"/>
    <BigValue data={plateforms_count} value=value title="Plateformes"/>
</Grid>

<Tabs>
    <Tab label="Jeux">

```sql games_count_select
    SELECT count() as nb_games
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
```

```sql games
    SELECT steam_id, name_game, notes
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
        AND year(release_game) LIKE '${inputs.year.value}'
    ORDER BY notes DESC
    LIMIT 3
```

```sql games_list
    SELECT
        year(release_game) AS year,
        count(*) as nb_games,
        avg(price) as price
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
        AND release_game is not null
    GROUP BY 1
    ORDER BY year
```

<BigValue data={games_count_select} value=nb_games title="Jeux pour la sélection" fmt="#,##0"/>

<BarChart
    data={games}
    x=name_game
    y=notes
    swapXY=true
    title="Top 3 des jeux les mieux notés"
    colorPalette={["#00B34E"]}
/>

<BarChart
    data={games_list}
    title="Sorties par an et prix moyen"
    x=year
    y=nb_games
    yAxisTitle="Nombre de jeux"
    y2=price
    y2SeriesType=line
    y2AxisTitle="Prix moyen (€)"
    y2Fmt="eur"
    colorPalette={["#00B34E", "#007661"]}
/>

    </Tab>
    <Tab label="Catégories">

```sql categories_count_select
    SELECT count() as nb_categories
    FROM data_games_viz.obt_categories
    WHERE
        case plateforms
            WHEN 'Windows' THEN 1
            WHEN 'Mac' THEN 2
            WHEN 'Linux' THEN 4
        END
        IN ${inputs.plateforme.value}
```

```sql categories
    SELECT name_categorie, sum(value) as value
    FROM data_games_viz.obt_categories
    WHERE
        case plateforms
            WHEN 'Windows' THEN 1
            WHEN 'Mac' THEN 2
            WHEN 'Linux' THEN 4
        END
        IN ${inputs.plateforme.value}
    GROUP BY name_categorie
    ORDER BY value DESC
    LIMIT 3
```

```sql categories_list
    SELECT
        year(release_date) AS year,
        count() as nb_categories
    FROM data_games_viz.obt_categories
    WHERE
        case plateforms
            WHEN 'Windows' THEN 1
            WHEN 'Mac' THEN 2
            WHEN 'Linux' THEN 4
        END
        IN ${inputs.plateforme.value}
        AND release_date is not null
    GROUP BY 1
    ORDER BY year
```

<BigValue data={categories_count_select} value=nb_categories title="Catégories pour la sélection" fmt="#,##0"/>

<BarChart
    data={categories}
    x=name_categorie
    y=value
    swapXY=true
    title="Top 3 des catégories les plus représentées"
    colorPalette={["#00C2FF"]}
/>

<BarChart
    data={categories_list}
    title="Catégories par année"
    x=year
    y=nb_categories
    colorPalette={["#00C2FF", "#00E7DA"]}
/>

    </Tab>
    <Tab label="Plateformes">

```sql plateformes
    SELECT categorie_name, plateforms, count() as value
    FROM data_games_viz.obt_plateforms
    WHERE categorie_name LIKE '%-player%'
        AND year(release_date) LIKE '${inputs.year.value}'
    GROUP BY categorie_name, plateforms
```

Répartition des jeux solo / multijoueur par plateforme.

<SankeyDiagram
    data={plateformes}
    sourceCol=categorie_name
    targetCol=plateforms
    valueCol=value
    colorPalette={["#0053E9", "#CF38C7", "#FF4493", "#FF8165", "#FFC051", "#F9F871"]}
/>

    </Tab>
</Tabs>

## Explorer les jeux

```sql search_games
    SELECT
        name_game AS "Jeu",
        '/' || steam_id::int as link
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
        AND year(release_game) LIKE '${inputs.year.value}'
    ORDER BY name_game
```

Cliquez sur un jeu pour ouvrir sa fiche détaillée.

<DataTable data={search_games} search=true link=link rows=8/>
