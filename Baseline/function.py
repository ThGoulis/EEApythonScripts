import csv


def updateTables(conn):
    cur = conn.cursor()

    update1 = '''UPDATE swRBD_Europe_data SET C_StatusFailing = REPLACE(REPLACE(REPLACE(C_StatusFailing, ' ', ''), '\t', ''), '\n', '');'''
    update2 = '''UPDATE swRBD_Europe_data SET C_StatusKnown = REPLACE(REPLACE(REPLACE(C_StatusKnown, ' ', ''), '\t', ''), '\n', '');'''

    cur.execute(update1)
    conn.commit()
    cur.execute(update2)
    conn.commit()


def rbdCodeNames(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_Status_Maps/GWB_Status_RBD?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory +'rbdCodeNames'+str(cYear)+'.csv',
            'w+', newline='') as f:
        headers = ["Country", "RBD Code", "RBD Name"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('''SELECT DISTINCT NUTS0,
                                    euRBDCode, rbdName
                      FROM swRBD_Europe_data
                     WHERE NUTS0 = "''' + country + '''"
                     ORDER BY euRBDCode;
                            '''
                               ).fetchall()

            write.writerows(data)


def WISE_SOW_SurfaceWaterBody_SWB_Table(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_NumberSize?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '1.surfaceWaterBodyNumberAndSite2016.csv',
            'w+', newline='') as f:
        headers = ['Country', 'Number', 'Number (%)', 'Length (km)', 'Length (%)', 'Area (km^2)', 'Area (%)', 'Median Length (%)', 'Median Area (%)']
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        country = ''.join(countryCode)
        dropMedianArea = '''drop table if exists swMedianArea;'''

        MedianArea = '''CREATE TEMPORARY TABLE swMedianArea AS SELECT countryCode,
                                              round(AVG(cArea), 1) AS medianArea
                                         FROM (
                                                  SELECT countryCode,
                                                         cArea
                                                    FROM SOW_SWB_SurfaceWaterBody
                                                   WHERE countryCode = "''' + country + '''" AND 
                                                         countryCode IS NOT NULL AND 
                                                         cArea IS NOT NULL AND 
                                                         cYear = ''' + str(cYear) + '''
                                                   ORDER BY cArea
                                                   LIMIT 2 - (
                                                                 SELECT COUNT( * ) 
                                                                   FROM SOW_SWB_SurfaceWaterBody
                                                                  WHERE countryCode = "''' + country + '''" AND 
                                                                        countryCode IS NOT NULL AND 
                                                                        cArea IS NOT NULL AND 
                                                                        cYear = ''' + str(cYear) + '''
                                                             )
%                                                            2 OFFSET (
                                                             SELECT (COUNT( * ) - 1) / 2
                                                               FROM SOW_SWB_SurfaceWaterBody
                                                              WHERE countryCode = "''' + country + '''" AND 
                                                                    countryCode IS NOT NULL AND 
                                                                    cArea IS NOT NULL AND 
                                                                    cYear = ''' + str(cYear) + '''
                                                              GROUP BY countryCode = "''' + country + '''"
                                                         )
                                              );'''

        dropMedianLength = '''drop table if exists swMedianLength; '''

        MedianLength = '''CREATE TEMPORARY TABLE swMedianLength AS SELECT countryCode,
                                                round(AVG(cLength), 1) AS medianLength
                                           FROM (
                                                    SELECT countryCode,
                                                           cLength
                                                      FROM SOW_SWB_SurfaceWaterBody
                                                     WHERE countryCode = "''' + country + '''" AND 
                                                           countryCode IS NOT NULL AND 
                                                           cLength IS NOT NULL AND 
                                                           cYear = ''' + str(cYear) + '''
                                                     ORDER BY cLength
                                                     LIMIT 2 - (
                                                                   SELECT COUNT( * ) 
                                                                     FROM SOW_SWB_SurfaceWaterBody
                                                                    WHERE countryCode = "''' + country + '''" AND 
                                                                          countryCode IS NOT NULL AND 
                                                                          cLength IS NOT NULL AND 
                                                                          cYear = ''' + str(cYear) + '''
                                                               )
%                                                              2 OFFSET (
                                                               SELECT (COUNT( * ) - 1) / 2
                                                                 FROM SOW_SWB_SurfaceWaterBody
                                                                WHERE countryCode = "''' + country + '''" AND 
                                                                      countryCode IS NOT NULL AND 
                                                                      cLength IS NOT NULL AND 
                                                                      cYear = ''' + str(cYear) + '''
                                                                GROUP BY countryCode = "''' + country + '''"
                                                           )
                                                );'''

        final = '''SELECT countryCode,
                   count(euSurfaceWaterBodyCode),
                   round(count(euSurfaceWaterBodyCode) * 100 / (
                                                 SELECT round(count(euSurfaceWaterBodyCode)) 
                                                   FROM SOW_SWB_SurfaceWaterBody
                                                  WHERE cYear = ''' + str(cYear) + '''
                                             ), 1),
                   round(sum(cLength) ),
                   round(sum(cLength) * 100.0 / (
                                      SELECT sum(cLength) 
                                        FROM SOW_SWB_SurfaceWaterBody
                                       WHERE cYear = ''' + str(cYear) + '''
                                   ), 1) ,
                   round(sum(cArea) ),
                   round(sum(cArea) * 100.0 / (
                                      SELECT sum(cArea) 
                                        FROM SOW_SWB_SurfaceWaterBody
                                       WHERE cYear = ''' + str(cYear) + '''
                                  ), 1),
                   (
                       SELECT medianLength
                         FROM swMedianLength
                   ),
                   (
                       SELECT medianArea
                         FROM swMedianArea
                   )
              FROM SOW_SWB_SurfaceWaterBody
             WHERE cYear = ''' + str(cYear) + ''' AND 
                   countryCode = "''' + country + '''";'''

        cur.execute(dropMedianArea)
        cur.execute(MedianArea)
        cur.execute(dropMedianLength)
        cur.execute(MedianLength)
        data = cur.execute(final).fetchall()

        write.writerows(data)
            
            
def WISE_SOW_SurfaceWaterBody_SWB_Category(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_CategoryType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no

    headers = ["Country", "Year", 'Surface Water Body Category', "Type", "Total"]
    with open(
            working_directory + '3.surfaceWaterBodyCategory2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        WDFCode = ["RW", "LW", "TW", "CW", "TeW"]
        naturalAWBHMWB = ["Natural water body", "Heavily modified water body", "Artificial water body"]
        cur = conn.cursor()
        for country in countryCode:
            for wdf in WDFCode:
                for types in naturalAWBHMWB:
                    data = cur.execute('SELECT countryCode, '
                                            'cYear, '
                                            'surfaceWaterBodyCategory, '
                                            'naturalAWBHMWB, '
                                            'COUNT(surfaceWaterBodyCategory) '
                                            'FROM SOW_SWB_SurfaceWaterBody '
                                            'WHERE countryCode = ? '
                                            'AND cYear == ? '
                                            'and surfaceWaterBodyCategory = ? '
                                            'and naturalAWBHMWB == ? '
                                            'and countryCode = ? ',
                               (country, cYear, wdf, types, country)).fetchall()
                    write.writerows(data)
                    

def Surface_water_bodies_Ecological_exemptions_and_pressures(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_SWE_swEcologicalExemptionPressure/SWB_SWE_swEcologicalExemptionPressure?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '6.Surface_water_bodies_Ecological_exemptions_and_pressures2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Ecological Exemption Type Group",
                  "Ecological Exemption Type", "Ecological Exemption Pressure Group", "Ecological Exemption Pressure", "Number"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               cYear,
                               swEcologicalExemptionTypeGroup,
                               swEcologicalExemptionType,
                               swEcologicalExemptionPressureGroup,
                               swEcologicalExemptionPressure,
                               count(DISTINCT euSurfaceWaterBodyCode) 
                          FROM SOW_SWB_SWE_swEcologicalExemptionPressure
                         WHERE cYear = ? AND 
                               countryCode = ?
                         GROUP BY swEcologicalExemptionTypeGroup,
                                  swEcologicalExemptionType,
                                  swEcologicalExemptionPressureGroup,
                                  swEcologicalExemptionPressure;
                        ''', (cYear, country)
                            ).fetchall()
            write.writerows(data)
            

def Surface_water_bodies_Ecological_exemptions_Type(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_SWEcologicalExemptionType/SWB_SWEcologicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '6.Surface_water_bodies_Ecological_exemptions_Type2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Ecological Exemption Type Group", "Ecological Exemption Type", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]
        cur = conn.cursor()
        for country in countryCode:
            for values in swEcologicalExemptionTypeGroup:

                data = cur.execute('select countryCode, cYear, swEcologicalExemptionTypeGroup, swEcologicalExemptionType, count(Distinct euSurfaceWaterBodyCode), '
                                'round(count(distinct euSurfaceWaterBodyCode) *100.0 / ( '
                                'select count(distinct euSurfaceWaterBodyCode) '
                                'from SOW_SWB_SWEcologicalExemptionType '
                                   'where cYear = ? '
                                        'and countryCode = ? ' 
                                        'AND swEcologicalExemptionTypeGroup = ? '
                                ')) '
                                'from SOW_SWB_SWEcologicalExemptionType '
                                    'where cYear = ? and swEcologicalExemptionTypeGroup <> "None" '
                                        'and swEcologicalExemptionTypeGroup <> "Unpopulated" ' 
                                        'AND countryCode = ? '
                                        'AND swEcologicalExemptionTypeGroup = ? '
                                'group by swEcologicalExemptionType ', (cYear, country, values, cYear, country, values)).fetchall()
                write.writerows(data)
                

def Surface_water_bodies_Quality_element_exemptions_Type(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_QE_qeEcologicalExemptionType/SWB_QE_qeEcologicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '6.Surface_water_bodies_Quality_element_exemptions_Type2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quality Element Exemption Type Group", "Quality Element Exemption Type", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        swEcologicalExemptionTypeGroup = ["Article4(4)", "Article4(5)", "Article4(6)", "Article4(7)"]
        cur = conn.cursor()
        for country in countryCode:
            for values in swEcologicalExemptionTypeGroup:
                data = cur.execute('select countryCode, cYear, qeEcologicalExemptionTypeGroup, qeEcologicalExemptionType, count(Distinct euSurfaceWaterBodyCode), '
                                'round(count(distinct euSurfaceWaterBodyCode) *100.0 / ( '
                                'select count(distinct euSurfaceWaterBodyCode) '
                                'from SOW_SWB_QE_qeEcologicalExemptionType '
                                   'where cYear = ? '
                                        'and countryCode = ? ' 
                                        'AND qeEcologicalExemptionTypeGroup = ? '
                                ')) '
                                'from SOW_SWB_QE_qeEcologicalExemptionType '
                                    'where cYear = ? and qeEcologicalExemptionTypeGroup <> "None" '
                                        'and qeEcologicalExemptionTypeGroup <> "Unpopulated" ' 
                                        'AND countryCode = ? '
                                        'AND qeEcologicalExemptionTypeGroup = ? '
                                'group by qeEcologicalExemptionType ', (cYear, country, values, cYear, country, values)).fetchall()
                write.writerows(data)
                

def SWB_Chemical_exemption_type(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_SWP_SWChemicalExemptionType/SWB_SWP_SWChemicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ["Country", "Chemical Exemption Type Group", "Chemical Exemption Type", "Area (km^2)", "Area (%)"]
    with open(
            working_directory + '6.swChemical_exemption_type2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swChemicalExemptionTypeGroup = cur.execute('''select distinct swChemicalExemptionTypeGroup
                                            from SOW_SWB_SWP_SWChemicalExemptionType
                                            where cYear = 2016 and swChemicalExemptionTypeGroup <> "None";''').fetchall()
        swChemicalExemptionType = cur.execute('''select distinct swChemicalExemptionType
                                            from SOW_SWB_SWP_SWChemicalExemptionType
                                            where cYear = 2016 and swChemicalExemptionType <> "None"''').fetchall()
        for country in countryCode:
            for chgroup in swChemicalExemptionTypeGroup:
                for chtype in swChemicalExemptionType:
                    tempgroup = ','.join(chgroup)
                    temptype = ','.join(chtype)
                    sqlDropValues = '''DROP TABLE IF EXISTS DistinctValues;'''

                    sqlValues = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euSurfaceWaterBodyCode,surfaceWaterBodyCategory,
                                                                 swChemicalExemptionTypeGroup,
                                                                 swChemicalExemptionType,
                                                                 cArea AS A
                                                   FROM SOW_SWB_SWP_SWChemicalExemptionType
                                                  WHERE cYear = '''+str(cYear)+''' AND 
                                                        countryCode = "'''+country+'''" AND                                              
                                                        swEcologicalStatusOrPotentialValue <> "unknown" and
                                                        naturalAWBHMWB <> "unpopulated" AND 
                                                        swChemicalStatusValue <> "unpopulated" AND 
                                                        swChemicalExemptionTypeGroup = "'''+tempgroup+'''" AND 
                                                        swChemicalExemptionType = "'''+temptype+'''";'''

                    sqlDropArea = '''DROP TABLE IF EXISTS DistinctArea;'''

                    sqlArea = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euSurfaceWaterBodyCode,surfaceWaterBodyCategory, cArea as G
                                      FROM SOW_SWB_SWP_SWChemicalExemptionType
                                    WHERE cYear = '''+str(cYear)+''' AND 
                                      countryCode = "'''+country+'''" AND 
                                      naturalAWBHMWB <> "unpopulated" AND 
                                      swChemicalStatusValue <> "unpopulated" AND 
                                      swChemicalExemptionTypeGroup = "'''+tempgroup+'''";
                    '''

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
                              FROM SOW_SWB_SWP_SWChemicalExemptionType
                             WHERE cYear = '''+str(cYear)+''' AND 
                                   countryCode = "'''+country+'''" AND 
                                   naturalAWBHMWB <> "unpopulated" AND 
                                   swChemicalStatusValue <> "unpopulated" AND 
                                   swChemicalExemptionTypeGroup = "'''+tempgroup+'''" AND 
                                   swChemicalExemptionType = "'''+temptype+'''" 
                             GROUP BY swChemicalExemptionTypeGroup,
                                      swChemicalExemptionType;
                            '''
                    cur.execute(sqlDropValues)
                    cur.execute(sqlValues)
                    cur.execute(sqlDropArea)
                    cur.execute(sqlArea)
                    data = cur.execute(sqlexecute).fetchall()
                    
                    write.writerows(data)


def WISE_SOW_SurfaceWaterBody_SWB_ChemicalStatus_Table(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_ChemicalStatus?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Year', "Chemical Status Value", 'Number', 'Number(%)', 'Length (km)', 'Length(%)', 'Area (km^2)', 'Area(%)']
    with open(
            working_directory + '12.surfaceWaterBodyChemicalStatusGood2016.csv',
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
                                                                                       FROM SOW_SWB_SurfaceWaterBody
                                                                                      WHERE cYear = ? AND 
                                                                                            countryCode = ? AND 
                                                                                            swChemicalStatusValue <> "unknown" AND 
                                                                                            swChemicalStatusValue <> "Unpopulated"
                                                                                 ), 1),
                                    ROUND(SUM(cLength), 0),
                                    ROUND(SUM(cLength) * 100.0 / (
                                                                     SELECT SUM(cLength) 
                                                                       FROM SOW_SWB_SurfaceWaterBody
                                                                      WHERE cYear == ? AND 
                                                                            countryCode = ? AND 
                                                                            swChemicalStatusValue <> "unknown" AND 
                                                                            swChemicalStatusValue <> "Unpopulated"
                                                                 ), 1),
                                    ROUND(SUM(CASE WHEN surfaceWaterBodyCategory <> "RW"  AND cArea is not Null THEN cArea END), 0),
                                    ROUND(SUM(CASE WHEN surfaceWaterBodyCategory <> "RW"  AND cArea is not Null THEN cArea END) * 100.0 / (
                                                                   SELECT SUM(CASE WHEN surfaceWaterBodyCategory <> "RW"  AND cArea is not Null THEN cArea END) 
                                                                     FROM SOW_SWB_SurfaceWaterBody
                                                                    WHERE cYear = ? AND 
                                                                          countryCode = ? AND 
                                                                          swChemicalStatusValue <> "unknown" AND 
                                                                          swChemicalStatusValue <> "Unpopulated"
                                                               ), 1) 
                      FROM SOW_SWB_SurfaceWaterBody
                     WHERE cYear = ? AND 
                           swChemicalStatusValue = ? AND 
                           swChemicalStatusValue <> "unknown" AND 
                           swChemicalStatusValue <> "Unpopulated" AND 
                           surfaceWaterBodyCategory <> "Unpopulated" AND 
                           naturalAWBHMWB <> "Unpopulated" AND 
                           naturalAWBHMWB <> "Unknown" AND 
                           countryCode = ? ;
                ''', (cYear, country, cYear, country, cYear, country, cYear, value, country)).fetchall()

                write.writerows(data)
                

def SurfaceWaterBody_ChemicalStatus_Table_by_Category(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_Category_ChemicalStatus?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Year', 'Surface Water Body Category', 'Chemical Status Value', 'Number', 'Number(%)']
    with open(
            # ιδιο για 10 12
            working_directory + '12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        WDFCode = ["RW", "LW", "TW", "CW", "TeW"]
        chemicalStatus = ["2", "3", "unknown"]
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
                                                                                                   FROM SOW_SWB_SurfaceWaterBody
                                                                                                  WHERE cYear = ? AND 
                                                                                                        countryCode = ? AND 
                                                                                                        swChemicalStatusValue <> "Unpopulated" AND 
                                                                                                        surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                                                        surfaceWaterBodyCategory = ?
                                                                                             ), 1) 
                                                  FROM SOW_SWB_SurfaceWaterBody
                                                 WHERE cYear = ? AND 
                                                       swChemicalStatusValue = ? AND 
                                                       swChemicalStatusValue <> "Unpopulated" AND 
                                                       surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                       countryCode = ? AND 
                                                       surfaceWaterBodyCategory = ?;''', (cYear, country, wdf,  cYear, status, country, wdf)).fetchall()
                    
                    write.writerows(data)


def Surface_water_bodies_Ecological_status_or_potential_groupGoodHigh(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_EcologicalStatusGroup?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ["Country", "Year", "Number", "Number(%)", "Length (km)", "Length(%)", "Area (km^2)", "Area(%)"]
    with open(
            working_directory + '8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               cYear,
                               count(swEcologicalStatusOrPotentialValue),
                               round(count(swEcologicalStatusOrPotentialValue) * 100.0 / (
                             SELECT count(swEcologicalStatusOrPotentialValue) 
                               FROM SOW_SWB_SurfaceWaterBody
                              WHERE countryCode = ? AND 
                                    cYear = ? AND 
                                    swEcologicalStatusOrPotentialValue <> "inapplicable" and
                                    swEcologicalStatusOrPotentialValue <> "unknown" AND 
                                    swEcologicalStatusOrPotentialValue <> "Other" AND 
                                    surfaceWaterBodyCategory <> "Unpopulated" AND 
                                    naturalAWBHMWB <> "Unknown" AND 
                                    naturalAWBHMWB <> "Unpopulated"
                         ), 1),
                               round(sum(case when surfaceWaterBodyCategory = "RW" then  cLength end)),
                               round(sum(case when surfaceWaterBodyCategory = "RW" then  cLength end) * 100.0 / (
                                    SELECT sum(case when surfaceWaterBodyCategory = "RW" then  cLength end) 
                                      FROM SOW_SWB_SurfaceWaterBody
                                     WHERE countryCode = ? AND 
                                           cYear = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "inapplicable" and
                                           swEcologicalStatusOrPotentialValue <> "unknown" AND 
                                           swEcologicalStatusOrPotentialValue <> "Other" AND 
                                           surfaceWaterBodyCategory <> "Unpopulated" AND 
                                           naturalAWBHMWB <> "Unknown" AND 
                                           naturalAWBHMWB <> "Unpopulated"
                                ), 1),
                               round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) ),
                               round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) * 100.0 / (
                              SELECT sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) 
                                                            FROM SOW_SWB_SurfaceWaterBody
                                                           WHERE countryCode = ? AND 
                                                                 cYear = ? AND 
                                                                 swEcologicalStatusOrPotentialValue <> "inapplicable" and
                                                                 swEcologicalStatusOrPotentialValue <> "unknown" AND 
                                                                 swEcologicalStatusOrPotentialValue <> "Other" AND 
                                                                 surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                 naturalAWBHMWB <> "Unknown" AND 
                                                                 naturalAWBHMWB <> "Unpopulated"
                                                      ), 1) 
                              FROM SOW_SWB_SurfaceWaterBody
                             WHERE swEcologicalStatusOrPotentialValue IN ("1", "2") AND 
                                   countryCode = ? AND 
                                   cYear = ? AND 
                                   swEcologicalStatusOrPotentialValue <> "inapplicable" and
                               swEcologicalStatusOrPotentialValue <> "unknown" AND 
                               swEcologicalStatusOrPotentialValue <> "Other" AND 
                               surfaceWaterBodyCategory <> "Unpopulated" AND 
                               naturalAWBHMWB <> "Unknown" AND 
                               naturalAWBHMWB <> "Unpopulated";''', (country, cYear, country, cYear, country, cYear, country, cYear)).fetchall()
            write.writerows(data)
            

def Surface_water_bodies_Ecological_status_or_potential_groupFailling(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_EcologicalStatusGroup?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ["Country", "Year", "Number", "Number(%)", "Length (km)", "Length(%)", "Area (km^2)", "Area(%)"]
    with open(
            working_directory + '8.Surface_water_bodies_Ecological_status_or_potential_group_Failing.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               cYear,
                               count(swEcologicalStatusOrPotentialValue),
                               round(count(swEcologicalStatusOrPotentialValue) * 100.0 / (
                             SELECT count(swEcologicalStatusOrPotentialValue) 
                               FROM SOW_SWB_SurfaceWaterBody
                              WHERE countryCode = ? AND 
                                    cYear = ? AND 
                                    swEcologicalStatusOrPotentialValue <> "inapplicable" and
                                    swEcologicalStatusOrPotentialValue <> "unknown" AND 
                                    swEcologicalStatusOrPotentialValue <> "Other" AND 
                                    surfaceWaterBodyCategory <> "Unpopulated" AND 
                                    naturalAWBHMWB <> "Unknown" AND 
                                    naturalAWBHMWB <> "Unpopulated"
                         ), 1),
                               round(sum(case when surfaceWaterBodyCategory = "RW" then  cLength end)),
                               round(sum(case when surfaceWaterBodyCategory = "RW" then  cLength end) * 100.0 / (
                                    SELECT sum(case when surfaceWaterBodyCategory = "RW" then  cLength end) 
                                      FROM SOW_SWB_SurfaceWaterBody
                                     WHERE countryCode = ? AND 
                                           cYear = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "inapplicable" and
                                           swEcologicalStatusOrPotentialValue <> "unknown" AND 
                                           swEcologicalStatusOrPotentialValue <> "Other" AND 
                                           surfaceWaterBodyCategory <> "Unpopulated" AND 
                                           naturalAWBHMWB <> "Unknown" AND 
                                           naturalAWBHMWB <> "Unpopulated"
                                ), 1),
                               round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) ),
                               round(sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) * 100.0 / (
                              SELECT sum(CASE WHEN surfaceWaterBodyCategory <> "RW" THEN cArea END) 
                                                            FROM SOW_SWB_SurfaceWaterBody
                                                           WHERE countryCode = ? AND 
                                                                 cYear = ? AND 
                                                                 swEcologicalStatusOrPotentialValue <> "inapplicable" and
                                                                 swEcologicalStatusOrPotentialValue <> "unknown" AND 
                                                                 swEcologicalStatusOrPotentialValue <> "Other" AND 
                                                                 surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                 naturalAWBHMWB <> "Unknown" AND 
                                                                 naturalAWBHMWB <> "Unpopulated"
                                                      ), 1) 
                              FROM SOW_SWB_SurfaceWaterBody
                             WHERE swEcologicalStatusOrPotentialValue IN ("3", "4", "5") AND 
                                   countryCode = ? AND 
                                   cYear = ? AND 
                                   swEcologicalStatusOrPotentialValue <> "inapplicable" and
                               swEcologicalStatusOrPotentialValue <> "unknown" AND 
                               swEcologicalStatusOrPotentialValue <> "Other" AND 
                               surfaceWaterBodyCategory <> "Unpopulated" AND 
                               naturalAWBHMWB <> "Unknown" AND 
                               naturalAWBHMWB <> "Unpopulated";
                            ''', (country, cYear, country, cYear, country, cYear, country, cYear)).fetchall()
            write.writerows(data)
            

def swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_Category_EcologicalStatus?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ["Country", "Year", "Surface Water Body Category", "Ecological Status Or Potential Value", "Number"]
    with open(
            working_directory + '8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        WDFCode = ["RW", "LW", "TW", "CW", "TeW"]
        swEcologicalStatusOrPotentialValue = ["1", "2", "3", "4", "5", "unknown"]
        cur = conn.cursor()

        for country in countryCode:
            for category in WDFCode:
                for value in swEcologicalStatusOrPotentialValue:
                    data = cur.execute('select countryCode, cYear, surfaceWaterBodyCategory, swEcologicalStatusOrPotentialValue, '
                                    'COUNT(surfaceWaterBodyCategory) '
                                    'from SOW_SWB_SurfaceWaterBody '
                                    'where cYear = ? and countryCode = ? '
                                    'and surfaceWaterBodyCategory <> "unpopulated" '
                                    'and surfaceWaterBodyCategory = ? '
                                    'and swEcologicalStatusOrPotentialValue = ? ', (cYear, country, category, value)).fetchall()
                    write.writerows(data)
                    

def swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SurfaceWaterBody/SWB_Category_EcologicalStatus?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ["Country", "Year", "Surface Water Body Category", "Ecological Status Or Potential Value", "Number"]
    with open(
            working_directory + '9.swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        WDFCode = ["RW", "LW", "TW", "CW"]
        swEcologicalStatusOrPotentialValue = ["unknown"]
        cur = conn.cursor()

        for country in countryCode:
            for category in WDFCode:
                for value in swEcologicalStatusOrPotentialValue:
                    data = cur.execute('select countryCode, cYear, surfaceWaterBodyCategory, swEcologicalStatusOrPotentialValue, '
                                    'COUNT(surfaceWaterBodyCategory) '
                                    'from SOW_SWB_SurfaceWaterBody '
                                    'where cYear = ? and countryCode = ? '
                                    'and surfaceWaterBodyCategory <> "unpopulated" '
                                    'and surfaceWaterBodyCategory = ? '
                                    'and swEcologicalStatusOrPotentialValue = ? ', (cYear, country, category, value)).fetchall()
                    write.writerows(data)
                    

def swEcologicalStatusOrPotentialChemical_by_Country(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '15.swEcologicalStatusOrPotential_by_Country2016.csv',
            'w+', newline='') as f:
        headers = ["Country", "Ecological Status Or Potential Value", "Number", "Number(%)"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('SELECT countryCode, swEcologicalStatusOrPotentialValue, '
                            'COUNT(swEcologicalStatusOrPotentialValue), '
                            'round(count(swEcologicalStatusOrPotentialValue) * 100.0 / ( '
                                'SELECT count(swEcologicalStatusOrPotentialValue) '
                            'FROM SOW_SWB_SurfaceWaterBody '
                                'WHERE cYear = ? '
                            'AND countryCode = ? '
                            'AND naturalAWBHMWB <> "Unpopulated" '
                            '), 0) '
                            'FROM SOW_SWB_SurfaceWaterBody '
                            'WHERE cYear = ? '
                            'AND naturalAWBHMWB <> "Unpopulated" '
                            'AND countryCode = ? '
                            'GROUP BY swEcologicalStatusOrPotentialValue; ', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)
    with open(
            working_directory + '15.swChemicalStatusValue_by_Country2016.csv',
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
                            'FROM SOW_SWB_SurfaceWaterBody '
                                'WHERE cYear = ? '
                            'AND countryCode = ? '
                            'AND naturalAWBHMWB <> "Unpopulated" '
                            '), 0) '
                            'FROM SOW_SWB_SurfaceWaterBody '
                            'WHERE cYear = ? '
                            'AND naturalAWBHMWB <> "Unpopulated" '
                            'AND countryCode = ? '
                            'GROUP BY swChemicalStatusValue; ', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_Status/SWB_Status_Country?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '15.swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ.csv',
            'w+', newline='') as f:
        headers = ['Country', 'Year', 'Categories', 'Ecological Status Value', 'Number', 'Number(%)']

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swEcologicalStatusOrPotentialValue = ["1", "2", "3", "4", "5", "unknown"]
        swEcologicalStatusCategories = ["RW", "LW", "CW", "TW", "TeW"]

        # for country in countryCode:
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
                                                                       FROM SOW_SWB_SurfaceWaterBody
                                                                      WHERE cYear = ? AND 
                                                                            countryCode = ? and
                                                                            naturalAWBHMWB <> "Unpopulated" AND 
                                                                            surfaceWaterBodyCategory <> "Unpopulated" and
                                                                            surfaceWaterBodyCategory = ?
                                                                 )
                                                       )
                                                  FROM SOW_SWB_SurfaceWaterBody
                                                 WHERE cYear = ? AND 
                                                       countryCode = ? AND 
                                                       surfaceWaterBodyCategory <> "Unpopulated" AND
                                                       swEcologicalStatusOrPotentialValue = ? and
                                                       naturalAWBHMWB <> "Unpopulated" AND 
                                                       surfaceWaterBodyCategory = ?
                                                       ''', (cYear, country, categ, cYear, country, status, categ)).fetchall()
                        write.writerows(data)
    with open(
            working_directory + '15.swChemicalStatusValue_by_Country_by_Categ2016.csv',
            'w+', newline='') as f:
        headers = ['Country', 'Year', 'Categories', 'Chemical Status Value', 'Number', 'Number(%)']

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        swChemicalStatusValue = ["2", "3", "unknown"]
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
                                                                           FROM SOW_SWB_SurfaceWaterBody
                                                                          WHERE cYear = ? AND 
                                                                                countryCode = ? and
                                                                                naturalAWBHMWB <> "Unpopulated" AND 
                                                                                surfaceWaterBodyCategory <> "Unpopulated" and
                                                                                surfaceWaterBodyCategory = ?
                                                                     )
                                                           )
                                                      FROM SOW_SWB_SurfaceWaterBody
                                                     WHERE cYear = ? AND 
                                                           countryCode = ? AND 
                                                           surfaceWaterBodyCategory <> "Unpopulated" AND
                                                           swChemicalStatusValue = ? and
                                                           naturalAWBHMWB <> "Unpopulated" AND 
                                                           surfaceWaterBodyCategory = ?
                                                           ''', (cYear, country, categ, cYear, country, status, categ)
                        ).fetchall()
                    write.writerows(data)


