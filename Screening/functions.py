import csv
import pandas as pd
from statistics import median

def swNumberAndSize(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Number', 'Number (%)', 'Length (km)', 'Length (%)', 'Area (km^2)', 'Area (%)',
               'Median Length', 'Median Area']
    with open(
            working_directory + '1.swNumberAndSize' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            dropMedianArea = '''drop table if exists swMedianArea;'''

            MedianArea = '''create temporary table swMedianArea as SELECT countryCode,
                       cYear,
                       round(AVG(cArea), 1) as medianArea
                  FROM (
                           SELECT countryCode,
                                  cYear,
                                  cArea
                             FROM [WFD2022extract.SWB_SurfaceWaterBody]
                            WHERE countryCode = "''' + country + '''" AND 
                                  countryCode IS NOT NULL AND 
                                  cArea IS NOT NULL AND 
                                  cYear = ''' + str(cYear) + '''
                            ORDER BY cArea
                            LIMIT 2 - (
                                          SELECT COUNT( * ) 
                                            FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                           WHERE countryCode = "''' + country + '''" AND 
                                                 countryCode IS NOT NULL AND 
                                                 cArea IS NOT NULL AND 
                                                 cYear = ''' + str(cYear) + '''
                                      )
                %                     2 OFFSET (
                                      SELECT (COUNT( * ) - 1) / 2
                                        FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                       WHERE countryCode = "''' + country + '''" AND 
                                             countryCode IS NOT NULL AND 
                                             cArea IS NOT NULL AND 
                                             cYear = ''' + str(cYear) + '''
                                       GROUP BY countryCode = "''' + country + '''"
                                  )
                       );'''

            dropMedianLength = '''drop table if exists swMedianLength;'''

            MedianLength = '''create temporary table swMedianLength as SELECT countryCode,
                                   cYear,
                                   round(AVG(cLength), 1) as medianLength
                              FROM (
                                       SELECT countryCode,
                                              cYear,
                                              cLength
                                         FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                        WHERE countryCode = "''' + country + '''" AND 
                                              countryCode IS NOT NULL AND 
                                              cLength IS NOT NULL AND 
                                              cYear = 2022
                                        ORDER BY cLength
                                        LIMIT 2 - (
                                          SELECT COUNT( * ) 
                                            FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                           WHERE countryCode = "''' + country + '''" AND 
                                                 countryCode IS NOT NULL AND 
                                                 cLength IS NOT NULL AND 
                                                 cYear = 2022
                                                  )
                            %                     2 OFFSET (
                                                  SELECT (COUNT( * ) - 1) / 2
                                                    FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                   WHERE countryCode = "''' + country + '''" AND 
                                                         countryCode IS NOT NULL AND 
                                                         cLength IS NOT NULL AND 
                                                         cYear = 2022
                                                   GROUP BY countryCode = "''' + country + '''"
                                              )
                                   );'''

            final = '''SELECT countryCode,
                       cYear,
                       count(euSurfaceWaterBodyCode),
                       'NaN',
                       round(sum(cLength) ),
                       'NaN',
                       round(sum(cArea) ), 
                       'NaN',
                       (select medianLength from swMedianLength),
                       (select medianArea from swMedianArea)
                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                 WHERE cYear = ''' + str(cYear) + ''' AND
                       countryCode = "''' + country + '''";'''



            # count(euSurfaceWaterBodyCode) * 100.0 /
            # (select count(euSurfaceWaterBodyCode)
            # from
            # [WFD2022extract.SWB_SurfaceWaterBody] )
            # round(sum(cLength) * 100.0 /
            #       (select sum(cLength)
            # from
            # [WFD2022extract.SWB_SurfaceWaterBody]))
            # round(sum(cArea) * 100.0 /
            #       (select sum(cArea)
            # from
            # [WFD2022extract.SWB_SurfaceWaterBody]))

            cur.execute(dropMedianArea)
            cur.execute(MedianArea)
            cur.execute(dropMedianLength)
            cur.execute(MedianLength)
            data = cur.execute(final).fetchall()

            write.writerows(data)


def gwNumberAndSize(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Number', 'Number (%)', 'Area (km^2)', 'Area (%)', 'Median Area']
    with open(
            working_directory + '2.gwNumberAndSize' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            dropMedianArea = '''drop table if exists GWMedian;'''

            MedianArea = '''create temporary table GWMedian as SELECT countryCode,
                   cYear,
                   round(AVG(cArea), 1) as median
              FROM (
                       SELECT countryCode,
                              cYear,
                              cArea
                         FROM [WFD2022extract.GWB_GroundWaterBody]
                        WHERE countryCode = "''' + country + '''" AND 
                              countryCode IS NOT NULL AND 
                              cArea IS NOT NULL AND 
                              cYear = ''' + str(cYear) + '''
                        ORDER BY cArea
                        LIMIT 2 - (
                                      SELECT COUNT( * ) 
                                        FROM [WFD2022extract.GWB_GroundWaterBody]
                                       WHERE countryCode = "''' + country + '''" AND 
                                             countryCode IS NOT NULL AND 
                                             cArea IS NOT NULL AND 
                                             cYear = ''' + str(cYear) + '''
                                  )
            %                     2 OFFSET (
                                  SELECT (COUNT( * ) - 1) / 2
                                    FROM [WFD2022extract.GWB_GroundWaterBody]
                                   WHERE countryCode = "''' + country + '''" AND 
                                         countryCode IS NOT NULL AND 
                                         cArea IS NOT NULL AND 
                                         cYear = ''' + str(cYear) + '''
                                   GROUP BY countryCode = "''' + country + '''"
                              )
                   );'''

            final = '''SELECT countryCode,
                       cYear,
                       count(groundWaterBodyName),
                       'NaN',
                       round(sum(cArea) ), 
                       'NaN',
                       (select median from GWMedian)
                  FROM [WFD2022extract.GWB_GroundWaterBody]
                 WHERE cYear = ''' + str(cYear) + ''' AND
                       countryCode = "''' + country + '''";'''
            # count(groundWaterBodyName) * 100.0 / (select count(groundWaterBodyName)
            # from
            # [WFD2022extract.GWB_GroundWaterBody]),

            # round(sum(cArea) * 100.0 / (select sum(cArea)
            # from
            # [WFD2022extract.GWB_GroundWaterBody])),

            cur.execute(dropMedianArea)
            cur.execute(MedianArea)
            data = cur.execute(final).fetchall()

            write.writerows(data)


def swWater_body_category_and_Type(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Surface Water Body Category', 'Type', 'Total']
    with open(
            working_directory + '3.swWater_body_category_and_Type' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            final = '''SELECT countryCode,
                   cYear,
                   surfaceWaterBodyCategory,
                   naturalAWBHMWB,
                   count(euSurfaceWaterBodyCode) 
              FROM [WFD2022extract.SWB_SurfaceWaterBody]
             WHERE countryCode = "''' + country + '''" AND 
                   cYear = ''' + str(cYear) + '''
             GROUP BY surfaceWaterBodyCategory,
                      naturalAWBHMWB;'''

            data = cur.execute(final).fetchall()

            write.writerows(data)


def swNumber_of_impacts_by_country(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Impact 0 - Number', 'Impact 0 - Number (%)',
               'Impact 1 - Number', 'Impact 1 - Number (%)',
               'Impact 2 - Number', 'Impact 2 - Number (%)',
               'Impact 3 - Number', 'Impact 3 - Number (%)',
               'Impact 4+ - Number', 'Impact 4+ - Number (%)']
    with open(
            working_directory + '4.swNumber_of_impacts_by_country' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer((f))
        write.writerow(headers)
        cur = conn.cursor()

        for country in countryCode:
            drop = '''DROP TABLE IF EXISTS val;'''

            temp1 = '''CREATE TEMPORARY TABLE val AS SELECT DISTINCT countryCode,
                                              cYear,
                                              euSurfaceWaterBodyCode,
                                              count(swSignificantImpactType) AS Counter
                                FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
                               WHERE countryCode = "''' + country + '''" AND 
                                     cYear = 2022
                               GROUP BY euSurfaceWaterBodyCode;'''

            drop1 = '''DROP TABLE IF EXISTS val1;'''

            temp2 = '''CREATE TEMPORARY TABLE val1 AS SELECT countryCode, CASE WHEN Counter = 0 THEN count(euSurfaceWaterBodyCode) END AS t0,
                                      CASE WHEN Counter = 1 THEN count(euSurfaceWaterBodyCode) END AS t1,
                                      CASE WHEN Counter = 2 THEN count(euSurfaceWaterBodyCode) END AS t2,
                                      CASE WHEN Counter = 3 THEN count(euSurfaceWaterBodyCode) END AS t3,
                                      CASE WHEN Counter >= 4 THEN count(euSurfaceWaterBodyCode) END AS t4
                                 FROM val
                                GROUP BY Counter;'''

            final = '''SELECT countryCode, round(sum(t0)),
                       round(sum(t0) * 100.0 / (
                                             SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                               FROM val1
                                         )),
                       round(sum(t1)),
                       round(sum(t1) * 100.0 / (
                                             SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                               FROM val1
                                         )),
                       round(sum(t2)),
                       round(sum(t2) * 100.0 / (
                                             SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                               FROM val1
                                         )),
                       round(sum(t3)),
                       round(sum(t3) * 100.0 / (
                                             SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                               FROM val1
                                         )),
                       round(sum(t4)),
                       round(sum(t4) * 100.0 / (
                                             SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                               FROM val1
                                         ))
                  FROM val1;'''
            cur.execute(drop)
            cur.execute(temp1)
            cur.execute(drop1)
            cur.execute(temp2)
            data = cur.execute(final).fetchall()
            write.writerows(data)


def swSignificantPressureType(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Significant Pressure Type Group', 'Significant Pressure Type', 'Number',
               'Number (%)']
    with open(
            working_directory + '4.swSignificantPressureType' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        country = ','.join(countryCode)
        swSignificantPressureType = cur.execute('''SELECT DISTINCT swSignificantPressureTypeGroup
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantPressureType]
                      WHERE swSignificantPressureTypeGroup IS NOT NULL 
                      and countryCode = "''' + country + '''";''').fetchall()

        for country in countryCode:
            for spt in swSignificantPressureType:
                temp = ','.join(spt)
                
                droptable = '''DROP TABLE IF EXISTS GroupValues; '''

                tempArea = '''CREATE TEMPORARY TABLE GroupValues AS SELECT DISTINCT euSurfaceWaterBodyCode,
                                                                  euSurfaceWaterBodyCode AS Code
                                                    FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantPressureType]
                                                   WHERE swSignificantPressureTypeGroup = "''' + temp + '''" and
                                                    cYear = ''' + str(cYear) + ''' AND 
                                                    countryCode = "''' + country + '''";'''

                finaltable = '''SELECT countryCode,
                                   cYear,
                                   swSignificantPressureTypeGroup,
                                   swSignificantPressureType,
                                   round(count(euSurfaceWaterBodyCode) ),
                                   round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                  SELECT count(Code)
                                                                    FROM GroupValues
                                                              )
                                   )
                              FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantPressureType]
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   countryCode = "''' + country + '''" AND 
                                   swSignificantPressureTypeGroup = "''' + temp + '''" 
                             GROUP BY swSignificantPressureType;'''

                cur.execute(droptable)
                cur.execute(tempArea)
                data = cur.execute(finaltable).fetchall()

                write.writerows(data)


def swSignificant_pressures_reported_as_Other(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Significant Pressure Other', 'Number', 'Number (%)']
    with open(
            working_directory + '4.swSignificant_pressures_reported_as_Other' + str(cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            final = '''SELECT distinct countryCode,
                   cYear,
                   swSignificantPressureOther,
                   count(distinct surfaceWaterBodyName),
                   round(count(distinct surfaceWaterBodyName) * 100.0 / (
                                SELECT count(distinct surfaceWaterBodyName)
                               FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantPressureType]
                              WHERE countryCode = "''' + country + '''" AND 
                                    swSignificantPressureOther IS NOT NULL
                            ),2
                   ) 
                  FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantPressureType]
                 WHERE countryCode = "''' + country + '''" AND 
                       cYear = 2022 AND
                       swSignificantPressureOther IS NOT NULL
                 GROUP BY swSignificantPressureOther order by COUNT(swSignificantPressureOther) DESC;'''

            data = cur.execute(final).fetchall()

            write.writerows(data)


def swSignificantImpactType_Table_Other(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_PressuresImpacts/SWB_Impacts_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Significant Impact Other', 'Number', 'Number(%)']
    with open(
            working_directory + '4.swSignificantImpactType_Table_Other' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               swSignificantImpactOther,
                               COUNT(swSignificantImpactOther),
                               round(COUNT(swSignificantImpactOther) * 100.0 / (
                                                                                   SELECT COUNT(swSignificantImpactOther) 
                                                                                     FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
                                                                                    WHERE cYear = ? AND 
                                                                                          countryCode = ?
                                                                               ))
                                              FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
                                             WHERE surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                   swSignificantImpactOther <> "Adverse effects on ecological indices" AND 
                                                   swSignificantImpactOther <> "Dėl nežinomų priežasčių geros ekologinės būklės reikalavimų neatitinka biologinių elementų rodikliai" AND 
                                                   swSignificantImpactOther <> "Dėl nežinomų priežasčių geros ekologinės būklės reikalavimų galimai neatitinka biologiniai rodikliai (yra netikrumas dėl būklės)" AND 
                                                   swSignificantImpactOther <> "Dėl galimo žuvininkystės tvenkinių poveikio geros ekologinės būklės reikalavimų neatitinka biologinių elementų rodikliai" AND 
                                                   swSignificantImpactOther <> "Dėl istorinės taršos geros ekologinės būklės reikalavimų neatitinka biologinių elementų rodikliai" AND 
                                                   swSignificantImpactOther <> "Dėl galimo žuvininkystės taršos poveikio geros ekologinės būklės reikalavimų neatitinka biologinių elementų rodikliai" AND 
                                                   swSignificantImpactOther <> "Dėl bendro istorinės ir dabartinės taršos poveikio geros ekologinės būklės reikalavimų neatitinka biologinių elementų rodikliai" AND 
                                                   swSignificantImpactOther <> "Nustatytas specifinių teršalų koncentracijų viršijimas" AND 
                                                   swSignificantImpactOther <> "Urban run-off" AND 
                                                   cYear == ? AND 
                                                   countryCode = ?
                                             GROUP BY swSignificantImpactOther
                                             ORDER BY COUNT(swSignificantImpactOther) DESC;
                                            ''', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def swSignificant_impacts(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Significant Impact Type', 'Number', 'Number (%)']
    with open(
            working_directory + '4.swSignificant_impacts' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            droptable = '''drop table if exists distinctValues;'''
            temp = '''create temporary table distinctValues as 
                        select Distinct euSurfaceWaterBodyCode as Value 
                        from [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
                        WHERE countryCode = "''' + country + '''";'''

            final = '''SELECT countryCode,
                   cYear,
                   swSignificantImpactType,
                   count(euSurfaceWaterBodyCode),
                   round(count(euSurfaceWaterBodyCode) * 100.0 / (
                            select count(Value) from distinctValues
                                                    )
                   ) 
              FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
             WHERE countryCode = "''' + country + '''"
             GROUP BY swSignificantImpactType;'''

            cur.execute(droptable)
            cur.execute(temp)
            data = cur.execute(final).fetchall()

            write.writerows(data)


def gwSignificantImpactType_Other(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_PressuresImpacts/GWB_Impacts_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '5.gwSignificantImpactType_Other' + str(cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        header = ["Country", "Year", "Significant Impact Other", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('SELECT countryCode, cYear, gwSignificantImpactOther, round(sum(cArea)), '
                               'round(sum(cArea) * 100.0 / ( '
                               'SELECT sum(cArea) '
                               'FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType] '
                               'WHERE cYear = ? AND countryCode = ? '
                               ')) '
                               'FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType] '
                               'WHERE cYear = ? AND countryCode = ? '
                               'and gwSignificantImpactOther is not Null '
                               'GROUP BY gwSignificantImpactOther ', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def gwSignificant_impacts(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Significant Impact Type', 'Area (km^2)', 'Area (%)']
    with open(
            working_directory + '5.gwSignificant_impacts' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            droptable = '''drop table if exists distinctValues;'''

            temp = '''create temporary table distinctValues as 
                        select Distinct groundWaterBodyName, cArea as Value 
                        from [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                        where countryCode = "''' + country + '''";'''

            final = '''SELECT countryCode,
                       cYear,
                       gwSignificantImpactType,
                       round(sum(cArea)),
                       round(sum(cArea) * 100.0 / (
                                select sum(Value) from distinctValues
                                                        )
                       ) 
                  FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                 WHERE countryCode = "''' + country + '''"
                 GROUP BY gwSignificantImpactType;'''

            cur.execute(droptable)
            cur.execute(temp)
            data = cur.execute(final).fetchall()

            write.writerows(data)


def gwSignificantPressureType_Table(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_PressuresImpacts/GWB_Pressures?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Significant Pressure Type Group', 'Significant Pressure Type', 'Area (km^2)', 'Area (%)']
    with open(
            working_directory + '5.gwSignificantPressureType_Table' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        gwSignificantPressureTypeGroup = cur.execute('''select distinct gwSignificantPressureTypeGroup
                                            from [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType]
                                            where cYear = ''' + str(cYear) + ''' and gwSignificantPressureTypeGroup <> "Unpopulated" and 
                                             gwSignificantPressureTypeGroup is not Null;''').fetchall()

        gwSignificantPressureType = cur.execute('''select distinct gwSignificantPressureType
                                                from [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType]
                                                where cYear = ''' + str(cYear) + ''' and gwSignificantPressureType <> "Unpopulated"''').fetchall()

        for country in countryCode:
            for pgroup in gwSignificantPressureTypeGroup:
                for ptype in gwSignificantPressureType:
                    temppgroup = ','.join(pgroup)
                    tempptype = ','.join(ptype)
                    sqlDropValues = '''DROP TABLE IF EXISTS DistinctValues;'''

                    sqlDistinct = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euGroundWaterBodyCode,
                                                                     gwSignificantPressureType,
                                                                     gwSignificantPressureTypeGroup,
                                                                     cArea AS A
                                                       FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType]
                                                      WHERE cYear = ''' + str(cYear) + ''' AND 
                                                            countryCode = "''' + country + '''" AND 
                                                            gwQuantitativeStatusValue <> "unpopulated" and
                                                            gwChemicalStatusValue <> "unpopulated" AND 
                                                            gwSignificantPressureTypeGroup = "''' + temppgroup + '''" AND 
                                                            gwSignificantPressureType = "''' + tempptype + '''";'''

                    sqlDropdenominator = '''DROP TABLE IF EXISTS DistinctArea;'''

                    sqlDenominator = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euGroundWaterBodyCode, cArea as G
                                          FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType]
                                        WHERE cYear = ''' + str(cYear) + ''' AND 
                                          countryCode = "''' + country + '''" AND
                                          gwChemicalStatusValue <> "unpopulated" AND 
                                          gwQuantitativeStatusValue <> "unpopulated" and 
                                          gwSignificantPressureType <> "unpopulated" AND 
                                          gwSignificantPressureTypeGroup = "''' + temppgroup + '''";'''

                    sqlFinal = '''SELECT countryCode,
                                   gwSignificantPressureTypeGroup,
                                   gwSignificantPressureType,
                                   (
                                       SELECT ROUND(SUM(A) ) 
                                         FROM DistinctValues
                                   ),
                                   ROUND((
                                              SELECT sum(A) 
                                                FROM DistinctValues
                                          )
                            *             100.0 / (
                                                      SELECT sum(G) 
                                                        FROM DistinctArea
                                                  )
                                   )
                              FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType]
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   countryCode = "''' + country + '''" AND 
                                   gwQuantitativeStatusValue <> "unpopulated" and
                                   gwChemicalStatusValue <> "unpopulated" AND 
                                   gwSignificantPressureType = "''' + tempptype + '''" AND 
                                   gwSignificantPressureTypeGroup = "''' + temppgroup + '''" and 
                                    gwSignificantPressureTypeGroup is not Null

                             GROUP BY gwSignificantPressureTypeGroup,
                                      gwSignificantPressureType;'''

                    cur.execute(sqlDropValues)
                    cur.execute(sqlDistinct)
                    cur.execute(sqlDropdenominator)
                    cur.execute(sqlDenominator)
                    data = cur.execute(sqlFinal).fetchall()

                    write.writerows(data)


def gwSignificantPressureType_OtherTable(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_PressuresImpacts/GWB_Pressures_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Year', 'Significant Pressure Other', 'Area (km^2)', 'Area (%)']
    with open(
            working_directory + '5.gwSignificantPressureType_OtherTable' + str(cYear) + '.csv',
            'w+', newline='', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('SELECT countryCode, cYear, gwSignificantPressureOther, round(sum(cArea) ),'
                               'round(sum(cArea) * 100.0 / ( '
                               'SELECT sum(cArea) '
                               'FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType] '
                               'WHERE cYear = ? AND countryCode = ? and gwSignificantPressureOther is not Null '
                               ')) '
                               'FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType] '
                               'WHERE cYear = ? AND countryCode = ? and gwSignificantPressureOther is not Null '
                               'GROUP BY gwSignificantPressureOther '
                               , (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def gwSignificantImpactTypeByCountry2022(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Impact 0 - Area (km^2)', 'Impact 0 - Area (%)',
               'Impact 1 - Area (km^2)', 'Impact 1 - Area (%)',
               'Impact 2 - Area (km^2)', 'Impact 2 - Area (%)',
               'Impact 3 - Area (km^2)', 'Impact 3 - Area (%)',
               'Impact 4+ - Area (km^2)', 'Impact 4+ - Area (%)']
    with open(
            working_directory + '5.1.gwSignificantImpactTypeByCountry' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        for county in countryCode:
            drop1 = '''DROP TABLE IF EXISTS val;'''

            temp1 = '''CREATE TEMPORARY TABLE val AS SELECT DISTINCT countryCode,
                                                      cYear,
                                                      cArea,
                                                      euGroundWaterBodyCode,
                                                      case when gwSignificantImpactType = "None" then count(gwSignificantImpactType) end as NullValues, 
                                                      case when gwSignificantImpactType <> "None" then count(gwSignificantImpactType) end AS Counter
                                        FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                                       WHERE countryCode = "''' + county + '''" AND 
                                             cYear = 2022
                                       GROUP BY euGroundWaterBodyCode;'''

            drop2 = '''DROP TABLE IF EXISTS val1;'''

            temp2 = '''CREATE TEMPORARY TABLE val1 AS SELECT countryCode, CASE WHEN NullValues THEN sum(cArea) END AS t0,
                                                  CASE WHEN Counter = 1 THEN sum(cArea) END AS t1,
                                                  CASE WHEN Counter = 2 THEN sum(cArea) END AS t2,
                                                  CASE WHEN Counter = 3 THEN sum(cArea) END AS t3,
                                                  CASE WHEN Counter >= 4 THEN sum(cArea) END AS t4
                                             FROM val
                                            GROUP BY Counter;'''

            final = '''SELECT countryCode, round(sum(t0)),
                   round(sum(t0) * 100.0 / (
                                         SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                           FROM val1
                                     )),
                   round(sum(t1)),
                   round(sum(t1) * 100.0 / (
                                         SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                           FROM val1
                                     )),
                   round(sum(t2)),
                   round(sum(t2) * 100.0 / (
                                         SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                           FROM val1
                                     )),
                   round(sum(t3)),
                   round(sum(t3) * 100.0 / (
                                         SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                           FROM val1
                                     )),
                   round(sum(t4)),
                   round(sum(t4) * 100.0 / (
                                         SELECT total(t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                           FROM val1
                                     ))
              FROM val1;'''

            cur.execute(drop1)
            cur.execute(temp1)
            cur.execute(drop2)
            cur.execute(temp2)
            data = cur.execute(final).fetchall()
            write.writerows(data)


def swNumber_of_impacts_by_country_CreateTable_UploadData(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year',
               'Impact 0 - Area (km^2)', 'Impact 0 - Area (%)',
               'Impact 1 - Area (km^2)', 'Impact 1 - Area (%)',
               'Impact 2 - Area (km^2)', 'Impact 2 - Area (%)',
               'Impact 3 - Area (km^2)', 'Impact 3 - Area (%)',
               'Impact 4 - Area (km^2)', 'Impact 4 - Area (%)',

               ]
    with open(
            working_directory + '4.swNumber_of_impacts_by_country' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        update = '''insert into swNumber_of_impacts_by_country VALUES(?,?,?,?,?,?,?,?,?)
                    '''

        surfaceWaterBodyName = cur.execute(
            '''select distinct surfaceWaterBodyName from [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]''').fetchall()

        for country in countryCode:
            for temp in surfaceWaterBodyName:
                names = ','.join(temp)
                sql = cur.execute('''SELECT countryCode,
                           cYear,
                           cArea,
                           surfaceWaterBodyName,
                           case when surfaceWaterBodyName = "''' + names + '''" and count(swSignificantImpactType) == 0 then count(euSurfaceWaterBodyCode) end as "Impact0",
                           case when surfaceWaterBodyName = "''' + names + '''" and count(swSignificantImpactType) == 1 then count(euSurfaceWaterBodyCode) end as "Impact1",
                           case when surfaceWaterBodyName = "''' + names + '''" and count(swSignificantImpactType) == 2 then count(euSurfaceWaterBodyCode) end as "Impact2",
                           case when surfaceWaterBodyName = "''' + names + '''" and count(swSignificantImpactType) == 3 then count(euSurfaceWaterBodyCode) end as "Impact3",
                           case when surfaceWaterBodyName = "''' + names + '''" and count(swSignificantImpactType) >= 4 then count(euSurfaceWaterBodyCode) end as "Impact4"
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
                     WHERE countryCode = "''' + country + '''" and surfaceWaterBodyName = "''' + names + '''"
                     GROUP BY surfaceWaterBodyName;''').fetchall()

                cur.executemany(update, sql)
                conn.commit()


def gwSignificantImpactType(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_PressuresImpacts/GWB_Impacts?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '5.gwSignificantImpactType' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Significant Impact Type", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        country = ','.join(countryCode)
        SOW_GWB_gwSignificantImpactType = cur.execute('''select distinct gwSignificantImpactType
                                                        from [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                                                        where cYear = ''' + str(cYear) + ''' 
                                                        and gwSignificantImpactType <> "Unpopulated" 
                                                        and countryCode = "''' + country + '''";''').fetchall()

        for country in countryCode:
            for Itype in SOW_GWB_gwSignificantImpactType:
                temptype = ','.join(Itype)

                sqldropValues = '''DROP TABLE IF EXISTS DistinctValues; '''

                sqlDistinct = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euGroundWaterBodyCode,
                                                         cArea AS A
                                           FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                                          WHERE cYear = ''' + str(cYear) + ''' AND 
                                                countryCode = "''' + country + '''" AND 
                                                gwQuantitativeStatusValue <> "unpopulated" AND 
                                                gwChemicalStatusValue <> "unpopulated" AND 
                                                gwSignificantImpactType = "''' + temptype + '''"; '''

                sqlDropArea = '''DROP TABLE IF EXISTS DistinctArea; '''

                sqlArea = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euGroundWaterBodyCode,
                                                       cArea AS G
                                         FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                                        WHERE cYear = ''' + str(cYear) + ''' AND 
                                              countryCode = "''' + country + '''" AND 
                                              gwQuantitativeStatusValue <> "unpopulated" AND 
                                              gwChemicalStatusValue <> "unpopulated" AND
                                              gwSignificantImpactType <> "Unpopulated";
                                               '''

                sqlFinal = '''SELECT countryCode,
                           gwSignificantImpactType,
                           (
                               SELECT ROUND(SUM(A) ) 
                                 FROM DistinctValues
                           ),
                           ROUND( (
                                      SELECT sum(A) 
                                        FROM DistinctValues
                                  )
                    *             100.0 / (
                                              SELECT sum(G) 
                                                FROM DistinctArea
                                          )
                           ) 
                      FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
                     WHERE cYear = ''' + str(cYear) + ''' AND 
                           countryCode = "''' + country + '''" AND 
                           gwChemicalStatusValue <> "unpopulated" AND 
                           gwQuantitativeStatusValue <> "unpopulated" AND 
                           gwSignificantImpactType = "''' + temptype + '''"
                     GROUP BY gwSignificantImpactType;'''

                cur.execute(sqldropValues)
                cur.execute(sqlDistinct)
                cur.execute(sqlDropArea)
                cur.execute(sqlArea)
                data = cur.execute(sqlFinal).fetchall()

                write.writerows(data)


def swEcologicalexemptionandpressure(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Ecological Exemption Type Group', 'Ecological Exemption Type',
               'Ecological Exemption Pressure', 'Number']
    with open(
            working_directory + '6.swEcologicalexemptionandpressure' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        country = ','.join(countryCode)
        swEcologicalExemptionTypeGroup = cur.execute(
            '''select distinct swEcologicalExemptionTypeGroup from [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType] 
                        WHERE swEcologicalExemptionTypeGroup IS NOT NULL and
                        countryCode = "''' + country + '''" ''').fetchall()
        

        for country in countryCode:
            for exemptiongroup in swEcologicalExemptionTypeGroup:
                temptypegroup = ','.join(exemptiongroup)
                
                final = cur.execute('''SELECT countryCode,
                           cYear,
                           swEcologicalExemptionTypeGroup,
                           swEcologicalExemptionType,
                           swEcologicalExemptionPressure,
                           round(count(DISTINCT euSurfaceWaterBodyCode) )
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                     WHERE countryCode = "''' + country + '''" AND 
                           swEcologicalExemptionTypeGroup = "''' + temptypegroup + '''"
                           group by swEcologicalExemptionType, swEcologicalExemptionPressure;'''
                                    ).fetchall()

                write.writerows(final)


def swEcologicalexemption(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Ecological Exemption Type Group', 'Ecological Exemption Type', 'Number',
               'Number (%)']
    with open(
            working_directory + '6.swEcologicalexemption' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        country = ','.join(countryCode)
        EcologicalExemptionGroup = cur.execute('''select distinct swEcologicalExemptionTypeGroup 
                                from [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                                where swEcologicalExemptionTypeGroup is not NULL AND
                                countryCode = "''' + country + '''";''').fetchall()

        EcologicalExemption = cur.execute('''SELECT DISTINCT swEcologicalExemptionType
                                  FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                                 WHERE swEcologicalExemptionType IS NOT NULL AND 
                                       countryCode = "''' + country + '''";''').fetchall()
        for country in countryCode:
            for temp in EcologicalExemption:
                for temp1 in EcologicalExemptionGroup:
                    temptype = ','.join(temp)
                    temptypegroup = ','.join(temp1)
                    final = '''SELECT countryCode,
                                   cYear,
                                   swEcologicalExemptionTypeGroup,
                                   swEcologicalExemptionType,
                                   round(count(distinct euSurfaceWaterBodyCode) ),
                                   round(count(distinct euSurfaceWaterBodyCode) * 100.0 / (
                                             SELECT count(distinct euSurfaceWaterBodyCode) 
                                               FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                                              WHERE countryCode = "''' + country + '''" AND 
                                                    swEcologicalExemptionTypeGroup = "''' + temptypegroup + '''"
                                         )
                                   ) 
                              FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType] 
                             WHERE countryCode = "''' + country + '''" and 
                             swEcologicalExemptionType = "''' + temptype + '''" and
                             swEcologicalExemptionTypeGroup = "''' + temptypegroup + '''"
                             group by swEcologicalExemptionTypeGroup, swEcologicalExemptionType;'''

                    data = cur.execute(final).fetchall()

                    write.writerows(data)


def SWB_Chemical_exemption_type(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_SWP_SWChemicalExemptionType/SWB_SWP_SWChemicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ["Country", "Chemical Exemption Type Group", "Chemical Exemption Type", "Area (km^2)", "Area (%)"]
    with open(
            working_directory + '6.swChemical_exemption_type' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        country = ','.join(countryCode)
        swChemicalExemptionTypeGroup = cur.execute('''select distinct swChemicalExemptionTypeGroup
                                            from [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                                            where cYear = ''' + str(cYear) + ''' and swChemicalExemptionTypeGroup is not Null and 
                                            countryCode = "''' + country + '''";''').fetchall()
        swChemicalExemptionType = cur.execute('''select distinct swChemicalExemptionType
                                            from [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                                            where cYear = ''' + str(cYear) + ''' and swChemicalExemptionType <> "None" and 
                                            countryCode = "''' + country + '''";''').fetchall()
        for country in countryCode:
            for chgroup in swChemicalExemptionTypeGroup:
                for chtype in swChemicalExemptionType:
                    tempgroup = ','.join(chgroup)
                    temptype = ','.join(chtype)
                    sqlDropValues = '''DROP TABLE IF EXISTS DistinctValues;'''

                    sqlValues = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euSurfaceWaterBodyCode,surfaceWaterBodyCategory,
                                                                    swChemicalExemptionTypeGroup, swChemicalExemptionType,
                                                                 cArea AS A
                                                   FROM [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                                                  WHERE cYear = ''' + str(cYear) + ''' AND 
                                                        countryCode = "''' + country + '''" AND                                              
                                                        swEcologicalStatusOrPotentialValue <> "Unknown" and
                                                        naturalAWBHMWB <> "Unpopulated" AND 
                                                        swChemicalStatusValue <> "Unpopulated" AND 
                                                        swChemicalExemptionTypeGroup = "''' + tempgroup + '''" AND 
                                                        swChemicalExemptionType = "''' + temptype + '''";'''

                    sqlDropArea = '''DROP TABLE IF EXISTS DistinctArea;'''

                    sqlArea = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euSurfaceWaterBodyCode,surfaceWaterBodyCategory,swChemicalExemptionTypeGroup, swChemicalExemptionType, cArea as G
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                                    WHERE cYear = ''' + str(cYear) + ''' AND 
                                      countryCode = "''' + country + '''" AND 
                                      naturalAWBHMWB <> "Unpopulated" AND 
                                      swChemicalStatusValue <> "Unpopulated" AND 
                                      swChemicalExemptionTypeGroup = "''' + tempgroup + '''";'''

                    sqlexecute = '''SELECT countryCode,
                                   swChemicalExemptionTypeGroup,
                                   swChemicalExemptionType,
                                   (
                                       SELECT ROUND(SUM(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN A END) ) 
                                         FROM DistinctValues
                                   ),
                                   ROUND((
                                              SELECT SUM(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN A END) 
                                                FROM DistinctValues
                                          )
                            *             100.0 / (
                                                      SELECT sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN G END) 
                                                        FROM DistinctArea
                                                  )
                                   ) AS percent
                              FROM [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   countryCode = "''' + country + '''" AND 
                                   naturalAWBHMWB <> "Unpopulated" AND 
                                   swChemicalStatusValue <> "Unpopulated" AND 
                                   swChemicalExemptionTypeGroup = "''' + tempgroup + '''" AND 
                                   swChemicalExemptionType = "''' + temptype + '''" 
                             GROUP BY swChemicalExemptionTypeGroup,
                                      swChemicalExemptionType;'''

                    cur.execute(sqlDropValues)
                    cur.execute(sqlValues)
                    cur.execute(sqlDropArea)
                    cur.execute(sqlArea)
                    data = cur.execute(sqlexecute).fetchall()

                    write.writerows(data)


def Surface_water_bodies_Quality_element_exemptions_Type(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_QE_qeEcologicalExemptionType/SWB_QE_qeEcologicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '6.Surface_water_bodies_Quality_element_exemptions_Type' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quality Element Exemption Type Group", "Quality Element Exemption Type", "Number",
                  "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        country = ','.join(countryCode)
        swEcologicalExemptionTypeGroup = cur.execute('''select distinct qeEcologicalExemptionTypeGroup 
                                                    from [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType]
                                                    where countryCode = "''' + country + '''" and 
                                                    qeEcologicalExemptionTypeGroup is not Null AND
                                                    qeEcologicalExemptionTypeGroup != "None";''').fetchall()

        for country in countryCode:
            for temp in swEcologicalExemptionTypeGroup:
                values = ','.join(temp)
                data = cur.execute('''SELECT countryCode,
                                   cYear,
                                   qeEcologicalExemptionTypeGroup,
                                   qeEcologicalExemptionType,
                                   count(DISTINCT euSurfaceWaterBodyCode),
                                   round(count(DISTINCT euSurfaceWaterBodyCode) * 100.0 / (
                                                              SELECT count(DISTINCT euSurfaceWaterBodyCode) 
                                                                FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType]
                                                               WHERE cYear = 2022 AND 
                                                                     countryCode = "''' + country + '''" AND 
                                                                     qeEcologicalExemptionTypeGroup = "''' + values + '''"
                                                          ), 1) 
                              FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType]
                             WHERE cYear = 2022 AND 
                                   qeEcologicalExemptionTypeGroup <> "None" AND 
                                   countryCode = "''' + country + '''" AND 
                                   qeEcologicalExemptionTypeGroup = "''' + values + '''"
                             GROUP BY qeEcologicalExemptionType;''').fetchall()
                write.writerows(data)


def gwChemical_Exemption_Type(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_GWB_GWP_GWChemicalExemptionType/GWB_GWP_GWChemicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '7.gwChemical_Exemption_Type' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Chemical Exemption Type Group", "Chemical Exemption Type", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        gwChemicalExemptionTypeGroup = cur.execute('''select distinct gwChemicalExemptionTypeGroup
                                                        from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                                                        where gwChemicalExemptionTypeGroup <> "Unpopulated"
                                                        and gwChemicalExemptionTypeGroup <> "GWD Article 6(3)"
                                                        and gwChemicalExemptionTypeGroup <> "Article4(6)"
                                                        and gwChemicalExemptionTypeGroup <> "Article4(7)"
                                                        and gwChemicalExemptionTypeGroup is not Null;
                                        ''').fetchall()

        gwChemicalExemptionType = cur.execute('''select distinct gwChemicalExemptionType
                                                from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                                                where gwChemicalExemptionType <> "Unpopulated" AND
                                                gwChemicalExemptionType <> "GWD Article 6(3) - Measures: increased risk" AND
                                                gwChemicalExemptionType <> "GWD Article 6(3) - Measures: disproportionate cost" and
                                                gwChemicalExemptionType <> "Missing";''').fetchall()

        for country in countryCode:
            for chgroup in gwChemicalExemptionTypeGroup:
                for chtype in gwChemicalExemptionType:
                    tempgroup = ','.join(chgroup)
                    temptype = ','.join(chtype)
                    sqlDropValues = '''DROP TABLE IF EXISTS DistinctValues;'''

                    sqlDistinct = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euGroundWaterBodyCode,
                                                             cArea AS A
                                               FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                                              WHERE cYear = ''' + str(cYear) + ''' AND 
                                                    countryCode = "''' + country + '''" AND 
                                                    gwChemicalStatusValue <> "2" AND 
                                                    gwChemicalStatusValue <> "Missing" AND 
                                                    gwChemicalStatusValue <> "unpopulated" AND 
                                                    gwChemicalExemptionTypeGroup = "''' + tempgroup + '''" AND 
                                                    gwChemicalExemptionType = "''' + temptype + '''";
                    '''

                    sqlDropArea = '''DROP TABLE IF EXISTS DistinctArea;'''

                    sqlArea = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euGroundWaterBodyCode,
                                                       cArea AS G
                                         FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                                        WHERE cYear = ''' + str(cYear) + ''' AND 
                                              countryCode = "''' + country + '''" AND 
                                              gwChemicalStatusValue <> "2" AND 
                                              gwChemicalStatusValue <> "Missing" AND 
                                              gwChemicalStatusValue <> "unpopulated" AND 
                                              gwChemicalExemptionTypeGroup <> "Unpopulated" AND 
                                              gwChemicalExemptionTypeGroup <> "GWD Article 6(3)" AND 
                                              gwChemicalExemptionTypeGroup <> "Article4(6)" AND 
                                              gwChemicalExemptionTypeGroup <> "Article4(7)" AND
                                              gwChemicalStatusValue <> "unpopulated" AND 
                                              gwChemicalExemptionTypeGroup = "''' + tempgroup + '''";
                    '''

                    sqlFinal = '''SELECT countryCode,
                                   gwChemicalExemptionTypeGroup,
                                   gwChemicalExemptionType,
                                   (
                                       SELECT ROUND(SUM(A) ) 
                                         FROM DistinctValues
                                   ),
                                   ROUND( (
                                              SELECT sum(A) 
                                                FROM DistinctValues
                                          )
                            *             100.0 / (
                                                      SELECT sum(G) 
                                                        FROM DistinctArea
                                                  )
                                   ) AS percent
                              FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   countryCode = "''' + country + '''" AND 
                                   gwChemicalStatusValue <> "2" AND 
                                   gwChemicalStatusValue <> "Missing" AND 
                                   gwChemicalStatusValue <> "unpopulated" AND 
                                   gwChemicalExemptionTypeGroup = "''' + tempgroup + '''" AND 
                                   gwChemicalExemptionType = "''' + temptype + '''"
                             GROUP BY gwChemicalExemptionTypeGroup,
                                      gwChemicalExemptionType;
                                '''

                    cur.execute(sqlDropValues)
                    cur.execute(sqlDistinct)
                    cur.execute(sqlDropArea)
                    cur.execute(sqlArea)
                    data = cur.execute(sqlFinal).fetchall()

                    write.writerows(data)


def gwChemical_exemptions_and_pressures(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_GWB_GWP_GWChemicalExemptionPressure/GWB_GWP_GWC_gwChemicalExemptionPressure?:isGuestRedirectFromVizportal=y&:embed=y
    with open(
            working_directory + '7.gwChemical_exemptions_and_pressures' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Exemption Type Group", "Chemical Exemption Type",
                  "Chemical Pressure Type Group", "Chemical Pressure Type", "Area (km^2)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()

        gwChemicalExemptionTypeGroup = cur.execute('''select distinct gwChemicalExemptionTypeGroup 
                    from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType] where gwChemicalExemptionTypeGroup is not Null;''').fetchall()
        gwChemicalExemptionType = cur.execute('''select distinct gwChemicalExemptionType 
                    from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                    where gwChemicalExemptionType <> "Missing"''').fetchall()
        gwChemicalExemptionPressureTypeGroup = cur.execute('''select distinct gwChemicalExemptionPressureGroup 
                                    from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType] where gwChemicalExemptionPressureGroup is not Null''').fetchall()
        gwChemicalExemptionPressureType = cur.execute('''select distinct gwChemicalExemptionPressure 
                    from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType] where gwChemicalExemptionPressure is not null''').fetchall()
        for country in countryCode:
            for cetg in gwChemicalExemptionTypeGroup:
                for cet in gwChemicalExemptionType:
                    for ceptg in gwChemicalExemptionPressureTypeGroup:
                        for cept in gwChemicalExemptionPressureType:
                            ChemicalExemption = ','.join(cet)
                            ChemicalExemptionGroup = ','.join(cetg)
                            ChemicalExemptionPressure = ','.join(cept)
                            ChemicalExemptionPressureGroup = ','.join(ceptg)

                            data = cur.execute('''select countryCode, cYear, gwChemicalExemptionTypeGroup,
                                                          gwChemicalExemptionType, 
                                                          gwChemicalExemptionPressureGroup, 
                                                          gwChemicalExemptionPressure,
                                                          round(sum(cArea))
                                                from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                                                where countryCode = "''' + country + '''" and 
                                                gwChemicalExemptionTypeGroup = "''' + ChemicalExemptionGroup + '''" and
                                                gwChemicalExemptionType = "''' + ChemicalExemption + '''" and
                                                gwChemicalExemptionPressure = "''' + ChemicalExemptionPressure + '''" and
                                                gwChemicalExemptionPressureGroup = "''' + ChemicalExemptionPressureGroup + '''"
                                                ''').fetchall()
                            write.writerows(data)


def generate_quantitivetypeandpressure_table(conn):
    cur = conn.cursor()

    droptable = '''DROP TABLE IF EXISTS [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionTypePressure];'''

    createtable = '''CREATE TABLE [GWB_GroundWaterBody_gwQuantitativeExemptionTypePressure] (
                        cYear                                       INTEGER,
                        fileUrl                                     VARCHAR (1000),
                        countryCode                                 VARCHAR (2),
                        countryName                                 VARCHAR (31),
                        euRBDCode                                   VARCHAR (42),
                        rbdName                                     VARCHAR (254),
                        GwbID                                       INTEGER,
                        wiseEvolutionType                           VARCHAR (254),
                        groundWaterBodyName                         VARCHAR (254),
                        cArea                                       REAL (18, 3),
                        euGroundWaterBodyCode                       VARCHAR (42),
                        linkSurfaceWaterBody                        VARCHAR (300),
                        linkTerrestrialEcosystem                    VARCHAR (300),
                        geologicalFormation                         VARCHAR (300),
                        groundwaterBodyTransboundary                VARCHAR (300),
                        gwSignificantPressureOther                  VARCHAR (1000),
                        gwSignificantImpactOther                    VARCHAR (1000),
                        gwAtRiskQuantitative                        VARCHAR (300),
                        gwEORiskQuantitative                        VARCHAR (300),
                        gwQuantitativeStatusValue                   VARCHAR (400),
                        gwQuantitativeAssessmentYear                VARCHAR (10),
                        gwQuantitativeAssessmentConfidence          VARCHAR (400),
                        gwQuantitativeStatusExpectedAchievementDate VARCHAR (300),
                        gwAtRiskChemical                            VARCHAR (300),
                        gwEORiskChemical                            VARCHAR (300),
                        gwChemicalStatusValue                       VARCHAR (400),
                        gwChemicalAssessmentYear                    VARCHAR (10),
                        gwChemicalAssessmentConfidence              VARCHAR (400),
                        gwChemicalStatusExpectedAchievementDate     VARCHAR (300),
                        GroundwaterbodyID                           INTEGER,
                        gwQuantitativeExemptionTypeID               INTEGER,
                        gwQuantitativeExemptionPressure             VARCHAR (300),
                        gwQuantitativeExemptionPressureGroup        VARCHAR (400),
                        gwQuantitativeExemptionType                 VARCHAR (300),
                        gwQuantitativeExemptionTypeGroup            VARCHAR (400) 
                    );'''

    insertintotable = '''INSERT INTO [GWB_GroundWaterBody_gwQuantitativeExemptionTypePressure] SELECT [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].cYear,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].fileUrl,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].countryCode,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].countryName,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].euRBDCode,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].rbdName,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].GwbID,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].wiseEvolutionType,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].groundWaterBodyName,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].cArea,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].euGroundWaterBodyCode,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].linkSurfaceWaterBody,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].linkTerrestrialEcosystem,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].geologicalFormation,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].groundwaterBodyTransboundary,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwSignificantPressureOther,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwSignificantImpactOther,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwAtRiskQuantitative,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwEORiskQuantitative,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeStatusValue,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeAssessmentYear,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeAssessmentConfidence,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeStatusExpectedAchievementDate,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwAtRiskChemical,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwEORiskChemical,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwChemicalStatusValue,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwChemicalAssessmentYear,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwChemicalAssessmentConfidence,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwChemicalStatusExpectedAchievementDate,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].GroundwaterbodyID,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeExemptionTypeID,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionPressure].gwQuantitativeExemptionPressure,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionPressure].gwQuantitativeExemptionPressureGroup,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeExemptionType,
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].gwQuantitativeExemptionTypeGroup
                     FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType]
                          JOIN
                          [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionPressure] ON [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionPressure].GroundwaterbodyID = [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType].GroundwaterbodyID;'''

    cur.execute(droptable)
    cur.execute(createtable)
    cur.execute(insertintotable)

def update_SWB_SurfaceWaterBody_SWEcologicalExemptionType_values(conn):
    cur = conn.cursor()

    updateValues = '''UPDATE [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                            SET swEcologicalExemptionType = 
                            CASE WHEN swEcologicalExemptionType IS NULL THEN 'Article4(6) - Force Majeure' END;'''

    cur.execute(updateValues)

def gwQuantitiveTypeAndPressure(working_directory, conn, countryCode, cYear):
    headers = ["Country", "Year", "Quantitative Exemption Type Group", "Quantitative Exemption Type",
               "Quantitative Exemption Pressure Group",
               "Quantitative Exemption Pressure", "Area (km^2)"]
    with open(
            working_directory + '7.gwQuantitiveTypeAndPressure' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        country = ','.join(countryCode)
        cur = conn.cursor()
        sql = cur.execute('''SELECT countryCode,
                       cYear,
                       gwQuantitativeExemptionTypeGroup,
                       gwQuantitativeExemptionType,
                       gwQuantitativeExemptionPressureGroup,
                       gwQuantitativeExemptionPressure,
                       round(sum(cArea) ) 
                  FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionTypePressure]
                 WHERE countryCode = "''' + country + '''"
                 GROUP BY gwQuantitativeExemptionTypeGroup,
                          gwQuantitativeExemptionType,
                          gwQuantitativeExemptionPressureGroup,
                          gwQuantitativeExemptionPressure;''').fetchall()

        write.writerows(sql)


def Surface_water_bodies_Ecological_status_or_potential_groupGood(working_directory, conn, countryCode, cYear):
    headers = ["Country", "Year", "Number", "Number(%)", "Length (km)", "Length (%)", "Area (km^2)", "Area(%)"]
    with open(
            working_directory + '8.Surface_water_bodies_Ecological_status_or_potential_groupGood' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            sql = '''SELECT countryCode,
                       cYear,
                       count(swEcologicalStatusOrPotentialValue),
                       round(count(swEcologicalStatusOrPotentialValue) * 100.0 / (
                                             SELECT count(swEcologicalStatusOrPotentialValue) 
                                               FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                              WHERE countryCode = "''' + country + '''" AND 
                                                    cYear = ''' + str(cYear) + ''' AND 
                                                    swEcologicalStatusOrPotentialValue <> "Inapplicable" and
                                                    swEcologicalStatusOrPotentialValue <> "Unknown" AND 
                                                    swEcologicalStatusOrPotentialValue <> "Other" AND 
                                                    surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                    naturalAWBHMWB <> "Unknown" AND 
                                                    naturalAWBHMWB <> "Unpopulated"
                                         ), 1),
                       round(sum(CASE WHEN surfaceWaterBodyCategory = "RW" THEN cLength END) ),
                       round(sum(CASE WHEN surfaceWaterBodyCategory = "RW" THEN cLength END) * 100.0 / (
                                           SELECT sum(CASE WHEN surfaceWaterBodyCategory = "RW" THEN cLength END) 
                                             FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                            WHERE countryCode = "''' + country + '''" AND 
                                                  cYear = ''' + str(cYear) + ''' AND 
                                                  swEcologicalStatusOrPotentialValue <> "Other" AND 
                                                  swEcologicalStatusOrPotentialValue <> "Inapplicable" and
                                                  swEcologicalStatusOrPotentialValue <> "Unknown" AND 
                                                  surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                  naturalAWBHMWB <> "Unknown" AND 
                                                  naturalAWBHMWB <> "Unpopulated"
                                       ), 1),
                       round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) ),
                       round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) * 100.0 / (
                                      SELECT sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) 
                                        FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                       WHERE countryCode = "''' + country + '''" AND 
                                             cYear = ''' + str(cYear) + ''' AND 
                                             swEcologicalStatusOrPotentialValue <> "Inapplicable" and
                                             swEcologicalStatusOrPotentialValue <> "Unknown" AND 
                                             swEcologicalStatusOrPotentialValue <> "Other" AND 
                                             surfaceWaterBodyCategory <> "Unpopulated" AND 
                                             naturalAWBHMWB <> "Unknown" AND 
                                             naturalAWBHMWB <> "Unpopulated"
                                  ), 1) 
                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                 WHERE swEcologicalStatusOrPotentialValue IN ("1", "2") AND 
                       countryCode = "''' + country + '''" AND 
                       cYear = ''' + str(cYear) + ''' AND 
                       swEcologicalStatusOrPotentialValue <> "Other" AND 
                       surfaceWaterBodyCategory <> "Unpopulated" AND 
                       naturalAWBHMWB <> "Unknown" AND 
                       naturalAWBHMWB <> "Unpopulated";'''

            data = cur.execute(sql).fetchall()

            write.writerows(data)


def swEcologicalStatusOrPotential_by_Category(working_directory, conn, countryCode, cYear):
    headers = ["Country", "Year", "Surface Water Body Category", "Ecological Status Or Potential Value", "Number"]
    with open(
            working_directory + '8.swEcologicalStatusOrPotential_by_Category' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        WDFCode = ["RW", "LW", "TW", "CW", "TeW"]
        swEcologicalStatusOrPotentialValue = ["1", "2", "3", "4", "5", "Unknown"]
        cur = conn.cursor()

        for country in countryCode:
            for category in WDFCode:
                for value in swEcologicalStatusOrPotentialValue:
                    data = cur.execute('''select countryCode, cYear, surfaceWaterBodyCategory, swEcologicalStatusOrPotentialValue, 
                                    COUNT(surfaceWaterBodyCategory) 
                                    from [WFD2022extract.SWB_SurfaceWaterBody] 
                                    where cYear = "''' + str(cYear) + '''" and countryCode = "''' + country + '''" 
                                    and surfaceWaterBodyCategory <> "unpopulated" 
                                    and surfaceWaterBodyCategory = "''' + category + '''" 
                                    and swEcologicalStatusOrPotentialValue = "''' + value + '''" ''')
                    write.writerows(data)


def Surface_water_bodies_Ecological_status_or_potential_groupFailing(working_directory, conn, countryCode, cYear):
    headers = ["Country", "Year", "Number", "Number(%)", "Length (km)", "Length (%)", "Area (km^2)", "Area (%)"]
    with open(
            working_directory + '8.Surface_water_bodies_Ecological_status_or_potential_groupFailing' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            sql = '''SELECT countryCode,
                       cYear,
                       count(swEcologicalStatusOrPotentialValue),
                       round(count(swEcologicalStatusOrPotentialValue) * 100.0 / (
                                 SELECT count(swEcologicalStatusOrPotentialValue) 
                                   FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                  WHERE countryCode = "''' + country + '''" AND 
                                        cYear = ''' + str(cYear) + ''' AND 
                                        swEcologicalStatusOrPotentialValue <> "Inapplicable" and
                                        swEcologicalStatusOrPotentialValue <> "Unknown" AND
                                        swEcologicalStatusOrPotentialValue <> "Other" AND 
                                        surfaceWaterBodyCategory <> "Unpopulated" AND 
                                        naturalAWBHMWB <> "Unknown" AND 
                                        naturalAWBHMWB <> "Unpopulated"
                             ), 1),
                       round(sum(CASE WHEN surfaceWaterBodyCategory = "RW" THEN cLength END) ),
                       round(sum(CASE WHEN surfaceWaterBodyCategory = "RW" THEN cLength END) * 100.0 / (
                                   SELECT sum(CASE WHEN surfaceWaterBodyCategory = "RW" THEN cLength END) 
                                     FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                    WHERE countryCode = "''' + country + '''" AND 
                                          cYear = ''' + str(cYear) + ''' AND 
                                          swEcologicalStatusOrPotentialValue <> "Inapplicable" and
                                         swEcologicalStatusOrPotentialValue <> "Unknown" AND 
                                          swEcologicalStatusOrPotentialValue <> "Other" AND 
                                          surfaceWaterBodyCategory <> "Unpopulated" AND 
                                          naturalAWBHMWB <> "Unknown" AND 
                                          naturalAWBHMWB <> "Unpopulated"
                               ), 3),
                       round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) ),
                       round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) * 100.0 / (
                                  SELECT sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) 
                                    FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                   WHERE countryCode = "''' + country + '''" AND 
                                         cYear = ''' + str(cYear) + ''' AND 
                                         swEcologicalStatusOrPotentialValue <> "Other" AND 
                                         swEcologicalStatusOrPotentialValue <> "Inapplicable" and
                                         swEcologicalStatusOrPotentialValue <> "Unknown" AND 
                                         surfaceWaterBodyCategory <> "Unpopulated" AND 
                                         naturalAWBHMWB <> "Unknown" AND 
                                         naturalAWBHMWB <> "Unpopulated"
                              ), 1) 
                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                 WHERE swEcologicalStatusOrPotentialValue IN ("3", "4","5") AND 
                       countryCode = "''' + country + '''" AND 
                       cYear = ''' + str(cYear) + ''' AND 
                       swEcologicalStatusOrPotentialValue <> "Other" AND 
                       surfaceWaterBodyCategory <> "Unpopulated" AND 
                       naturalAWBHMWB <> "Unknown" AND 
                       naturalAWBHMWB <> "Unpopulated";'''

            data = cur.execute(sql).fetchall()

            write.writerows(data)


def swEcologicalStatusOrPotential_Unknown_Category(working_directory, conn, countryCode, cYear):
    headers = ["Country", "Year", "Surface Water Body Category", "Ecological Status Or Potential Value", "Number"]
    with open(
            working_directory + '9.swEcologicalStatusOrPotential_Unknown_Category' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        WDFCode = ["RW", "LW", "TW", "CW"]
        for country in countryCode:
            for code in WDFCode:
                sql = '''select countryCode, cYear, surfaceWaterBodyCategory, swEcologicalStatusOrPotentialValue, 
                                            COUNT(surfaceWaterBodyCategory) 
                                            from [WFD2022extract.SWB_SurfaceWaterBody] 
                                            where cYear = "''' + str(cYear) + '''" and 
                                            countryCode = "''' + country + '''"
                                            and surfaceWaterBodyCategory <> "unpopulated" 
                                            and surfaceWaterBodyCategory = "''' + code + '''" 
                                            and swEcologicalStatusOrPotentialValue = "Unknown" '''

                data = cur.execute(sql).fetchall()

                write.writerows(data)


def SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Surface Water Body Category', 'Chemical Status Value', 'Number', 'Number(%)']
    with open(
            working_directory + '10.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        WDFCode = ["RW", "LW", "TW", "CW", "TeW"]
        chemicalStatus = ["2", "3", "Unknown"]
        for country in countryCode:
            for wdf in WDFCode:
                for status in chemicalStatus:
                    sql = '''SELECT DISTINCT countryCode,
                                cYear,
                                surfaceWaterBodyCategory,
                                swChemicalStatusValue,
                                COUNT(swChemicalStatusValue),
                                round(COUNT(swChemicalStatusValue) * 100.0 / (
                                                 SELECT count(swChemicalStatusValue) 
                                                   FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                  WHERE cYear = ''' + str(cYear) + ''' AND 
                                                        countryCode = "''' + country + '''" AND 
                                                        swChemicalStatusValue <> "Unpopulated" AND 
                                                        surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                        surfaceWaterBodyCategory = "''' + wdf + '''"
                                             ), 1) 
                                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                 WHERE cYear = ''' + str(cYear) + ''' AND 
                                       swChemicalStatusValue = "''' + status + '''" AND 
                                       swChemicalStatusValue <> "Unpopulated" AND 
                                       surfaceWaterBodyCategory <> "Unpopulated" AND 
                                       countryCode = "''' + country + '''" AND 
                                       surfaceWaterBodyCategory = "''' + wdf + '''";'''

                    data = cur.execute(sql).fetchall()

                    write.writerows(data)


def SurfaceWaterBody_ChemicalStatus_Table_by_Category(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Surface Water Body Category', 'Chemical Status Value', 'Number', 'Number(%)']
    with open(
            working_directory + '10.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        WDFCode = ["RW", "LW", "TW", "CW", "TeW"]
        chemicalStatus = ["2", "3", "Unknown"]
        for country in countryCode:
            for wdf in WDFCode:
                for status in chemicalStatus:
                    data = cur.execute('''SELECT DISTINCT countryCode,
                                                cYear,
                                                surfaceWaterBodyCategory,
                                                swChemicalStatusValue,
                                                COUNT(swChemicalStatusValue),
                                                round(COUNT(swChemicalStatusValue) * 100.0 / (
                                                                 SELECT count(swChemicalStatusValue) 
                                                                   FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                                  WHERE cYear = ? AND 
                                                                        countryCode = ? AND 
                                                                        swChemicalStatusValue <> "Unpopulated" AND 
                                                                        surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                        surfaceWaterBodyCategory = ?
                                                             ), 1) 
                                                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                 WHERE cYear = ? AND 
                                                       swChemicalStatusValue = ? AND 
                                                       swChemicalStatusValue <> "Unpopulated" AND 
                                                       surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                       countryCode = ? AND 
                                                       surfaceWaterBodyCategory = ?;
                                                    ''', (cYear, country, wdf, cYear, status, country, wdf)).fetchall()

                    write.writerows(data)


def surfaceWaterBodyChemicalStatusGood(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SurfaceWaterBody/SWB_ChemicalStatus?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Year', "Chemical Status Value", 'Number', 'Number(%)', 'Length (km)', 'Length(%)',
               'Area (km^2)', 'Area(%)']
    with open(
            working_directory + '10.surfaceWaterBodyChemicalStatusGood' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swChemicalStatusValue = ["2", "3"]
        for country in countryCode:
            for value in swChemicalStatusValue:
                data = cur.execute('''SELECT DISTINCT countryCode,
                                    cYear,
                                    swChemicalStatusValue,
                                    COUNT(swChemicalStatusValue),
                                    ROUND(COUNT(swChemicalStatusValue) * 100.0 / (
                                                                                     SELECT COUNT(swChemicalStatusValue) 
                                                                                       FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                                                      WHERE cYear = ? AND 
                                                                                            countryCode = ? AND 
                                                                                            swChemicalStatusValue <> "Unknown" AND 
                                                                                            swChemicalStatusValue <> "Unpopulated"
                                                                                 ), 1),
                                    ROUND(SUM(cLength), 0),
                                    ROUND(SUM(cLength) * 100.0 / (
                                                                     SELECT SUM(cLength) 
                                                                       FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                                      WHERE cYear == ? AND 
                                                                            countryCode = ? AND 
                                                                            swChemicalStatusValue <> "Unknown" AND 
                                                                            swChemicalStatusValue <> "Unpopulated"
                                                                 ), 1),
                                    ROUND(SUM(CASE WHEN surfaceWaterBodyCategory <> "RW"  AND cArea is not Null THEN cArea END), 0),
                                    ROUND(SUM(CASE WHEN surfaceWaterBodyCategory <> "RW"  AND cArea is not Null THEN cArea END) * 100.0 / (
                                                                   SELECT SUM(CASE WHEN surfaceWaterBodyCategory <> "RW"  AND cArea is not Null THEN cArea END) 
                                                                     FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                                    WHERE cYear = ? AND 
                                                                          countryCode = ? AND 
                                                                          swChemicalStatusValue <> "Unknown" AND 
                                                                          swChemicalStatusValue <> "Unpopulated"
                                                               ), 1) 
                      FROM [WFD2022extract.SWB_SurfaceWaterBody]
                     WHERE cYear = ? AND 
                           swChemicalStatusValue = ? AND 
                           swChemicalStatusValue <> "Unknown" AND 
                           swChemicalStatusValue <> "Unpopulated" AND 
                           surfaceWaterBodyCategory <> "Unpopulated" AND 
                           naturalAWBHMWB <> "Unpopulated" AND 
                           naturalAWBHMWB <> "Unknown" AND 
                           countryCode = ? ;
                ''', (cYear, country, cYear, country, cYear, country, cYear, value, country)).fetchall()

                write.writerows(data)


def swEcologicalStatusOrPotentialChemical_by_Country(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_Status_Compare/SWB_EcologicalStatus_Category?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '11.swEcologicalStatusOrPotential_by_Country' + str(cYear) + '.csv',
            'w+', newline='') as f:
        headers = ["Country", "Ecological Status Or Potential Value", "Number", "Number(%)"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode, swEcologicalStatusOrPotentialValue, 
                               COUNT(swEcologicalStatusOrPotentialValue), 
                               round(count(swEcologicalStatusOrPotentialValue) * 100.0 / ( 
                                       SELECT count(swEcologicalStatusOrPotentialValue) 
                                       FROM [WFD2022extract.SWB_SurfaceWaterBody] 
                                       WHERE cYear = ''' + str(cYear) + '''
                                       AND countryCode = "''' + country + '''" 
                                       AND naturalAWBHMWB <> "Unpopulated" 
                                       ), 1) 
                               FROM [WFD2022extract.SWB_SurfaceWaterBody] 
                               WHERE cYear = ''' + str(cYear) + ''' 
                               AND naturalAWBHMWB <> "Unpopulated" 
                               AND countryCode = "''' + country + '''"
                               GROUP BY swEcologicalStatusOrPotentialValue
            ''').fetchall()
            
            write.writerows(data)

    with open(
            working_directory + '11.swChemical_by_Country' + str(cYear) + '.csv',
            'w+', newline='') as f:
        headers = ["Country", "Chemical Status Value", "Number", "Number(%)"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('SELECT countryCode, swChemicalStatusValue, '
                               'COUNT(swChemicalStatusValue), '
                               'round(count(swChemicalStatusValue) * 100.0 / ( '
                               'SELECT count(swChemicalStatusValue) '
                               'FROM [WFD2022extract.SWB_SurfaceWaterBody] '
                               'WHERE cYear = ? '
                               'AND countryCode = ? '
                               'AND naturalAWBHMWB <> "Unpopulated" '
                               '), 1) '
                               'FROM [WFD2022extract.SWB_SurfaceWaterBody] '
                               'WHERE cYear = ? '
                               'AND naturalAWBHMWB <> "Unpopulated" '
                               'AND countryCode = ? '
                               'GROUP BY swChemicalStatusValue; '
                               , (cYear, country, cYear, country)).fetchall()
            
            write.writerows(data)


def swEcological_status_or_potential_and_chemical_status_by_category(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_Status/SWB_Status_Country?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '12.swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        headers = ['Country', 'Year', 'Categories', 'Ecological Status Value', 'Number', 'Number(%)']

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalStatusOrPotentialValue = ["1", "2", "3", "4", "5", "Unknown"]
        swEcologicalStatusCategories = ["RW", "LW", "CW", "TW", "TeW"]

        for country in countryCode:
            for categ in swEcologicalStatusCategories:
                for status in swEcologicalStatusOrPotentialValue:
                    data = cur.execute('''SELECT countryCode,
                                               cYear,
                                               surfaceWaterBodyCategory,
                                               swEcologicalStatusOrPotentialValue,
                                               round(count(surfaceWaterBodyCategory) ),
                                               round(count(surfaceWaterBodyCategory) * 100.0 / (
                                                           SELECT count(surfaceWaterBodyCategory) 
                                                             FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                            WHERE cYear = 2022 AND 
                                                                  countryCode = "''' + country + '''" AND 
                                                                  naturalAWBHMWB <> "Unpopulated" AND 
                                                                  surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                  surfaceWaterBodyCategory = "''' + categ + '''"
                                                       )
                                           ) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                     WHERE cYear = 2022 AND 
                                           countryCode = "''' + country + '''" AND 
                                           surfaceWaterBodyCategory <> "Unpopulated" AND 
                                           swEcologicalStatusOrPotentialValue = "''' + status + '''" AND 
                                           naturalAWBHMWB <> "Unpopulated" AND 
                                           surfaceWaterBodyCategory = "''' + categ + '''";''').fetchall()
                    write.writerows(data)
    with open(
            working_directory + '12.swChemicalStatusValue_by_Country_by_Categ' + str(cYear) + '.csv',
            'w+', newline='') as f:
        headers = ['Country', 'Year', 'Categories', 'Chemical Status Value', 'Number', 'Number(%)']

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swChemicalStatusValue = ["2", "3", "Unknown"]
        swEcologicalStatusCategories = ["RW", "LW", "CW", "TW", "TeW"]

        for country in countryCode:
            for categ in swEcologicalStatusCategories:
                for status in swChemicalStatusValue:
                    data = cur.execute('''SELECT countryCode,
                                                   cYear,
                                                   surfaceWaterBodyCategory,
                                                   swChemicalStatusValue,
                                                   round(count(surfaceWaterBodyCategory) ),
                                                   round(count(surfaceWaterBodyCategory) * 100.0 / (
                                                                         SELECT count(surfaceWaterBodyCategory) 
                                                                           FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                                          WHERE cYear = ? AND 
                                                                                countryCode = ? and
                                                                                naturalAWBHMWB <> "Unpopulated" AND 
                                                                                surfaceWaterBodyCategory <> "Unpopulated" and
                                                                                surfaceWaterBodyCategory = ?
                                                                     )
                                                           )
                                                      FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                     WHERE cYear = ? AND 
                                                           countryCode = ? AND 
                                                           surfaceWaterBodyCategory <> "Unpopulated" AND
                                                           swChemicalStatusValue = ? and
                                                           naturalAWBHMWB <> "Unpopulated" AND 
                                                           surfaceWaterBodyCategory = ?
                                                           '''
                                       , (cYear, country, categ, cYear, country, status, categ)).fetchall()
                    write.writerows(data)


def Groundwater_bodies_quantitative_status(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '13.Groundwater_bodies_quantitative_status' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Area (km^2)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        QuantitativeStatus = ["2", "3", "Unknown"]
        for country in countryCode:
            for status in QuantitativeStatus:
                data = cur.execute('SELECT DISTINCT countryCode, cYear, gwQuantitativeStatusValue, '
                                   'ROUND(SUM(cArea)), count(distinct euGroundWaterBodyCode) '
                                   'FROM [WFD2022extract.GWB_GroundWaterBody] '
                                   'WHERE countryCode = ? '
                                   'and gwQuantitativeStatusValue = ? '
                                   'and cYear == ?'
                                   , (country, status, cYear)).fetchall()
                write.writerows(data)


def GroundWaterBodyCategoryChemical_status(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '14.GroundWaterBodyCategoryChemical_status' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Area (km^2)", "Area (%)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        chemicalStatus = ["2", "3", "Unknown"]
        for country in countryCode:
            for status in chemicalStatus:
                data = cur.execute('''SELECT DISTINCT countryCode,
                                    cYear,
                                    gwChemicalStatusValue,
                                    ROUND(SUM(cArea), 0),
                                    round(sum(cArea) * 100.0 / (
                                                                   SELECT sum(cArea) 
                                                                     FROM [WFD2022extract.GWB_GroundWaterBody]
                                                                    WHERE countryCode = ? AND 
                                                                          cYear = ?
                                                               ),1
                                    ), count(distinct euGroundWaterBodyCode)
                                      FROM [WFD2022extract.GWB_GroundWaterBody]
                                     WHERE countryCode = ? AND 
                                           gwChemicalStatusValue = ? AND 
                                           cYear = ?;'''
                                   , (country, cYear, country, status, cYear)).fetchall()
                write.writerows(data)


def gwPollutant(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '15.gwPollutant' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Pollutant", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        for country in countryCode:
            drop = '''DROP TABLE IF EXISTS tempValues;'''

            temp = '''CREATE TEMPORARY TABLE tempValues AS SELECT DISTINCT groundWaterBodyName,
                                                             cArea AS Area
                                               FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant]
                                              WHERE countryCode = "''' + country + '''"; '''

            sql = '''SELECT countryCode,
                       cYear,
                       gwPollutantCode,
                       round(sum(cArea)),
                       round(sum(cArea) * 100.0 / (
                                                SELECT sum(Area) 
                                                  FROM tempValues
                                            ))
                  FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant]
                 WHERE countryCode = "''' + country + '''" and 
                    gwPollutantCode is not Null
                 GROUP BY gwPollutantCode;'''

            cur.execute(drop)
            cur.execute(temp)
            data = cur.execute(sql).fetchall()

            write.writerows(data)


def gwPollutantOther(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '15.gwPollutantOther' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Pollutant reported as 'Other'", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        for country in countryCode:
            drop = '''DROP TABLE IF EXISTS tempValues;'''

            temp = '''CREATE TEMPORARY TABLE tempValues AS SELECT DISTINCT groundWaterBodyName,
                                                             cArea AS Area
                                               FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant]
                                              WHERE countryCode = "''' + country + '''"; '''

            sql = '''SELECT countryCode,
                       cYear,
                       gwPollutantOther,
                       round(sum(cArea)),
                       round(sum(cArea) * 100.0 / (
                                                SELECT sum(Area) 
                                                  FROM tempValues
                                            ))
                  FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant]
                 WHERE countryCode = "''' + country + '''" and 
                    gwPollutantOther is not Null
                 GROUP BY gwPollutantOther;'''

            cur.execute(drop)
            cur.execute(temp)
            data = cur.execute(sql).fetchall()

            write.writerows(data)


def gwChemical_status(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '16.gwChemical_status' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        chemicalStatus = ["2", "3", "Unknown"]
        for country in countryCode:
            for status in chemicalStatus:
                data = cur.execute('''SELECT DISTINCT countryCode,
                                    cYear,
                                    gwChemicalStatusValue,
                                    ROUND(SUM(cArea), 0),
                                    round(sum(cArea) * 100.0 / (
                                                                   SELECT sum(cArea) 
                                                                     FROM [WFD2022extract.GWB_GroundWaterBody]
                                                                    WHERE countryCode = ? AND 
                                                                          cYear = ?
                                                               ),1
                                    ) 
                                      FROM [WFD2022extract.GWB_GroundWaterBody]
                                     WHERE countryCode = ? AND 
                                           gwChemicalStatusValue = ? AND 
                                           cYear = ?;'''
                                   , (country, cYear, country, status, cYear)).fetchall()
                write.writerows(data)


def gwQuantitativeStatusValue_gwChemicalStatusValue(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_Status/GWB_Status_Country?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '16.gwQuantitativeStatusValue_Percent_Country' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        gwQuantitativeStatusValue = ["2", "3", "Unknown"]
        for country in countryCode:
            for value in gwQuantitativeStatusValue:
                data = cur.execute(
                    'select countryCode,cYear, gwQuantitativeStatusValue, round(sum(cArea)), round(sum(cArea) * 100.0 / ('
                    'select sum(cArea) from [WFD2022extract.GWB_GroundWaterBody] '
                    'where cYear = ? and countryCode = ?)) '
                    'from [WFD2022extract.GWB_GroundWaterBody] '
                    'where cYear = ? '
                    'and countryCode = ?'
                    'and gwQuantitativeStatusValue = ? '
                    , (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)


def Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status(working_directory, conn, countryCode,
                                                                              cYear):
    with open(
            working_directory + '17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Area (km^2)", "Area(%)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                           cYear,
                           gwAtRiskQuantitative,
                           round(sum(cArea), 0),
                           round(sum(cArea) * 100 / (
                                            SELECT sum(cArea) 
                                              FROM [WFD2022extract.GWB_GroundWaterBody]
                                             WHERE countryCode = "''' + country + '''" AND 
                                                   cYear == ''' + str(cYear) + '''
                                        ), 1), count(distinct euGroundWaterBodyCode)
                      FROM [WFD2022extract.GWB_GroundWaterBody]
                     WHERE cYear == ''' + str(cYear) + ''' AND 
                           countryCode = "''' + country + '''"
                     GROUP BY gwAtRiskQuantitative;'''
                               ).fetchall()

            write.writerows(data)


def gwQuantitativeReasonsForFailure_Table(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '17.GWB_gwQuantitativeReasonsForFailure_Table' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Quantitative Reasons For Failure", "Area (km^2)",
                  "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        for country in countryCode:
            sql = '''SELECT countryCode,
                   cYear,
                   gwQuantitativeStatusValue,
                   gwQuantitativeReasonsForFailure,
                   round(sum(cArea)),
                   round(sum(cArea) * 100.0 / (
                                            SELECT sum(cArea) 
                                              FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeReasonsForFailure]
                                             WHERE gwQuantitativeStatusValue = 3 and
                                             countryCode = "''' + country + '''"
                                        ))
              FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeReasonsForFailure]
             WHERE gwQuantitativeStatusValue = 3 and countryCode = "''' + country + '''"
             GROUP BY gwQuantitativeReasonsForFailure;
            '''
        data = cur.execute(sql).fetchall()

        write.writerows(data)


def gwChemicalStatusValue_Table(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '22.gwChemicalStatusValue_Table' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        ChemicalStatusValue = ["No", "Yes"]
        cur = conn.cursor()
        for country in countryCode:
            for risk in ChemicalStatusValue:
                data = cur.execute('''SELECT countryCode,
                                       cYear,
                                       gwAtRiskChemical,
                                       round(sum(cArea), 0),
                                       round(sum(cArea) * 100 / (
                                                                    SELECT sum(cArea) 
                                                                      FROM [WFD2022extract.GWB_GroundWaterBody]
                                                                     WHERE countryCode = ? AND 
                                                                           cYear == ?
                                                                ), 0) 
                                  FROM [WFD2022extract.GWB_GroundWaterBody]
                                 WHERE cYear = ? AND 
                                       gwEORiskChemical <> "unpopulated" AND 
                                       gwEORiskChemical <> "Not in WFD2010" AND 
                                       gwAtRiskChemical <> "Not in WFD2010" AND 
                                       gwAtRiskChemical <> "unpopulated" AND 
                                       gwChemicalStatusValue <> "unpopulated" AND 
                                       countryCode = ? AND 
                                       gwAtRiskChemical = ?;
                '''
                                   , (country, cYear, cYear, country, risk)).fetchall()
                write.writerows(data)


def SOW_GWB_gwChemicalReasonsForFailure_Table(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '22.gwChemicalReasonsForFailure_Table' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Chemical Reasons For Failure", "Area (km^2)", "Area (%)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        ChemicalStatusValue = cur.execute('''select distinct gwChemicalReasonsForFailure 
                        from [WFD2022extract.GWB_GroundWaterBody_gwChemicalReasonsForFailure] where gwChemicalReasonsForFailure is not Null''').fetchall()

        for country in countryCode:
            for temp in ChemicalStatusValue:
                values = ','.join(temp)
                sqlDrop = '''DROP TABLE IF EXISTS Area;'''

                sqlArea = '''CREATE TEMPORARY TABLE Area AS SELECT DISTINCT euGroundWaterBodyCode,
                                               sum(DISTINCT cArea) as S
                                 FROM [WFD2022extract.GWB_GroundWaterBody_gwChemicalReasonsForFailure]
                                WHERE cYear = ''' + str(cYear) + ''' AND 
                                      countryCode = "''' + country + '''" AND 
                                      gwChemicalReasonsForFailure <> "Unpopulated" AND 
                                      gwChemicalStatusValue = "3";'''

                sqlFinal = '''SELECT countryCode,
                                   cYear,
                                   gwChemicalStatusValue,
                                   gwChemicalReasonsForFailure,
                                   round(sum(cArea), 0),
                                   round(sum(cArea) * 100 / (
                                                                select S from Area
                                                            ), 0),
                                    count(distinct euGroundWaterBodyCode)
                              FROM [WFD2022extract.GWB_GroundWaterBody_gwChemicalReasonsForFailure]
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   gwChemicalReasonsForFailure <> "Unpopulated" AND 
                                   gwChemicalStatusValue = "3" AND 
                                   countryCode = "''' + country + '''" AND 
                                   gwChemicalReasonsForFailure = "''' + values + '''";
                                            '''
                cur.execute(sqlDrop)
                cur.execute(sqlArea)
                data = cur.execute(sqlFinal).fetchall()

                write.writerows(data)


def gwQuantitativeAssessmentConfidence(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '27.gwQuantitativeAssessmentConfidence' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Assessment Confidence", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        gwQuantitativeAssessmentConfidence = ["High", "Medium", "Low", "Unknown"]
        cur = conn.cursor()
        for country in countryCode:
            for value in gwQuantitativeAssessmentConfidence:
                data = cur.execute(
                    'select countryCode, cYear, gwQuantitativeAssessmentConfidence, round(sum(cArea),0), '
                    'round(sum(cArea) * 100 / (select sum(cArea) '
                    'from [WFD2022extract.GWB_GroundWaterBody] where '
                    'cYear == ? and countryCode = ?),0) '
                    'from [WFD2022extract.GWB_GroundWaterBody] '
                    'where cYear == ? and countryCode = ? '
                    'and gwQuantitativeAssessmentConfidence <> "unpopulated" '
                    'and gwQuantitativeAssessmentConfidence = ? '
                    , (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)


def gwChemicalAssessmentConfidence(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '28.gwChemicalAssessmentConfidence' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Assessment Confidence", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        gwChemicalAssessmentConfidence = ["High", "Medium", "Low", "Unknown"]
        cur = conn.cursor()
        for country in countryCode:
            for value in gwChemicalAssessmentConfidence:
                data = cur.execute('select countryCode, cYear, gwChemicalAssessmentConfidence, round(sum(cArea),0), '
                                   'round(sum(cArea) * 100 / (select sum(cArea) '
                                   'from [WFD2022extract.GWB_GroundWaterBody] where '
                                   'cYear == ? and countryCode = ?),0) '
                                   'from [WFD2022extract.GWB_GroundWaterBody] '
                                   'where cYear == ? and countryCode = ? '
                                   'and gwChemicalAssessmentConfidence <> "unpopulated" '
                                   'and gwChemicalAssessmentConfidence = ? '
                                   , (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)


def geologicalFormation(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_GroundWaterBody/GWB_Category?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '29.GWB_geologicalFormation' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Geological Formation", "Area (km^2)"]
        write = csv.writer(f)
        write.writerow(header)
        geologicalFormation = ["Porous aquifers - highly productive", "Porous aquifers - moderately productive",
                               "Fissured aquifers including karst - highly productive",
                               "Fissured aquifers including karst - moderately productive",
                               "Fractured aquifers - highly productive", "Fractured aquifers - moderately productive"]
        cur = conn.cursor()
        for country in countryCode:
            for value in geologicalFormation:
                data = cur.execute('select countryCode, cYear, geologicalFormation, round(sum(cArea),0) '
                                   'from [WFD2022extract.GWB_GroundWaterBody] where '
                                   'geologicalFormation = ? '
                                   'and countryCode = ? '
                                   'and cYear == ? '
                                   'and gwQuantitativeStatusValue <> "Unknown" '
                                   'and geologicalFormation <> "Missing" '
                                   'and geologicalFormation <> "Unknown" '
                                   'and geologicalFormation <> "Insignificant aquifers - local and limited groundwater" '
                                   'and geologicalFormation <> "unpopulated" '
                                   'and countryCode = ? '
                                   , (value, country, cYear, country)).fetchall()
                write.writerows(data)


def gwQuantitativeStatusExpectedAchievementDate(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '24.gwQuantitativeStatusExpectedAchievementDate' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Expected Date", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        gwQuantitativeStatusExpectedAchievementDate = cur.execute('''select distinct gwQuantitativeStatusExpectedAchievementDate 
        from [WFD2022extract.GWB_GroundWaterBody]''').fetchall()

        for country in countryCode:
            for date in gwQuantitativeStatusExpectedAchievementDate:
                data = cur.execute(
                    'select countryCode, cYear, gwQuantitativeStatusExpectedAchievementDate, round(sum(cArea),0), round(sum(cArea) * 100 / '
                    '(select sum(cArea) from [WFD2022extract.GWB_GroundWaterBody] where countryCode = ? and cYear = ?),0) '
                    'from [WFD2022extract.GWB_GroundWaterBody] '
                    'where countryCode = ? and cYear == ? '
                    'and gwQuantitativeStatusExpectedAchievementDate <> "unpopulated" '
                    'and gwQuantitativeStatusExpectedAchievementDate = ? '
                    , (country, cYear, country, cYear, *date)).fetchall()
                write.writerows(data)


def gwChemicalStatusExpectedGoodIn2022(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '26.gwChemicalStatusExpectedGoodIn' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Good Chemical Status Expected Date", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                       cYear,
                       gwChemicalStatusExpectedAchievementDate,
                       round(sum(cArea), 1),
                       round(sum(cArea) * 100 / (
                                SELECT sum(cArea) 
                                  FROM [WFD2022extract.GWB_GroundWaterBody]
                                 WHERE cYear == ''' + str(cYear) + ''' AND 
                                       countryCode = "''' + country + '''"
                            ), 3) 
                  FROM [WFD2022extract.GWB_GroundWaterBody]
                 WHERE cYear == ''' + str(cYear) + ''' AND
                       countryCode = "''' + country + '''"
                 GROUP BY gwChemicalStatusExpectedAchievementDate;
            ''').fetchall()

            write.writerows(data)


def gwChemicalStatusExpectedAchievementDate(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '26.gwChemicalStatusExpectedAchievementDate' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Expected Achievement Date", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        gwQuantitativeStatusExpectedAchievementDate = cur.execute('''select distinct gwChemicalStatusExpectedAchievementDate 
        from [WFD2022extract.GWB_GroundWaterBody]''').fetchall()
        for country in countryCode:
            for date in gwQuantitativeStatusExpectedAchievementDate:
                data = cur.execute(
                    'select countryCode, cYear, gwChemicalStatusExpectedAchievementDate, round(sum(cArea),0), round(sum(cArea) * 100 / '
                    '(select sum(cArea) from [WFD2022extract.GWB_GroundWaterBody] where countryCode = ? and cYear = ?),0) '
                    'from [WFD2022extract.GWB_GroundWaterBody] '
                    'where countryCode = ? and cYear == ? '
                    'and gwChemicalStatusExpectedAchievementDate <> "unpopulated" '
                    'and gwChemicalStatusExpectedAchievementDate = ? '
                    , (country, cYear, country, cYear, *date)).fetchall()
                write.writerows(data)


def swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Assessment Confidence", "Chemical Monitoring Results", "Number",
                  "Number (%)"]
        write = csv.writer(f)
        write.writerow(header)
        AssessmentConfidence = ["High", "Medium", "Low", "Unknown"]
        MonitoringResult = ["Missing", "Expert judgement", "Monitoring", "Grouping"]
        cur = conn.cursor()
        for country in countryCode:
            for assessment in AssessmentConfidence:
                for monitoring in MonitoringResult:
                    data = cur.execute('select countryCode, cYear, '
                                       'swChemicalAssessmentConfidence, '
                                       'swChemicalMonitoringResults, '
                                       'CASE WHEN swChemicalAssessmentConfidence = "" THEN swChemicalAssessmentConfidence ELSE '
                                       'round(count(swChemicalAssessmentConfidence)) END, '
                                       'case when swChemicalAssessmentConfidence = "" then swChemicalAssessmentConfidence ELSE '
                                       'round(count(swChemicalAssessmentConfidence) * 100.0 / ( '
                                       'select count(swChemicalAssessmentConfidence) from [WFD2022extract.SWB_SurfaceWaterBody] '
                                       'where cYear == ? and countryCode = ? and swChemicalAssessmentConfidence = ?)) END '
                                       'from [WFD2022extract.SWB_SurfaceWaterBody] '
                                       'where cYear == ? '
                                       'and countryCode = ? '
                                       'and swChemicalAssessmentConfidence = ? '
                                       'and swChemicalMonitoringResults = ? '
                                       ,
                                       (cYear, country, assessment, cYear, country, assessment, monitoring)).fetchall()
                    write.writerows(data)


def Surface_water_bodies_River_basin_specific_pollutants(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_FailingRBSPOther/SWB_FailingRBSPOther?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '31.Surface_water_bodies_River_basin_specific_pollutants' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "River Basin Specific Pollutant", "Number", "Number (%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('select countryCode, cYear, swFailingRBSP, count(swFailingRBSP), '
                               'ROUND(count(swFailingRBSP) * 100.0 / ( '
                               'select count(swFailingRBSP) '
                               'from [WFD2022extract.SWB_SurfaceWaterBody_FailingRBSP] '
                               'where cYear = ? '
                               'and countryCode = ? '
                               'AND swFailingRBSP IS NOT NULL '
                               ')) '
                               'from [WFD2022extract.SWB_SurfaceWaterBody_FailingRBSP] '
                               'where cYear == ? '
                               'and countryCode = ? '
                               'AND swFailingRBSP IS NOT NULL '
                               'GROUP BY swFailingRBSP ORDER BY count(swFailingRBSP) DESC'
                               , (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_FailingRBSPOther/SWB_FailingRBSPOther?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Failing RBSP Other", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('select countryCode, cYear, swFailingRBSPOther, count(swFailingRBSPOther), '
                               'ROUND(count(swFailingRBSP) * 100.0 / ( '
                               'select count(swFailingRBSP) '
                               'from [WFD2022extract.SWB_SurfaceWaterBody_FailingRBSP] '
                               'where cYear = ? '
                               'and countryCode = ? '
                               'AND swFailingRBSPOther IS NOT NULL '
                               ')) '
                               'from [WFD2022extract.SWB_SurfaceWaterBody_FailingRBSP] '
                               'where cYear == ? '
                               'and countryCode = ? '
                               'AND swFailingRBSPOther IS NOT NULL '
                               'GROUP BY swFailingRBSPOther ORDER BY count(swFailingRBSP) DESC'
                               , (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def Surface_water_bodies_QE1__assessment(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '32.Surface_water_bodies_QE1_assessment' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from [WFD2022extract.SWB_SurfaceWaterBody_QualityElement] '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE1%" '
                             , (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                          SELECT count(euSurfaceWaterBodyCode) 
                                                                                            FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                                                                           WHERE countryCode = ? AND 
                                                                                                 cYear = ? and
                                                                                                 qeCode = ?
                                                                                      ), 0) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    '''
                                       , (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)


def Surface_water_bodies_QE2_assessment(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '32.Surface_water_bodies_QE2_assessment' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from [WFD2022extract.SWB_SurfaceWaterBody_QualityElement] '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE2%" '
                             , (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                          SELECT count(euSurfaceWaterBodyCode) 
                                                                                            FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                                                                           WHERE countryCode = ? AND 
                                                                                                 cYear = ? and
                                                                                                 qeCode = ?
                                                                                      ), 0) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    '''
                                       , (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)


def Surface_water_bodies_QE3_assessment(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '32.Surface_water_bodies_QE3_assessment' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from [WFD2022extract.SWB_SurfaceWaterBody_QualityElement] '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE3-1%" '
                             , (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                          SELECT count(euSurfaceWaterBodyCode) 
                                                                                            FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                                                                           WHERE countryCode = ? AND 
                                                                                                 cYear = ? and
                                                                                                 qeCode = ?
                                                                                      ), 0) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    '''
                                       , (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)


def Surface_water_bodies_QE3_3_assessment(working_directory, conn, countryCode, cYear):
    # https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '32.Surface_water_bodies_QE3_3_assessment' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from [WFD2022extract.SWB_SurfaceWaterBody_QualityElement] '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE3-3%" '
                             , (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                      SELECT count(euSurfaceWaterBodyCode) 
                                                        FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                                       WHERE countryCode = ? AND 
                                                             cYear = ? and
                                                             qeCode = ?
                                                  ), 0) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement]
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    '''
                                       , (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)


def swEcologicalStatusOrPotentialExpectedAchievementDate(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '34.swEcologicalStatusOrPotentialExpectedAchievementDate' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Ecological Status Or Potential Expected Achievement Date", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        country = ','.join(countryCode)
        swEcologicalStatusOrPotentialExpectedAchievementDate = cur.execute('''SELECT DISTINCT swEcologicalStatusOrPotentialExpectedAchievementDate 
                                            from [WFD2022extract.SWB_SurfaceWaterBody] 
                                            where swEcologicalStatusOrPotentialExpectedAchievementDate is not null and
                                            swEcologicalStatusOrPotentialExpectedAchievementDate != "None" AND
                                            countryCode = "''' + country + '''";''').fetchall()


        for country in countryCode:
            for temp in swEcologicalStatusOrPotentialExpectedAchievementDate:
                years = ','.join(temp)
                data = cur.execute('''SELECT countryCode,
                                       cYear,
                                       swEcologicalStatusOrPotentialExpectedAchievementDate,
                                       COUNT(euSurfaceWaterBodyCode),
                                       round(COUNT(euSurfaceWaterBodyCode) * 100.0 / (
                                                             SELECT COUNT(euSurfaceWaterBodyCode) 
                                                               FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                                              WHERE countryCode = ? AND 
                                                                    cYear = ? AND 
                                                                    naturalAWBHMWB <> "unpopulated" AND 
                                                                    swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                                                    swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                                    swEcologicalStatusOrPotentialExpectedAchievementDate <> "Unpopulated"
                                                         ), 0) AS PERCENT
                                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                 WHERE countryCode = ? AND 
                                        cYear = ? and
                                       naturalAWBHMWB <> "unpopulated" AND 
                                       swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                       swEcologicalStatusOrPotentialValue <> "Unpopulated" AND  
                                       swEcologicalStatusOrPotentialExpectedAchievementDate = ?;'''
                                   , (country, cYear, country, cYear, years)).fetchall()
                write.writerows(data)


def swChemicalStatusExpectedAchievementDate(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + '36.swChemicalStatusExpectedAchievementDate' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Expected Achievement Date", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        swChemicalStatusExpectedAchievementDate = cur.execute('''select distinct swChemicalStatusExpectedAchievementDate 
                                            from [WFD2022extract.SWB_SurfaceWaterBody] where swChemicalStatusExpectedAchievementDate is not null''').fetchall()

        for country in countryCode:
            for date in swChemicalStatusExpectedAchievementDate:
                data = cur.execute('select countryCode, cYear, swChemicalStatusExpectedAchievementDate, COUNT( '
                                   'swChemicalStatusExpectedAchievementDate), '
                                   'round(COUNT(swChemicalStatusExpectedAchievementDate) * 100.0 / '
                                   '(select COUNT(swChemicalStatusExpectedAchievementDate) '
                                   'from [WFD2022extract.SWB_SurfaceWaterBody] '
                                   'where countryCode = ? '
                                   'and cYear == ? '
                                   'and swChemicalStatusExpectedAchievementDate <> "Unpopulated"), 0) '
                                   'from [WFD2022extract.SWB_SurfaceWaterBody] '
                                   'where countryCode = ? '
                                   'and cYear == ? '
                                   'and swChemicalStatusExpectedAchievementDate <> "Unpopulated" '
                                   'and swChemicalStatusExpectedAchievementDate = ? '
                                   , (country, cYear, country, cYear, *date)).fetchall()
                write.writerows(data)


'''New dashboards'''


def swSignificant_Pressure_Type_Table_Overall(working_directory, conn, countryCode, cYear):
    headers = ['Significant Pressure Type Group', 'Significant Pressure Type', 'Countries', 'Number', 'Length (km)',
               'Area (km^2)', 'Categories']
    with open(
            working_directory + '101.swSignificant_Pressure_Type_Table_Overall' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT swSignificantPressureTypeGroup,
                       swSignificantPressureType,
                       count(DISTINCT countryCode),
                       count(euSubUnitCode),
                       CAST (round(sum(CASE WHEN surfaceWaterBodyCategory <> "TW" THEN cLength END),0 ) AS INT),
                       CAST (round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END),0 ) AS INT),
                       count(DISTINCT surfaceWaterBodyCategory) 
                  FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantPressureType]
                 WHERE cYear = ? AND 
                       swEcologicalStatusOrPotentialValue <> "inapplicable" and
                       surfaceWaterBodyCategory <> "Unpopulated"
                 GROUP BY swSignificantPressureTypeGroup,
                          swSignificantPressureType;'''
                           , (cYear,)).fetchall()
        write.writerows(data)


def swSignificantImpactType_Table_Overall(working_directory, conn, countryCode, cYear):
    headers = ['Significant Impact Type', 'Countries', 'Number of water bodies', 'Length (km)', 'Area (km^2)',
               'Categories']
    with open(
            working_directory + '102.swSignificantImpactType_Table_Overall' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        impactType = ["Chemical pollution", "Altered habitats due to morphological changes", "None",
                      "Nutrient pollution", "Organic pollution", "Altered habitats due to hydrological changes",
                      "Unknown", "Acidification", "Other", "Elevated temperatures", "Microbiological pollution",
                      "Saline or other intrusion", "Dependent terrestrial ecosystems", "Associated surface waters",
                      "Inapplicable", "Litter"]

        for type in impactType:
            cur = conn.cursor()
            data = cur.execute('''SELECT swSignificantImpactType,
                           COUNT(DISTINCT countryCode),
                           COUNT(euSurfaceWaterBodyCode),
                           CAST (ROUND(SUM(cLength),0 ) AS INT),
                           CAST (ROUND(SUM(case when surfaceWaterBodyCategory <> "RW" then cArea end), 0) AS INT),
                           count(DISTINCT surfaceWaterBodyCategory) 
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_swSignificantImpactType]
                     WHERE swSignificantImpactType = ? AND 
                           swSignificantImpactType <> "Unpopulated" AND 
                           surfaceWaterBodyCategory <> "Unpopulated" AND 
                           swSignificantImpactType <> "Unpopulated" AND 
                           swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                           swChemicalStatusValue <> "Unpopulated" AND 
                           cYear = ?
                     GROUP BY swSignificantImpactType;
            ''', (type, cYear)).fetchall()
            write.writerows(data)


def gwSignificant_Pressure_Overall(working_directory, conn, countryCode, cYear):
    headers = ['Significant Pressure Type Group', 'Significant Pressure Type', 'Countries', 'Number', 'Area (km^2)']
    with open(
            working_directory + '103.gwSignificant_Pressure_Overall' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT gwSignificantPressureTypeGroup,
                   gwSignificantPressureType,
                   count(DISTINCT countryCode),
                   count(euGroundWaterBodyCode),
                   CAST (round(sum(cArea),0) AS INT) 
                  FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantPressureType]
                 WHERE cYear = ? AND 
                 gwChemicalStatusValue <> "Unpopulated" AND
                 gwSignificantPressureTypeGroup <> "Unpopulated"
                 GROUP BY gwSignificantPressureTypeGroup,
                      gwSignificantPressureType;''', (cYear,)).fetchall()
        write.writerows(data)


def gwSignificant_Impact_Overall(working_directory, conn, countryCode, cYear):
    headers = ['Significant Impact Type', 'Countries', 'Number', 'Area (km^2)']
    with open(
            working_directory + '104.gwSignificant_Impact_Overall' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT gwSignificantImpactType,
                   count(DISTINCT countryCode),
                   count(euGroundWaterBodyCode),
                   CAST (round(sum(cArea),0 ) AS INT)
              FROM [WFD2022extract.GWB_GroundWaterBody_gwSignificantImpactType]
             WHERE cYear = ? AND 
             gwChemicalStatusValue <> "Unpopulated" and
             gwSignificantImpactType <> "Unpopulated"
             GROUP BY gwSignificantImpactType;''', (cYear,)).fetchall()
        write.writerows(data)


def sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Unchanged', 'Unchanged (%)']
    with open(
            working_directory + '109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode, cYear,
                               count(euSurfaceWaterBodyCode),
                               round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                     SELECT count(euSurfaceWaterBodyCode) 
                                       FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                      WHERE cYear = ? AND 
                                            countryCode = ?
                                 )
                               ) 
                              FROM [WFD2022extract.SWB_SurfaceWaterBody]
                             WHERE cYear = ? AND 
                               countryCode = ? AND 
                               wiseEvolutionType IN ("noChange", "changeCode", "change");''',
                               (cYear, country, cYear, country)).fetchall()
            write.writerows(data)

    headers = ['Country', 'Year', 'Other', 'Other (%)']
    with open(
            working_directory + '109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode, cYear,
                               count(euSurfaceWaterBodyCode),
                               round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                     SELECT count(euSurfaceWaterBodyCode) 
                                       FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                      WHERE cYear = ? AND 
                                            countryCode = ?
                                 )
                               ) 
                              FROM [WFD2022extract.SWB_SurfaceWaterBody]
                             WHERE cYear = ? AND 
                               countryCode = ? AND 
                               wiseEvolutionType not IN ("noChange", "changeCode", "change");''',
                               (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, cYear):
    headers = ['Category', 'Year', 'Evolution Type', 'Number', 'Number (%)']
    with open(
            working_directory + '109.2.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        surface_water_body_category = ["RW", "LW", "TW", "CW", "TeW"]
        cur = conn.cursor()
        country = ','.join(countryCode)
        for category in surface_water_body_category:
            data = cur.execute('''SELECT surfaceWaterBodyCategory, cYear, wiseEvolutionType,
                               count(euSurfaceWaterBodyCode),
                               round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                         SELECT count(euSurfaceWaterBodyCode) 
                                           FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                          WHERE cYear = ? AND 
                                          surfaceWaterBodyCategory = ? AND
                                          countryCode = "''' + country + '''"
                                     )
                               )
                              FROM [WFD2022extract.SWB_SurfaceWaterBody]
                             WHERE cYear = ? AND 
                               surfaceWaterBodyCategory = ? AND
                               countryCode = "''' + country + '''"
                               GROUP BY wiseEvolutionType;''', (cYear, category, cYear, category)).fetchall()

            write.writerows(data)


def sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Evolution Type', 'Number', 'Number (%)']
    with open(
            working_directory + '109.3.sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode, cYear, wiseEvolutionType,
                               count(euSurfaceWaterBodyCode),
                               round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                         SELECT count(euSurfaceWaterBodyCode) 
                                           FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                          WHERE cYear = ? AND 
                                          countryCode = ?
                                     )
                               )
                              FROM [WFD2022extract.SWB_SurfaceWaterBody]
                             WHERE cYear = ? AND 
                               countryCode = ?
                               GROUP BY wiseEvolutionType;''', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Unchanged Area (km^2)', 'Unchanged Area (%)', 'Other Area (km^2)', 'Other Area (%)']
    with open(
            working_directory + '10.1.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            dropUnchange = '''DROP TABLE IF EXISTS Unchange;'''

            createUnchange = '''CREATE TEMPORARY TABLE Unchange AS SELECT countryCode, cYear,  
                               round(sum(cArea)) AS UnchangeArea,
                               round(sum(cArea) * 100.0 / (
                                     SELECT sum(cArea) 
                                       FROM [WFD2022extract.GWB_GroundWaterBody]
                                      WHERE cYear = ''' + str(cYear) + ''' AND 
                                      countryCode = "''' + country + '''"
                                 )
                               ) as UnchangeAreaPercent
                          FROM [WFD2022extract.GWB_GroundWaterBody]
                         WHERE cYear = ''' + str(cYear) + ''' AND 
                               countryCode = "''' + country + '''" AND 
                               wiseEvolutionType IN ("noChange", "changeCode", "change");'''

            dropOther = '''DROP TABLE IF EXISTS Other;'''

            createOther = '''CREATE TEMPORARY TABLE Other AS SELECT countryCode, cYear,  
                               round(sum(cArea)) as OtherArea,
                               round(sum(cArea) * 100.0 / (
                                     SELECT sum(cArea) 
                                       FROM [WFD2022extract.GWB_GroundWaterBody]
                                      WHERE cYear = ''' + str(cYear) + ''' AND 
                                      countryCode = "''' + country + '''"
                                 )
                               ) as OtherAreaPercent
                          FROM [WFD2022extract.GWB_GroundWaterBody]
                         WHERE cYear = ''' + str(cYear) + ''' AND 
                               countryCode = "''' + country + '''" AND 
                               wiseEvolutionType not IN ("noChange", "changeCode", "change");'''

            final = '''SELECT CASE WHEN Unchange.countryCode IS NOT NULL THEN Unchange.countryCode ELSE Other.countryCode END,
                               CASE WHEN Unchange.cYear IS NOT NULL THEN Unchange.cYear ELSE Other.cYear END,
                               (
                                   SELECT UnchangeArea
                                     FROM Unchange
                               ),
                               (
                                   SELECT UnchangeAreaPercent
                                     FROM Unchange
                               ),
                               (
                                   SELECT OtherArea
                                     FROM Other
                               ),
                               (
                                   SELECT OtherAreaPercent
                                     FROM Other
                               )
                          FROM Other,
                               Unchange;'''

            cur.execute(dropUnchange)
            cur.execute(dropOther)
            cur.execute(createUnchange)
            cur.execute(createOther)
            data = cur.execute(final).fetchall()
            write.writerows(data)


def gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Evolution Type', 'Area (km^2)', 'Area (%)']
    with open(
            working_directory + '10.2.gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode, cYear, wiseEvolutionType, 
                               round(sum(cArea)),
                               round(sum(cArea) * 100.0 / (
                                     SELECT sum(cArea) 
                                       FROM [WFD2022extract.GWB_GroundWaterBody]
                                      WHERE cYear = ? AND 
                                      countryCode = ?
                                 )
                               ) 
                          FROM [WFD2022extract.GWB_GroundWaterBody]
                         WHERE cYear = ? AND 
                               countryCode = ? 
                               group by wiseEvolutionType;

            ''', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def ecologicalMonitoring(working_directory, conn, countryCode, cYear):
    headers = ['RBD Code', 'Year', 'Yes', 'No', 'Unknown', 'Inapplicable']
    with open(
            working_directory + '129.1.ecologicalMonitoring' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            drop = '''drop table if exists valuesDistinct; '''

            temp = '''create temporary table valuesDistinct as SELECT euRBDCode, cYear, 
                   CAST (CASE WHEN ecologicalMonitoring = "Yes" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) AS t1,
                   CAST (CASE WHEN ecologicalMonitoring = "No" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) AS t2,
                   CAST (CASE WHEN ecologicalMonitoring = "Unknown" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t3,
                   CAST (CASE WHEN ecologicalMonitoring = "Inapplicable" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t4 
              FROM [WFD2022extract.Monitoring_MonitoringSite_ChemicalEcologicalQuantitativeMonitoring]
             WHERE countryCode = "''' + country + '''"
             GROUP BY euRBDCode,
                      ecologicalMonitoring;'''

            final = '''select euRBDCode, cYear, max(t1), max(t2), max(t3), max(t4) from valuesDistinct group by euRBDCode;'''

            cur.execute(drop)
            cur.execute(temp)
            data = cur.execute(final).fetchall()
            write.writerows(data)


def chemicalMonitoring(working_directory, conn, countryCode, cYear):
    headers = ['RBD Code', 'Year', 'Yes', 'No', 'Unknown', 'Inapplicable']
    with open(
            working_directory + '129.2.chemicalMonitoring' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            drop = '''drop table if exists valuesDistinct; '''

            temp = '''create temporary table valuesDistinct as SELECT euRBDCode,cYear,
                               CAST (CASE WHEN chemicalMonitoring = "Yes" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) AS t1,
                               CAST (CASE WHEN chemicalMonitoring = "No" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t2,
                               CAST (CASE WHEN chemicalMonitoring = "Unknown" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t3,
                               CAST (CASE WHEN chemicalMonitoring = "Inapplicable" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t4
                          FROM [WFD2022extract.Monitoring_MonitoringSite_ChemicalEcologicalQuantitativeMonitoring]
                         WHERE countryCode = "''' + country + '''"
                         GROUP BY euRBDCode,
                                  chemicalMonitoring;'''

            final = '''select euRBDCode, cYear, max(t1), max(t2), max(t3), max(t4) from valuesDistinct group by euRBDCode;'''

            cur.execute(drop)
            cur.execute(temp)
            data = cur.execute(final).fetchall()
            write.writerows(data)


def quantitativeMonitoring(working_directory, conn, countryCode, cYear):
    headers = ['RBD Code', 'Year', 'Yes', 'No', 'Unknown', 'Inapplicable']
    with open(
            working_directory + '129.3.quantitativeMonitoring' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            drop = '''drop table if exists valuesDistinct; '''

            temp = '''create temporary table valuesDistinct as SELECT euRBDCode,cYear,
                               CAST (CASE WHEN quantitativeMonitoring = "Yes" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t1,
                               CAST (CASE WHEN quantitativeMonitoring = "No" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t2,
                               CAST (CASE WHEN quantitativeMonitoring = "Unknown" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t3,
                               CAST (CASE WHEN quantitativeMonitoring = "Inapplicable" THEN count(DISTINCT euMonitoringSiteCode) END AS INT) as t4
                          FROM [WFD2022extract.Monitoring_MonitoringSite_ChemicalEcologicalQuantitativeMonitoring]
                         WHERE countryCode = "''' + country + '''"
                         GROUP BY euRBDCode,
                                  quantitativeMonitoring;'''

            final = '''select euRBDCode, cYear, max(t1), max(t2), max(t3), max(t4) from valuesDistinct group by euRBDCode;'''

            cur.execute(drop)
            cur.execute(temp)
            data = cur.execute(final).fetchall()
            write.writerows(data)


def surfaceWaterBodyTypeCode(working_directory, conn, countryCode, cYear):
    headers = ['Country', 'Year', 'Category', 'Type Code', 'Number', 'Length (km)', 'Area (km^2)']
    with open(
            working_directory + 'NewDash.6.surfaceWaterBodyTypeCode' + str(cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            sql = '''SELECT countryCode,
                           cYear,
                           surfaceWaterBodyCategory,
                           surfaceWaterBodyTypeCode,
                           count(surfaceWaterBodyName),
                           round(sum(cLength)),
                           round(sum(cArea)) 
                      FROM [WFD2022extract.SWB_SurfaceWaterBody]
                      WHERE countryCode = "''' + country + '''"
                      and cYear = 2022
                     GROUP BY surfaceWaterBodyCategory, surfaceWaterBodyTypeCode ;'''
            data = cur.execute(sql).fetchall()
            write.writerows(data)


def swEcologicalStatus_ChemicalStatus_Assessment_confidence_by_country_by_category(working_directory, conn, countryCode,
                                                                                   cYear):
    with open(
            working_directory + 'NewDash.20.swEcologicalStatus_by_country_by_category' + str(cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Category", "Ecological status or potential", "Number", "Number (%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        category = cur.execute('''select distinct surfaceWaterBodyCategory 
                                    from [WFD2022extract.SWB_SurfaceWaterBody] 
                                    where surfaceWaterBodyCategory <> "Unpopulated"''').fetchall()

        for country in countryCode:
            for temp in category:
                categ = ','.join(temp)
                sql = '''SELECT countryCode,
                       cYear,
                       surfaceWaterBodyCategory,
                       swEcologicalAssessmentConfidence,
                       count(DISTINCT euSurfaceWaterBodyCode),
                       CAST (ROUND(count(DISTINCT euSurfaceWaterBodyCode) * 100.0 / (
                                    SELECT count(DISTINCT euSurfaceWaterBodyCode) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                     WHERE cYear = 2022 AND 
                                           countryCode = "''' + country + '''" AND
                                           surfaceWaterBodyCategory = "''' + categ + '''" and
                                           naturalAWBHMWB <> "Unpopulated" and
                                           swEcologicalStatusOrPotentialValue <> "Unpopulated"
                                )
                       ) AS INT) 
                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                 WHERE countryCode = "''' + country + '''" AND 
                       cYear = 2022 AND
                       surfaceWaterBodyCategory = "''' + categ + '''" and
                       naturalAWBHMWB <> "Unpopulated" and
                       swEcologicalStatusOrPotentialValue <> "Unpopulated"
                 GROUP BY swEcologicalAssessmentConfidence;'''
                data = cur.execute(sql).fetchall()
                write.writerows(data)

    with open(
            working_directory + 'NewDash.20.ChemicalStatus_Assessment_confidence_by_country_by_category' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Category", "Chemical status", "Number", "Number (%)"]
        write = csv.writer(f)
        write.writerow(header)
        for country in countryCode:
            for temp in category:
                categ = ','.join(temp)
                sql = '''SELECT countryCode,
                       cYear,
                       surfaceWaterBodyCategory,
                       swChemicalAssessmentConfidence,
                       count(DISTINCT euSurfaceWaterBodyCode),
                       CAST (ROUND(count(DISTINCT euSurfaceWaterBodyCode) * 100.0 / (
                                    SELECT count(DISTINCT euSurfaceWaterBodyCode) 
                                      FROM [WFD2022extract.SWB_SurfaceWaterBody]
                                     WHERE cYear = 2022 AND 
                                           countryCode = "''' + country + '''" AND
                                           surfaceWaterBodyCategory = "''' + categ + '''" AND
                                           swChemicalStatusValue <> "Unpopulated"
                                )
                       ) AS INT) 
                  FROM [WFD2022extract.SWB_SurfaceWaterBody]
                 WHERE countryCode = "''' + country + '''" AND 
                       cYear = 2022 AND
                       surfaceWaterBodyCategory = "''' + categ + '''" AND
                       swChemicalStatusValue <> "Unpopulated"
                 GROUP BY swChemicalAssessmentConfidence;'''

                data = cur.execute(sql).fetchall()
                write.writerows(data)


def rbdCodeNames(working_directory, conn, countryCode, cYear):
    with open(
            working_directory + 'rbdCodeNames' + str(cYear) + '.csv',
            'w+', newline='') as f:
        headers = ["Country", "RBD Code", "RBD Name"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''select distinct countryCode, euRBDCode, rbdName from 
                        [WFD2022extract.GWB_GroundWaterBody] order by euRBDCode;
                        '''
                           ).fetchall()
        write.writerows(data)

# Extra csv
def per_RBD_ExemptionType(directory, conn, countryCode, cYear):
    # per RBD Exemption Type
    code = ''.join(countryCode)
    with open(
            directory + 'swEcologicalExemptionType_' + code + '_per_RBD_ExemptionType' + str(
                cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        headers = ["Country", "Year", "RBD Code", "Ecological Exemption Type Group", "Ecological Exemption Type",
                   "Number"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]

        for country in countryCode:
            for value in swEcologicalExemptionTypeGroup:
                
                data = cur.execute('''SELECT countryCode,
                           cYear,
                           euRBDCode,
                           swEcologicalExemptionTypeGroup,
                           swEcologicalExemptionType,
                           count(DISTINCT euSurfaceWaterBodyCode)
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                     WHERE cYear = ''' + str(cYear) + ''' AND
                           swEcologicalExemptionTypeGroup <> "None" AND
                           swEcologicalExemptionTypeGroup <> "Unpopulated" AND
                           countryCode = "''' + country + '''" AND
                           swEcologicalExemptionTypeGroup = ?
                     GROUP BY euRBDCode,
                              swEcologicalExemptionType;''', (value,)).fetchall()
                
                write.writerows(data)

    with open(
            directory + 'gwQuantitativeExemptionType_' + code + '_per_RBD_ExemptionType' + str(
                cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        headers = ["Country", "Year", "RBD Code", "Quantitative Exemption Type Group", "Quantitative Exemption Type",
                   "Number"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]

        for country in countryCode:
            for value in swEcologicalExemptionTypeGroup:
                
                data = cur.execute('''SELECT countryCode,
                               cYear,
                               euRBDCode,
                               gwQuantitativeExemptionTypeGroup,
                               gwQuantitativeExemptionType,
                               count(DISTINCT euGroundWaterBodyCode)
                          FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType]
                         WHERE cYear = ''' + str(cYear) + ''' AND 
                               gwQuantitativeExemptionTypeGroup <> "None" AND 
                               gwQuantitativeExemptionTypeGroup <> "Unpopulated" AND 
                               countryCode = "''' + country + '''" AND 
                               gwQuantitativeExemptionTypeGroup = ?
                         GROUP BY euRBDCode,
                                  gwQuantitativeExemptionTypeGroup;

                        ''', (value,)).fetchall()
                
                write.writerows(data)

    with open(
            directory + 'sw_QE_EcologicalExemptionType_' + code + '_per_RBD_ExemptionType' + str(
                cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        headers = ["Country", "Year", "RBD Code", "Quality Element Ecological Exemption Type Group",
                   "Quality Element Ecological Exemption Type", "Number"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]

        for country in countryCode:
            for value in swEcologicalExemptionTypeGroup:
                
                data = cur.execute('''SELECT countryCode,
                               cYear,
                               euRBDCode,
                               qeEcologicalExemptionTypeGroup,
                               qeEcologicalExemptionType,
                               count(DISTINCT euSurfaceWaterBodyCode)
                          FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType]
                         WHERE cYear = ''' + str(cYear) + ''' AND 
                               qeEcologicalExemptionTypeGroup <> "None" AND 
                               qeEcologicalExemptionTypeGroup <> "Unpopulated" AND 
                               countryCode = "''' + country + '''" AND 
                               qeEcologicalExemptionTypeGroup = ?
                         GROUP BY euRBDCode,
                                  qeEcologicalExemptionTypeGroup;

                        ''', (value,)).fetchall()
                
                write.writerows(data)

    with open(
            directory+'swChemicalExemptionType_' + code + '_per_RBD_ExemptionType' + str(
                cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        headers = ["Country", "Year", "RBD Code", "Chemical Exemption Type Group", "Chemical Exemption Type", "Number"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]

        for country in countryCode:
            for value in swEcologicalExemptionTypeGroup:
                
                data = cur.execute('''SELECT countryCode,
                               cYear,
                               euRBDCode,
                               swChemicalExemptionTypeGroup,
                               swChemicalExemptionType,
                               count(DISTINCT euSurfaceWaterBodyCode)
                          FROM [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                         WHERE cYear = ''' + str(cYear) + ''' AND 
                               swChemicalExemptionTypeGroup <> "None" AND 
                               swChemicalExemptionTypeGroup <> "Unpopulated" AND 
                               countryCode = "''' + country + '''" AND 
                               swChemicalExemptionTypeGroup = ?
                         GROUP BY euRBDCode,
                                  swChemicalExemptionTypeGroup;
                        ''', (value,)).fetchall()
                
                write.writerows(data)

    with open(
            directory + 'gwChemicalExemptionType_' + code + '_per_RBD_ExemptionType' + str(
                cYear) + '.csv',
            'w+', newline='', encoding='utf-8') as f:
        headers = ["Country", "Year", "RBD Code", "Chemical Exemption Type Group", "Chemical Exemption Type", "Number"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]

        for country in countryCode:
            for value in swEcologicalExemptionTypeGroup:
                
                data = cur.execute('''SELECT countryCode,
                               cYear,
                               euRBDCode,
                               gwChemicalExemptionTypeGroup,
                               gwChemicalExemptionType,
                               count(DISTINCT euGroundWaterBodyCode)
                          FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                         WHERE cYear = ''' + str(cYear) + ''' AND 
                               gwChemicalExemptionTypeGroup <> "None" AND 
                               gwChemicalExemptionTypeGroup <> "Unpopulated" AND 
                               countryCode = "''' + country + '''" AND 
                               gwChemicalExemptionTypeGroup = ?
                         GROUP BY euRBDCode,
                                  gwChemicalExemptionTypeGroup;

                        ''', (value,)).fetchall()
                
                write.writerows(data)

    # Per RBD
    
    with open(directory + 'swEcologicalExemptionType_' + code + '_per_RBD_' + str(
                cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
        headers = ['RBDCode', 'Number']

        write = csv.writer(f)

        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT euRBDCode,
                           count(DISTINCT euSurfaceWaterBodyCode) 
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                     WHERE countryCode = "''' + code + '''" AND 
                     swEcologicalExemptionType IS NOT NULL
                     GROUP BY euRBDCode,
                              swEcologicalExemptionType;''').fetchall()

        write.writerows(data)

    with open(directory + 'swChemicalExemptionType_' + code + '_per_RBD_' + str(
                cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
        headers = ['RBDCode', 'Number']

        write = csv.writer(f)

        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT 
                               euRBDCode,
                               count(DISTINCT euSurfaceWaterBodyCode) 
                          FROM [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                          WHERE countryCode = "''' + code + '''" AND 
                            swChemicalExemptionType IS NOT NULL
                         ''').fetchall()

        write.writerows(data)

        with open(directory + 'qeEcologicalExemptionTypeGroup_' + code + '_per_RBD_' + str(
                cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
            headers = ['RBDCode', 'Number']
    
            write = csv.writer(f)
    
            write.writerow(headers)
            cur = conn.cursor()
    
            data = cur.execute('''SELECT euRBDCode,
                               count(DISTINCT euSurfaceWaterBodyCode) 
                          FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType]
                         WHERE countryCode = "''' + code + '''" AND 
                            qeEcologicalExemptionTypeGroup IS NOT NULL
                         GROUP BY euRBDCode,
                                  qeEcologicalExemptionTypeGroup;''').fetchall()
    
            write.writerows(data)
        
    with open(directory + 'gwChemicalExemptionType_' + code + '_per_RBD_' + str(
                cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:

        headers = ['RBDCode', 'Number']

        write = csv.writer(f)

        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT euRBDCode,
                           count(DISTINCT euGroundWaterBodyCode) 
                      FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                     WHERE countryCode = "''' + code + '''" AND 
                         gwChemicalExemptionTypeGroup IS NOT NULL
                     GROUP BY euRBDCode,
                              gwChemicalExemptionTypeGroup;''').fetchall()

        write.writerows(data)

    with open(directory + 'gwQuantitativeExemptionType_' + code + '_per_RBD_' + str(
                cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
        headers = ['RBDCode', 'Number']

        write = csv.writer(f)

        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT euRBDCode,
                           count(DISTINCT euGroundWaterBodyCode) 
                      FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType]
                      WHERE countryCode = "''' + code + '''"
                     GROUP BY euRBDCode,
                              gwQuantitativeExemptionTypeGroup;''').fetchall()

        write.writerows(data)

    with open(directory + 'swEcologicalExemptionType_' + code + '_per_RBD_' + str(
                cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
        headers = ['RBDCode', 'Number']

        write = csv.writer(f)

        write.writerow(headers)
        cur = conn.cursor()

        data = cur.execute('''SELECT euRBDCode,
                           count(DISTINCT euSurfaceWaterBodyCode) 
                      FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                     WHERE countryCode = "''' + code + '''" AND 
                     swEcologicalExemptionType IS NOT NULL
                     GROUP BY euRBDCode,
                              swEcologicalExemptionType;''').fetchall()

        write.writerows(data)

    # Overall
    cur = conn.execute('''select * from [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType] WHERE countryCode = "''' + country + '''"''')
    columns = list(map(lambda x: x[0], cur.description))

    with open(directory + 'gwChemicalExemptionType_Overall_' + code + '_' + str(
            cYear) + '.csv',
              'w+', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(columns)

        data = cur.execute('''SELECT *
                        FROM [WFD2022extract.GWB_GroundWaterBody_GWPollutant_GWChemicalExemptionType]
                        WHERE countryCode = "''' + country + '''";''').fetchall()

        write.writerows(data)

    cur = conn.execute('''select * from [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType] WHERE countryCode = "''' + country + '''"''')
    columns = list(map(lambda x: x[0], cur.description))

    with open(directory + 'gwQuantitativeExemptionType_Overall_' + code + '_' + str(
            cYear) + '.csv',
              'w+', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(columns)

        data = cur.execute('''SELECT *
                        FROM [WFD2022extract.GWB_GroundWaterBody_gwQuantitativeExemptionType]
                        WHERE countryCode = "''' + country + '''";''').fetchall()

        write.writerows(data)

    cur = conn.execute('''select * from [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType] 
    WHERE countryCode = "''' + country + '''"''')
    columns = list(map(lambda x: x[0], cur.description))

    with open(directory + 'swEcologicalExemptionType_Overall_' + code + '_' + str(
            cYear) + '.csv',
              'w+', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(columns)
        data = cur.execute('''select *
                    FROM [WFD2022extract.SWB_SurfaceWaterBody_SWEcologicalExemptionType]
                    WHERE countryCode = "''' + country + '''";''').fetchall()

        write.writerows(data)

    cur = conn.execute('''select * from [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType] 
                    WHERE countryCode = "''' + country + '''";''')
    columns = list(map(lambda x: x[0], cur.description))

    with open(directory + 'swQE_EcologicalExemptionType_Overall_' + code + '_' + str(
            cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(columns)
        cur = conn.cursor()
        data = cur.execute('''SELECT *
                    FROM [WFD2022extract.SWB_SurfaceWaterBody_QualityElement_qeEcologicalExemptionType]
                    WHERE countryCode = "''' + country + '''";''').fetchall()

        write.writerows(data)

    cur = conn.execute('''select * from [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                        WHERE countryCode = "''' + country + '''"''')
    columns = list(map(lambda x: x[0], cur.description))

    with open(directory + 'swChemicalExemptionType_Overall_' + code + '_' + str(
            cYear) + '.csv', 'w+', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(columns)
        cur = conn.cursor()
        data = cur.execute('''SELECT *
                        FROM [WFD2022extract.SWB_SurfaceWaterBody_SWPrioritySubstance_SWChemicalExemptionType]
                        WHERE countryCode = "''' + country + '''";''').fetchall()

        write.writerows(data)

        f.close()


