import csv
import pandas as pd

empty_line = ['', '', '', '', '', '']
country = ['AT']

def _1_swNumberAndSize(working_directory, conn, file):
    headers = ['1', '', 'Number and size of surface water bodies', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()
    DatabaseHeader = ["Number", "Length (km)", "Area (km^2)", ]

    for temp in DatabaseHeader:
        dhead = ''.join(temp)
        print(dhead)
        data = cur.execute('''SELECT null, [1.surfaceWaterBodyNumberAndSite2016].Country,
                       ?,
                       [1.surfaceWaterBodyNumberAndSite2016]."'''+dhead+'''",
                       [1.swNumberAndSize2022]."'''+dhead+'''",
                       round( ([1.swNumberAndSize2022]."'''+dhead+'''" - [1.surfaceWaterBodyNumberAndSite2016]."'''+dhead+'''") / round([1.surfaceWaterBodyNumberAndSite2016]."'''+dhead+'''") * 100.0, 2)
                  FROM [1.surfaceWaterBodyNumberAndSite2016],
                       [1.swNumberAndSize2022]
                 WHERE [1.surfaceWaterBodyNumberAndSite2016].Country = [1.swNumberAndSize2022].Country;''', (dhead,)).fetchmany()
        print(data)

        write.writerows(data)

def _2_gwNumberAndSize(working_directory, conn, file):
    headers = ['2','', 'Number and size of groundwater bodies', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)

    cur = conn.cursor()
    DatabaseHeader = ["Number", "Area (km^2)", ]

    for temp in DatabaseHeader:
        dhead = ''.join(temp)
        print(dhead)
        data = cur.execute('''SELECT null, [2.GroundWaterBodyCategory2016].Country,
                       ?,
                       [2.GroundWaterBodyCategory2016]."'''+dhead+'''",
                       [2.gwNumberAndSize2022]."'''+dhead+'''",
                       round(round( ([2.gwNumberAndSize2022]."'''+dhead+'''" - [2.GroundWaterBodyCategory2016]."'''+dhead+'''") ) / [2.GroundWaterBodyCategory2016]."'''+dhead+'''" * 100.0, 2)
                  FROM [2.GroundWaterBodyCategory2016],
                       [2.gwNumberAndSize2022]
                 WHERE [2.GroundWaterBodyCategory2016].Country = [2.gwNumberAndSize2022].Country;''', (dhead,)).fetchmany()
        print(data)

        write.writerows(data)

def _3_surfaceWaterBodyCategory(working_directory, conn, file):
    headers = ['3','', 'Number of surface water bodies by category and type', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    categories = ["RW", "LW", "CW", "TW", "TeW"]
    typevalues = ["Natural water body", "Heavily modified water body", "Artificial water body"]
    for temp1 in categories:
        for temp2 in typevalues:
            categ = ''.join(temp1)
            values = ''.join(temp2)
            print(categ)
            print(values)
            data = cur.execute('''SELECT null, [3.surfaceWaterBodyCategory2016].Country,
                       ?,
                       [3.surfaceWaterBodyCategory2016].Total,
                       [3.swWater_body_category_and_Type2022].Total,
                       round(round([3.swWater_body_category_and_Type2022].Total - [3.surfaceWaterBodyCategory2016].Total) / [3.surfaceWaterBodyCategory2016].Total * 100.0, 2) 
                  FROM [3.surfaceWaterBodyCategory2016],
                       [3.swWater_body_category_and_Type2022]
                 WHERE [3.surfaceWaterBodyCategory2016].Country = [3.swWater_body_category_and_Type2022].Country AND 
                       [3.surfaceWaterBodyCategory2016].[Surface Water Body Category] = "'''+categ+'''" AND 
                       [3.swWater_body_category_and_Type2022].[Surface Water Body Category] = "'''+categ+'''" AND 
                       [3.surfaceWaterBodyCategory2016].Type = "'''+values+'''" AND 
                       [3.swWater_body_category_and_Type2022].Type = "'''+values+'''" AND 
                       [3.surfaceWaterBodyCategory2016].Total != 0 AND 
                       [3.swWater_body_category_and_Type2022].Total != 0;''',(categ + " " + values,)).fetchmany()
            print(data)

            write.writerows(data)

def _4_SignificantImpactType_Table(working_directory, conn, file):
    headers = ['', '', 'Significant Impacts (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [4.SignificantImpactType_Table2016].Country,
                                                [4.SignificantImpactType_Table2016]."Significant Impact Type",
                                                [4.SignificantImpactType_Table2016].[Number] AS Cycle2Pressure,
                                                [4.swSignificant_impacts2022].[Number] AS Cycle3Pressure
                                           FROM [4.SignificantImpactType_Table2016]
                                                LEFT JOIN
                                                [4.swSignificant_impacts2022] ON [4.swSignificant_impacts2022].Country = [4.SignificantImpactType_Table2016].Country AND 
                                                                                           [4.swSignificant_impacts2022]."Significant Impact Type" = [4.SignificantImpactType_Table2016].[Significant Impact Type]
                                          WHERE [4.SignificantImpactType_Table2016].Country = "''' + code + '''"
                                            UNION ALL
                                            SELECT [4.swSignificant_impacts2022].Country,
                                                   [4.swSignificant_impacts2022].[Significant Impact Type],
                                                   [4.SignificantImpactType_Table2016].[Number] AS Cycle2Pressure,
                                                   [4.swSignificant_impacts2022].[Number] AS Cycle3Pressure
                                              FROM [4.swSignificant_impacts2022]
                                                   LEFT JOIN
                                                   [4.SignificantImpactType_Table2016] ON [4.SignificantImpactType_Table2016].Country = [4.swSignificant_impacts2022].Country AND 
                                                                                              [4.swSignificant_impacts2022].[Significant Impact Type] = [4.SignificantImpactType_Table2016].[Significant Impact Type]
                                             WHERE [4.swSignificant_impacts2022].Country = "''' + code + '''"; '''

    sql = '''SELECT DISTINCT NULL,
                Country,
                [Significant Impact Type],
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY [Significant Impact Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _4_Significant_impacts_other(working_directory, conn, file):
    headers = ['', '', 'Significant Impacts other (Number)', '', '', '']
    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [4.swSignificantImpactType_Table_Other2016].Country,
                       [4.swSignificantImpactType_Table_Other2016]."Significant Impact Other",
                       [4.swSignificantImpactType_Table_Other2016].Number AS Cycle2Pressure,
                       [4.swSignificantImpactType_Table_Other2022].Number AS Cycle3Pressure
                  FROM [4.swSignificantImpactType_Table_Other2016]
                       left JOIN
                [4.swSignificantImpactType_Table_Other2022] ON [4.swSignificantImpactType_Table_Other2016]."Significant Impact Other" = [4.swSignificantImpactType_Table_Other2022]."Significant Impact Other" AND 
                                        [4.swSignificantImpactType_Table_Other2022].Country = [4.swSignificantImpactType_Table_Other2016].Country
                                        where [4.swSignificantImpactType_Table_Other2016].Country = "''' + code + '''"
                UNION ALL
                SELECT [4.swSignificantImpactType_Table_Other2022].Country,
                       [4.swSignificantImpactType_Table_Other2022]."Significant Impact Other",
                       [4.swSignificantImpactType_Table_Other2016].Number AS Cycle2Pressure,
                       [4.swSignificantImpactType_Table_Other2022].Number AS Cycle3Pressure
                  FROM [4.swSignificantImpactType_Table_Other2022]
                       left JOIN
                       [4.swSignificantImpactType_Table_Other2016] ON [4.swSignificantImpactType_Table_Other2016]."Significant Impact Other" = [4.swSignificantImpactType_Table_Other2022]."Significant Impact Other" AND 
                                                            [4.swSignificantImpactType_Table_Other2022].Country = [4.swSignificantImpactType_Table_Other2016].Country
                                                            where [4.swSignificantImpactType_Table_Other2022].Country = "''' + code + '''"; '''

    sql = '''SELECT DISTINCT null, Country,
                [Significant Impact Other],
                Cycle2Pressure,
                Cycle3Pressure,
                round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0,2)
              FROM distinctValues
             ORDER BY [Significant Impact Other];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _4_swNumber_of_impacts_by_country(working_directory, conn, file):
    headers_topic =['4', '', 'Surface water bodies significant pressures and impacts', '', '', '']
    headers = ['', '', 'Number of impacts', '', '', '']

    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    categories = ['Impact 0 - Number',
                   'Impact 1 - Number',
                   'Impact 2 - Number',
                   'Impact 3 - Number',
                   'Impact 4+ - Number']

    for temp in categories:
        categ = ''.join(temp)
        data = cur.execute('''SELECT null, [NewDash.7.swNumber_of_impacts_by_country_2016].Country,
                            ?,
                           [NewDash.7.swNumber_of_impacts_by_country_2016]."''' + categ + '''",
                           [4.swNumber_of_impacts_by_country2022]."''' + categ + '''",
                           round(round([4.swNumber_of_impacts_by_country2022]."''' + categ + '''" - [NewDash.7.swNumber_of_impacts_by_country_2016]."''' + categ + '''") / [NewDash.7.swNumber_of_impacts_by_country_2016]."''' + categ + '''" * 100.0, 2) 
                      FROM [NewDash.7.swNumber_of_impacts_by_country_2016],
                           [4.swNumber_of_impacts_by_country2022]
                     WHERE [NewDash.7.swNumber_of_impacts_by_country_2016].Country = [4.swNumber_of_impacts_by_country2022].Country;''',(categ,)).fetchmany()
        print(data)

        write.writerows(data)

def _4_swSignificant_Pressure_Type_Table(working_directory, conn, file):
    headers = ['', '', 'Significant Pressures (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [4.swSignificant_Pressure_Type_Table2016].Country,
                       [4.swSignificant_Pressure_Type_Table2016].[Significant Pressure Type],
                       [4.swSignificant_Pressure_Type_Table2016].Number AS Cycle2Pressure,
                       [4.swSignificantPressureType2022].Number AS Cycle3Pressure
                  FROM [4.swSignificant_Pressure_Type_Table2016]
                       left JOIN
                       [4.swSignificantPressureType2022] ON [4.swSignificant_Pressure_Type_Table2016].[Significant Pressure Type] = [4.swSignificantPressureType2022].[Significant Pressure Type] AND 
                                                            [4.swSignificantPressureType2022].Country = [4.swSignificant_Pressure_Type_Table2016].Country
                                                            where [4.swSignificant_Pressure_Type_Table2016].Country = "'''+ code +'''"
                UNION ALL
                SELECT [4.swSignificantPressureType2022].Country,
                       [4.swSignificantPressureType2022].[Significant Pressure Type],
                       [4.swSignificant_Pressure_Type_Table2016].Number AS Cycle2Pressure,
                       [4.swSignificantPressureType2022].Number AS Cycle3Pressure
                  FROM [4.swSignificantPressureType2022]
                       left JOIN
                       [4.swSignificant_Pressure_Type_Table2016] ON [4.swSignificant_Pressure_Type_Table2016].[Significant Pressure Type] = [4.swSignificantPressureType2022].[Significant Pressure Type] AND 
                                                            [4.swSignificantPressureType2022].Country = [4.swSignificant_Pressure_Type_Table2016].Country
                                                            where [4.swSignificantPressureType2022].Country = "'''+ code + '''";'''

    sql = '''SELECT DISTINCT null, Country,
                [Significant Pressure Type],
                Cycle2Pressure,
                Cycle3Pressure,
                round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure *100.0,2)
              FROM distinctValues
             ORDER BY [Significant Pressure Type];'''
    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _4_swSignificant_Pressure_Type_Table_Others(working_directory, conn, file):
    headers = ['', '', 'Significant Pressures Other', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [4.swSignificantPressureType_Table_Other].Country,
                       [4.swSignificantPressureType_Table_Other].[Significant Pressure Other],
                       [4.swSignificantPressureType_Table_Other].Number AS Cycle2Pressure,
                       [4.swSignificant_pressures_reported_as_Other2022].Number AS Cycle3Pressure
                  FROM [4.swSignificantPressureType_Table_Other]
                       left JOIN
                [4.swSignificant_pressures_reported_as_Other2022] ON [4.swSignificantPressureType_Table_Other].[Significant Pressure Other] = [4.swSignificant_pressures_reported_as_Other2022].[Significant Pressure Other] AND 
                                        [4.swSignificant_pressures_reported_as_Other2022].Country = [4.swSignificantPressureType_Table_Other].Country
                                        where [4.swSignificantPressureType_Table_Other].Country = "'''+code+'''"
                UNION ALL
                SELECT [4.swSignificant_pressures_reported_as_Other2022].Country,
                       [4.swSignificant_pressures_reported_as_Other2022].[Significant Pressure Other],
                       [4.swSignificantPressureType_Table_Other].Number AS Cycle2Pressure,
                       [4.swSignificant_pressures_reported_as_Other2022].Number AS Cycle3Pressure
                  FROM [4.swSignificant_pressures_reported_as_Other2022]
                       left JOIN
                       [4.swSignificantPressureType_Table_Other] ON [4.swSignificantPressureType_Table_Other].[Significant Pressure Other] = [4.swSignificant_pressures_reported_as_Other2022].[Significant Pressure Other] AND 
                                                            [4.swSignificant_pressures_reported_as_Other2022].Country = [4.swSignificantPressureType_Table_Other].Country
                                                            where [4.swSignificant_pressures_reported_as_Other2022].Country = "'''+code+'''";'''
    sql = '''SELECT DISTINCT null, Country,
                [Significant Pressure Other],
                Cycle2Pressure,
                Cycle3Pressure,
                round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0,2)
              FROM distinctValues
             ORDER BY [Significant Pressure Other];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    print(data)
    write.writerows(data)


def _5_1_gwSignificantImpactTypeByCountry(working_directory, conn, file):
    header_topic = ['5', '', 'Groundwater bodies significant pressures and impacts', '', '', '']
    headers = ['', '', 'Number of Impacts (Area km2)', '', '', '']

    write = csv.writer(file)
    write.writerow(header_topic)
    write.writerow(headers)

    cur = conn.cursor()
    values = ["Impact 0 - Area (km^2)", "Impact 1 - Area (km^2)", "Impact 2 - Area (km^2)", "Impact 3 - Area (km^2)", "Impact 4+ - Area (km^2)"]
    for temp in values:
        data = cur.execute('''select null, [5.1.gwSignificantImpactTypeByCountry].Country,
                    ?,
                    [5.1.gwSignificantImpactTypeByCountry]."'''+temp+'''",
                    [5.1.gwSignificantImpactTypeByCountry2022]."'''+temp+'''",
                    round(([5.1.gwSignificantImpactTypeByCountry2022]."'''+temp+'''" - [5.1.gwSignificantImpactTypeByCountry]."'''+temp+'''") / [5.1.gwSignificantImpactTypeByCountry]."'''+temp+'''" * 100.0, 2)
                    from [5.1.gwSignificantImpactTypeByCountry],[5.1.gwSignificantImpactTypeByCountry2022]
                    where [5.1.gwSignificantImpactTypeByCountry].Country = [5.1.gwSignificantImpactTypeByCountry2022].Country;''',(temp,)).fetchmany()

        write.writerows(data)

def _5_gwSignificantImpactType(working_directory, conn, file):
    headers = ['','', 'Significant Impact (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [5.gwSignificantImpactType2016].Country,
               [5.gwSignificantImpactType2016].[Significant Impact Type],
               [5.gwSignificantImpactType2016]."Area (km^2)" AS Cycle2Pressure,
               [5.gwSignificant_impacts2022]."Area (km^2)" AS Cycle3Pressure
          FROM [5.gwSignificantImpactType2016]
               left JOIN
               [5.gwSignificant_impacts2022] ON [5.gwSignificant_impacts2022]."Significant Impact Type" = [5.gwSignificantImpactType2016].[Significant Impact Type] AND 
                                                    [5.gwSignificant_impacts2022].Country = [5.gwSignificantImpactType2016].Country
                                                    where [5.gwSignificantImpactType2016].Country = "''' + code + '''"
        UNION ALL
        SELECT [5.gwSignificant_impacts2022].Country,
               [5.gwSignificant_impacts2022]."Significant Impact Type",
               [5.gwSignificantImpactType2016]."Area (km^2)" AS Cycle2Pressure,
               [5.gwSignificant_impacts2022]."Area (km^2)" AS Cycle3Pressure
          FROM [5.gwSignificant_impacts2022]
               left JOIN
               [5.gwSignificantImpactType2016] ON [5.gwSignificant_impacts2022].[Significant Impact Type] = [5.gwSignificantImpactType2016].[Significant Impact Type] AND 
                                                    [5.gwSignificant_impacts2022].Country = [5.gwSignificantImpactType2016].Country
                                                    where [5.gwSignificant_impacts2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Significant Impact Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure *100.0,2)
          FROM distinctValues
         ORDER BY [Significant Impact Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)


def _5_gwSignificantImpactTypeOther(working_directory, conn, file):
    headers = ['', '', 'Significant Impact Other (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [5.gwSignificantImpactType_Other].Country,
               [5.gwSignificantImpactType_Other].[Significant Impact Other],
               [5.gwSignificantImpactType_Other]."Area (km^2)" AS Cycle2Pressure,
               [5.gwSignificantImpactType_Other2022]."Area (km^2)" AS Cycle3Pressure
          FROM [5.gwSignificantImpactType_Other]
               left JOIN
               [5.gwSignificantImpactType_Other2022] ON [5.gwSignificantImpactType_Other2022]."Significant Impact Other" = [5.gwSignificantImpactType_Other].[Significant Impact Other] AND 
                                                    [5.gwSignificantImpactType_Other2022].Country = [5.gwSignificantImpactType_Other].Country
                                                    where [5.gwSignificantImpactType_Other].Country = "''' + code + '''"
        UNION ALL
        SELECT [5.gwSignificantImpactType_Other2022].Country,
               [5.gwSignificantImpactType_Other2022]."Significant Impact Other",
               [5.gwSignificantImpactType_Other]."Area (km^2)" AS Cycle2Pressure,
               [5.gwSignificantImpactType_Other2022]."Area (km^2)" AS Cycle3Pressure
          FROM [5.gwSignificantImpactType_Other2022]
               left JOIN
               [5.gwSignificantImpactType_Other] ON [5.gwSignificantImpactType_Other2022].[Significant Impact Other] = [5.gwSignificantImpactType_Other].[Significant Impact Other] AND 
                                                    [5.gwSignificantImpactType_Other2022].Country = [5.gwSignificantImpactType_Other].Country
                                                    where [5.gwSignificantImpactType_Other2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Significant Impact Other],
            Cycle2Pressure,
            Cycle3Pressure,
            round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure *100.0,2)
          FROM distinctValues
         ORDER BY [Significant Impact Other];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _5_gwSignificantPressureType(working_directory, conn, file):
    headers = ['','', 'Significant Pressure (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [5.gwSignificantPressureType2016].Country,
               [5.gwSignificantPressureType2016].[Significant Pressure Type],
               [5.gwSignificantPressureType2016]."Area (km^2)" AS Cycle2Pressure,
               [5.gwSignificantPressureType_Table2022]."Area (km^2)" AS Cycle3Pressure
          FROM [5.gwSignificantPressureType2016]
               left JOIN
               [5.gwSignificantPressureType_Table2022] ON [5.gwSignificantPressureType2016].[Significant Pressure Type] = [5.gwSignificantPressureType_Table2022].[Significant Pressure Type] AND 
                                                    [5.gwSignificantPressureType_Table2022].Country = [5.gwSignificantPressureType2016].Country
                                                    where [5.gwSignificantPressureType2016].Country = "'''+code+'''"
        UNION ALL
        SELECT [5.gwSignificantPressureType_Table2022].Country,
               [5.gwSignificantPressureType_Table2022].[Significant Pressure Type],
               [5.gwSignificantPressureType2016]."Area (km^2)" AS Cycle2Pressure,
               [5.gwSignificantPressureType_Table2022]."Area (km^2)" AS Cycle3Pressure
          FROM [5.gwSignificantPressureType_Table2022]
               left JOIN
               [5.gwSignificantPressureType2016] ON [5.gwSignificantPressureType2016].[Significant Pressure Type] = [5.gwSignificantPressureType_Table2022].[Significant Pressure Type] AND 
                                                    [5.gwSignificantPressureType_Table2022].Country = [5.gwSignificantPressureType2016].Country
                                                    where [5.gwSignificantPressureType_Table2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Significant Pressure Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure *100.0,2)
          FROM distinctValues
         ORDER BY [Significant Pressure Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _5_gwSignificantPressureTypeOther(working_directory, conn, file):
    headers = ['','', 'Significant Pressure Other (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''create temporary table distinctValues as SELECT [5.gwSignificantPressureType_OtherTable2016].Country,
                   [5.gwSignificantPressureType_OtherTable2016].[Significant Pressure Other],
                   [5.gwSignificantPressureType_OtherTable2016]."Area (km^2)" AS Cycle2Pressure,
                   [5.gwSignificantPressureType_OtherTable2022]."Area (km^2)" AS Cycle3Pressure
              FROM [5.gwSignificantPressureType_OtherTable2016]
                   left JOIN
                   [5.gwSignificantPressureType_OtherTable2022] ON [5.gwSignificantPressureType_OtherTable2016].[Significant Pressure Other] = [5.gwSignificantPressureType_OtherTable2022].[Significant Pressure Other] AND 
                                                        [5.gwSignificantPressureType_OtherTable2022].Country = [5.gwSignificantPressureType_OtherTable2016].Country
                                                        where [5.gwSignificantPressureType_OtherTable2016].Country = "'''+ code +'''"
            UNION ALL
            SELECT [5.gwSignificantPressureType_OtherTable2022].Country,
                   [5.gwSignificantPressureType_OtherTable2022].[Significant Pressure Other],
                   [5.gwSignificantPressureType_OtherTable2016]."Area (km^2)" AS Cycle2Pressure,
                   [5.gwSignificantPressureType_OtherTable2022]."Area (km^2)" AS Cycle3Pressure
              FROM [5.gwSignificantPressureType_OtherTable2022]
                   left JOIN
                   [5.gwSignificantPressureType_OtherTable2016] ON [5.gwSignificantPressureType_OtherTable2016].[Significant Pressure Other] = [5.gwSignificantPressureType_OtherTable2022].[Significant Pressure Other] AND 
                                                        [5.gwSignificantPressureType_OtherTable2022].Country = [5.gwSignificantPressureType_OtherTable2016].Country
                                                        where [5.gwSignificantPressureType_OtherTable2022].Country = "'''+ code +'''"'''

    sql = '''SELECT DISTINCT null, Country,
            [Significant Pressure Other],
            Cycle2Pressure,
            Cycle3Pressure,
            round((Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0,2)
          FROM distinctValues
         ORDER BY [Significant Pressure Other];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _6_swChemical_exemption_type(working_directory, conn, file):
    headers_topic = ['6', '', 'Surface water bodies exemptions and pressures', '', '', '']
    headers = ['','', 'Chemical exemptions (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [6.swChemical_exemption_type2016].Country,
                                            [6.swChemical_exemption_type2016].[Chemical Exemption Type],
                                            [6.swChemical_exemption_type2016].[Area (km^2)] AS Cycle2Pressure,
                                            [6.swChemical_exemption_type2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [6.swChemical_exemption_type2016]
                                            LEFT JOIN
                                            [6.swChemical_exemption_type2022] ON [6.swChemical_exemption_type2016].[Chemical Exemption Type] = [6.swChemical_exemption_type2022].[Chemical Exemption Type] AND 
                                                                                 [6.swChemical_exemption_type2022].Country = [6.swChemical_exemption_type2016].Country
                                      WHERE [6.swChemical_exemption_type2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [6.swChemical_exemption_type2022].Country,
                                           [6.swChemical_exemption_type2022].[Chemical Exemption Type],
                                           [6.swChemical_exemption_type2016].[Area (km^2)] AS Cycle2Pressure,
                                           [6.swChemical_exemption_type2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [6.swChemical_exemption_type2022]
                                           LEFT JOIN
                                           [6.swChemical_exemption_type2016] ON [6.swChemical_exemption_type2016].[Chemical Exemption Type] = [6.swChemical_exemption_type2022].[Chemical Exemption Type] AND 
                                                                                [6.swChemical_exemption_type2022].Country = [6.swChemical_exemption_type2016].Country
                                     WHERE [6.swChemical_exemption_type2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Chemical Exemption Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY [Chemical Exemption Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _6_swEcological_exemption_type(working_directory, conn, file):
    headers = ['','', 'Ecological Exemption (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [6.Surface_water_bodies_Ecological_exemptions_Type2016].Country,
                                            [6.Surface_water_bodies_Ecological_exemptions_Type2016].[Ecological Exemption Type],
                                            [6.Surface_water_bodies_Ecological_exemptions_Type2016].Number AS Cycle2Pressure,
                                            [6.swEcologicalexemption2022].Number AS Cycle3Pressure
                                       FROM [6.Surface_water_bodies_Ecological_exemptions_Type2016]
                                            LEFT JOIN
                                            [6.swEcologicalexemption2022] ON [6.Surface_water_bodies_Ecological_exemptions_Type2016].[Ecological Exemption Type] = [6.swEcologicalexemption2022].[Ecological Exemption Type] AND 
                                                                             [6.swEcologicalexemption2022].Country = [6.Surface_water_bodies_Ecological_exemptions_Type2016].Country
                                      WHERE [6.Surface_water_bodies_Ecological_exemptions_Type2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [6.swEcologicalexemption2022].Country,
                                           [6.swEcologicalexemption2022].[Ecological Exemption Type],
                                           [6.Surface_water_bodies_Ecological_exemptions_Type2016].Number AS Cycle2Pressure,
                                           [6.swEcologicalexemption2022].Number AS Cycle3Pressure
                                      FROM [6.swEcologicalexemption2022]
                                           LEFT JOIN
                                           [6.Surface_water_bodies_Ecological_exemptions_Type2016] ON [6.Surface_water_bodies_Ecological_exemptions_Type2016].[Ecological Exemption Type] = [6.swEcologicalexemption2022].[Ecological Exemption Type] AND 
                                                                                                      [6.swEcologicalexemption2022].Country = [6.Surface_water_bodies_Ecological_exemptions_Type2016].Country
                                     WHERE [6.swEcologicalexemption2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Ecological Exemption Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY [Ecological Exemption Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _6_Ecological_Exemptions_Pressures(working_directory, conn, file):
    headers = ['','', 'Ecological Exemptions Pressures (Number)', '', '', '']
    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].Country,
                                                [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].[Ecological Exemption Type] || '-' || [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].[Ecological Exemption Pressure] AS Values2016,
                                                [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].Number AS Cycle2Pressure,
                                                [6.swEcologicalexemptionandpressure2022].Number AS Cycle3Pressure
                                           FROM [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016]
                                                LEFT JOIN
                                                [6.swEcologicalexemptionandpressure2022] ON 
                                                [6.swEcologicalexemptionandpressure2022].[Ecological Exemption Type] || '-' || ([6.swEcologicalexemptionandpressure2022].[Ecological Exemption Pressure]) = 
                                                [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].[Ecological Exemption Type] || '-' || [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].[Ecological Exemption Pressure] AND
                                                [6.swEcologicalexemptionandpressure2022].Country = [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].Country
                                                where [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].Country = "''' + code + '''"
                    UNION ALL
                    SELECT [6.swEcologicalexemptionandpressure2022].Country,
                           [6.swEcologicalexemptionandpressure2022].[Ecological Exemption Type] || '-' || ([6.swEcologicalexemptionandpressure2022].[Ecological Exemption Pressure]) AS Values2022,
                           [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].Number AS Cycle2Pressure,
                           round([6.swEcologicalexemptionandpressure2022].Number) AS Cycle3Pressure
                      FROM [6.swEcologicalexemptionandpressure2022]
                           LEFT JOIN
                           [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016] ON 
                           [6.swEcologicalexemptionandpressure2022].[Ecological Exemption Type] || '-' || ([6.swEcologicalexemptionandpressure2022].[Ecological Exemption Pressure]) = 
                           [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].[Ecological Exemption Type] || '-' || [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].[Ecological Exemption Pressure] and
                           [6.swEcologicalexemptionandpressure2022].Country = [6.Surface_water_bodies_Ecological_exemptions_and_pressures2016].Country
                           WHERE [6.swEcologicalexemptionandpressure2022].Country = "''' + code + '''";'''


    sql = '''SELECT DISTINCT NULL,
                    Country,
                    Values2016,
                    Cycle2Pressure,
                    round(Cycle3Pressure),
                    round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
      FROM distinctValues
      GROUP BY Values2016
     ORDER BY Values2016;
'''
    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _6_swQuality_exemption_type(working_directory, conn, file):
    headers = ['','', 'Quality Element Exemptions (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [6.Surface_water_bodies_Quality_element_exemptions_Type2016].Country,
                                            [6.Surface_water_bodies_Quality_element_exemptions_Type2016].[Quality Element Exemption Type],
                                            [6.Surface_water_bodies_Quality_element_exemptions_Type2016].Number AS Cycle2Pressure,
                                            [6.Surface_water_bodies_Quality_element_exemptions_Type2022].Number AS Cycle3Pressure
                                       FROM [6.Surface_water_bodies_Quality_element_exemptions_Type2016]
                                            LEFT JOIN
                                            [6.Surface_water_bodies_Quality_element_exemptions_Type2022] ON [6.Surface_water_bodies_Quality_element_exemptions_Type2016].[Quality Element Exemption Type] = [6.Surface_water_bodies_Quality_element_exemptions_Type2022].[Quality Element Exemption Type] AND 
                                                                                                            [6.Surface_water_bodies_Quality_element_exemptions_Type2022].Country = [6.Surface_water_bodies_Quality_element_exemptions_Type2016].Country
                                      WHERE [6.Surface_water_bodies_Quality_element_exemptions_Type2016].Country = "'''+code+'''"
                            UNION ALL
                            SELECT [6.Surface_water_bodies_Quality_element_exemptions_Type2022].Country,
                                   [6.Surface_water_bodies_Quality_element_exemptions_Type2022].[Quality Element Exemption Type],
                                   [6.Surface_water_bodies_Quality_element_exemptions_Type2016].Number AS Cycle2Pressure,
                                   [6.Surface_water_bodies_Quality_element_exemptions_Type2022].Number AS Cycle3Pressure
                              FROM [6.Surface_water_bodies_Quality_element_exemptions_Type2022]
                                   LEFT JOIN
                                   [6.Surface_water_bodies_Quality_element_exemptions_Type2016] ON [6.Surface_water_bodies_Quality_element_exemptions_Type2016].[Quality Element Exemption Type] = [6.Surface_water_bodies_Quality_element_exemptions_Type2022].[Quality Element Exemption Type] AND 
                                                                                                   [6.Surface_water_bodies_Quality_element_exemptions_Type2016].Country = [6.Surface_water_bodies_Quality_element_exemptions_Type2022].Country
                             WHERE [6.Surface_water_bodies_Quality_element_exemptions_Type2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Quality Element Exemption Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
          FROM distinctValues
         ORDER BY [Quality Element Exemption Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _7_gwChemical_Exemption_Type(working_directory, conn, file):
    headers_topic = ['7', '', 'Groundwater bodies exemptions and pressures', '', '', '']
    headers = ['', '', 'Chemical exemptions (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [7.Groundwater_bodies_Chemical_Exemption_Type2016].Country,
                                            [7.Groundwater_bodies_Chemical_Exemption_Type2016].[Chemical Exemption Type],
                                            [7.Groundwater_bodies_Chemical_Exemption_Type2016].[Area (km^2)] AS Cycle2Pressure,
                                            [7.gwChemical_Exemption_Type2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [7.Groundwater_bodies_Chemical_Exemption_Type2016]
                                            LEFT JOIN
                                            [7.gwChemical_Exemption_Type2022] ON [7.Groundwater_bodies_Chemical_Exemption_Type2016].[Chemical Exemption Type] = [7.gwChemical_Exemption_Type2022].[Chemical Exemption Type] AND 
                                                                                 [7.gwChemical_Exemption_Type2022].Country = [7.Groundwater_bodies_Chemical_Exemption_Type2016].Country
                                      WHERE [7.Groundwater_bodies_Chemical_Exemption_Type2016].Country = "'''+code+'''"
                                UNION ALL
                                SELECT [7.gwChemical_Exemption_Type2022].Country,
                                       [7.gwChemical_Exemption_Type2022].[Chemical Exemption Type],
                                       [7.Groundwater_bodies_Chemical_Exemption_Type2016].[Area (km^2)] AS Cycle2Pressure,
                                       [7.gwChemical_Exemption_Type2022].[Area (km^2)] AS Cycle3Pressure
                                  FROM [7.gwChemical_Exemption_Type2022]
                                       LEFT JOIN
                                       [7.Groundwater_bodies_Chemical_Exemption_Type2016] ON [7.Groundwater_bodies_Chemical_Exemption_Type2016].[Chemical Exemption Type] = [7.gwChemical_Exemption_Type2022].[Chemical Exemption Type] AND 
                                                                                             [7.Groundwater_bodies_Chemical_Exemption_Type2016].Country = [7.gwChemical_Exemption_Type2022].Country
                                 WHERE [7.gwChemical_Exemption_Type2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Chemical Exemption Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY [Chemical Exemption Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _7_gwChemical_Pressure_Type(working_directory, conn, file):
    headers = ['', '', 'Chemical Pressure Type', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [7.gwChemical_exemptions_and_pressures].Country,
                                            [7.gwChemical_exemptions_and_pressures].[Chemical Exemption Type],
                                            [7.gwChemical_exemptions_and_pressures].[Area (km^2)] AS Cycle2Pressure,
                                            [7.gwChemical_exemptions_and_pressures2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [7.gwChemical_exemptions_and_pressures]
                                            LEFT JOIN
                                            [7.gwChemical_exemptions_and_pressures2022] ON [7.gwChemical_exemptions_and_pressures].[Chemical Exemption Type] = [7.gwChemical_exemptions_and_pressures2022].[Chemical Exemption Type] AND 
                                                                                 [7.gwChemical_exemptions_and_pressures2022].Country = [7.gwChemical_exemptions_and_pressures].Country
                                      WHERE [7.gwChemical_exemptions_and_pressures].Country = "''' + code + '''"
                                UNION ALL
                                SELECT [7.gwChemical_exemptions_and_pressures2022].Country,
                                       [7.gwChemical_exemptions_and_pressures2022].[Chemical Exemption Type],
                                       [7.gwChemical_exemptions_and_pressures].[Area (km^2)] AS Cycle2Pressure,
                                       [7.gwChemical_exemptions_and_pressures2022].[Area (km^2)] AS Cycle3Pressure
                                  FROM [7.gwChemical_exemptions_and_pressures2022]
                                       LEFT JOIN
                                       [7.gwChemical_exemptions_and_pressures] ON [7.gwChemical_exemptions_and_pressures].[Chemical Exemption Type] = [7.gwChemical_exemptions_and_pressures2022].[Chemical Exemption Type] AND 
                                                                                             [7.gwChemical_exemptions_and_pressures].Country = [7.gwChemical_exemptions_and_pressures2022].Country
                                 WHERE [7.gwChemical_exemptions_and_pressures2022].Country = "''' + code + '''"'''

    sql = '''SELECT DISTINCT null, Country,
            [Chemical Exemption Type],
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY [Chemical Exemption Type];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _7_gwQuantitative_Exemption_Type(working_directory, conn, file):
    headers = ['','', 'Quantitative Exemptions Pressures (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].Country,
                                            [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016]."Quantitative Exemption Pressure",
                                            [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].[Area (km^2)] AS Cycle2Pressure,
                                            [7.gwQuantitiveTypeAndPressure2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016]
                                            LEFT JOIN
                                            [7.gwQuantitiveTypeAndPressure2022] ON [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].[Quantitative Exemption Pressure] = [7.gwQuantitiveTypeAndPressure2022].[Quantitative Exemption Pressure] AND 
                                                                                 [7.gwQuantitiveTypeAndPressure2022].Country = [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].Country
                                      WHERE [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [7.gwQuantitiveTypeAndPressure2022].Country,
                                           [7.gwQuantitiveTypeAndPressure2022].[Quantitative Exemption Pressure],
                                           [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].[Area (km^2)] AS Cycle2Pressure,
                                           [7.gwQuantitiveTypeAndPressure2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [7.gwQuantitiveTypeAndPressure2022]
                                           LEFT JOIN
                                           [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016] ON [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].[Quantitative Exemption Pressure] = [7.gwQuantitiveTypeAndPressure2022].[Quantitative Exemption Pressure] AND 
                                                                                                 [7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016].Country = [7.gwQuantitiveTypeAndPressure2022].Country
                                     WHERE [7.gwQuantitiveTypeAndPressure2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Quantitative Exemption Pressure],
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY [Quantitative Exemption Pressure];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _8_Surface_water_bodies_Ecological_status_or_potential_group_Failing(working_directory, conn, file):
    headers_topic = ['8', '', 'Number and percent of surface water bodies at good or high and failling to achieve good ecological status or potential', '', '', '']
    headers = ['', '', 'Failing to achieve good ecological status or potential', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    values = ["Number", "Length (km)", "Area (km^2)"]

    for temp in values:
        drop = '''DROP TABLE IF EXISTS distinctValues;'''

        temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing].Country,
                                            [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing].[''' + temp + '''] AS Cycle2Pressure,
                                            [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022].[''' + temp + '''] AS Cycle3Pressure
                                       FROM [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing]
                                            LEFT JOIN
                                            [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022] ON 
                                                                                 [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022].Country = [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing].Country
                                      WHERE [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing].Country = "''' + code + '''"
                        UNION ALL
                        SELECT [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022].Country,
                               [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing].[''' + temp + '''] AS Cycle2Pressure,
                               [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022].[''' + temp + '''] AS Cycle3Pressure
                          FROM [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022]
                               LEFT JOIN
                               [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing] ON 
                                                                                     [8.Surface_water_bodies_Ecological_status_or_potential_group_Failing].Country = [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022].Country
                         WHERE [8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022].Country = "''' + code + '''";'''

        sql = '''SELECT DISTINCT null, Country,
                    "''' + temp +'''",
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
                  FROM distinctValues
                 ORDER BY "''' + temp +'''"; '''

        cur.execute(drop)
        cur.execute(temporary)
        data = cur.execute(sql).fetchall()
        write.writerows(data)

def _8_gwGoodorHighEcologicalStatusorPotential(working_directory, conn, file):
    headers = ['','', 'Good or high ecological status or potential', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)

    write.writerow(headers)
    cur = conn.cursor()
    values = ["Number", "Length","Area (km^2)"]
    for temp in values:
        print(temp)
        drop = '''DROP TABLE IF EXISTS distinctValues;'''

        temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High].Country,
                                            [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High].['''+temp+'''] AS Cycle2Pressure,
                                            [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022].['''+temp+'''] AS Cycle3Pressure
                                       FROM [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High]
                                            LEFT JOIN
                                            [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022] ON 
                                                                                 [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022].Country = [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High].Country
                                      WHERE [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High].Country = "'''+code+'''"
                        UNION ALL
                        SELECT [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022].Country,
                               [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High].['''+temp+'''] AS Cycle2Pressure,
                               [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022].['''+temp+'''] AS Cycle3Pressure
                          FROM [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022]
                               LEFT JOIN
                               [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High] ON 
                                                                                     [8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High].Country = [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022].Country
                         WHERE [8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022].Country = "'''+code+'''";'''

        sql = '''SELECT DISTINCT null, Country,
            "'''+temp+'''",
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
          FROM distinctValues
         ORDER BY "'''+temp+'''"'''

        cur.execute(drop)
        cur.execute(temporary)
        data = cur.execute(sql).fetchall()
        write.writerows(data)

def _8_Ecological_Status_Or_potential_per_surface_water_body_category(working_directory, conn, file):
    headers = ['','', 'Ecological Status Or Potential per surface water body category (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country,
                                                [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Ecological Status Or Potential Value] AS Values2016,
                                                [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Number AS Cycle2Pressure,
                                                [8.swEcologicalStatusOrPotential_by_Category2022].Number AS Cycle3Pressure
                                           FROM [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016]
                                                LEFT JOIN
                                                [8.swEcologicalStatusOrPotential_by_Category2022] ON [8.swEcologicalStatusOrPotential_by_Category2022].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_by_Category2022].[Ecological Status Or Potential Value] = [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Ecological Status Or Potential Value] AND 
                                                                                                     [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country = [8.swEcologicalStatusOrPotential_by_Category2022].Country
                                          WHERE [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country = "''' + code + '''"
                                UNION ALL
                                SELECT [8.swEcologicalStatusOrPotential_by_Category2022].Country,
                                       [8.swEcologicalStatusOrPotential_by_Category2022].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_by_Category2022].[Ecological Status Or Potential Value] AS Cycle2Pressure,
                                       [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Number AS Cycle2Pressure,
                                       [8.swEcologicalStatusOrPotential_by_Category2022].Number AS Cycle3Pressure
                                  FROM [8.swEcologicalStatusOrPotential_by_Category2022]
                                       LEFT JOIN
                                       [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016] ON [8.swEcologicalStatusOrPotential_by_Category2022].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_by_Category2022].[Ecological Status Or Potential Value] = [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Ecological Status Or Potential Value] AND 
                                                                                                      [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country = [8.swEcologicalStatusOrPotential_by_Category2022].Country
                                 WHERE [8.swEcologicalStatusOrPotential_by_Category2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT NULL,
                        Country,
                        Values2016,
                        Cycle2Pressure,
                        Cycle3Pressure,
                        round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
          FROM distinctValues
         ORDER BY Values2016;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _9_swEcologicalStatusOrPotential_Unknown_Category(working_directory, conn, file):
    headers = ['9', '', 'Number of surface water bodies at unknown ecological status by category', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    values = ["Unknown"]
    for temp in values:
        data = cur.execute('''SELECT null, [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016].Country,
                            ?,
                           [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016].Number,
                               [9.swEcologicalStatusOrPotential_Unknown_Category2022].Number,
                           round(round([9.swEcologicalStatusOrPotential_Unknown_Category2022].Number - [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016].Number) / [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016].Number * 100.0,2)
                      FROM [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016],
                           [9.swEcologicalStatusOrPotential_Unknown_Category2022]
                     WHERE [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016].Country = [9.swEcologicalStatusOrPotential_Unknown_Category2022].Country and
                     [9.swEcologicalStatusOrPotential_Unknown_Category2022]."Ecological Status Or Potential Value" = "'''+ temp +'''" and
                     [9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016]."Ecological Status Or Potential Value" = "'''+ temp +'''";''',(temp,)).fetchmany()

        write.writerows(data)

def _10_surfaceWaterBodyChemicalStatusGood(working_directory, conn, file):
    headers = ['10','', 'Chemical Status Good (2)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    values = ["Number", "Length (km)", "Area (km^2)"]

    for temp in values:
        data = cur.execute('''SELECT null, [12.surfaceWaterBodyChemicalStatusGood2016].Country,
                           ?,
                           [12.surfaceWaterBodyChemicalStatusGood2016]."'''+ temp +'''",
                               [10.surfaceWaterBodyChemicalStatusGood2022]."'''+temp+'''",
                           round(round([10.surfaceWaterBodyChemicalStatusGood2022]."'''+ temp +'''" - [12.surfaceWaterBodyChemicalStatusGood2016]."'''+ temp +'''") / [12.surfaceWaterBodyChemicalStatusGood2016]."'''+ temp + '''" * 100.0,2)
                      FROM [12.surfaceWaterBodyChemicalStatusGood2016],
                           [10.surfaceWaterBodyChemicalStatusGood2022]
                     WHERE [12.surfaceWaterBodyChemicalStatusGood2016].Country = [10.surfaceWaterBodyChemicalStatusGood2022].Country and
                      [12.surfaceWaterBodyChemicalStatusGood2016]."Chemical Status Value" = "2" and 
                      [10.surfaceWaterBodyChemicalStatusGood2022]."Chemical Status Value" = "2";''',(temp,)).fetchmany()
        write.writerows(data)

def _10_Chemical_status_of_surface_water_bodies_by_category(working_directory, conn, file):
    headers = ['','', 'Chemical status of surface water bodies by category (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country,
                                                [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016]."Surface Water Body Category" || '-' || [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016]."Chemical Status Value" AS Values2016,
                                                [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Number AS Cycle2Pressure,
                                                [12.swChemicalStatusValue_by_Country_by_Categ2022].Number AS Cycle3Pressure
                                           FROM [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016]
                                                LEFT JOIN
                                                [12.swChemicalStatusValue_by_Country_by_Categ2022] ON [12.swChemicalStatusValue_by_Country_by_Categ2022].[Categories] || '-' || [12.swChemicalStatusValue_by_Country_by_Categ2022].[Chemical Status Value] = 
                                                [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Surface Water Body Category] || '-' || [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Chemical Status Value] AND 
                                                                                                      [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country = [12.swChemicalStatusValue_by_Country_by_Categ2022].Country
                                          WHERE [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country = "''' + code + '''"
                            UNION ALL
                            SELECT [12.swChemicalStatusValue_by_Country_by_Categ2022].Country,
                                   [12.swChemicalStatusValue_by_Country_by_Categ2022].[Categories] || '-' || [12.swChemicalStatusValue_by_Country_by_Categ2022]."Chemical Status Value" AS Cycle2Pressure,
                                   [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Number AS Cycle2Pressure,
                                   [12.swChemicalStatusValue_by_Country_by_Categ2022].Number AS Cycle3Pressure
                              FROM [12.swChemicalStatusValue_by_Country_by_Categ2022]
                                   LEFT JOIN
                                   [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016] ON [12.swChemicalStatusValue_by_Country_by_Categ2022].[Categories] || '-' || [12.swChemicalStatusValue_by_Country_by_Categ2022].[Chemical Status Value] = 
                                   [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Surface Water Body Category] || '-' || [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Chemical Status Value] AND 
                                                                                                     [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country = [12.swChemicalStatusValue_by_Country_by_Categ2022].Country
                             WHERE [12.swChemicalStatusValue_by_Country_by_Categ2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT NULL,
                                Country,
                                Values2016,
                                Cycle2Pressure,
                                Cycle3Pressure,
                                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
                  FROM distinctValues
                 ORDER BY Values2016;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _10_surfaceWaterBodyChemicalStatusPoor(working_directory, conn, file):
    headers = ['','', 'Chemical Status Poor (3)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    values = ["Number", "Length (km)", "Area (km^2)"]

    for temp in values:
        data = cur.execute('''SELECT null, [12.surfaceWaterBodyChemicalStatusGood2016].Country,
                           ?,
                           [12.surfaceWaterBodyChemicalStatusGood2016]."'''+ temp +'''",
                               [10.surfaceWaterBodyChemicalStatusGood2022]."'''+temp+'''",
                           round(round([10.surfaceWaterBodyChemicalStatusGood2022]."'''+ temp +'''" - [12.surfaceWaterBodyChemicalStatusGood2016]."'''+ temp +'''") / [12.surfaceWaterBodyChemicalStatusGood2016]."'''+ temp + '''" * 100.0,2)
                      FROM [12.surfaceWaterBodyChemicalStatusGood2016],
                           [10.surfaceWaterBodyChemicalStatusGood2022]
                     WHERE [12.surfaceWaterBodyChemicalStatusGood2016].Country = [10.surfaceWaterBodyChemicalStatusGood2022].Country and
                      [12.surfaceWaterBodyChemicalStatusGood2016]."Chemical Status Value" = "3" and 
                      [10.surfaceWaterBodyChemicalStatusGood2022]."Chemical Status Value" = "3";''',(temp,)).fetchmany()
        write.writerows(data)

def _11_Surface_water_bodies_ecological_status_or_potential_and_chemical_status_by_country(working_directory, conn, file):
    headers_topic = ['11', '', 'Surface water bodies ecological status or potential and chemical status by country', '', '', '']
    headers = ['', '', 'Chemical Status Good (2)', '', '', '']
    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [15.swChemicalStatusValue_by_Country2016].Country,
                                                [15.swChemicalStatusValue_by_Country2016].[Chemical Status Value],
                                                [15.swChemicalStatusValue_by_Country2016].Number AS Cycle2Pressure,
                                                [11.swChemical_by_Country2022].Number AS Cycle3Pressure
                                           FROM [15.swChemicalStatusValue_by_Country2016]
                                                LEFT JOIN
                                                [11.swChemical_by_Country2022] ON [15.swChemicalStatusValue_by_Country2016].Country = [11.swChemical_by_Country2022].Country and
                                                [11.swChemical_by_Country2022]."Chemical Status Value" = [15.swChemicalStatusValue_by_Country2016]."Chemical Status Value"
                                          WHERE [15.swChemicalStatusValue_by_Country2016].Country = "''' + code + '''"
                                            UNION ALL
                                            SELECT [11.swChemical_by_Country2022].Country,
                                                   [11.swChemical_by_Country2022].[Chemical Status Value],
                                                   [15.swChemicalStatusValue_by_Country2016].Number AS Cycle2Pressure,
                                                   [11.swChemical_by_Country2022].Number AS Cycle3Pressure
                                              FROM [11.swChemical_by_Country2022]
                                                   LEFT JOIN
                                                   [15.swChemicalStatusValue_by_Country2016] ON [15.swChemicalStatusValue_by_Country2016].Country = [11.swChemical_by_Country2022].Country and
                                                   [11.swChemical_by_Country2022]."Chemical Status Value" = [15.swChemicalStatusValue_by_Country2016]."Chemical Status Value"
                                             WHERE [11.swChemical_by_Country2022].Country = "''' + code + '''" ;'''


    sql = '''SELECT DISTINCT NULL,
                Country,
                [Chemical Status Value],
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
            FROM distinctValues
            where [Chemical Status Value] = "2";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['','', 'Chemical Status Poor (3)', '', '', '']
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [15.swChemicalStatusValue_by_Country2016].Country,
                                                [15.swChemicalStatusValue_by_Country2016].[Chemical Status Value],
                                                [15.swChemicalStatusValue_by_Country2016].Number AS Cycle2Pressure,
                                                [11.swChemical_by_Country2022].Number AS Cycle3Pressure
                                           FROM [15.swChemicalStatusValue_by_Country2016]
                                                LEFT JOIN
                                                [11.swChemical_by_Country2022] ON [15.swChemicalStatusValue_by_Country2016].Country = [11.swChemical_by_Country2022].Country and
                                                [11.swChemical_by_Country2022]."Chemical Status Value" = [15.swChemicalStatusValue_by_Country2016]."Chemical Status Value"
                                          WHERE [15.swChemicalStatusValue_by_Country2016].Country = "''' + code + '''"
                                            UNION ALL
                                            SELECT [11.swChemical_by_Country2022].Country,
                                                   [11.swChemical_by_Country2022].[Chemical Status Value],
                                                   [15.swChemicalStatusValue_by_Country2016].Number AS Cycle2Pressure,
                                                   [11.swChemical_by_Country2022].Number AS Cycle3Pressure
                                              FROM [11.swChemical_by_Country2022]
                                                   LEFT JOIN
                                                   [15.swChemicalStatusValue_by_Country2016] ON [15.swChemicalStatusValue_by_Country2016].Country = [11.swChemical_by_Country2022].Country and
                                                   [11.swChemical_by_Country2022]."Chemical Status Value" = [15.swChemicalStatusValue_by_Country2016]."Chemical Status Value"
                                             WHERE [11.swChemical_by_Country2022].Country = "''' + code + '''" ;'''


    sql = '''SELECT DISTINCT NULL,
                Country,
                [Chemical Status Value],
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
            FROM distinctValues
            where [Chemical Status Value] = "3";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['','', 'Chemical Status Poor (Unknown)', '', '', '']
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [15.swChemicalStatusValue_by_Country2016].Country,
                                                [15.swChemicalStatusValue_by_Country2016].[Chemical Status Value],
                                                [15.swChemicalStatusValue_by_Country2016].Number AS Cycle2Pressure,
                                                [11.swChemical_by_Country2022].Number AS Cycle3Pressure
                                           FROM [15.swChemicalStatusValue_by_Country2016]
                                                LEFT JOIN
                                                [11.swChemical_by_Country2022] ON [15.swChemicalStatusValue_by_Country2016].Country = [11.swChemical_by_Country2022].Country and
                                                [11.swChemical_by_Country2022]."Chemical Status Value" = [15.swChemicalStatusValue_by_Country2016]."Chemical Status Value"
                                          WHERE [15.swChemicalStatusValue_by_Country2016].Country = "''' + code + '''"
                                            UNION ALL
                                            SELECT [11.swChemical_by_Country2022].Country,
                                                   [11.swChemical_by_Country2022].[Chemical Status Value],
                                                   [15.swChemicalStatusValue_by_Country2016].Number AS Cycle2Pressure,
                                                   [11.swChemical_by_Country2022].Number AS Cycle3Pressure
                                              FROM [11.swChemical_by_Country2022]
                                                   LEFT JOIN
                                                   [15.swChemicalStatusValue_by_Country2016] ON [15.swChemicalStatusValue_by_Country2016].Country = [11.swChemical_by_Country2022].Country and
                                                   [11.swChemical_by_Country2022]."Chemical Status Value" = [15.swChemicalStatusValue_by_Country2016]."Chemical Status Value"
                                             WHERE [11.swChemical_by_Country2022].Country = "''' + code + '''" ;'''


    sql = '''SELECT DISTINCT NULL,
                Country,
                [Chemical Status Value],
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
            FROM distinctValues
            where [Chemical Status Value] = "Unknown";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _11_EcologicalStatus(working_directory, conn, file):
    headers = ['','', 'Ecological Status Or Potential (1)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
           'Number',
           [15.swEcologicalStatusValue_by_Country2016].Number,
           [11.swEcologicalStatusOrPotential_by_Country2022].Number,
           round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
      FROM [15.swEcologicalStatusValue_by_Country2016],
           [11.swEcologicalStatusOrPotential_by_Country2022]
     WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
           [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "1" and 
           [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "1";''').fetchmany()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Ecological Status Or Potential (2)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
               'Number',
               [15.swEcologicalStatusValue_by_Country2016].Number,
               [11.swEcologicalStatusOrPotential_by_Country2022].Number,
               round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
          FROM [15.swEcologicalStatusValue_by_Country2016],
               [11.swEcologicalStatusOrPotential_by_Country2022]
         WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
               [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "2" and 
               [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "2";''').fetchmany()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Ecological Status Or Potential (3)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
                   'Number',
                   [15.swEcologicalStatusValue_by_Country2016].Number,
                   [11.swEcologicalStatusOrPotential_by_Country2022].Number,
                   round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
              FROM [15.swEcologicalStatusValue_by_Country2016],
                   [11.swEcologicalStatusOrPotential_by_Country2022]
             WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
                   [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "3" and 
                   [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "3";''').fetchmany()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Ecological Status Or Potential (4)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
                   'Number',
                   [15.swEcologicalStatusValue_by_Country2016].Number,
                   [11.swEcologicalStatusOrPotential_by_Country2022].Number,
                   round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
              FROM [15.swEcologicalStatusValue_by_Country2016],
                   [11.swEcologicalStatusOrPotential_by_Country2022]
             WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
                   [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "4" and 
                   [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "4";''').fetchmany()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Ecological Status Or Potential (5)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
                   'Number',
                   [15.swEcologicalStatusValue_by_Country2016].Number,
                   [11.swEcologicalStatusOrPotential_by_Country2022].Number,
                   round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
              FROM [15.swEcologicalStatusValue_by_Country2016],
                   [11.swEcologicalStatusOrPotential_by_Country2022]
             WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
                   [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "5" and 
                   [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "5";''').fetchmany()

    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Ecological Status Or Potential (Unknown)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
                   'Number',
                   [15.swEcologicalStatusValue_by_Country2016].Number,
                   [11.swEcologicalStatusOrPotential_by_Country2022].Number,
                   round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
              FROM [15.swEcologicalStatusValue_by_Country2016],
                   [11.swEcologicalStatusOrPotential_by_Country2022]
             WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
                   [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "unknown" and 
                   [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "Unknown";''').fetchmany()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Ecological Status Or Potential (Inapplicable)', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT null, [15.swEcologicalStatusValue_by_Country2016].Country,
                       'Number',
                       [15.swEcologicalStatusValue_by_Country2016].Number,
                       [11.swEcologicalStatusOrPotential_by_Country2022].Number,
                       round(round([11.swEcologicalStatusOrPotential_by_Country2022].Number - [15.swEcologicalStatusValue_by_Country2016].Number) / [15.swEcologicalStatusValue_by_Country2016].Number * 100.0, 2) 
                  FROM [15.swEcologicalStatusValue_by_Country2016],
                       [11.swEcologicalStatusOrPotential_by_Country2022]
                 WHERE [15.swEcologicalStatusValue_by_Country2016].Country = [11.swEcologicalStatusOrPotential_by_Country2022].Country AND 
                       [15.swEcologicalStatusValue_by_Country2016].[Ecological Status or Potential Value] = "inapplicable" and 
                       [11.swEcologicalStatusOrPotential_by_Country2022].[Ecological Status or Potential Value] = "Inapplicable";''').fetchmany()
    write.writerows(data)

def _12_Ecological_Status_or_Potential(working_directory, conn, file):
    headers_topic = ['12', '', 'Surface water bodies ecological status or potential and chemical status by category', '', '', '']
    headers = ['', '', 'Ecological Status or Potential (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country,
                                                [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Ecological Status Or Potential Value] AS Values2016,
                                                [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Number AS Cycle2Pressure,
                                                [8.swEcologicalStatusOrPotential_by_Category2022].Number AS Cycle3Pressure
                                           FROM [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016]
                                                LEFT JOIN
                                                [8.swEcologicalStatusOrPotential_by_Category2022] ON [8.swEcologicalStatusOrPotential_by_Category2022].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_by_Category2022].[Ecological Status Or Potential Value] = [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Ecological Status Or Potential Value] AND 
                                                                                                     [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country = [8.swEcologicalStatusOrPotential_by_Category2022].Country
                                          WHERE [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country = "''' + code + '''"
                                UNION ALL
                                SELECT [8.swEcologicalStatusOrPotential_by_Category2022].Country,
                                       [8.swEcologicalStatusOrPotential_by_Category2022].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_by_Category2022].[Ecological Status Or Potential Value] AS Cycle2Pressure,
                                       [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Number AS Cycle2Pressure,
                                       [8.swEcologicalStatusOrPotential_by_Category2022].Number AS Cycle3Pressure
                                  FROM [8.swEcologicalStatusOrPotential_by_Category2022]
                                       LEFT JOIN
                                       [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016] ON [8.swEcologicalStatusOrPotential_by_Category2022].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_by_Category2022].[Ecological Status Or Potential Value] = [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Surface Water Body Category] || '-' || [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].[Ecological Status Or Potential Value] AND 
                                                                                                      [8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016].Country = [8.swEcologicalStatusOrPotential_by_Category2022].Country
                                 WHERE [8.swEcologicalStatusOrPotential_by_Category2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT NULL,
                        Country,
                        Values2016,
                        Cycle2Pressure,
                        Cycle3Pressure,
                        round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
          FROM distinctValues
         ORDER BY Values2016;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _12_Chemical_Status(working_directory, conn, file):
    headers = ['', '', 'Chemical Status (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country,
                                                [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016]."Surface Water Body Category" || '-' || [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016]."Chemical Status Value" AS Values2016,
                                                [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Number AS Cycle2Pressure,
                                                [12.swChemicalStatusValue_by_Country_by_Categ2022].Number AS Cycle3Pressure
                                           FROM [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016]
                                                LEFT JOIN
                                                [12.swChemicalStatusValue_by_Country_by_Categ2022] ON [12.swChemicalStatusValue_by_Country_by_Categ2022].[Categories] || '-' || [12.swChemicalStatusValue_by_Country_by_Categ2022].[Chemical Status Value] = 
                                                [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Surface Water Body Category] || '-' || [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Chemical Status Value] AND 
                                                                                                      [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country = [12.swChemicalStatusValue_by_Country_by_Categ2022].Country
                                          WHERE [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country = "''' + code + '''"
                            UNION ALL
                            SELECT [12.swChemicalStatusValue_by_Country_by_Categ2022].Country,
                                   [12.swChemicalStatusValue_by_Country_by_Categ2022].[Categories] || '-' || [12.swChemicalStatusValue_by_Country_by_Categ2022]."Chemical Status Value" AS Cycle2Pressure,
                                   [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Number AS Cycle2Pressure,
                                   [12.swChemicalStatusValue_by_Country_by_Categ2022].Number AS Cycle3Pressure
                              FROM [12.swChemicalStatusValue_by_Country_by_Categ2022]
                                   LEFT JOIN
                                   [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016] ON [12.swChemicalStatusValue_by_Country_by_Categ2022].[Categories] || '-' || [12.swChemicalStatusValue_by_Country_by_Categ2022].[Chemical Status Value] = 
                                   [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Surface Water Body Category] || '-' || [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].[Chemical Status Value] AND 
                                                                                                     [12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016].Country = [12.swChemicalStatusValue_by_Country_by_Categ2022].Country
                             WHERE [12.swChemicalStatusValue_by_Country_by_Categ2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT NULL,
                                Country,
                                Values2016,
                                Cycle2Pressure,
                                Cycle3Pressure,
                                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
                  FROM distinctValues
                 ORDER BY Values2016;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _13_Groundwater_bodies_quantitative_status_Area_km2(working_directory, conn, file):
    headers = ['13', '', 'Groundwater bodies quantitative status (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [18.GroundWaterBodyCategoryQuantitative_status2016].Country,
                    [18.GroundWaterBodyCategoryQuantitative_status2016].[Quantitative Status Value],
                                                                    [18.GroundWaterBodyCategoryQuantitative_status2016].[Area (km^2)] AS Cycle2Pressure,
                                                                    [13.Groundwater_bodies_quantitative_status2022].[Area (km^2)] AS Cycle3Pressure
                                                               FROM [18.GroundWaterBodyCategoryQuantitative_status2016]
                                                                    LEFT JOIN
                                                                    [13.Groundwater_bodies_quantitative_status2022] ON [13.Groundwater_bodies_quantitative_status2022].Country = [18.GroundWaterBodyCategoryQuantitative_status2016].Country and
                           [13.Groundwater_bodies_quantitative_status2022]."Quantitative Status Value" = [18.GroundWaterBodyCategoryQuantitative_status2016]."Quantitative Status Value"
                                      WHERE [18.GroundWaterBodyCategoryQuantitative_status2016].Country = "'''+code+'''"
                    UNION ALL
                    SELECT [13.Groundwater_bodies_quantitative_status2022].Country,
                    [13.Groundwater_bodies_quantitative_status2022].[Quantitative Status Value],
                           [18.GroundWaterBodyCategoryQuantitative_status2016].[Area (km^2)] AS Cycle2Pressure,
                           [13.Groundwater_bodies_quantitative_status2022].[Area (km^2)] AS Cycle3Pressure
                      FROM [13.Groundwater_bodies_quantitative_status2022]
                           LEFT JOIN
                           [18.GroundWaterBodyCategoryQuantitative_status2016] ON [18.GroundWaterBodyCategoryQuantitative_status2016].Country = [13.Groundwater_bodies_quantitative_status2022].Country and
                           [13.Groundwater_bodies_quantitative_status2022]."Quantitative Status Value" = [18.GroundWaterBodyCategoryQuantitative_status2016]."Quantitative Status Value"
                     WHERE [13.Groundwater_bodies_quantitative_status2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Quantitative Status Value],
                            Cycle2Pressure,
                            Cycle3Pressure,
                            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
              order by [Quantitative Status Value];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _14_Groundwater_bodies_chemical_status_Area_km2(working_directory, conn, file):
    headers = ['14', '', 'Groundwater bodies chemical status (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()
    values = ["Good (2)", "Poor (3)"]
    status = ["2","3"]
    for temp1,temp2 in zip(values,status):
        data = cur.execute('''SELECT null, [20.GroundWaterBodyCategoryChemical_status2016].Country,
                           ?,
                           [20.GroundWaterBodyCategoryChemical_status2016]."Area (km^2)",
                           [16.gwChemical_status2022]."Area (km^2)",
                           round(round([16.gwChemical_status2022]."Area (km^2)" - [20.GroundWaterBodyCategoryChemical_status2016]."Area (km^2)") / [20.GroundWaterBodyCategoryChemical_status2016]."Area (km^2)" * 100.0, 2)
                      FROM [20.GroundWaterBodyCategoryChemical_status2016],
                           [16.gwChemical_status2022]
                     WHERE [20.GroundWaterBodyCategoryChemical_status2016].Country = [16.gwChemical_status2022].Country AND
                           [20.GroundWaterBodyCategoryChemical_status2016].[Chemical Status Value] = "'''+temp2+'''" AND 
                           [16.gwChemical_status2022].[Chemical Status Value] = "'''+temp2+'''";''',(temp1,)).fetchall()
        write.writerows(data)

def _15_Groundwater_bodies_pollutants_and_pollutants_reported_as_other(working_directory, conn, file):
    headers = ['15', '', 'Groundwater bodies pollutants and pollutants reported as other', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [21.SOW_GWB_gwPollutant_Table2016].Country,
                                            [21.SOW_GWB_gwPollutant_Table2016]."Pollutant",
                                            [21.SOW_GWB_gwPollutant_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                            [15.gwPollutant2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [21.SOW_GWB_gwPollutant_Table2016]
                                            LEFT JOIN
                                            [15.gwPollutant2022] ON [15.gwPollutant2022].Country = [21.SOW_GWB_gwPollutant_Table2016].Country AND 
                                                                         [15.gwPollutant2022]."Pollutant" = [21.SOW_GWB_gwPollutant_Table2016]."Pollutant"
                                      WHERE [21.SOW_GWB_gwPollutant_Table2016].Country = "'''+code+'''"
                    UNION ALL
                    SELECT [15.gwPollutant2022].Country,
                           [15.gwPollutant2022]."Pollutant",
                           [21.SOW_GWB_gwPollutant_Table2016].[Area (km^2)] AS Cycle2Pressure,
                           [15.gwPollutant2022].[Area (km^2)] AS Cycle3Pressure
                      FROM [15.gwPollutant2022]
                           LEFT JOIN
                           [21.SOW_GWB_gwPollutant_Table2016] ON [21.SOW_GWB_gwPollutant_Table2016].Country = [15.gwPollutant2022].Country AND 
                                                                       [15.gwPollutant2022]."Pollutant" = [21.SOW_GWB_gwPollutant_Table2016]."Pollutant"
                     WHERE [15.gwPollutant2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                "Pollutant",
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY "Pollutant";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

    write.writerow(empty_line)
    headers = ['', '', 'Pollutants reported as', '', '', '']
    write.writerow(headers)
    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [21.SOW_GWB_gwPollutant_Table2016_Other].Country,
                                            [21.SOW_GWB_gwPollutant_Table2016_Other]."Pollutant reported as 'Other'",
                                            [21.SOW_GWB_gwPollutant_Table2016_Other].[Area (km^2)] AS Cycle2Pressure,
                                            [15.gwPollutantOther2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [21.SOW_GWB_gwPollutant_Table2016_Other]
                                            LEFT JOIN
                                            [15.gwPollutantOther2022] ON [15.gwPollutantOther2022].Country = [21.SOW_GWB_gwPollutant_Table2016_Other].Country AND 
                                                                         [15.gwPollutantOther2022]."Pollutant reported as 'Other'" = [21.SOW_GWB_gwPollutant_Table2016_Other]."Pollutant reported as 'Other'"
                                      WHERE [21.SOW_GWB_gwPollutant_Table2016_Other].Country = "''' + code + '''"
                                UNION ALL
                                SELECT [15.gwPollutantOther2022].Country,
                                       [15.gwPollutantOther2022]."Pollutant reported as 'Other'",
                                       [21.SOW_GWB_gwPollutant_Table2016_Other].[Area (km^2)] AS Cycle2Pressure,
                                       [15.gwPollutantOther2022].[Area (km^2)] AS Cycle3Pressure
                                  FROM [15.gwPollutantOther2022]
                                       LEFT JOIN
                                       [21.SOW_GWB_gwPollutant_Table2016_Other] ON [21.SOW_GWB_gwPollutant_Table2016_Other].Country = [15.gwPollutantOther2022].Country AND 
                                                                                   [15.gwPollutantOther2022]."Pollutant reported as 'Other'" = [21.SOW_GWB_gwPollutant_Table2016_Other]."Pollutant reported as 'Other'"
                                 WHERE [15.gwPollutantOther2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT null, Country,
                "Pollutant reported as 'Other'",
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY "Pollutant reported as 'Other'";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)


def _16_Chemical_Status(working_directory, conn, file):
    headers_topic = ['16', '', '% Groundwater bodies quantitative and chemical status', '', '', '']
    headers = ['', '', 'Chemical Status', '', '', '']

    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()
    values = ["Good (2)", "Poor (3)"]
    status = ["2","3"]
    for temp1,temp2 in zip(values,status):
        data = cur.execute('''SELECT null, [20.GroundWaterBodyCategoryChemical_status2016].Country,
                           ?,
                           [20.GroundWaterBodyCategoryChemical_status2016]."Area (km^2)",
                           [16.gwChemical_status2022]."Area (km^2)",
                           round(round([16.gwChemical_status2022]."Area (km^2)" - [20.GroundWaterBodyCategoryChemical_status2016]."Area (km^2)") / [20.GroundWaterBodyCategoryChemical_status2016]."Area (km^2)" * 100.0, 2)
                      FROM [20.GroundWaterBodyCategoryChemical_status2016],
                           [16.gwChemical_status2022]
                     WHERE [20.GroundWaterBodyCategoryChemical_status2016].Country = [16.gwChemical_status2022].Country AND
                           [20.GroundWaterBodyCategoryChemical_status2016].[Chemical Status Value] = "'''+temp2+'''" AND 
                           [16.gwChemical_status2022].[Chemical Status Value] = "'''+temp2+'''";''',(temp1,)).fetchall()
        write.writerows(data)

def _16_Quantitative_Status(working_directory, conn, file):
    headers = ['', '', 'Quantitative Status', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [18.GroundWaterBodyCategoryQuantitative_status2016].Country,
                                                                    [18.GroundWaterBodyCategoryQuantitative_status2016].[Quantitative Status Value],
                                                                    [18.GroundWaterBodyCategoryQuantitative_status2016].[Area (km^2)] AS Cycle2Pressure,
                                                                    [13.Groundwater_bodies_quantitative_status2022].[Area (km^2)] AS Cycle3Pressure
                                                               FROM [18.GroundWaterBodyCategoryQuantitative_status2016]
                                                                    LEFT JOIN
                                                                    [13.Groundwater_bodies_quantitative_status2022] ON [13.Groundwater_bodies_quantitative_status2022].Country = [18.GroundWaterBodyCategoryQuantitative_status2016].Country and
                           [13.Groundwater_bodies_quantitative_status2022]."Quantitative Status Value" = [18.GroundWaterBodyCategoryQuantitative_status2016]."Quantitative Status Value"
                                      WHERE [18.GroundWaterBodyCategoryQuantitative_status2016].Country = "'''+code+'''"
                    UNION ALL
                    SELECT [13.Groundwater_bodies_quantitative_status2022].Country,
                            [13.Groundwater_bodies_quantitative_status2022].[Quantitative Status Value],
                           [18.GroundWaterBodyCategoryQuantitative_status2016].[Area (km^2)] AS Cycle2Pressure,
                           [13.Groundwater_bodies_quantitative_status2022].[Area (km^2)] AS Cycle3Pressure
                      FROM [13.Groundwater_bodies_quantitative_status2022]
                           LEFT JOIN
                           [18.GroundWaterBodyCategoryQuantitative_status2016] ON [18.GroundWaterBodyCategoryQuantitative_status2016].Country = [13.Groundwater_bodies_quantitative_status2022].Country and
                           [13.Groundwater_bodies_quantitative_status2022]."Quantitative Status Value" = [18.GroundWaterBodyCategoryQuantitative_status2016]."Quantitative Status Value"
                     WHERE [13.Groundwater_bodies_quantitative_status2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            [Quantitative Status Value],
                            Cycle2Pressure,
                            Cycle3Pressure,
                            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _17_Groundwater_bodies_at_risk_of_failing_to_achieve_good_quantitative_status_and_reasons_for_failure_Area_km2(working_directory, conn, file):
    headers = ['17', '', 'Groundwater bodies at risk of failing to achieve good quantitative status and reasons for failure (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016].Country,
                                            [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016]."Quantitative Status Value",
                                            [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016].[Area (km^2)] AS Cycle2Pressure,
                                            [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016]
                                            LEFT JOIN
                                            [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022] ON [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022].Country = [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016].Country AND 
                                                                         [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022]."Quantitative Status Value" = [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016]."Quantitative Status Value"
                                      WHERE [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022].Country,
                                           [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022]."Quantitative Status Value",
                                           [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016].[Area (km^2)] AS Cycle2Pressure,
                                           [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022]
                                           LEFT JOIN
                                           [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016] ON [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016].Country = [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022].Country AND 
                                                                                       [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022]."Quantitative Status Value" = [25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016]."Quantitative Status Value"
                                     WHERE [17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                "Quantitative Status Value",
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY "Quantitative Status Value";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _17_Quantitative_Reasons_For_Failure_Area_km2(working_directory, conn, file):
    headers = ['', '',
               'Quantitative Reasons For Failure (Area km2)',
               '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016].Country,
                                            [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016]."Quantitative Reasons For Failure",
                                            [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                            [17.GWB_gwQuantitativeReasonsForFailure_Table2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016]
                                            LEFT JOIN
                                            [17.GWB_gwQuantitativeReasonsForFailure_Table2022] ON [17.GWB_gwQuantitativeReasonsForFailure_Table2022].Country = [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016].Country AND 
                                                                         [17.GWB_gwQuantitativeReasonsForFailure_Table2022]."Quantitative Reasons For Failure" = [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016]."Quantitative Reasons For Failure"
                                      WHERE [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [17.GWB_gwQuantitativeReasonsForFailure_Table2022].Country,
                                           [17.GWB_gwQuantitativeReasonsForFailure_Table2022]."Quantitative Reasons For Failure",
                                           [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                           [17.GWB_gwQuantitativeReasonsForFailure_Table2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [17.GWB_gwQuantitativeReasonsForFailure_Table2022]
                                           LEFT JOIN
                                           [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016] ON [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016].Country = [17.GWB_gwQuantitativeReasonsForFailure_Table2022].Country AND 
                                                                                       [17.GWB_gwQuantitativeReasonsForFailure_Table2022]."Quantitative Reasons For Failure" = [25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016]."Quantitative Reasons For Failure"
                                     WHERE [17.GWB_gwQuantitativeReasonsForFailure_Table2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                "Quantitative Reasons For Failure",
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY "Quantitative Reasons For Failure";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _18_Groundwater_bodies_at_risk_of_failing_to_achieve_good_chemical_status_and_reasons_for_failure_Area_km2(working_directory, conn, file):
    headers = ['18', '',
               'Groundwater bodies at risk of failing to achieve good chemical status and reasons for failure (Area km2)',
               '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [26.gwChemicalStatusValue_Table2016].Country,
                                            [26.gwChemicalStatusValue_Table2016]."Chemical Status Value",
                                            [26.gwChemicalStatusValue_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                            [22.gwChemicalStatusValue_Table2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [26.gwChemicalStatusValue_Table2016]
                                            LEFT JOIN
                                            [22.gwChemicalStatusValue_Table2022] ON [22.gwChemicalStatusValue_Table2022].Country = [26.gwChemicalStatusValue_Table2016].Country AND 
                                                                         [22.gwChemicalStatusValue_Table2022]."Chemical Status Value" = [26.gwChemicalStatusValue_Table2016]."Chemical Status Value"
                                      WHERE [26.gwChemicalStatusValue_Table2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [22.gwChemicalStatusValue_Table2022].Country,
                                           [22.gwChemicalStatusValue_Table2022]."Chemical Status Value",
                                           [26.gwChemicalStatusValue_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                           [22.gwChemicalStatusValue_Table2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [22.gwChemicalStatusValue_Table2022]
                                           LEFT JOIN
                                           [26.gwChemicalStatusValue_Table2016] ON [26.gwChemicalStatusValue_Table2016].Country = [22.gwChemicalStatusValue_Table2022].Country AND 
                                                                                       [22.gwChemicalStatusValue_Table2022]."Chemical Status Value" = [26.gwChemicalStatusValue_Table2016]."Chemical Status Value"
                                     WHERE [22.gwChemicalStatusValue_Table2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            "Chemical Status Value",
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY "Chemical Status Value";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _18_Chemical_Reasons_For_Failure_Area_km2(working_directory, conn, file):
    headers = ['', '',
               'Chemical Reasons For Failure (Area km2)',
               '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [26.gwChemicalReasonsForFailure_Table2016].Country,
                                            [26.gwChemicalReasonsForFailure_Table2016]."Chemical Reasons For Failure",
                                            [26.gwChemicalReasonsForFailure_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                            [22.gwChemicalReasonsForFailure_Table2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [26.gwChemicalReasonsForFailure_Table2016]
                                            LEFT JOIN
                                            [22.gwChemicalReasonsForFailure_Table2022] ON [22.gwChemicalReasonsForFailure_Table2022].Country = [26.gwChemicalReasonsForFailure_Table2016].Country AND 
                                                                         [22.gwChemicalReasonsForFailure_Table2022]."Chemical Reasons For Failure" = [26.gwChemicalReasonsForFailure_Table2016]."Chemical Reasons For Failure"
                                      WHERE [26.gwChemicalReasonsForFailure_Table2016].Country = "''' + code + '''"
                                    UNION ALL
                                    SELECT [22.gwChemicalReasonsForFailure_Table2022].Country,
                                           [22.gwChemicalReasonsForFailure_Table2022]."Chemical Reasons For Failure",
                                           [26.gwChemicalReasonsForFailure_Table2016].[Area (km^2)] AS Cycle2Pressure,
                                           [22.gwChemicalReasonsForFailure_Table2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [22.gwChemicalReasonsForFailure_Table2022]
                                           LEFT JOIN
                                           [26.gwChemicalReasonsForFailure_Table2016] ON [26.gwChemicalReasonsForFailure_Table2016].Country = [22.gwChemicalReasonsForFailure_Table2022].Country AND 
                                                                                       [22.gwChemicalReasonsForFailure_Table2022]."Chemical Reasons For Failure" = [26.gwChemicalReasonsForFailure_Table2016]."Chemical Reasons For Failure"
                                     WHERE [22.gwChemicalReasonsForFailure_Table2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                "Chemical Reasons For Failure",
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY "Chemical Reasons For Failure";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _19_Groundwater_bodies_good_quantitative_expected_date_Area_km2(working_directory, conn, file):
    headers = ['19', '', 'Groundwater bodies good quantitative expected date (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [30.gwQuantitativeStatusExpectedAchievementDate2016].Country,
                                            [30.gwQuantitativeStatusExpectedAchievementDate2016]."Quantitative Status Expected Date",
                                            [30.gwQuantitativeStatusExpectedAchievementDate2016].[Area (km^2)] AS Cycle2Pressure,
                                            [24.gwQuantitativeStatusExpectedAchievementDate2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [30.gwQuantitativeStatusExpectedAchievementDate2016]
                                            LEFT JOIN
                                            [24.gwQuantitativeStatusExpectedAchievementDate2022] ON [24.gwQuantitativeStatusExpectedAchievementDate2022].Country = [30.gwQuantitativeStatusExpectedAchievementDate2016].Country AND 
                                                                         [24.gwQuantitativeStatusExpectedAchievementDate2022]."Quantitative Status Expected Date" = [30.gwQuantitativeStatusExpectedAchievementDate2016]."Quantitative Status Expected Date"
                                      WHERE [30.gwQuantitativeStatusExpectedAchievementDate2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [24.gwQuantitativeStatusExpectedAchievementDate2022].Country,
                                           [24.gwQuantitativeStatusExpectedAchievementDate2022]."Quantitative Status Expected Date",
                                           [30.gwQuantitativeStatusExpectedAchievementDate2016].[Area (km^2)] AS Cycle2Pressure,
                                           [24.gwQuantitativeStatusExpectedAchievementDate2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [24.gwQuantitativeStatusExpectedAchievementDate2022]
                                           LEFT JOIN
                                           [30.gwQuantitativeStatusExpectedAchievementDate2016] ON [30.gwQuantitativeStatusExpectedAchievementDate2016].Country = [24.gwQuantitativeStatusExpectedAchievementDate2022].Country AND 
                                                                                       [24.gwQuantitativeStatusExpectedAchievementDate2022]."Quantitative Status Expected Date" = [30.gwQuantitativeStatusExpectedAchievementDate2016]."Quantitative Status Expected Date"
                                     WHERE [24.gwQuantitativeStatusExpectedAchievementDate2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            "Quantitative Status Expected Date",
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY "Quantitative Status Expected Date";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _20_Groundwater_bodies_good_chemical_expected_date_Area_km2(working_directory, conn, file):
    headers = ['20', '', 'Groundwater bodies good chemical expected date (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [32.gwChemicalStatusExpectedAchievementDate2016].Country,
                                            [32.gwChemicalStatusExpectedAchievementDate2016]."Good Chemical Status Expected Date",
                                            [32.gwChemicalStatusExpectedAchievementDate2016].[Area (km^2)] AS Cycle2Pressure,
                                            [26.gwChemicalStatusExpectedAchievementDate2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [32.gwChemicalStatusExpectedAchievementDate2016]
                                            LEFT JOIN
                                            [26.gwChemicalStatusExpectedAchievementDate2022] ON [26.gwChemicalStatusExpectedAchievementDate2022].Country = [32.gwChemicalStatusExpectedAchievementDate2016].Country AND 
                                                                         [26.gwChemicalStatusExpectedAchievementDate2022]."Chemical Status Expected Achievement Date" = [32.gwChemicalStatusExpectedAchievementDate2016]."Good Chemical Status Expected Date"
                                      WHERE [32.gwChemicalStatusExpectedAchievementDate2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [26.gwChemicalStatusExpectedAchievementDate2022].Country,
                                           [26.gwChemicalStatusExpectedAchievementDate2022]."Chemical Status Expected Achievement Date",
                                           [32.gwChemicalStatusExpectedAchievementDate2016].[Area (km^2)] AS Cycle2Pressure,
                                           [26.gwChemicalStatusExpectedAchievementDate2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [26.gwChemicalStatusExpectedAchievementDate2022]
                                           LEFT JOIN
                                           [32.gwChemicalStatusExpectedAchievementDate2016] ON [32.gwChemicalStatusExpectedAchievementDate2016].Country = [26.gwChemicalStatusExpectedAchievementDate2022].Country AND 
                                                                                       [26.gwChemicalStatusExpectedAchievementDate2022]."Chemical Status Expected Achievement Date" = [32.gwChemicalStatusExpectedAchievementDate2016]."Good Chemical Status Expected Date"
                                     WHERE [26.gwChemicalStatusExpectedAchievementDate2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                    "Good Chemical Status Expected Date",
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
      FROM distinctValues
     ORDER BY "Good Chemical Status Expected Date";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _21_gwQuantitativeAssessmentConfidence(working_directory, conn, file):
    headers = ['21', '', 'Groundwater bodies quantitative status assessment confidence (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [35.gwQuantitativeAssessmentConfidence2016].Country,
                                                [35.gwQuantitativeAssessmentConfidence2016].[Quantitative Assessment Confidence],
                                                [35.gwQuantitativeAssessmentConfidence2016].[Area (km^2)] AS Cycle2Pressure,
                                                [27.gwQuantitativeAssessmentConfidence2022].[Area (km^2)] AS Cycle3Pressure
                                           FROM [35.gwQuantitativeAssessmentConfidence2016]
                                                LEFT JOIN
                                                [27.gwQuantitativeAssessmentConfidence2022] ON [27.gwQuantitativeAssessmentConfidence2022].Country = [35.gwQuantitativeAssessmentConfidence2016].Country AND 
                                                                                           [27.gwQuantitativeAssessmentConfidence2022].[Quantitative Assessment Confidence] = [35.gwQuantitativeAssessmentConfidence2016].[Quantitative Assessment Confidence]
                                          WHERE [35.gwQuantitativeAssessmentConfidence2016].Country = "''' + code + '''"
                                            UNION ALL
                                            SELECT [27.gwQuantitativeAssessmentConfidence2022].Country,
                                                   [27.gwQuantitativeAssessmentConfidence2022].[Quantitative Assessment Confidence],
                                                   [35.gwQuantitativeAssessmentConfidence2016].[Area (km^2)] AS Cycle2Pressure,
                                                   [27.gwQuantitativeAssessmentConfidence2022].[Area (km^2)] AS Cycle3Pressure
                                              FROM [27.gwQuantitativeAssessmentConfidence2022]
                                                   LEFT JOIN
                                                   [35.gwQuantitativeAssessmentConfidence2016] ON [35.gwQuantitativeAssessmentConfidence2016].Country = [27.gwQuantitativeAssessmentConfidence2022].Country AND 
                                                                                              [27.gwQuantitativeAssessmentConfidence2022].[Quantitative Assessment Confidence] = [35.gwQuantitativeAssessmentConfidence2016].[Quantitative Assessment Confidence]
                                             WHERE [27.gwQuantitativeAssessmentConfidence2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT NULL,
                Country,
                [Quantitative Assessment Confidence],
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY [Quantitative Assessment Confidence];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _22_gwChemicalAssessmentConfidence(working_directory, conn, file):
    headers = ['22', '', 'Groundwater bodies chemical status assessment confidence (Area km2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [36.gwChemicalAssessmentConfidence2016].Country,
                                                [36.gwChemicalAssessmentConfidence2016].[Chemical Assessment Confidence],
                                                [36.gwChemicalAssessmentConfidence2016].[Area (km^2)] AS Cycle2Pressure,
                                                [28.gwChemicalAssessmentConfidence2022].[Area (km^2)] AS Cycle3Pressure
                                           FROM [36.gwChemicalAssessmentConfidence2016]
                                                LEFT JOIN
                                                [28.gwChemicalAssessmentConfidence2022] ON [28.gwChemicalAssessmentConfidence2022].Country = [36.gwChemicalAssessmentConfidence2016].Country AND 
                                                                                           [28.gwChemicalAssessmentConfidence2022].[Chemical Assessment Confidence] = [36.gwChemicalAssessmentConfidence2016].[Chemical Assessment Confidence]
                                          WHERE [36.gwChemicalAssessmentConfidence2016].Country = "''' + code + '''"
                                            UNION ALL
                                            SELECT [28.gwChemicalAssessmentConfidence2022].Country,
                                                   [28.gwChemicalAssessmentConfidence2022].[Chemical Assessment Confidence],
                                                   [36.gwChemicalAssessmentConfidence2016].[Area (km^2)] AS Cycle2Pressure,
                                                   [28.gwChemicalAssessmentConfidence2022].[Area (km^2)] AS Cycle3Pressure
                                              FROM [28.gwChemicalAssessmentConfidence2022]
                                                   LEFT JOIN
                                                   [36.gwChemicalAssessmentConfidence2016] ON [36.gwChemicalAssessmentConfidence2016].Country = [28.gwChemicalAssessmentConfidence2022].Country AND 
                                                                                              [28.gwChemicalAssessmentConfidence2022].[Chemical Assessment Confidence] = [36.gwChemicalAssessmentConfidence2016].[Chemical Assessment Confidence]
                                             WHERE [28.gwChemicalAssessmentConfidence2022].Country = "''' + code + '''";'''

    sql = '''SELECT DISTINCT NULL,
                Country,
                [Chemical Assessment Confidence],
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
              FROM distinctValues
             ORDER BY [Chemical Assessment Confidence];'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _23_Number_of_groundwater_bodies_by_geological_formation(working_directory, conn, file):
    headers = ['23', '', 'Number of groundwater bodies by geological formation', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [38.GWB_geologicalFormation2016].Country,
                                            [38.GWB_geologicalFormation2016]."Geological Formation",
                                            [38.GWB_geologicalFormation2016].[Area (km^2)] AS Cycle2Pressure,
                                            [29.GWB_geologicalFormation2022].[Area (km^2)] AS Cycle3Pressure
                                       FROM [38.GWB_geologicalFormation2016]
                                            LEFT JOIN
                                            [29.GWB_geologicalFormation2022] ON [29.GWB_geologicalFormation2022].Country = [38.GWB_geologicalFormation2016].Country AND 
                                                                         [29.GWB_geologicalFormation2022]."Geological Formation" = [38.GWB_geologicalFormation2016]."Geological Formation"
                                      WHERE [38.GWB_geologicalFormation2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [29.GWB_geologicalFormation2022].Country,
                                           [29.GWB_geologicalFormation2022]."Geological Formation",
                                           [38.GWB_geologicalFormation2016].[Area (km^2)] AS Cycle2Pressure,
                                           [29.GWB_geologicalFormation2022].[Area (km^2)] AS Cycle3Pressure
                                      FROM [29.GWB_geologicalFormation2022]
                                           LEFT JOIN
                                           [38.GWB_geologicalFormation2016] ON [38.GWB_geologicalFormation2016].Country = [29.GWB_geologicalFormation2022].Country AND 
                                                                                       [29.GWB_geologicalFormation2022]."Geological Formation" = [38.GWB_geologicalFormation2016]."Geological Formation"
                                     WHERE [29.GWB_geologicalFormation2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
            "Geological Formation",
            Cycle2Pressure,
            Cycle3Pressure,
            round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
          FROM distinctValues
         ORDER BY "Geological Formation";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _24_Chemical_assessment_using_monitoring_grouping_or_expert_Number(working_directory, conn, file):
    headers = ['24', '', 'Chemical assessment using monitoring, grouping or expert (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].Country,
                                            [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].[Chemical Assessment Confidence] || ' ' ||
                                            [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].[Chemical Monitoring Results] as Names,
                                            [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].Number AS Cycle2Pressure,
                                            [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].Number AS Cycle3Pressure
                                       FROM [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016]
                                            LEFT JOIN
                                            [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022] ON [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].Country = [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].Country AND 
                                                                                                                              [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].[Chemical Assessment Confidence] = [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].[Chemical Assessment Confidence] AND 
                                                                                                                              [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].[Chemical Monitoring Results] = [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].[Chemical Monitoring Results]
                                      WHERE [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].Country,
                                           [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].[Chemical Assessment Confidence] || ' ' ||
                                           [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].[Chemical Monitoring Results] as Names,
                                           [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].Number AS Cycle2Pressure,
                                           [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].Number AS Cycle3Pressure
                                      FROM [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022]
                                           LEFT JOIN
                                           [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016] ON [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].Country = [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].Country AND 
                                                                                                                             [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].[Chemical Assessment Confidence] = [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].[Chemical Assessment Confidence] AND 
                                                                                                                             [39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016].[Chemical Monitoring Results] = [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].[Chemical Monitoring Results]
                                     WHERE [30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                    Names,
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / Cycle2Pressure * 100.0, 2) 
                  FROM distinctValues
                 ORDER BY Names;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _25_Specific_pollutants_Number(working_directory, conn, file):
    headers_topic = ['25', '', 'River basin specific pollutants and pollutants reported as Other', '', '', '']
    headers = ['', '', 'Specific pollutants (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [40.swRBsPollutants].Country,
                                            [40.swRBsPollutants]."River Basin Specific Pollutant",
                                            [40.swRBsPollutants].Number AS Cycle2Pressure,
                                            [31.Surface_water_bodies_River_basin_specific_pollutants2022].Number AS Cycle3Pressure
                                       FROM [40.swRBsPollutants]
                                            LEFT JOIN
                                            [31.Surface_water_bodies_River_basin_specific_pollutants2022] ON [31.Surface_water_bodies_River_basin_specific_pollutants2022].Country = [40.swRBsPollutants].Country AND 
                                                                                                                              [40.swRBsPollutants]."River Basin Specific Pollutant" = [31.Surface_water_bodies_River_basin_specific_pollutants2022]."River Basin Specific Pollutant"
                                      WHERE [40.swRBsPollutants].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [31.Surface_water_bodies_River_basin_specific_pollutants2022].Country,
                                           [31.Surface_water_bodies_River_basin_specific_pollutants2022]."River Basin Specific Pollutant",
                                           [40.swRBsPollutants].Number AS Cycle2Pressure,
                                           [31.Surface_water_bodies_River_basin_specific_pollutants2022].Number AS Cycle3Pressure
                                      FROM [31.Surface_water_bodies_River_basin_specific_pollutants2022]
                                           LEFT JOIN
                                           [40.swRBsPollutants] ON [40.swRBsPollutants].Country = [31.Surface_water_bodies_River_basin_specific_pollutants2022].Country AND 
                                                                                                                             [40.swRBsPollutants]."River Basin Specific Pollutant" = [31.Surface_water_bodies_River_basin_specific_pollutants2022]."River Basin Specific Pollutant"
                                     WHERE [31.Surface_water_bodies_River_basin_specific_pollutants2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                    "River Basin Specific Pollutant",
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100.0, 2) 
                  FROM distinctValues
                 ORDER BY "River Basin Specific Pollutant";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _25_RBSP_Other_Number_(working_directory, conn, file):
    headers = ['', '', 'RBSP Other (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].Country,
                                            [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].[Failing RBSP Other],
                                            [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].Number AS Cycle2Pressure,
                                            [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].Number AS Cycle3Pressure
                                       FROM [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016]
                                            LEFT JOIN
                                            [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022] ON [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].Country = [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].Country AND 
                                                                                                                               [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].[Failing RBSP Other] = [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].[Failing RBSP Other]
                                      WHERE [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].Country,
                                           [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].[Failing RBSP Other],
                                           [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].Number AS Cycle2Pressure,
                                           [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].Number AS Cycle3Pressure
                                      FROM [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022]
                                           LEFT JOIN
                                           [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016] ON [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].Country = [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].Country AND 
                                                                                                                              [40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016].[Failing RBSP Other] = [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].[Failing RBSP Other]
                                     WHERE [31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                    "Failing RBSP Other",
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
                  FROM distinctValues
                 ORDER BY "Failing RBSP Other";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)

def _26_Surface_water_bodies_biological_quality_elements_status(working_directory, conn, file):
    headers = ['26', '',  'Surface water bodies biological quality elements status (1)', '', '', '']
    country = ['AT']
    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)

    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Country,
                                            [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016]."Monitoring Results" || ' ' || [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Code as Names,
                                            [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Number AS Cycle2Pressure,
                                            [32.Surface_water_bodies_QE1_assessment2022].Number AS Cycle3Pressure
                                       FROM [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016]
                                            LEFT JOIN
                                            [32.Surface_water_bodies_QE1_assessment2022] ON [32.Surface_water_bodies_QE1_assessment2022].Country = [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Country AND 
                                                                                                                               [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE1_assessment2022]."Monitoring Results" and
                                                                                                                               [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Code = [32.Surface_water_bodies_QE1_assessment2022].Code
                                      WHERE [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Country = "'''+code+'''"
                                    UNION ALL
                                    SELECT [32.Surface_water_bodies_QE1_assessment2022].Country,
                                           [32.Surface_water_bodies_QE1_assessment2022]."Monitoring Results" || ' ' || [32.Surface_water_bodies_QE1_assessment2022].Code as Names,
                                           [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Number AS Cycle2Pressure,
                                           [32.Surface_water_bodies_QE1_assessment2022].Number AS Cycle3Pressure
                                      FROM [32.Surface_water_bodies_QE1_assessment2022]
                                           LEFT JOIN
                                           [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016] ON [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Country = [32.Surface_water_bodies_QE1_assessment2022].Country AND 
                                                                                                                              [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE1_assessment2022]."Monitoring Results" and
                                                                                                                                                                       [42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016].Code = [32.Surface_water_bodies_QE1_assessment2022].Code
                                     WHERE [32.Surface_water_bodies_QE1_assessment2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                    Names,
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
                  FROM distinctValues
                 ORDER BY Names;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Surface water bodies biological quality elements status (2)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [42.Surface_water_bodies_QE2_assessment2016].Country,
                                        [42.Surface_water_bodies_QE2_assessment2016]."Monitoring Results" || ' ' || [42.Surface_water_bodies_QE2_assessment2016].Code as Names,
                                        [42.Surface_water_bodies_QE2_assessment2016].Number AS Cycle2Pressure,
                                        [32.Surface_water_bodies_QE2_assessment2022].Number AS Cycle3Pressure
                                   FROM [42.Surface_water_bodies_QE2_assessment2016]
                                        LEFT JOIN
                                        [32.Surface_water_bodies_QE2_assessment2022] ON [32.Surface_water_bodies_QE2_assessment2022].Country = [42.Surface_water_bodies_QE2_assessment2016].Country AND 
                                                                                                                           [42.Surface_water_bodies_QE2_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE2_assessment2022]."Monitoring Results" and
                                                                                                                           [42.Surface_water_bodies_QE2_assessment2016].Code = [32.Surface_water_bodies_QE2_assessment2022].Code
                                  WHERE [42.Surface_water_bodies_QE2_assessment2016].Country = "'''+code+'''"
                                UNION ALL
                                SELECT [32.Surface_water_bodies_QE2_assessment2022].Country,
                                [32.Surface_water_bodies_QE2_assessment2022]."Monitoring Results" || ' ' || [32.Surface_water_bodies_QE2_assessment2022].Code as Names,
                                [42.Surface_water_bodies_QE2_assessment2016].Number AS Cycle2Pressure,
                                [32.Surface_water_bodies_QE2_assessment2022].Number AS Cycle3Pressure
                                FROM [32.Surface_water_bodies_QE2_assessment2022]
                                LEFT JOIN
                                [42.Surface_water_bodies_QE2_assessment2016] ON [42.Surface_water_bodies_QE2_assessment2016].Country = [32.Surface_water_bodies_QE2_assessment2022].Country AND 
                                                                                                          [42.Surface_water_bodies_QE2_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE2_assessment2022]."Monitoring Results" and
                                                                                                                                                   [42.Surface_water_bodies_QE2_assessment2016].Code = [32.Surface_water_bodies_QE2_assessment2022].Code
                                WHERE [32.Surface_water_bodies_QE2_assessment2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                Names,
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
              FROM distinctValues
             ORDER BY Names;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Surface water bodies biological quality elements status (3)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [42.Surface_water_bodies_QE3_assessment2016].Country,
                                        [42.Surface_water_bodies_QE3_assessment2016]."Monitoring Results" || ' ' || [42.Surface_water_bodies_QE3_assessment2016].Code as Names,
                                        [42.Surface_water_bodies_QE3_assessment2016].Number AS Cycle2Pressure,
                                        [32.Surface_water_bodies_QE3_assessment2022].Number AS Cycle3Pressure
                                   FROM [42.Surface_water_bodies_QE3_assessment2016]
                                        LEFT JOIN
                                        [32.Surface_water_bodies_QE3_assessment2022] ON [32.Surface_water_bodies_QE3_assessment2022].Country = [42.Surface_water_bodies_QE3_assessment2016].Country AND 
                                                                                                                           [42.Surface_water_bodies_QE3_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE3_assessment2022]."Monitoring Results" and
                                                                                                                           [42.Surface_water_bodies_QE3_assessment2016].Code = [32.Surface_water_bodies_QE3_assessment2022].Code
                                  WHERE [42.Surface_water_bodies_QE3_assessment2016].Country = "'''+code+'''"
                                UNION ALL
                                SELECT [32.Surface_water_bodies_QE3_assessment2022].Country,
                                [32.Surface_water_bodies_QE3_assessment2022]."Monitoring Results" || ' ' || [32.Surface_water_bodies_QE3_assessment2022].Code as Names,
                                [42.Surface_water_bodies_QE3_assessment2016].Number AS Cycle2Pressure,
                                [32.Surface_water_bodies_QE3_assessment2022].Number AS Cycle3Pressure
                                FROM [32.Surface_water_bodies_QE3_assessment2022]
                                LEFT JOIN
                                [42.Surface_water_bodies_QE3_assessment2016] ON [42.Surface_water_bodies_QE3_assessment2016].Country = [32.Surface_water_bodies_QE3_assessment2022].Country AND 
                                                                                                          [42.Surface_water_bodies_QE3_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE3_assessment2022]."Monitoring Results" and
                                                                                                                                                   [42.Surface_water_bodies_QE3_assessment2016].Code = [32.Surface_water_bodies_QE3_assessment2022].Code
                                WHERE [32.Surface_water_bodies_QE3_assessment2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                Names,
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
              FROM distinctValues
             ORDER BY Names;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)
    write.writerow(empty_line)

    headers = ['', '', 'Surface water bodies biological quality elements status (3.3)', '', '', '']
    country = ['AT']
    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [42.Surface_water_bodies_QE3_3_assessment2016].Country,
                                        [42.Surface_water_bodies_QE3_3_assessment2016]."Monitoring Results" || ' ' || [42.Surface_water_bodies_QE3_3_assessment2016].Code as Names,
                                        [42.Surface_water_bodies_QE3_3_assessment2016].Number AS Cycle2Pressure,
                                        [32.Surface_water_bodies_QE3_3_assessment2022].Number AS Cycle3Pressure
                                   FROM [42.Surface_water_bodies_QE3_3_assessment2016]
                                        LEFT JOIN
                                        [32.Surface_water_bodies_QE3_3_assessment2022] ON [32.Surface_water_bodies_QE3_3_assessment2022].Country = [42.Surface_water_bodies_QE3_3_assessment2016].Country AND 
                                                                                                                           [42.Surface_water_bodies_QE3_3_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE3_3_assessment2022]."Monitoring Results" and
                                                                                                                           [42.Surface_water_bodies_QE3_3_assessment2016].Code = [32.Surface_water_bodies_QE3_3_assessment2022].Code
                                  WHERE [42.Surface_water_bodies_QE3_3_assessment2016].Country = "'''+code+'''"
                                UNION ALL
                                SELECT [32.Surface_water_bodies_QE3_3_assessment2022].Country,
                                [32.Surface_water_bodies_QE3_3_assessment2022]."Monitoring Results" || ' ' || [32.Surface_water_bodies_QE3_3_assessment2022].Code as Names,
                                [42.Surface_water_bodies_QE3_3_assessment2016].Number AS Cycle2Pressure,
                                [32.Surface_water_bodies_QE3_3_assessment2022].Number AS Cycle3Pressure
                                FROM [32.Surface_water_bodies_QE3_3_assessment2022]
                                LEFT JOIN
                                [42.Surface_water_bodies_QE3_3_assessment2016] ON [42.Surface_water_bodies_QE3_3_assessment2016].Country = [32.Surface_water_bodies_QE3_3_assessment2022].Country AND 
                                                                                                          [42.Surface_water_bodies_QE3_3_assessment2016]."Monitoring Results" = [32.Surface_water_bodies_QE3_3_assessment2022]."Monitoring Results" and
                                                                                                                                                   [42.Surface_water_bodies_QE3_3_assessment2016].Code = [32.Surface_water_bodies_QE3_3_assessment2022].Code
                                WHERE [32.Surface_water_bodies_QE3_3_assessment2022].Country = "'''+code+'''";'''

    sql = '''SELECT DISTINCT null, Country,
                Names,
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
              FROM distinctValues
             ORDER BY Names;'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)
    write.writerow(empty_line)


def _27_swEcologicalStatusOrPotentialExpectedAchievementDate(working_directory, conn, file):
    headers = ['27', '', 'Ecological status or potential Expected Achievement Date', '', '', '']
    country = ['AT']
    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = ['Good status already achieved', '2021 or earlier', '2022--2027', 'Less stringent objectives already achieved', 'Unknown']
    for values in data:

        drop = '''DROP TABLE IF EXISTS distinctValues;'''

        temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].Country,
                                                [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016]."Ecological Status Or Potential Expected Achievement Date",
                                                [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].Number AS Cycle2Pressure,
                                                [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].Number AS Cycle3Pressure
                                           FROM [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016]
                                                LEFT JOIN
                                                [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022] ON [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].Country = [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].Country AND 
                                                                                                                 [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].[Ecological Status Or Potential Expected Achievement Date] = [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].[Ecological Status Or Potential Expected Achievement Date]
                                          WHERE [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].Country = "''' + code + '''"
                        UNION ALL
                        SELECT [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].Country,
                        [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022]."Ecological Status Or Potential Expected Achievement Date",
                               [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].Number AS Cycle2Pressure,
                               [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].Number AS Cycle3Pressure
                          FROM [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022]
                               LEFT JOIN
                               [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016] ON [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].Country = [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].Country AND 
                                                                                                [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].[Ecological Status Or Potential Expected Achievement Date] = [45.swEcologicalStatusOrPotentialExpectedAchievementDate2016].[Ecological Status Or Potential Expected Achievement Date]
                         WHERE [34.swEcologicalStatusOrPotentialExpectedAchievementDate2022].Country = "''' + code + '''";'''

        sql = '''SELECT DISTINCT null, Country,
                    "Ecological Status Or Potential Expected Achievement Date",
                    Cycle2Pressure,
                    Cycle3Pressure,
                    round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
                  FROM distinctValues
                  where "Ecological Status Or Potential Expected Achievement Date" = "'''+ values +'''";'''

        cur.execute(drop)
        cur.execute(temporary)
        data = cur.execute(sql).fetchall()
        write.writerows(data)

def _28_swChemicalStatusExpectedAchievementDate2022(working_directory, conn, file):
    headers = ['28', '', 'Chemical Status Expected Achievement Date', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    drop = '''DROP TABLE IF EXISTS distinctValues;'''

    temporary = '''CREATE TEMPORARY TABLE distinctValues AS SELECT [47.swChemicalStatusExpectedAchievementDate2016].Country,
                    [47.swChemicalStatusExpectedAchievementDate2016]."Chemical Status Expected Achievement Date",
                                            [47.swChemicalStatusExpectedAchievementDate2016].Number AS Cycle2Pressure,
                                            [36.swChemicalStatusExpectedAchievementDate2022].Number AS Cycle3Pressure
                                       FROM [47.swChemicalStatusExpectedAchievementDate2016]
                                            LEFT JOIN
                                            [36.swChemicalStatusExpectedAchievementDate2022] ON [36.swChemicalStatusExpectedAchievementDate2022].Country = [47.swChemicalStatusExpectedAchievementDate2016].Country and
                                            [36.swChemicalStatusExpectedAchievementDate2022]."Chemical Status Expected Achievement Date" = [47.swChemicalStatusExpectedAchievementDate2016]."Chemical Status Expected Achievement Date"
                                      WHERE [47.swChemicalStatusExpectedAchievementDate2016].Country = "''' + code + '''"
                    UNION ALL
                    SELECT [36.swChemicalStatusExpectedAchievementDate2022].Country,
                            [36.swChemicalStatusExpectedAchievementDate2022]."Chemical Status Expected Achievement Date",
                           [47.swChemicalStatusExpectedAchievementDate2016].Number AS Cycle2Pressure,
                           [36.swChemicalStatusExpectedAchievementDate2022].Number AS Cycle3Pressure
                      FROM [36.swChemicalStatusExpectedAchievementDate2022]
                           LEFT JOIN
                           [47.swChemicalStatusExpectedAchievementDate2016] ON [47.swChemicalStatusExpectedAchievementDate2016].Country = [36.swChemicalStatusExpectedAchievementDate2022].Country and
                           [36.swChemicalStatusExpectedAchievementDate2022]."Chemical Status Expected Achievement Date" = [47.swChemicalStatusExpectedAchievementDate2016]."Chemical Status Expected Achievement Date"
                     WHERE [36.swChemicalStatusExpectedAchievementDate2022].Country = "'''+ code + '''";'''

    sql = '''SELECT DISTINCT null, Country,
                "Chemical Status Expected Achievement Date",
                Cycle2Pressure,
                Cycle3Pressure,
                round( (Cycle3Pressure - Cycle2Pressure) / round(Cycle2Pressure) * 100,2)
              FROM distinctValues
             ORDER BY "Chemical Status Expected Achievement Date";'''

    cur.execute(drop)
    cur.execute(temporary)
    data = cur.execute(sql).fetchall()
    write.writerows(data)


def _29_Surface_water_bodies_delineation_of_the_management_units_in_the_3rd_RBMP(working_directory, conn, file):
    headers = ['29', '', 'Surface water bodies: delineation of the management units in the 3rd RBMP', '', '', '']

    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT NULL,
                       [9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016].Country,
                       'Unchanged',
                       null,
                       [109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2022].Unchanged AS Cycle3Pressure,
                       null 
                  FROM [9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016],
                       [109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2022]
                 WHERE [109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2022].Country = 
                        [9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016].Country;''').fetchall()

    write.writerows(data)

    data = cur.execute('''SELECT NULL,
                       [9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016].Country,
                       'Other',
                       null,
                       [109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2022].Other AS Cycle3Pressure,
                       null 
                  FROM [9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016],
                       [109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2022]
                 WHERE [9.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016].Country = 
                        [109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2022].Country''').fetchall()

    write.writerows(data)

def _29_Surface_water_bodies_evolution_type_by_category_3rd_Cycle(working_directory, conn, file):
    headers = ['', '', 'Surface water bodies evolution type by category 3rd Cycle (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT NULL,"''' + code + '''",   
                       [109.2.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2022].Category || '-' || [109.2.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2022]."Evolution Type", 
                       null,
                       [109.2.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2022].Number AS Cycle3Pressure,
                       null
                       FROM [109.2.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2022];''').fetchall()

    write.writerows(data)

def _29_Surface_water_bodies_evolution_type_by_country_3rd_Cycle(working_directory, conn, file):
    headers = ['', '', 'Surface water bodies evolution type by country 3rd Cycle (Number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data1 = cur.execute('''SELECT NULL,"''' + code + '''",
                       [109.3.sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022]."Evolution Type", 
                       null,
                       [109.3.sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022].Number AS Cycle3Pressure,
                       null
                       FROM [109.3.sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022];''').fetchall()

    write.writerows(data1)

def _30_Groundwater_bodies_delineation_and_evolution_type(working_directory, conn, file):
    headers = ['30', '', 'Groundwater bodies delineation and evolution type', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data1 = cur.execute('''SELECT NULL,
                   "''' + code + '''",
                   "Unchanged (Area (km^2)",
                   NULL,
                   round([10.1.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022]."Unchanged Area (km^2)"),
                   NULL
              FROM [10.1.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022];''').fetchall()

    write.writerows(data1)

    data = cur.execute('''SELECT NULL,
                       "''' + code + '''",
                       "Other (Area (km^2)",
                       NULL,
                       round([10.1.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022]."Other Area (km^2)"),
                       NULL
                  FROM [10.1.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022];''').fetchall()

    write.writerows(data)


def _30_Evolution_Type(working_directory, conn, file):
    headers = ['', '', 'Evolution Type', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()

    data = cur.execute('''SELECT NULL,
                       "''' + code + '''",
                       [10.2.gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022]."Evolution Type",
                       NULL,
                       round([10.2.gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022]."Area (km^2)") AS Cycle3Pressure,
                       NULL
                  FROM [10.2.gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022];''').fetchall()

    write.writerows(data)

def _31_Ecological_Monitoring(working_directory, conn, file):
    headers_topic = ['31', '', 'Monitoring', '', '', '']
    headers = ['', '', 'Ecological Monitoring', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers_topic)
    write.writerow(headers)
    cur = conn.cursor()
    columns_name = ['Yes', 'No','Unknown', 'Inapplicable']
    rbd_code = cur.execute('''select distinct "RBD Code" from [129.1.ecologicalMonitoring2022]''').fetchall()

    for rbd in rbd_code:
        for temp in columns_name:
            rbd_name = ''.join(rbd)
            print(temp)
            print(rbd_name)
            print(code)
            data = cur.execute('''SELECT NULL,
                            "''' + code + '''",
                           "''' + rbd_name + '''" || '-' || " ''' + temp + ''' ",
                           NULL,
                           round([129.1.ecologicalMonitoring2022]."''' + temp + '''"),
                           NULL
                      FROM [129.1.ecologicalMonitoring2022]
                        where "RBD Code" = "''' + rbd_name + '''"''').fetchall()

            write.writerows(data)
        write.writerow(empty_line)

def _31_Chemical_Monitoring(working_directory, conn, file):
    headers = ['', '', 'Chemical Monitoring', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()
    columns_name = ['Yes', 'No','Unknown', 'Inapplicable']
    rbd_code = cur.execute('''select distinct "RBD Code" from [129.2.chemicalMonitoring2022]''').fetchall()

    for rbd in rbd_code:
        for temp in columns_name:
            rbd_name = ''.join(rbd)
            print(temp)
            print(rbd_name)
            print(code)
            data = cur.execute('''SELECT NULL,
                            "''' + code + '''",
                           "''' + rbd_name + '''" || '-' || " ''' + temp + ''' ",
                           NULL,
                           round([129.2.chemicalMonitoring2022]."''' + temp + '''"),
                           NULL
                      FROM [129.2.chemicalMonitoring2022]
                        where "RBD Code" = "''' + rbd_name + '''"''').fetchall()

            write.writerows(data)
        write.writerow(empty_line)



def _31_Quantitative_Monitoring(working_directory, conn, file):
    headers = ['', '', 'Quantitative Monitoring', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()
    columns_name = ['Yes', 'No','Unknown', 'Inapplicable']
    rbd_code = cur.execute('''select distinct "RBD Code" from [129.3.quantitativeMonitoring2022]''').fetchall()

    for rbd in rbd_code:
        for temp in columns_name:
            rbd_name = ''.join(rbd)
            print(temp)
            print(rbd_name)
            print(code)
            data = cur.execute('''SELECT NULL,
                            "''' + code + '''",
                           "''' + rbd_name + '''" || '-' || " ''' + temp + ''' ",
                           NULL,
                           round([129.3.quantitativeMonitoring2022]."''' + temp + '''"),
                           NULL
                      FROM [129.3.quantitativeMonitoring2022]
                        where "RBD Code" = "''' + rbd_name + '''"''').fetchall()

            write.writerows(data)
        write.writerow(empty_line)



def _32_Surface_water_bodies_broad_types(working_directory, conn, file):
    headers = ['32', '', 'Surface water bodies broad types (number)', '', '', '']

    code = ''.join(country)
    write = csv.writer(file)
    write.writerow(headers)
    cur = conn.cursor()
    data = cur.execute('''SELECT NULL,
              [NewDash.6.surfaceWaterBodyTypeCode2022].Country,
              [NewDash.6.surfaceWaterBodyTypeCode2022].Category || '-' || [NewDash.6.surfaceWaterBodyTypeCode2022]."Type Code",
              NULL,
               [NewDash.6.surfaceWaterBodyTypeCode2022].Number, 
               NULL
          FROM [NewDash.6.surfaceWaterBodyTypeCode2022];''').fetchall()

    write.writerows(data)