def Surface_water_bodies_Failing_notUnknown_by_RBD2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_Status_Maps/SWB_Status_RBD?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '17.Surface_water_bodies_Failing_notUnknown_by_RBD2016.csv',
            'w+', newline='') as f:
        header = ["Country",  "RBD Name", "Known Status", "Failing Status", "Failing Status(%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''select NUTS0, rbdName, C_StatusKnown, C_StatusFailing, 
                            C_StatusFailingPercent * 100 
                            from swRBD_Europe_data
                            where NUTS0 = "''' + country + '''" 
                            group by NUTS0, rbdName; ''').fetchall()
            
            write.writerows(data)


def swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Assessment Confidence", "Chemical Monitoring Results", "Number", "Number(%)"]
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
                                       'select count(swChemicalAssessmentConfidence) from SOW_SWB_SurfaceWaterBody '
                                       'where cYear == ? and countryCode = ? and swChemicalAssessmentConfidence = ?)) END '
                                    'from SOW_SWB_SurfaceWaterBody '
                                    'where cYear == ? '
                                        'and countryCode = ? '
                                        'and swChemicalAssessmentConfidence = ? '
                                        'and swChemicalMonitoringResults = ? ', (cYear, country, assessment, cYear,
                                                                                 country, assessment, monitoring)).fetchall()
                    write.writerows(data)
                    
def swRBsPollutants(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '40.swRBsPollutants.csv',
            'w+', newline='') as f:
        headers = ["Country", "River Basin Specific Pollutant", "Number", "Number(%)"]

        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()

        country = ''.join(countryCode)

        data = cur.execute('''SELECT countryCode,
                               swFailingRBSP,
                               count(euSurfaceWaterBodyCode),
                               round(count(euSurfaceWaterBodyCode) * 100 / (
                                                                               SELECT count(DISTINCT euSurfaceWaterBodyCode) 
                                                                                 FROM SOW_SWB_FailingRBSP
                                                                                WHERE countryCode = "''' + country + '''" AND 
                                                                                      cYear = 2016 AND 
                                                                                      swFailingRBSP <> "None"
                                                                           )
                               ) 
                          FROM SOW_SWB_FailingRBSP
                         WHERE countryCode = "''' + country + '''" AND
                               cYear = 2016 AND 
                               swFailingRBSP <> "None"
                         GROUP BY swFailingRBSP;''').fetchall()
            
        write.writerows(data)
            
def swEcologicalStatusOrPotentialExpectedGoodIn2015(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '44.swEcologicalStatusOrPotentialExpectedGoodIn2015.csv',
            'w+', newline='') as f:
        header = ["Country",  "Ecological Status Or Potential Expected Good In 2015", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        values = ["Yes", "No"]
        cur = conn.cursor()
        for country in countryCode:
            for value in values:
                data = cur.execute('''SELECT countryCode,
                                       swEcologicalStatusOrPotentialExpectedGoodIn2015,
                                       count(surfaceWaterBodyCategory),
                                       round(count(surfaceWaterBodyCategory) * 100.0 / (
                                                               SELECT count(surfaceWaterBodyCategory) 
                                                                 FROM SOW_SWB_SurfaceWaterBody
                                                                WHERE countryCode = ? AND 
                                                                      cYear = ? AND 
                                                                      naturalAWBHMWB <> "unpopulated" AND 
                                                                      swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                                                      swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                                      swEcologicalStatusOrPotentialExpectedGoodIn2015 <> "Unpopulated"
                                                           ), 0) 
                                  FROM SOW_SWB_SurfaceWaterBody
                                 WHERE surfaceWaterBodyCategory <> "unpopulated" AND 
                                       naturalAWBHMWB <> "unpopulated" AND 
                                       swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                       swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                       swEcologicalStatusOrPotentialExpectedGoodIn2015 <> "Unpopulated" AND 
                                       cYear == ? AND 
                                       countryCode = ? AND 
                                       swEcologicalStatusOrPotentialExpectedGoodIn2015 = ?;''', (country, cYear, cYear, country, value)).fetchall()
                write.writerows(data)
                
def swEcologicalStatusOrPotentialExpectedAchievementDate(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '45.swEcologicalStatusOrPotentialExpectedAchievementDate2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Ecological Status Or Potential Expected Achievement Date", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        swEcologicalStatusOrPotentialExpectedAchievementDate = [
            "Good status already achieved", "Less stringent objectives already achieved",
                "2016--2021", "2022--2027", "Beyond 2027", "Unknown"]
        cur = conn.cursor()
        for country in countryCode:
            for date in swEcologicalStatusOrPotentialExpectedAchievementDate:
                data = cur.execute('''SELECT countryCode,
                                       cYear,
                                       swEcologicalStatusOrPotentialExpectedAchievementDate,
                                       COUNT(euSurfaceWaterBodyCode),
                                       round(COUNT(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                         SELECT COUNT(euSurfaceWaterBodyCode) 
                                                                                           FROM SOW_SWB_SurfaceWaterBody
                                                                                          WHERE countryCode = ? AND 
                                                                                                cYear = ? AND 
                                                                                                naturalAWBHMWB <> "unpopulated" AND 
                                                                                                swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                                                                                swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                                                                swEcologicalStatusOrPotentialExpectedGoodIn2015 <> "Unpopulated"
                                                                                     ), 0) AS PERCENT
                                  FROM SOW_SWB_SurfaceWaterBody
                                 WHERE countryCode = ? AND 
                                        cYear = ? and
                                       naturalAWBHMWB <> "unpopulated" AND 
                                       swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                       swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                       swEcologicalStatusOrPotentialExpectedGoodIn2015 <> "Unpopulated" AND 
                                       swEcologicalStatusOrPotentialExpectedAchievementDate = ?;''', (country, cYear, country, cYear, date)).fetchall()
                write.writerows(data)


def swChemicalStatusExpectedGoodIn2015(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '46.swChemicalStatusExpectedGoodIn2015.csv',
            'w+', newline='') as f:
        header = ["Country",  "Chemical Status Expected Good In 2015", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        values = ["Yes", "No"]
        cur = conn.cursor()
        for country in countryCode:
            for value in values:
                data = cur.execute('''SELECT countryCode,
                                   swChemicalStatusExpectedGoodIn2015,
                                   count(surfaceWaterBodyCategory) as a,
                                   round(count(surfaceWaterBodyCategory) * 100.0 / (
                                                           SELECT count(surfaceWaterBodyCategory) 
                                                             FROM SOW_SWB_SurfaceWaterBody
                                                            WHERE countryCode = ? AND 
                                                                  cYear == ? AND 
                                                                  surfaceWaterBodyCategory <> "unpopulated" AND 
                                                                  swChemicalStatusValue <> "Unpopulated" and
                                                                  swChemicalStatusExpectedGoodIn2015 <> "Unpopulated"
                                                       )
                                       ) 
                                  FROM SOW_SWB_SurfaceWaterBody
                                 WHERE surfaceWaterBodyCategory <> "Unpopulated" AND 
                                       swChemicalStatusValue <> "Unpopulated" AND 
                                       cYear == ? AND 
                                       countryCode = ? AND 
                                       swChemicalStatusExpectedGoodIn2015 = ?;''', (country, cYear, cYear, country, value)).fetchall()
                write.writerows(data)


def swChemicalStatusExpectedAchievementDate(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '47.swChemicalStatusExpectedAchievementDate2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Expected Achievement Date", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        swChemicalStatusExpectedAchievementDate = [
            "Good status already achieved", "Less stringent objectives already achieved",
            "2016--2021", "2022--2027", "Beyond 2027", "Unknown"]
        cur = conn.cursor()
        for country in countryCode:
            for date in swChemicalStatusExpectedAchievementDate:
                data = cur.execute('''select countryCode, cYear, swChemicalStatusExpectedAchievementDate, COUNT( 
                                swChemicalStatusExpectedAchievementDate), 
                                round(COUNT(swChemicalStatusExpectedAchievementDate) * 100.0 / 
                                (select COUNT(swChemicalStatusExpectedAchievementDate) 
                                from SOW_SWB_SurfaceWaterBody 
                                where countryCode = "''' + country + '''"
                                and cYear == ''' + str(cYear) + '''
                                and swChemicalStatusExpectedAchievementDate <> "Unpopulated"), 0) 
                                from SOW_SWB_SurfaceWaterBody 
                                where countryCode = "''' + country + '''"
                                and cYear == ''' + str(cYear) + '''
                                and swChemicalStatusExpectedAchievementDate <> "Unpopulated"
                                and swChemicalStatusExpectedAchievementDate = "''' + date + '''"; ''').fetchall()
                write.writerows(data)


def GroundWaterBodyCategory2016(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '2.GroundWaterBodyCategory2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Number", "Number(%)", "Area (km^2)", "Area(%)", "Median Area (km^2)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        country = ''.join(countryCode)

        dropMedianArea = '''DROP TABLE IF EXISTS GWMedian;'''

        MedianArea = '''CREATE TEMPORARY TABLE GWMedian AS SELECT countryCode,
                                          cYear,
                                          round(AVG(cArea), 1) AS median
                                     FROM (
                                              SELECT countryCode,
                                                     cYear,
                                                     cArea
                                                FROM SOW_GWB_GroundWaterBody
                                               WHERE countryCode = "''' + country + '''" AND 
                                                     countryCode IS NOT NULL AND 
                                                     cArea IS NOT NULL AND 
                                                     cYear = ''' + str(cYear) + '''
                                               ORDER BY cArea
                                               LIMIT 2 - (
                                                             SELECT COUNT( * ) 
                                                               FROM SOW_GWB_GroundWaterBody
                                                              WHERE countryCode = "''' + country + '''" AND 
                                                                    countryCode IS NOT NULL AND 
                                                                    cArea IS NOT NULL AND 
                                                                    cYear = ''' + str(cYear) + '''
                                                         )
                                              %      2 OFFSET (
                                                         SELECT (COUNT( * ) - 1) / 2
                                                           FROM SOW_GWB_GroundWaterBody
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
                       round(count(groundWaterBodyName) * 100.0 / (
                                                                      SELECT round(count(groundWaterBodyName) ) 
                                                                        FROM SOW_GWB_GroundWaterBody
                                                                        where cYear = ''' + str(cYear) + '''
                                                                  )
                       ,1),
                       round(sum(cArea) ),
                       round(sum(cArea) * 100.0 / (
                                                      SELECT round(sum(cArea) )
                                                        FROM SOW_GWB_GroundWaterBody
                                                        where cYear = ''' + str(cYear) + '''
                                                  )
                       ,1),
                       (
                           SELECT median
                             FROM GWMedian
                       )
                  FROM SOW_GWB_GroundWaterBody
                 WHERE cYear = ''' + str(cYear) + ''' AND 
                       countryCode = "''' + country + '''";
                '''
        cur.execute(dropMedianArea)
        cur.execute(MedianArea)
        data = cur.execute(final).fetchall()

        write.writerows(data)


def Groundwater_bodies_Chemical_Exemption_Type(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_GWP_GWChemicalExemptionType/GWB_GWP_GWChemicalExemptionType?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '7.Groundwater_bodies_Chemical_Exemption_Type2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Chemical Exemption Type Group", "Chemical Exemption Type", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        gwChemicalExemptionTypeGroup = cur.execute('''select distinct gwChemicalExemptionTypeGroup
                                                        from SOW_GWB_GWP_GWChemicalExemptionType
                                                        where gwChemicalExemptionTypeGroup <> "Unpopulated"
                                                        and gwChemicalExemptionTypeGroup <> "GWD Article 6(3)"
                                                        and gwChemicalExemptionTypeGroup <> "Article4(6)"
                                                        and gwChemicalExemptionTypeGroup <> "Article4(7)";
                                        ''').fetchall()

        gwChemicalExemptionType = cur.execute('''select distinct gwChemicalExemptionType
                                                from SOW_GWB_GWP_GWChemicalExemptionType
                                                where gwChemicalExemptionType <> "Unpopulated" AND
                                                gwChemicalExemptionType <> "GWD Article 6(3) - Measures: increased risk" AND
                                                gwChemicalExemptionType <> "GWD Article 6(3) - Measures: disproportionate cost";''').fetchall()

        for country in countryCode:
            for chgroup in gwChemicalExemptionTypeGroup:
                for chtype in gwChemicalExemptionType:
                    tempgroup = ','.join(chgroup)
                    temptype = ','.join(chtype)
                    sqlDropValues = '''DROP TABLE IF EXISTS DistinctValues;'''

                    sqlDistinct = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euGroundWaterBodyCode,
                                                             cArea AS A
                                               FROM SOW_GWB_GWP_GWChemicalExemptionType
                                              WHERE cYear = ''' + str(cYear) + ''' AND 
                                                    countryCode = "''' + country + '''" AND 
                                                    gwChemicalStatusValue <> "2" AND 
                                                    gwChemicalStatusValue <> "missing" AND 
                                                    gwChemicalStatusValue <> "unpopulated" AND 
                                                    gwChemicalExemptionTypeGroup = "''' + tempgroup + '''" AND 
                                                    gwChemicalExemptionType = "''' + temptype + '''";'''

                    sqlDropArea = '''DROP TABLE IF EXISTS DistinctArea;'''

                    sqlArea = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euGroundWaterBodyCode,
                                                       cArea AS G
                                         FROM SOW_GWB_GWP_GWChemicalExemptionType
                                        WHERE cYear = ''' + str(cYear) + ''' AND 
                                              countryCode = "''' + country + '''" AND 
                                              gwChemicalStatusValue <> "2" AND 
                                              gwChemicalStatusValue <> "missing" AND 
                                              gwChemicalStatusValue <> "unpopulated" AND 
                                              gwChemicalExemptionTypeGroup <> "Unpopulated" AND 
                                              gwChemicalExemptionTypeGroup <> "GWD Article 6(3)" AND 
                                              gwChemicalExemptionTypeGroup <> "Article4(6)" AND 
                                              gwChemicalExemptionTypeGroup <> "Article4(7)" AND
                                              gwChemicalStatusValue <> "unpopulated" AND 
                                              gwChemicalExemptionTypeGroup = "''' + tempgroup + '''";'''

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
                              FROM SOW_GWB_GWP_GWChemicalExemptionType
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   countryCode = "''' + country + '''" AND 
                                   gwChemicalStatusValue <> "2" AND 
                                   gwChemicalStatusValue <> "missing" AND 
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


def Groundwater_bodies_Quantitative_Exemption_Type(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_gwQuantitativeExemptionType/GWB_gwQuantitativeExemptionType?:isGuestRedirectFromVizportal=y&:embed=y
    with open(
            working_directory + '7.Groundwater_bodies_Quantitative_Exemption_Type2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Quantitative Exemption Type Group", "Quantitative Exemption Type", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()

        country = ''.join(countryCode)

        gwQuantitativeExemptionTypeGroup = cur.execute('''select distinct gwQuantitativeExemptionTypeGroup 
                                from SOW_GWB_gwQuantitativeExemptionPressure 
                                where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        gwQuantitativeExemptionType = cur.execute('''select distinct gwQuantitativeExemptionType
                                from SOW_GWB_gwQuantitativeExemptionPressure 
                                where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        gwQuantitativeExemptionPressureGroup = cur.execute('''select distinct gwQuantitativeExemptionPressureGroup
                                from SOW_GWB_gwQuantitativeExemptionPressure 
                                where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        gwQuantitativeExemptionPressure = cur.execute('''select distinct gwQuantitativeExemptionPressure
                                        from SOW_GWB_gwQuantitativeExemptionPressure 
                                        where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        for temp1 in gwQuantitativeExemptionTypeGroup:
            for temp2 in gwQuantitativeExemptionType:
                for temp3 in gwQuantitativeExemptionPressureGroup:
                    for temp4 in gwQuantitativeExemptionPressure:
                        gwcetg = ''.join(temp1)
                        gwcet = ''.join(temp2)
                        gwcepg = ''.join(temp3)
                        gwcep = ''.join(temp4)

                        droptable = '''DROP TABLE IF EXISTS distinctvalues;'''

                        createtable = '''CREATE TEMPORARY TABLE IF NOT EXISTS distinctvalues AS SELECT DISTINCT countryCode,
                                                                                       euGroundWaterBodyCode,
                                                                                       cArea
                                                                         FROM SOW_GWB_gwQuantitativeExemptionPressure
                                                                        WHERE countryCode = "''' + country + '''" AND 
                                                                              cYear = 2016 AND 
                                                                              gwQuantitativeExemptionTypeGroup = "''' + gwcetg + '''" AND 
                                                                              gwQuantitativeExemptionType = "''' + gwcet + '''" AND 
                                                                              gwQuantitativeExemptionPressureGroup = "''' + gwcepg + '''" AND 
                                                                              gwQuantitativeExemptionPressure = "''' + gwcep + '''";'''

                        data = '''SELECT countryCode,
                                   gwQuantitativeExemptionTypeGroup,
                                   gwQuantitativeExemptionType,
                                   gwQuantitativeExemptionPressureGroup,
                                   gwQuantitativeExemptionPressure,
                                   (
                                       SELECT round(sum(cArea) ) 
                                         FROM distinctvalues
                                   )
                              FROM SOW_GWB_gwQuantitativeExemptionPressure
                             WHERE countryCode = "''' + country + '''" AND 
                                   cYear = 2016 AND 
                                   gwQuantitativeExemptionTypeGroup = "''' + gwcetg +'''" AND 
                                   gwQuantitativeExemptionType = "''' + gwcet + '''" AND 
                                   gwQuantitativeExemptionPressureGroup = "''' + gwcepg + '''" AND 
                                   gwQuantitativeExemptionPressure = "''' + gwcep + '''"
                             GROUP BY gwQuantitativeExemptionTypeGroup,
                                   gwQuantitativeExemptionType,
                                   gwQuantitativeExemptionPressureGroup,
                                   gwQuantitativeExemptionPressure;'''

                        cur.execute(droptable)
                        cur.execute(createtable)
                        alldata = cur.execute(data).fetchall()
                        write.writerows(alldata)
            

def gwChemical_exemptions_and_pressures(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_GWP_GWChemicalExemptionPressure/GWB_GWP_GWC_gwChemicalExemptionPressure?:isGuestRedirectFromVizportal=y&:embed=y
    with open(working_directory + '7.gwChemical_exemptions_and_pressures.csv', 'w+', newline='') as f:
        header = ["Country",  "Chemical Exemption Type Group", "Chemical Exemption Type", "Chemical Pressure Type Group", "Chemical Pressure Type", "Area (km^2)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()

        country = ''.join(countryCode)
        gwChemicalExemptionTypeGroup = cur.execute('''select distinct gwChemicalExemptionTypeGroup 
                                from SOW_GWB_GWP_GWC_gwChemicalExemptionPressure 
                                where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        gwChemicalExemptionType = cur.execute('''select distinct gwChemicalExemptionType
                                from SOW_GWB_GWP_GWC_gwChemicalExemptionPressure 
                                where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        gwChemicalExemptionPressureGroup = cur.execute('''select distinct gwChemicalExemptionPressureGroup
                                from SOW_GWB_GWP_GWC_gwChemicalExemptionPressure 
                                where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        gwChemicalExemptionPressure = cur.execute('''select distinct gwChemicalExemptionPressure
                                        from SOW_GWB_GWP_GWC_gwChemicalExemptionPressure 
                                        where countryCode = "''' + country + '''" and cYear = 2016''').fetchall()

        for temp1 in gwChemicalExemptionTypeGroup:
            for temp2 in gwChemicalExemptionType:
                for temp3 in gwChemicalExemptionPressureGroup:
                    for temp4 in gwChemicalExemptionPressure:
                        gwcetg = ''.join(temp1)
                        gwcet = ''.join(temp2)
                        gwcepg = ''.join(temp3)
                        gwcep = ''.join(temp4)
                        droptable = '''DROP TABLE IF EXISTS distinctvalues;'''

                        createtable = '''CREATE TEMPORARY TABLE IF NOT EXISTS distinctvalues AS SELECT DISTINCT countryCode,
                                                                                       euGroundWaterBodyCode,
                                                                                       cArea
                                                                         FROM SOW_GWB_GWP_GWC_gwChemicalExemptionPressure
                                                                        WHERE countryCode = "''' + country + '''" AND 
                                                                              cYear = 2016 AND 
                                                                              gwChemicalExemptionTypeGroup = "''' + gwcetg + '''" AND 
                                                                              gwChemicalExemptionType = "''' + gwcet + '''" AND 
                                                                              gwChemicalExemptionPressureGroup = "''' + gwcepg + '''" AND 
                                                                              gwChemicalExemptionPressure = "''' + gwcep + '''";'''

                        data = '''SELECT countryCode,
                                       gwChemicalExemptionTypeGroup,
                                       gwChemicalExemptionType,
                                       gwChemicalExemptionPressureGroup,
                                       gwChemicalExemptionPressure,
                                       (
                                           SELECT round(sum(cArea) )
                                             FROM distinctvalues
                                       )
                                  FROM SOW_GWB_GWP_GWC_gwChemicalExemptionPressure
                                 WHERE countryCode = "''' + country + '''" AND 
                                       cYear = 2016 AND 
                                       gwChemicalExemptionTypeGroup = "''' + gwcetg + '''" AND 
                                       gwChemicalExemptionType = "''' + gwcet + '''" AND 
                                       gwChemicalExemptionPressureGroup = "''' + gwcepg + '''" AND 
                                       gwChemicalExemptionPressure = "''' + gwcep + '''"
                                       group by gwChemicalExemptionTypeGroup,
                                       gwChemicalExemptionType,
                                       gwChemicalExemptionPressureGroup,
                                       gwChemicalExemptionPressure;'''
                        cur.execute(droptable)
                        cur.execute(createtable)
                        alldata = cur.execute(data).fetchall()

                        write.writerows(alldata)
            

def Groundwater_bodies_Quantitative_exemptions_and_pressures(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_gwQuantitativeExemptionPressure/GWB_gwQuantitativeExemptionPressure?:isGuestRedirectFromVizportal=y&:embed=y
    with open(
            working_directory + '7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Exemption Type Group", "Quantitative Exemption Type", "Quantitative Exemption Pressure Group",
                  "Quantitative Exemption Pressure", "Area (km^2)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''select countryCode, cYear, gwQuantitativeExemptionTypeGroup, gwQuantitativeExemptionType, 
                                gwQuantitativeExemptionPressureGroup, 
                                gwQuantitativeExemptionPressure, round(sum(cArea)) 
                                from SOW_GWB_gwQuantitativeExemptionPressure 
                                    where cYear = 2016 and
                                    countryCode = "''' + country + '''" 
                                        group by countryCode, gwQuantitativeExemptionTypeGroup, gwQuantitativeExemptionType, 
                                        gwQuantitativeExemptionPressureGroup, 
                                        gwQuantitativeExemptionPressure;'''
                               ).fetchall()
            
            write.writerows(data)


def SOW_GWB_GroundWaterBody_GWB_Chemical_status(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '20.GroundWaterBodyCategoryChemical_status2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Area (km^2)", "Area (%)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        chemicalStatus = ["2", "3", "unknown"]
        for country in countryCode:
            for status in chemicalStatus:
                data = cur.execute('''SELECT DISTINCT countryCode,
                                    cYear,
                                    gwChemicalStatusValue,
                                    ROUND(SUM(cArea), 0),
                                    round(sum(cArea) * 100.0 / (
                                                                   SELECT sum(cArea) 
                                                                     FROM SOW_GWB_GroundWaterBody
                                                                    WHERE countryCode = ? AND 
                                                                          cYear = ?
                                                               ),1
                                    ),COUNT(DISTINCT euGroundWaterBodyCode)  
                                      FROM SOW_GWB_GroundWaterBody
                                     WHERE countryCode = ? AND 
                                           gwChemicalStatusValue = ? AND 
                                           cYear = ?;''', (country, cYear, country, status, cYear)).fetchall()

                write.writerows(data)
                

def SOW_GWB_GroundWaterBody_GWB_Quantitative_status(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '18.GroundWaterBodyCategoryQuantitative_status2016.csv', 'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Area (km^2)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        QuantitativeStatus = ["2", "3", "unknown"]
        for country in countryCode:
            for status in QuantitativeStatus:
               data = cur.execute('SELECT DISTINCT countryCode, cYear, gwQuantitativeStatusValue, ROUND(SUM(cArea)), COUNT(DISTINCT euGroundWaterBodyCode) '
                                  'FROM SOW_GWB_GroundWaterBody '
                                'WHERE countryCode = ? '
                                'and gwQuantitativeStatusValue = ? '
                                'and cYear == ?', (country, status, cYear)).fetchall()
               write.writerows(data)
               

def gwQuantitativeStatusValue_gwChemicalStatusValue(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_Status/GWB_Status_Country?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '22.gwQuantitativeStatusValue_Percent_Country_2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        gwQuantitativeStatusValue = ["2", "3", "unknown"]
        for country in countryCode:
            for value in gwQuantitativeStatusValue:
                data = cur.execute('select countryCode,cYear, gwQuantitativeStatusValue, round(sum(cArea)), round(sum(cArea) * 100.0 / ('
                                   'select sum(cArea) from SOW_GWB_GroundWaterBody '
                                   'where cYear = ? and countryCode = ?)) '
                                'from SOW_GWB_GroundWaterBody '
                                'where cYear = ? '
                                'and countryCode = ?'
                                'and gwQuantitativeStatusValue = ? ', (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)

    with open(
            working_directory + '22.gwChemicalStatusValue_Percent_Country_2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Area (km^2)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        gwChemicalStatusValue = ["2", "3", "unknown"]
        for country in countryCode:
            for value in gwChemicalStatusValue:
                data = cur.execute('select countryCode, cYear, gwChemicalStatusValue, round(sum(cArea) * 100.0 / ( '
                                   'select sum(cArea) from SOW_GWB_GroundWaterBody '
                                   'where cYear = ? and countryCode = ?)) '
                                'from SOW_GWB_GroundWaterBody '
                                'where cYear = ? '
                                'and countryCode = ?'
                                'and gwChemicalStatusValue = ? ', (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)
                

def Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Area (km^2)", "Area (%)", "Number"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        gwAtRiskQuantitative = ["Yes", "No"]
        for country in countryCode:
            for status in gwAtRiskQuantitative:
                data = cur.execute('select countryCode, cYear,gwAtRiskQuantitative, round(sum(cArea),0), '
                                'round(sum(cArea) * 100 / (select sum(cArea) from SOW_GWB_GroundWaterBody ' 
                                    'where countryCode = ? ' 
                                    'AND cYear == ?'
                                    'and gwEORiskQuantitative <> "Not in WFD2010" '
                                    'and gwEORiskQuantitative <> "None" '
                                    'and gwEORiskQuantitative <> "Unpopulated" '
                                    'and gwAtRiskQuantitative <> "Unpopulated" '
                                    'and gwQuantitativeStatusValue <> "unpopulated"),0),'
                                'count(DISTINCT euGroundWaterBodyCode)  '
                                'from SOW_GWB_GroundWaterBody '
                                    'where cYear == ? '
                                        'and gwEORiskQuantitative <> "Not in WFD2010" '
                                        'and gwEORiskQuantitative <> "None" '
                                        'and gwEORiskQuantitative <> "Unpopulated" '
                                        'and gwAtRiskQuantitative <> "Unpopulated" '
                                        'and gwAtRiskQuantitative = ? '
                                        'and gwQuantitativeStatusValue <> "unpopulated" '
                                        'and countryCode = ? ', (country, cYear, cYear, status, country)).fetchall()

                write.writerows(data)


def SOW_GWB_gwQuantitativeReasonsForFailure_Table(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Value", "Quantitative Reasons For Failure", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        reasonOfFailure = ["Good status already achieved", "Water balance / Lowering water table", "Saline or other intrusion",
                           "Dependent terrestrial ecosystems", "Associated surface waters"]
        cur = conn.cursor()
        for country in countryCode:
            for types in reasonOfFailure:
                data = cur.execute('select countryCode, cYear, gwQuantitativeStatusValue, gwQuantitativeReasonsForFailure, '
                                'round(sum(cArea), 0), round(sum(cArea) * 100 / ('
                                'select sum(cArea) from SOW_GWB_GroundWaterBody '
                                'where countryCode = ? and cYear == ? ' 
                                'and gwAssociatedProtectedArea <> "unpopulated" ' 
                                'and gwQuantitativeStatusValue = "3")) ' 
                                'from SOW_GWB_gwQuantitativeReasonsForFailure '
                                'where cYear == ? ' 
                                'and gwQuantitativeReasonsForFailure <> "unpopulated" '
                                'and gwQuantitativeStatusValue = "3" '
                                'and countryCode = ? '
                                'and gwQuantitativeReasonsForFailure = ?', (country, cYear, cYear, country, types)).fetchall()

                write.writerows(data)


def SOW_GWB_gwChemicalReasonsForFailure_Table(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '26.gwChemicalReasonsForFailure_Table2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Chemical Reasons For Failure", 'Area (km^2)', "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        for country in countryCode:
            droptable = '''DROP TABLE IF EXISTS tempvalues;'''

            createtable = '''CREATE TABLE tempvalues AS SELECT DISTINCT countryCode,
                                       euGroundWaterBodyCode,
                                       cArea
                         FROM SOW_GWB_gwChemicalReasonsForFailure
                        WHERE cYear = 2016 AND 
                              countryCode = "''' + country + '''" AND 
                              gwChemicalStatusValue = 3;'''


            data = '''SELECT countryCode,
                               cYear,
                               gwChemicalStatusValue,
                               gwChemicalReasonsForFailure,
                               round(sum(cArea) ),
                               round(sum(cArea)  * 100 / (
                                                  SELECT sum(cArea) 
                                                    FROM tempvalues
                                            ))
                          FROM SOW_GWB_gwChemicalReasonsForFailure
                         WHERE countryCode = "''' + country + '''" AND 
                               cYear == 2016 AND 
                               gwAtRiskChemical <> "Annex 0" AND 
                               gwAtRiskChemical <> "unpopulated" AND 
                               gwChemicalStatusValue = 3;'''

            cur.execute(droptable)
            cur.execute(createtable)
            alldata = cur.execute(data).fetchall()
            write.writerows(alldata)
                

def gwChemicalStatusValue_Table(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '26.gwChemicalStatusValue_Table2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Value", "Area (km^2)", "Area (%)", "Number"]
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
                                                                      FROM SOW_GWB_GroundWaterBody
                                                                     WHERE countryCode = ? AND 
                                                                           cYear == ?
                                                                ), 0),
                                        COUNT(DISTINCT euGroundWaterBodyCode) 
                                  FROM SOW_GWB_GroundWaterBody
                                 WHERE cYear = ? AND 
                                       gwEORiskChemical <> "unpopulated" AND 
                                       gwEORiskChemical <> "Not in WFD2010" AND 
                                       gwAtRiskChemical <> "Not in WFD2010" AND 
                                       gwAtRiskChemical <> "unpopulated" AND 
                                       gwChemicalStatusValue <> "unpopulated" AND 
                                       countryCode = ? AND 
                                       gwAtRiskChemical = ?;
                ''', (country, cYear, cYear, country, risk)).fetchall()
                write.writerows(data)


def gwQuantitativeStatusExpectedGoodIn2015(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '29.gwQuantitativeStatusExpectedGoodIn2015.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Expected Good In 2015", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        gwQuantitativeStatusExpectedGoodIn2015 = ["Yes", "No"]

        for country in countryCode:
            for status in gwQuantitativeStatusExpectedGoodIn2015:
                data = cur.execute('''SELECT countryCode,
                                   cYear,
                                   gwQuantitativeStatusExpectedGoodIn2015,
                                   round(sum(cArea), 0),
                                   round(sum(cArea) * 100 / (
                                                                SELECT sum(cArea) 
                                                                  FROM SOW_GWB_GroundWaterBody
                                                                 WHERE countryCode = ? AND 
                                                                       cYear = ? AND 
                                                                       gwQuantitativeStatusValue <> "Unpopulated" AND 
                                                                       gwQuantitativeStatusExpectedGoodIn2015 <> "Unpopulated"
                                                            ), 0) 
                              FROM SOW_GWB_GroundWaterBody
                             WHERE countryCode = ? AND 
                                   gwQuantitativeStatusExpectedGoodIn2015 = ? AND 
                                   gwQuantitativeStatusValue <> "Unpopulated" AND 
                                   gwQuantitativeStatusExpectedGoodIn2015 <> "Unpopulated" AND 
                                   cYear = ? ;

                                     ''', (country, cYear, country, status, cYear)).fetchall()
                write.writerows(data)
                

def gwQuantitativeStatusExpectedAchievementDate(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '30.gwQuantitativeStatusExpectedAchievementDate2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Status Expected Date", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        gwQuantitativeStatusExpectedAchievementDate = [
            "Good status already achieved", "Less stringent objectives already achieved",
            "2016--2021", "2022--2027", "Beyond 2027", "Unknown"]

        for country in countryCode:
            for date in gwQuantitativeStatusExpectedAchievementDate:
                data = cur.execute('select countryCode, cYear, gwQuantitativeStatusExpectedAchievementDate, round(sum(cArea),0), round(sum(cArea) * 100 / '
                                   '(select sum(cArea) from SOW_GWB_GroundWaterBody where countryCode = ? and cYear = ?),0) '
                                    'from SOW_GWB_GroundWaterBody '
                                    'where countryCode = ? and cYear == ? '
                                    'and gwQuantitativeStatusExpectedAchievementDate <> "unpopulated" '
                                    'and gwQuantitativeStatusExpectedAchievementDate = ? ', (country, cYear, country, cYear, date)).fetchall()
                write.writerows(data)


def gwChemicalStatusExpectedGoodIn2015(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '31.gwChemicalStatusExpectedGoodIn2015.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Expected Achievement Date", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        gwQuantitativeStatusExpectedAchievementDate = ["Yes", "No"]
        cur = conn.cursor()
        for country in countryCode:
            for types in gwQuantitativeStatusExpectedAchievementDate:
                data = cur.execute('select countryCode, cYear, gwChemicalStatusExpectedGoodIn2015, round(sum(cArea),0), '
                                'round(sum(cArea) * 100 / (select sum(cArea) '
                                'from SOW_GWB_GroundWaterBody where ' 
                                'cYear == ? and countryCode = ?),0) '
                                'from SOW_GWB_GroundWaterBody '
                                'where cYear == ? '
                                'and gwChemicalStatusValue <> "unpopulated" '
                                'and countryCode = ? '
                                'and gwChemicalStatusExpectedGoodIn2015 = ? ', (cYear, country, cYear, country, types)).fetchall()
                write.writerows(data)
                

def gwChemicalStatusExpectedAchievementDate(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '32.gwChemicalStatusExpectedAchievementDate2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Status Expected Achievement Date", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        gwQuantitativeStatusExpectedAchievementDate = [
            "Good status already achieved", "Less stringent objectives already achieved",
            "2016--2021", "2022--2027", "Beyond 2027", "Unknown"]
        cur = conn.cursor()
        for country in countryCode:
            for date in gwQuantitativeStatusExpectedAchievementDate:
                data = cur.execute('select countryCode, cYear, gwChemicalStatusExpectedAchievementDate, round(sum(cArea),0), round(sum(cArea) * 100 / '
                                   '(select sum(cArea) from SOW_GWB_GroundWaterBody where countryCode = ? and cYear = ?),0) '
                                    'from SOW_GWB_GroundWaterBody '
                                    'where countryCode = ? and cYear == ? '
                                    'and gwChemicalStatusExpectedAchievementDate <> "unpopulated" '
                                    'and gwChemicalStatusExpectedAchievementDate = ? ', (country, cYear, country, cYear, date)).fetchall()
                write.writerows(data)
                

def gwQuantitativeAssessmentConfidence(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '35.gwQuantitativeAssessmentConfidence2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Quantitative Assessment Confidence", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        gwQuantitativeAssessmentConfidence = ["High", "Medium", "Low", "Unknown"]

        cur = conn.cursor()
        for country in countryCode:
            for value in gwQuantitativeAssessmentConfidence:
                data = cur.execute('select countryCode, cYear, gwQuantitativeAssessmentConfidence, round(sum(cArea),0), '
                            'round(sum(cArea) * 100 / (select sum(cArea) '
                            'from SOW_GWB_GroundWaterBody where ' 
                            'cYear == ? and countryCode = ?),0) '
                            'from SOW_GWB_GroundWaterBody '
                            'where cYear == ? and countryCode = ? '
                            'and gwQuantitativeAssessmentConfidence <> "unpopulated" '
                            'and gwQuantitativeAssessmentConfidence = ? ', (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)


def gwChemicalAssessmentConfidence(conn, countryCode, cYear, working_directory):
    with open(
            working_directory + '36.gwChemicalAssessmentConfidence2016.csv', 'w+', newline='') as f:
        header = ["Country", "Year", "Chemical Assessment Confidence", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        gwChemicalAssessmentConfidence = ["High", "Medium", "Low", "Unknown"]
        cur = conn.cursor()
        for country in countryCode:
            for value in gwChemicalAssessmentConfidence:
                data = cur.execute('select countryCode, cYear, gwChemicalAssessmentConfidence, round(sum(cArea),0), '
                            'round(sum(cArea) * 100 / (select sum(cArea) '
                            'from SOW_GWB_GroundWaterBody where ' 
                            'cYear == ? and countryCode = ?),0) '
                            'from SOW_GWB_GroundWaterBody '
                            'where cYear == ? and countryCode = ? '
                            'and gwChemicalAssessmentConfidence <> "unpopulated" '
                            'and gwChemicalAssessmentConfidence = ? ', (cYear, country, cYear, country, value)).fetchall()
                write.writerows(data)
           

def Number_of_groundwater_bodies_failing_to_achieve_good_status(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_GWP_GWChemicalExemptionPressure/GWB_GWP_GWC_gwChemicalExemptionPressure?:isGuestRedirectFromVizportal=y&:embed=y
    with open(
            working_directory + '37.Number_of_groundwater_bodies_failing_to_achieve_good_status.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Good", "Failing", "Number"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                   cYear,
                   count(CASE WHEN gwChemicalStatusValue = 2 and 
                             gwQuantitativeStatusValue = 2 THEN euGroundWaterBodyCode END) as Good,
                   count(CASE WHEN gwChemicalStatusValue = 3 OR 
                             gwQuantitativeStatusValue = 3 THEN euGroundWaterBodyCode END) as Failing,
                   count(distinct euGroundWaterBodyCode) as Total
              FROM SOW_GWB_GroundWaterBody 
             WHERE cYear = ''' + str(cYear) + ''' AND 
                   countryCode = "''' + country + '''";''').fetchall()

            write.writerows(data)


def geologicalFormation(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GroundWaterBody/GWB_Category?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '38.GWB_geologicalFormation2016.csv',
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
                                   'from SOW_GWB_GroundWaterBody where '
                                   'geologicalFormation = ? '
                                   'and countryCode = ? '
                                   'and cYear == ? '
                                   'and gwQuantitativeStatusValue <> "unknown" '
                                   'and geologicalFormation <> "Missing" '
                                   'and geologicalFormation <> "Unknown" '
                                   'and geologicalFormation <> "Insignificant aquifers - local and limited groundwater" '
                                   'and geologicalFormation <> "unpopulated" '
                                   'and countryCode = ? ', (value, country, cYear, country)).fetchall()
                
                write.writerows(data)
                

def swNumber_of_Impacts_by_country(conn, countryCode, cYear, working_directory):
    headers = ['Country', 'Year',
               'Impact 0 - Number', 'Impact 0 - Number (%)',
               'Impact 1 - Number', 'Impact 1 - Number (%)',
               'Impact 2 - Number', 'Impact 2 - Number (%)',
               'Impact 3 - Number', 'Impact 3 - Number (%)',
               'Impact 4+ - Number', 'Impact 4+ - Number (%)'
               ]
    with open(
            working_directory + 'NewDash.7.swNumber_of_impacts_by_country_2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            dropNoneValues = '''DROP TABLE IF EXISTS NoneValues;'''

            createNoneValues = '''CREATE TEMPORARY TABLE NoneValues AS SELECT countryCode,
                                            cYear,
                                            euSurfaceWaterBodyCode,
                                            CASE WHEN swSignificantImpactType = "None" THEN count(DISTINCT swSignificantImpactType) END AS NoneCounter
                                       FROM SOW_SWB_SWB_swSignificantImpactType
                                      WHERE countryCode = "''' + country + '''" AND 
                                            cYear = 2016 
                                      GROUP BY euSurfaceWaterBodyCode;'''

            dropVal = '''DROP TABLE IF EXISTS val;'''

            createVal = '''CREATE TEMPORARY TABLE val AS SELECT countryCode,
                                     cYear,
                                     euSurfaceWaterBodyCode,
                                     swSignificantImpactType,
                                     CASE WHEN swSignificantImpactType <> "None" THEN count(swSignificantImpactType) END AS Counter
                                FROM SOW_SWB_SWB_swSignificantImpactType
                               WHERE countryCode = "''' + country + '''" AND 
                                     cYear = 2016
                               GROUP BY euSurfaceWaterBodyCode; '''

            dropVal1 = '''DROP TABLE IF EXISTS val1;'''

            createVal1 = '''CREATE TEMPORARY TABLE val1 AS SELECT countryCode,
                                      cYear,
                                      (select count(NoneCounter) from NoneValues) AS t0,
                                      CASE WHEN Counter = 1 THEN count(DISTINCT euSurfaceWaterBodyCode) END AS t1,
                                      CASE WHEN Counter = 2 THEN count(DISTINCT euSurfaceWaterBodyCode) END AS t2,
                                      CASE WHEN Counter = 3 THEN count(DISTINCT euSurfaceWaterBodyCode) END AS t3,
                                      CASE WHEN Counter >= 4 THEN count(DISTINCT euSurfaceWaterBodyCode) END AS t4
                                 FROM val
                                GROUP BY Counter;'''

            final = '''SELECT countryCode,
                           cYear,
                           sum(distinct t0),
                           round(sum(distinct t0) * 100.0 / (
                                                       SELECT total(distinct t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                                         FROM val1
                                                   )
                           ),
                           round(sum(t1) ),
                           round(sum(t1) * 100.0 / (
                                                       SELECT total( distinct t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                                         FROM val1
                                                   )
                           ),
                           round(sum(t2) ),
                           round(sum(t2) * 100.0 / (
                                                       SELECT total( distinct t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                                         FROM val1
                                                   )
                           ),
                           round(sum(t3) ),
                           round(sum(t3) * 100.0 / (
                                                       SELECT total( distinct t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                                         FROM val1
                                                   )
                           ),
                           round(sum(t4) ),
                           round(sum(t4) * 100.0 / (
                                                       SELECT total( distinct t0) + total(t1) + total(t2) + total(t3) + total(t4) 
                                                         FROM val1
                                                   )
                           ) 
                      FROM val1;'''
            cur.execute(dropNoneValues)
            cur.execute(createNoneValues)
            cur.execute(dropVal)
            cur.execute(createVal)
            cur.execute(dropVal1)
            cur.execute(createVal1)
            data = cur.execute(final).fetchall()

            write.writerows(data)



def swSignificant_Pressure_Type_Table2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/SWB_Pressures?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country','Significant Pressure Type Group', 'Significant Pressure Type', 'Number', 'Number(%)']
    with open(
            working_directory + '4.swSignificant_Pressure_Type_Table2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)

        swSignificantPressureTypeGroup = ["P1 - Point sources", "P2 - Diffuse sources", "P2-7 - Diffuse - Atmospheric deposition ",
                                          "P3 - Abstraction", "P4 - Hydromorphology",
                                          "P5 - Introduced species and litter", "P6 - Groundwater recharge or water level",
                                          "P7 - Anthropogenic pressure - Other", "P8 - Anthropogenic pressure - Unknown",
                                          "P9 - Anthropogenic pressure - Historical pollution", "P0 - No significant anthropogenic pressure"]

        cur = conn.cursor()
        for country in countryCode:
            for types in swSignificantPressureTypeGroup:
                data = cur.execute('''SELECT DISTINCT countryCode,
                                                        swSignificantPressureTypeGroup,
                                                        swSignificantPressureType,
                                                        count(DISTINCT euSurfaceWaterBodyCode),
                                                        round(count(DISTINCT euSurfaceWaterBodyCode) * 100.0 / (
                                                                           SELECT count(DISTINCT euSurfaceWaterBodyCode) 
                                                                             FROM SOW_SWB_SWB_swSignificantPressureType
                                                                            WHERE cYear = ? AND 
                                                                                  countryCode = ? AND 
                                                                                  swSignificantPressureType <> "Unpopulated" AND 
                                                                                  naturalAWBHMWB <> "Unpopulated" AND 
                                                                                  surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                                  swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                                                  swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                                                                  swChemicalStatusValue <> "Unpopulated" AND
                                                                                  swSignificantPressureTypeGroup = ?
                                                                       )
                                                                        )
                                                          FROM SOW_SWB_SWB_swSignificantPressureType
                                                         WHERE cYear = ? AND 
                                                               countryCode = ? AND 
                                                               swSignificantPressureType <> "Unpopulated" AND 
                                                               naturalAWBHMWB <> "Unpopulated" AND 
                                                               surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                               swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                               swEcologicalStatusOrPotentialValue <> "inapplicable" AND 
                                                               swChemicalStatusValue <> "Unpopulated"
                                                               AND swSignificantPressureTypeGroup = ?
                                                         GROUP BY swSignificantPressureType;
                                    ''', (cYear, country, types, cYear, country, types)).fetchall()
                write.writerows(data)


def SignificantImpactType_Table2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/SWB_Impacts?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '4.SignificantImpactType_Table2016.csv',
            'w+', newline='') as f:
        headers = ['Country', 'Significant Impact Type', 'Number', 'Number(%)']
        write = csv.writer(f)
        write.writerow(headers)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT DISTINCT countryCode, 
                                    swSignificantImpactType,
                                    COUNT(euSurfaceWaterBodyCode),
                                    ROUND(COUNT(DISTINCT euSurfaceWaterBodyCode) * 100.0 / (
                                                                  SELECT COUNT(DISTINCT euSurfaceWaterBodyCode) 
                                                                    FROM SOW_SWB_SWB_swSignificantImpactType
                                                                   WHERE cYear == ? AND 
                                                                         countryCode = ? AND 
                                                                         surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                                         swSignificantImpactType <> "Unpopulated" AND 
                                                                         swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                                         swChemicalStatusValue <> "Unpopulated"
                                                              )
                                                                )
                                                  FROM SOW_SWB_SWB_swSignificantImpactType
                                                 WHERE surfaceWaterBodyCategory <> "Unpopulated" AND 
                                                       swSignificantImpactType <> "Unpopulated" AND 
                                                       swEcologicalStatusOrPotentialValue <> "Unpopulated" AND 
                                                       swChemicalStatusValue <> "Unpopulated" AND 
                                                       cYear == ? AND
                                                       countryCode = ? 

                                                 GROUP BY swSignificantImpactType;''', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def swSignificantImpactType_Table_Other2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/SWB_Impacts_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Significant Impact Other', 'Number', 'Number(%)']
    with open(
            working_directory + '4.swSignificantImpactType_Table_Other2016.csv',
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
                                                                                     FROM SOW_SWB_swSignificantImpactOther
                                                                                    WHERE cYear = ? AND 
                                                                                          countryCode = ?
                                                                               ))
                                              FROM SOW_SWB_swSignificantImpactOther
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
            

def swSignificantPressureType_Table_Other(conn, countryCode, cYear, working_directory):
    headers = ['Country', 'Significant Pressure Other', 'Number', 'Number(%)']
    with open(
            working_directory + '4.swSignificantPressureType_Table_Other.csv',
            'w+', newline='', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               swSignificantPressureOther,
                               COUNT(swSignificantPressureOther),
                               ROUND(count(swSignificantPressureOther) * 100.0 / (
                                                                                     SELECT count(swSignificantPressureOther) 
                                                                                       FROM SOW_SWB_swSignificantPressureOther
                                                                                      WHERE cYear = ? AND 
                                                                                            countryCode = ?
                                                                                 )
                               )
                          FROM SOW_SWB_swSignificantPressureOther
                         WHERE cYear = ? AND 
                               countryCode = ?
                         GROUP BY swSignificantPressureOther
                         ORDER BY COUNT(swSignificantPressureOther) DESC;
                         ''', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)
            

def gwSignificantImpactTypeByCountry(conn, countryCode, cYear, working_directory):
    headers = ['Country', 'Impact 0 - Area (km^2)', 'Impact 0 - Area (%)',
               'Impact 1 - Area (km^2)', 'Impact 1 - Area (%)',
               'Impact 2 - Area (km^2)', 'Impact 2 - Area (%)',
               'Impact 3 - Area (km^2)', 'Impact 3 - Area (%)',
               'Impact 4+ - Area (km^2)', 'Impact 4+ - Area (%)',
               'No', 'Inapplicable', 'Unknown']
    with open(
            working_directory + '5.1.gwSignificantImpactTypeByCountry.csv',
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
                                        FROM SOW_GWB_gwSignificantImpactType
                                       WHERE countryCode = "''' + county + '''" AND 
                                             cYear = 2016
                                       GROUP BY euGroundWaterBodyCode;'''

            drop2 = '''DROP TABLE IF EXISTS val1;'''

            temp2 = '''CREATE TEMPORARY TABLE val1 AS SELECT countryCode, CASE WHEN NullValues THEN sum(cArea) END AS t0,
                                                  CASE WHEN Counter = 1 THEN sum(cArea) END AS t1,
                                                  CASE WHEN Counter = 2 THEN sum(cArea) END AS t2,
                                                  CASE WHEN Counter = 3 THEN sum(cArea) END AS t3,
                                                  CASE WHEN Counter >= 4 THEN sum(cArea) END AS t4
                                             FROM val
                                            GROUP BY Counter;'''

            final = '''SELECT countryCode,sum(t0),
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


def swChemical_by_Country_2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_Status_Compare/SWB_ChemicalStatus_Country?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '14.swChemical_by_Country.csv',
            'w+', newline='') as f:
        headers = ["Country", "Year", "Chemical Status Value", "Number", "Number (%)"]

        write = csv.writer((f))
        write.writerow(headers)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('SELECT countryCode, cYear, swChemicalStatusValue, '
                               'COUNT(swChemicalStatusValue), '
                               'round(count(swChemicalStatusValue) * 100.0 / ( '
                               'SELECT count(swChemicalStatusValue) '
                               'FROM SOW_SWB_SurfaceWaterBody '
                               'WHERE cYear = 2016 '
                               'AND countryCode = ? '
                               'AND naturalAWBHMWB <> "Unpopulated" '
                               '), 1) '
                               'FROM SOW_SWB_SurfaceWaterBody '
                               'WHERE cYear = 2016 '
                               'AND naturalAWBHMWB <> "Unpopulated" '
                               'AND countryCode = ? '
                               'GROUP BY swChemicalStatusValue; '
                               , (country, country)).fetchall()
            write.writerows(data)

def gwSignificantImpactType2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/GWB_Impacts?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '5.gwSignificantImpactType2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Significant Impact Type", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        SOW_GWB_gwSignificantImpactType = cur.execute('''select distinct gwSignificantImpactType
                                                        from SOW_GWB_gwSignificantImpactType
                                                        where cYear = 2016 
                                                        and gwSignificantImpactType <> "Unpopulated";''').fetchall()

        for country in countryCode:
            for Itype in SOW_GWB_gwSignificantImpactType:
                temptype = ','.join(Itype)

                sqldropValues = '''DROP TABLE IF EXISTS DistinctValues; '''

                sqlDistinct = '''CREATE TEMPORARY TABLE DistinctValues AS SELECT DISTINCT euGroundWaterBodyCode, cYear,
                                                         cArea AS A
                                           FROM SOW_GWB_gwSignificantImpactType
                                          WHERE cYear = ''' + str(cYear) + ''' AND 
                                                countryCode = "''' + country + '''" AND 
                                                gwQuantitativeStatusValue <> "unpopulated" AND 
                                                gwChemicalStatusValue <> "unpopulated" AND 
                                                gwSignificantImpactType = "''' + temptype + '''"; '''

                sqlDropArea = '''DROP TABLE IF EXISTS DistinctArea; '''

                sqlArea = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euGroundWaterBodyCode,
                                                        cYear,
                                                       cArea AS G
                                         FROM SOW_GWB_gwSignificantImpactType
                                        WHERE cYear = ''' + str(cYear) + ''' AND 
                                              countryCode = "''' + country + '''" AND 
                                              gwQuantitativeStatusValue <> "unpopulated" AND 
                                              gwChemicalStatusValue <> "unpopulated" AND
                                              gwSignificantImpactType <> "Unpopulated";
                                               '''

                sqlFinal = '''SELECT countryCode,
                            cYear,
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
                      FROM SOW_GWB_gwSignificantImpactType
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
                

def gwSignificantImpactType_Other(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/GWB_Impacts_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '5.gwSignificantImpactType_Other.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Significant Impact Other", "Area (km^2)", "Area (%)"]
        write = csv.writer(f)
        write.writerow(header)

        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('SELECT countryCode, cYear, gwSignificantImpactOther, round(sum(cArea)), '
                            'round(sum(cArea) * 100.0 / ( '
                                'SELECT sum(cArea) '
                            'FROM SOW_GWB_gwSignificantImpactOther '
                            'WHERE cYear = ? AND countryCode = ? '
                            ')) '
                            'FROM SOW_GWB_gwSignificantImpactOther '
                            'WHERE cYear = ? AND countryCode = ? '
                            'GROUP BY gwSignificantImpactOther ', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/GWB_Pressures_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Number of Impacts', 'Area (km^2)', 'Percent(%)']
    with open(
            working_directory + ''
                                '5.SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country.csv',
            'w+', newline='', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        country = ''.join(countryCode)
        values = cur.execute('''select distinct gwSignificantPressureOther from SOW_GWB_gwSignificantPressureOther where cYear = ''' + str(cYear) + ''';''').fetchall()

        for temp in values:
            data = ''.join(temp)
            final = cur.execute('''SELECT countryCode,
                           gwSignificantPressureOther,
                           round(SUM(cArea) ),
                           round(sum(cArea) * 100 / (
                                                        SELECT round(sum(cArea) ) 
                                                          FROM SOW_GWB_gwSignificantPressureOther
                                                         WHERE countryCode = "''' + country + '''" AND 
                                                               cYear = ''' + str(cYear) + '''
                                                    )
                           ) 
                      FROM SOW_GWB_gwSignificantPressureOther
                     WHERE countryCode = "''' + country + '''" AND 
                           cYear = ''' + str(cYear) + ''' AND 
                           gwSignificantPressureOther = "''' + data + '''";''').fetchall()

            write.writerows(final)

def gwSignificantPressureType2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/GWB_Pressures?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Significant Pressure Type Group', 'Significant Pressure Type', 'Area (km^2)', 'Area (%)']
    with open(
            working_directory + '5.gwSignificantPressureType2016.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        gwSignificantPressureTypeGroup = cur.execute('''select distinct gwSignificantPressureTypeGroup
                                            from SOW_GWB_gwSignificantPressureType
                                            where cYear = 2016 and gwSignificantPressureTypeGroup <> "Unpopulated"''').fetchall()
        gwSignificantPressureType = cur.execute('''select distinct gwSignificantPressureType
                                                from SOW_GWB_gwSignificantPressureType
                                                where cYear = 2016 and gwSignificantPressureType <> "Unpopulated"''').fetchall()

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
                                                       FROM SOW_GWB_gwSignificantPressureType
                                                      WHERE cYear = ''' + str(cYear) + ''' AND 
                                                            countryCode = "''' + country + '''" AND 
                                                            gwQuantitativeStatusValue <> "unpopulated" and
                                                            gwChemicalStatusValue <> "unpopulated" AND 
                                                            gwSignificantPressureTypeGroup = "''' + temppgroup + '''" AND 
                                                            gwSignificantPressureType = "''' + tempptype + '''";'''

                    sqlDropdenominator = '''DROP TABLE IF EXISTS DistinctArea;'''

                    sqlDenominator = '''CREATE TEMPORARY TABLE DistinctArea AS SELECT DISTINCT euGroundWaterBodyCode, cArea as G
                                          FROM SOW_GWB_gwSignificantPressureType
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
                              FROM SOW_GWB_gwSignificantPressureType
                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                   countryCode = "''' + country + '''" AND 
                                   gwQuantitativeStatusValue <> "unpopulated" and
                                   gwChemicalStatusValue <> "unpopulated" AND 
                                   gwSignificantPressureType = "''' + tempptype + '''" AND 
                                   gwSignificantPressureTypeGroup = "''' + temppgroup + '''" 
                             GROUP BY gwSignificantPressureTypeGroup,
                                      gwSignificantPressureType;'''

                    cur.execute(sqlDropValues)
                    cur.execute(sqlDistinct)
                    cur.execute(sqlDropdenominator)
                    cur.execute(sqlDenominator)
                    data = cur.execute(sqlFinal).fetchall()
                    
                    write.writerows(data)
                    

def gwSignificantPressureType_OtherTable2016(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_PressuresImpacts/GWB_Pressures_Other?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    headers = ['Country', 'Year', 'Significant Pressure Other', 'Area (km^2)', 'Area(%)']
    with open(
            working_directory + ''
            '5.gwSignificantPressureType_OtherTable2016.csv',
            'w+', newline='', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('SELECT countryCode, cYear, gwSignificantPressureOther, round(sum(cArea) ),'
                               'round(sum(cArea) * 100.0 / ( '
                               'SELECT sum(cArea) '
                               'FROM SOW_GWB_gwSignificantPressureOther '
                               'WHERE cYear = ? AND countryCode = ? '
                               ')) '
                               'FROM SOW_GWB_gwSignificantPressureOther '
                               'WHERE cYear = ? AND countryCode = ? '
                               'GROUP BY gwSignificantPressureOther '
                               , (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def SOW_GWB_gwPollutant_Table(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_gwPollutant/GWB_gwPollutant?:isGuestRedirectFromVizportal=y&:embed=y
    with open(
            working_directory + '21.SOW_GWB_gwPollutant_Table2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Pollutant", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        country = ''.join(countryCode)

        droptable = '''DROP TABLE IF EXISTS distinctvalues;'''

        createtable = '''CREATE TEMPORARY TABLE IF NOT EXISTS distinctvalues AS SELECT DISTINCT countryCode,
                                                                       euGroundWaterBodyCode,
                                                                       cArea
                                                                       from SOW_GWB_gwPollutant
                                                                       where countryCode = "''' + country + '''" and
                                                                       cYear = 2016 and
                                                                       gwPollutantCausingFailure = "Yes";'''


        data = '''SELECT countryCode,
                           gwPollutantCode,
                           round(sum(cArea) ),
                           round(sum(cArea)  * 100 / (
                                                          SELECT sum(cArea) 
                                                          from distinctvalues
                                                          
                                                      ))
                      FROM SOW_GWB_gwPollutant
                     WHERE countryCode = "''' + country + '''" AND 
                           cYear = 2016 AND 
                           gwPollutantCausingFailure = "Yes"
                     GROUP BY gwPollutantCode;'''

        cur.execute(droptable)
        cur.execute(createtable)
        alldata = cur.execute(data).fetchall()

        write.writerows(alldata)
            

def SOW_GWB_gwPollutant_Table_Other(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_gwPollutantOther/WISE_SOW_gwPollutantOther?:isGuestRedirectFromVizportal=y&:embed=y
    with open(
            working_directory + '21.SOW_GWB_gwPollutant_Table' + str(cYear) + '_Other' + '.csv',
            'w+', newline='') as f:
        header = ["Country", "Pollutant reported as 'Other'", "Area (km^2)", "Area(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT DISTINCT countryCode,
                                    gwPollutantOther,
                                    round(sum(DISTINCT cArea) ),
                                    round(sum(DISTINCT cArea) * 100.0 / (
                                                                            SELECT sum(DISTINCT cArea) 
                                                                              FROM SOW_GWB_gwPollutantOther
                                                                             WHERE countryCode = ? AND 
                                                                                   gwPollutantCausingFailure = "Yes" AND 
                                                                                   cYear = ?
                                                                        )
                                                ) 
                                  FROM SOW_GWB_gwPollutantOther
                                 WHERE gwPollutantCausingFailure = "Yes" AND 
                                       cYear = ? AND 
                                       countryCode = ?
                                       GROUP BY gwPollutantOther
            ''', (country, cYear, cYear, country)).fetchall()
            write.writerows(data)


def swRiver_basin_specific_pollutants_reported_as_Other(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_FailingRBSPOther/SWB_FailingRBSPOther?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Year", "Failing RBSP Other", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()

        for country in countryCode:
            data = cur.execute('select countryCode, cYear, swFailingRBSPOther, count(swFailingRBSP), '
                        'ROUND(count(swFailingRBSP) * 100.0 / ( '
                        'select count(swFailingRBSP) from SOW_SWB_FailingRBSPOther where cYear = ? and countryCode = ?'
                        ')) '
                        'from SOW_SWB_FailingRBSPOther '
                        'where cYear == ? '
                        'and countryCode = ? '
                               'GROUP BY swFailingRBSPOther ORDER BY count(swFailingRBSP) ', (cYear, country, cYear, country)).fetchall()
            write.writerows(data)


def Ground_water_bodies_Failing_notUnknown_by_Country(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_Status_Maps/GWB_Status_NUTS0?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '23.Ground_water_bodies_Failing_notUnknown_by_Country2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Known Status", "Failing status", "Failing(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               round(sum(cArea) ),
                               round(sum(cArea) * 100 / (
                                                            SELECT sum(cArea) 
                                                              FROM SOW_GWB_GroundWaterBody
                                                             WHERE countryCode = "''' + country + '''" AND 
                                                                   cYear = ''' + str(cYear) + '''
                                                        )
                               ,1 ) 
                          FROM SOW_GWB_GroundWaterBody
                         WHERE countryCode = "''' + country + '''" AND 
                               cYear = ''' + str(cYear) + '''
                         GROUP BY gwChemicalStatusValue;''').fetchall()
            write.writerows(data)


def Ground_water_bodies_Failing_notUnknown_by_RBD(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_Status_Maps/GWB_Status_RBD?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '24.Ground_water_bodies_Failing_notUnknown_by_RBD2016.csv',
            'w+', newline='') as f:
        header = ["Country", "RBD Code", "RBD Name", "Known Status", "Failing status", "Failing(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        country = ''.join(countryCode)

        data = cur.execute('''SELECT DISTINCT euRBDCode
                      FROM swRBD_Europe_data
                     WHERE NUTS0 = "''' + country + '''";''').fetchall()

        for temp in data:
            values = ''.join(temp)
            data = cur.execute('''SELECT DISTINCT gwb.countryCode,
                                            gwb.euRBDCode,
                                            rdbeudata.rbdName,
                                            round(floor(sum(gwb.cArea) ) ),
                                            (
                                                SELECT round(floor(sum(cArea) ) ) 
                                                  FROM SOW_GWB_GroundWaterBody
                                                 WHERE countryCode = "''' + country + '''" AND 
                                                       cYear = ''' + str(cYear) + ''' AND 
                                                       (gwChemicalStatusValue = 3 OR 
                                                        gwQuantitativeStatusValue = 3) AND 
                                                       euRBDCode = "''' + values + '''"
                                            ),
                                            round( (
                                                       SELECT round(floor(sum(cArea) ) ) 
                                                         FROM SOW_GWB_GroundWaterBody
                                                        WHERE countryCode = "''' + country + '''" AND 
                                                              cYear = ''' + str(cYear) + ''' AND 
                                                              (gwChemicalStatusValue = 3 OR 
                                                               gwQuantitativeStatusValue = 3) AND 
                                                              euRBDCode = "''' + values + '''"
                                                   )
                            *                      100 / round(floor(sum(gwb.cArea) ) ) ) 
                              FROM SOW_GWB_GroundWaterBody AS gwb
                                   JOIN
                                   swRBD_Europe_data AS rdbeudata ON rdbeudata.euRBDCode = gwb.euRBDCode
                             WHERE gwb.countryCode = "''' + country + '''" AND 
                                   gwb.cYear = ''' + str(cYear) + ''' AND 
                                   gwb.gwChemicalStatusValue <> "unknown" AND 
                                   gwb.euRBDCode = "''' + values + '''";''').fetchall()
            write.writerows(data)


def Surface_water_bodies_Failing_notUnknown_by_Country(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_GWB_Status_Maps/GWB_Status_NUTS0?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '16.Surface_water_bodies_Failing_notUnknown_by_Country2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Known Status", "Failing status", "Failing(%)"]
        write = csv.writer(f)
        write.writerow(header)
        cur = conn.cursor()
        for country in countryCode:
            data = cur.execute('''SELECT countryCode,
                               round(sum(cArea) ),
                               round(sum(cArea) * 100 / (
                                                            SELECT sum(cArea) 
                                                              FROM SOW_SWB_SurfaceWaterBody
                                                             WHERE countryCode = "''' + country + '''" AND 
                                                                   cYear = ''' + str(cYear) + '''
                                                        )
                               ,1 ) 
                          FROM SOW_SWB_SurfaceWaterBody
                         WHERE countryCode = "''' + country + '''" AND 
                               cYear = ''' + str(cYear) + '''
                         GROUP BY swChemicalStatusValue;''').fetchall()
            write.writerows(data)


def Surface_water_bodies_QE1_Biological_quality_elements_assessment(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from SOW_SWB_QualityElement '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE1%" ', (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                              SELECT count(euSurfaceWaterBodyCode) 
                                                                FROM SOW_SWB_QualityElement
                                                               WHERE countryCode = ? AND 
                                                                     cYear = ? and
                                                                     qeCode = ?
                                                          ), 0) 
                                      FROM SOW_SWB_QualityElement
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    ''', (country, cYear, *value, cYear, country, *value, result)).fetchall()
                write.writerows(data)


def Surface_water_bodies_QE2_assessment(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '42.Surface_water_bodies_QE2_assessment2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from SOW_SWB_QualityElement '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE2%" ', (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                          SELECT count(euSurfaceWaterBodyCode) 
                                                            FROM SOW_SWB_QualityElement
                                                           WHERE countryCode = ? AND 
                                                                 cYear = ? and
                                                                 qeCode = ? AND 
                                                                 qeStatusOrPotentialValue <> "None"
                                                      ), 0) 
                                      FROM SOW_SWB_QualityElement
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    ''', (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)


def Surface_water_bodies_QE3_assessment(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '42.Surface_water_bodies_QE3_assessment2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from SOW_SWB_QualityElement '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE3-1%" ', (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                          SELECT count(euSurfaceWaterBodyCode) 
                                                                                            FROM SOW_SWB_QualityElement
                                                                                           WHERE countryCode = ? AND 
                                                                                                 cYear = ? and
                                                                                                 qeCode = ?
                                                                                      ), 0) 
                                      FROM SOW_SWB_QualityElement
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;
                    ''', (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)


def Surface_water_bodies_QE3_3_assessment(conn, countryCode, cYear, working_directory):
    # https://tableau-public.discomap.eea.europa.eu/views/WISE_SOW_SWB_qeMonitoringResults/SWB_qeMonitoringResults?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no
    with open(
            working_directory + '42.Surface_water_bodies_QE3_3_assessment2016.csv',
            'w+', newline='') as f:
        header = ["Country", "Monitoring Results", "Code", "Number", "Number(%)"]
        write = csv.writer(f)
        write.writerow(header)
        MonitoringResult = ["Monitoring", "Grouping", "Expert judgement", "Unpopulated"]
        cur = conn.cursor()
        values = cur.execute('select distinct qeCode '
                             'from SOW_SWB_QualityElement '
                             'where cYear == ? '
                             'and swEcologicalStatusOrPotentialValue <> "unpopulated" '
                             'and naturalAWBHMWB <> "unpopulated" '
                             'and qeCode like "QE3-3%" ', (cYear,)).fetchall()

        for country in countryCode:
            for result in MonitoringResult:
                for value in values:
                    data = cur.execute('''SELECT countryCode,
                                           qeMonitoringResults,
                                           qeCode,
                                           count(euSurfaceWaterBodyCode),
                                           round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                      SELECT count(euSurfaceWaterBodyCode) 
                                                        FROM SOW_SWB_QualityElement
                                                       WHERE countryCode = ? AND 
                                                             cYear = ? and
                                                             qeCode = ?
                                                  ), 0) 
                                      FROM SOW_SWB_QualityElement
                                     WHERE cYear == ? AND 
                                           countryCode = ? AND 
                                           swEcologicalStatusOrPotentialValue <> "unpopulated" AND 
                                           naturalAWBHMWB <> "unpopulated" AND 
                                           qeCode = ? AND 
                                           qeMonitoringResults = ?;''', (country, cYear, *value, cYear, country, *value, result)).fetchall()
                    write.writerows(data)

def sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP(conn, countryCode, cYear, working_directory):
    headers = ['Country', 'Year', 'Unchanged', 'Unchanged (%)', 'Other', 'Other (%)']
    with open(
            working_directory + '9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_' + str(
                cYear) + '.csv',
            'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        cur = conn.cursor()
        for country in countryCode:
            dropUnchange = '''DROP TABLE IF EXISTS Unchange;'''

            createUnchange = '''CREATE TEMPORARY TABLE Unchange AS SELECT countryCode,
                                          cYear,
                                          count(euSurfaceWaterBodyCode) AS UnchangeCount,
                                          round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                            SELECT count(euSurfaceWaterBodyCode) 
                                                                                              FROM SOW_SWB_SurfaceWaterBody
                                                                                             WHERE cYear = ''' + str(cYear) + ''' AND 
                                                                                                   countryCode = "''' + country + '''"
                                                                                        )
                                          ) AS UnchangePercent
                                     FROM SOW_SWB_SurfaceWaterBody
                                    WHERE cYear = ''' + str(cYear) + ''' AND 
                                          countryCode = "''' + country + '''" AND 
                                          wiseEvolutionType IN ("noChange", "changeCode", "change");'''

            dropOther = '''DROP TABLE IF EXISTS Other;'''

            createOther = '''CREATE TEMPORARY TABLE Other AS SELECT countryCode,
                                       cYear,
                                       count(euSurfaceWaterBodyCode) AS OtherCount,
                                       round(count(euSurfaceWaterBodyCode) * 100.0 / (
                                                                                         SELECT count(euSurfaceWaterBodyCode) 
                                                                                           FROM SOW_SWB_SurfaceWaterBody
                                                                                          WHERE cYear = ''' + str(cYear) + ''' AND 
                                                                                                countryCode = "''' + country + '''"
                                                                                     )
                                       ) AS OtherPercent
                                  FROM SOW_SWB_SurfaceWaterBody
                                 WHERE cYear = ''' + str(cYear) + ''' AND 
                                       countryCode = "''' + country + '''" AND 
                                       wiseEvolutionType not IN ("noChange", "changeCode", "change");'''

            final = '''SELECT CASE WHEN Unchange.countryCode IS NOT NULL THEN Unchange.countryCode ELSE Other.countryCode END,
                              CASE WHEN Unchange.cYear IS NOT NULL THEN Unchange.cYear ELSE Other.cYear END,
                                   (
                                       SELECT UnchangeCount
                                         FROM Unchange
                                   ),
                                   (
                                       SELECT UnchangePercent
                                         FROM Unchange
                                   ),
                                   (
                                       SELECT OtherCount
                                         FROM Other
                                   ),
                                   (
                                       SELECT OtherPercent
                                         FROM Other
                                   ) from Other, Unchange;'''
            cur.execute(dropUnchange)
            cur.execute(dropOther)
            cur.execute(createUnchange)
            cur.execute(createOther)
            data = cur.execute(final).fetchall()

            write.writerows(data)


