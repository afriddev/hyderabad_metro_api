all_station_details_query = 'WITH stationDetails AS ( SELECT "stationDetails"  FROM public."trainRoutes", jsonb_array_elements("stationsDetails") AS "stationDetails" )'

from_station_details_query = """fromStationDetail AS (SELECT "stationDetails" AS "fromStationDetail" FROM stationDetails, jsonb_array_elements_text("stationDetails"->'stationName') AS lang WHERE LOWER(lang) ILIKE LOWER(:fromStationName) AND (:fromStationNo = '' OR "stationDetails"->>'stationNo' = :fromStationNo) AND (:fromStationLineNo = '' OR "stationDetails"->>'lineNo' = :fromStationLineNo))"""

to_station_details_query = """toStationDetail AS (SELECT "stationDetails" AS "toStationDetail" FROM stationDetails, jsonb_array_elements_text("stationDetails"->'stationName') AS lang WHERE LOWER(lang) ILIKE LOWER(:toStationName) AND (:toStationNo = '' OR "stationDetails"->>'stationNo' = :toStationNo) AND (:toStationLineNo = '' OR "stationDetails"->>'lineNo' = :toStationLineNo) LIMIT 1)
"""
from_line_inter_change_station_query = """
fromLineInterChangeStations AS (SELECT "stationDetails" AS "fromLineInterChangeStations" FROM stationDetails, fromStationDetail WHERE "stationDetails"->'lineNo' = "fromStationDetail"->'lineNo' AND ("stationDetails"->'interChangeAndTerminus' = 'true' OR "stationDetails"->'interChange' = 'true' ) ORDER BY ABS(("stationDetails"->'stationNo')::int - ("fromStationDetail"->'stationNo')::int) ASC) """

to_line_inter_change_station_query = """toLineInterChangeStations AS (SELECT "stationDetails" AS "toLineInterChangeStations"FROM stationDetails, toStationDetail WHERE "stationDetails"->'lineNo' = "toStationDetail"->'lineNo' AND ("stationDetails"->'interChangeAndTerminus' = 'true' OR "stationDetails"->'interChange' = 'true' )ORDER BY ABS(("stationDetails"->'stationNo')::int - ("toStationDetail"->'stationNo')::int) ASC)"""

station_between_same_line_query = """stationsBetweenSameLine AS (
            SELECT "stationDetails"
            FROM stationDetails, fromStationDetail, toStationDetail
            WHERE ("fromStationDetail"->'lineNo') = ("toStationDetail"->'lineNo') 
            AND ("stationDetails"->'lineNo') = ("fromStationDetail"->'lineNo')
            AND ("stationDetails"->'stationNo')::int BETWEEN LEAST(("fromStationDetail"->'stationNo')::int, ("toStationDetail"->'stationNo')::int) 
            AND GREATEST(("fromStationDetail"->'stationNo')::int, ("toStationDetail"->'stationNo')::int)
        )
"""
stations_with_same_name = """stationWithSameName AS( 
SELECT "stationDetails"  FROM stationDetails,
jsonb_array_elements_text("stationDetails"->'stationName') AS "stationName"
WHERE(
    (LOWER("stationName") = LOWER(:fromStationName) OR LOWER("stationName") = LOWER(:toStationName) ) 
    AND ("stationDetails"->>'lineNo') != :fromLineNo AND ("stationDetails"->>'lineNo') != :toLineNo
)
LIMIT 2
)""" 
