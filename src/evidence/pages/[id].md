---
title: Fiche jeu
---

```sql game_meta
    SELECT
        name_game,
        year(release_game) as year,
        price,
        notes
    FROM data_games_viz.obt_games
    WHERE steam_id = ${params.id}
    LIMIT 1
```

```sql game_categories
    SELECT DISTINCT categorie_name AS "Catégorie"
    FROM data_games_viz.obt_plateforms
        JOIN data_games_viz.obt_games ON game_name = name_game
    WHERE steam_id = ${params.id}
    ORDER BY 1
```

```sql game_platforms
    SELECT DISTINCT obt_plateforms.plateforms AS "Plateforme"
    FROM data_games_viz.obt_plateforms
        JOIN data_games_viz.obt_games ON game_name = name_game
    WHERE steam_id = ${params.id}
    ORDER BY 1
```

```sql game_compare
    SELECT 'Ce jeu' AS reference, notes AS recommandations
    FROM data_games_viz.obt_games
    WHERE steam_id = ${params.id}
    UNION ALL
    SELECT 'Moyenne du catalogue' AS reference, round(avg(notes)) AS recommandations
    FROM data_games_viz.obt_games
```

```sql similar_games
    SELECT DISTINCT
        g.name_game AS "Jeu",
        g.notes AS recommandations,
        '/' || g.steam_id::int AS link
    FROM data_games_viz.obt_games g
        JOIN data_games_viz.obt_plateforms p ON g.name_game = p.game_name
    WHERE p.categorie_name IN (
            SELECT pp.categorie_name
            FROM data_games_viz.obt_plateforms pp
                JOIN data_games_viz.obt_games gg ON gg.name_game = pp.game_name
            WHERE gg.steam_id = ${params.id}
        )
        AND g.steam_id <> ${params.id}
    GROUP BY g.name_game, g.notes, g.steam_id
    ORDER BY recommandations DESC NULLS LAST
    LIMIT 8
```

```sql search_games
    SELECT
        name_game AS "Jeu",
        '/' || steam_id::int as link
    FROM data_games_viz.obt_games
    ORDER BY name_game
```

<a href="/" class="inline-block mb-2 text-sm text-blue-600 hover:underline">← Retour à l'accueil</a>

{#if game_meta.length > 0}

<p class="text-sm text-gray-500"><a href="/" class="text-blue-600 hover:underline">Accueil</a> › <strong>{game_meta[0].name_game}</strong></p>

# {game_meta[0].name_game}

<Grid cols=3>
    <BigValue data={game_meta} value=notes title="Recommandations" fmt="#,##0"/>
    <BigValue data={game_meta} value=year title="Année de sortie"/>
    <BigValue data={game_meta} value=price title="Prix (brut)" fmt="#,##0"/>
</Grid>

<BarChart
    data={game_compare}
    x=reference
    y=recommandations
    swapXY=true
    title="Recommandations — ce jeu vs moyenne du catalogue"
    colorPalette={["#00B34E", "#94a3b8"]}
/>

## Jeux similaires

Jeux partageant des catégories avec celui-ci, les mieux recommandés (cliquez pour ouvrir) :

<BarChart
    data={similar_games}
    x=Jeu
    y=recommandations
    swapXY=true
    title="Jeux similaires les mieux recommandés"
    colorPalette={["#00C2FF"]}
/>

<DataTable data={similar_games} link=link rows=5/>

## Détails

<Grid cols=2>
    <DataTable data={game_categories} title="Catégories"/>
    <DataTable data={game_platforms} title="Plateformes"/>
</Grid>

## Tous les jeux

<DataTable data={search_games} search=true link=link rows=8/>

{:else}

> Aucune donnée disponible pour le jeu **{params.id}**. <a href="/" class="text-blue-600 hover:underline">Revenir à l'accueil</a>.

{/if}
