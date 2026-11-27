/*
SCRIPT NAME    : d_fcb_player_info.sql
PROJECT        : BarcaKings
VERSION        : 1.0

DESCRIPTION:
    Dimmnention Table for FCB players

SOURCE TABLES:
    - workspace.bk_curated.fcb_full_squad
    - workspace.bk_curated.ucl_player_stats_discipline

TARGET TABLES:
    - workspace.bk_consumable.d_player_info

EXECUTION FREQUENCY:
    Daily - Truncate & Load
*/

SELECT 
    'football'                                                                AS sport,
    TRIM(`metadata_shirt-number`)                                             AS jersey_number,
    TRIM(title)                                                               AS player_name ,
    COALESCE(TRIM(sts.name),TRIM(sqd.title))                                  AS player_full_name,
    TRIM(UPPER(position))                                                     AS player_role,
    TRIM(ucl_dis.player_age)                                                  AS player_age,
    TRIM(ucl_dis.player_birthDate)                                            AS date_of_birth,
    TRIM(nationality)                                                         AS nationality,
    TRIM(sts.country_id)                                                      AS country_id,
    TRIM(city)                                                                AS city,
    TRIM(placeOfBirth)                                                        AS place_of_birth,
    TRIM(description)                                                         AS description,
    'Fútbol Club Barcelona'                                                   AS team_name,
    'FC Barcelona'                                                            AS team_display_name,
    'BAR'                                                                     AS team_code
FROM
    workspace.bk_curated.fcb_full_squad sqd
LEFT JOIN
    workspace.bk_curated.fcb_players_stats sts
    ON sqd.`metadata_shirt-number` = sts.shirt_number
LEFT JOIN
    workspace.bk_curated.ucl_player_stats_discipline ucl_dis
    ON ucl_dis.player_clubJerseyNumber = sqd.`metadata_shirt-number`
