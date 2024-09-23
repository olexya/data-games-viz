---
title: "Gaming : Etude de marché"
---

```sql games_count
    SELECT
        count() as nb_games
    FROM data_games_viz.obt_games
    GROUP BY ALL
```

```sql games_count_select
    SELECT
        count() as nb_games
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
    GROUP BY ALL
```

```sql games
    SELECT
        steam_id,
        name_game,
        notes
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
        AND year(release_game) LIKE '${inputs.year.value}'
    ORDER BY notes DESC
    LIMIT 3
```

```sql games_list
    SELECT
        release_game AS year,
        count(*) as nb_games,
        avg(price) as price
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
    GROUP BY all
    ORDER BY year
```

```sql categories_count
    SELECT
        count() as nb_categories
    FROM data_games_viz.obt_categories
    GROUP BY plateforms
```

```sql categories_count_select
    SELECT
        count() as nb_categories
    FROM data_games_viz.obt_categories
    WHERE
        case plateforms
            WHEN 'Windows' THEN 1
            WHEN 'Mac' THEN 2
            WHEN 'Linux' THEN 4
        END
        IN ${inputs.plateforme.value}
    GROUP BY plateforms
```

```sql categories
    SELECT
        name_categorie,
        sum(value) as value
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
        release_date AS year,
        count() as nb_categories
    FROM data_games_viz.obt_categories
    WHERE
        case plateforms
            WHEN 'Windows' THEN 1
            WHEN 'Mac' THEN 2
            WHEN 'Linux' THEN 4
        END
        IN ${inputs.plateforme.value}
    GROUP BY plateforms, year
    ORDER BY year
```

```sql search_games
    SELECT
        name_game,
        '/' || steam_id::int as link,
    FROM data_games_viz.obt_games
    WHERE plateforms in ${inputs.plateforme.value}
        AND year(release_game) LIKE '${inputs.year.value}'
```

```sql list_year
    SELECT
        year(release_game) as year
    FROM data_games_viz.obt_games
    GROUP BY release_game
```

```sql plateformes
    SELECT
        categorie_name,
        plateforms,
        count() as value
    FROM data_games_viz.obt_plateforms
    WHERE categorie_name LIKE '%-player%'
        AND year(release_date) LIKE '${inputs.year.value}'
    GROUP BY categorie_name, plateforms
```

```sql plateforms_count
    SELECT
        3 as value
    FROM
        data_games_viz.obt_plateforms
    LIMIT 1
```
<Dropdown name=plateforme title="Plateformes">
    <DropdownOption value="(1, 3, 5, 7)" valueLabel="Windows"/>
    <DropdownOption value="(2, 3, 6, 7)" valueLabel="Mac"/>
    <DropdownOption value="(3, 4, 5, 7)" valueLabel="Linux"/>
    <DropdownOption value="(1, 2, 3, 4, 5, 6, 7)" valueLabel="Toutes les plateformes"/>
</Dropdown>
<Dropdown title="Année" data={list_year} name=year value=year>
    <DropdownOption value="%" valueLabel="Toutes les années"/>
</Dropdown>

<Grid cols=3>
<BigValue 
    data={games_count} 
    value=nb_games
    title="Nombre de jeux enregistré"
    fmt="%d"
/>
<BigValue 
    data={categories_count}
    title="Nombre de catégories déclaré"
    value=nb_categories
/>
<BigValue 
    data={plateforms_count}
    title="Nombre de plateforms disponibles"
    value=value
/>
</Grid>

<Tabs>
    <Tab label="Games">
        <BigValue
            data={games_count_select}
            value=nb_games
            title="Nombre de jeu enregistré"
            fmt="%d"
        />

        <BarChart
            data={games}
            x=name_game
            y=notes
            swapXY=true
            title="Les 3 jeux les plus notés"
            colorPalette={
                "#00B34E"
            }
        />

        <BarChart
            data={games_list}
            title="Nombre de sortie par an, "
            x=year
            y=nb_games
            y2=price
            y2SeriesType=line
            colorPalette={[
                "#00B34E",
                "#007661"
            ]}
        />
    </Tab>
    <Tab label="Categories">
        <BigValue
            data={categories_count_select}
            value=nb_categories
            title="Nombre de catégories"
            fmt="%d"
        />

        <BarChart
            data={categories}
            x=name_categorie
            y=value
            swapXY=true
            title="Les 3 catégories avec le plus de jeux"
            colorPalette={
                "#00C2FF"
            }
        />

        <BarChart
            data={categories_list}
            title="Nombre de catégories créé chaque année"
            x=year
            y=nb_categories
            colorPalette={[
                "#00C2FF",
                "#00E7DA"
            ]}
        />
    </Tab>
    <Tab label="Plateformes">
        <BigValue 
            data={plateforms_count}
            title="Nombre de plateforms disponibles"
            value=value
        />
        <SankeyDiagram
            data={plateformes}
            sourceCol=categorie_name
            targetCol=plateforms
            valueCol=value
            colorPalette={[
                "#0053E9",
                "#CF38C7",
                "#FF4493",
                "#FF8165",
                "#FFC051",
                "#F9F871"
            ]}
        />
    </Tab>
</Tabs>
<DataTable data={search_games} search=true link=link/>
