import os
import sqlite3
from sqlite3 import Error
import openpyxl
from openpyxl.styles import PatternFill
import csvs_to_sqlite as csvsql
import pandas as pd
import csv
import re

import functions

# directory = 'C:\\Users\\Theofilos Goulis\\PycharmProjects\\Outliers\\venv\\Files\\'
working_directory = "C:\\Users\\Theofilos Goulis\\PycharmProjects\\Outliers\\venv\\ATFunctions\\"
Excel_directory = "C:\\Users\\Theofilos Goulis\\PycharmProjects\\Outliers\\venv\\ExcelAT\\"
final_Excel = "C:\\Users\\Theofilos Goulis\\Documents\\ScreeningAT\\"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

SqlDatabase = r"C:\Users\Theofilos Goulis\PycharmProjects\Outliers/BaselineScreeningOutliers.sqlite"

conn = create_connection(SqlDatabase)


# countryCode = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE",
#                "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT",
#                "LT", "LU", "LV", "MT", "NL", "NO", "PL", "PT",
#                "RO", "SE", "SI", "SK", "UK"]

countryCode = ["AT"]
code = ''.join(countryCode)

with conn:
    with open(final_Excel + 'Outliers - ' + code + '.csv',
            'w+', newline='', encoding='utf-8') as file:
        header_top = ['a/a','Country', 'Categories', '2nd', '3rd', 'Difference (%)']
        empty_line = ['', '', '', '', '', '']
        write = csv.writer(file)
        write.writerow(header_top)
        write.writerow(empty_line)

        functions._1_swNumberAndSize(working_directory, conn, file)
        write.writerow(empty_line)

        functions._2_gwNumberAndSize(working_directory, conn, file)
        write.writerow(empty_line)

        functions._3_surfaceWaterBodyCategory(working_directory, conn, file)
        write.writerow(empty_line)

        functions._4_swNumber_of_impacts_by_country(working_directory, conn, file)
        write.writerow(empty_line)

        functions._4_SignificantImpactType_Table(working_directory, conn, file)
        write.writerow(empty_line)

        functions._4_Significant_impacts_other(working_directory, conn, file)
        write.writerow(empty_line)
        functions._4_swSignificant_Pressure_Type_Table(working_directory, conn, file)
        write.writerow(empty_line)

        functions._4_swSignificant_Pressure_Type_Table_Others(working_directory, conn, file)
        write.writerow(empty_line)

        functions._5_1_gwSignificantImpactTypeByCountry(working_directory, conn, file)
        write.writerow(empty_line)

        functions._5_gwSignificantImpactType(working_directory, conn, file)
        write.writerow(empty_line)

        functions._5_gwSignificantImpactTypeOther(working_directory, conn, file)
        write.writerow(empty_line)

        functions._5_gwSignificantPressureType(working_directory, conn, file)
        write.writerow(empty_line)

        functions._5_gwSignificantPressureTypeOther(working_directory, conn, file)
        write.writerow(empty_line)

        functions._6_swChemical_exemption_type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._6_swEcological_exemption_type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._6_Ecological_Exemptions_Pressures(working_directory, conn, file)
        write.writerow(empty_line)

        functions._6_swQuality_exemption_type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._7_gwChemical_Exemption_Type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._7_gwQuantitative_Exemption_Type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._7_gwChemical_Pressure_Type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._8_Surface_water_bodies_Ecological_status_or_potential_group_Failing(working_directory, conn, file)
        write.writerow(empty_line)

        functions._8_gwGoodorHighEcologicalStatusorPotential(working_directory, conn, file)
        write.writerow(empty_line)

        functions._8_Ecological_Status_Or_potential_per_surface_water_body_category(working_directory, conn, file)
        write.writerow(empty_line)

        functions._9_swEcologicalStatusOrPotential_Unknown_Category(working_directory, conn, file)
        write.writerow(empty_line)

        functions._10_surfaceWaterBodyChemicalStatusGood(working_directory, conn, file)
        write.writerow(empty_line)

        functions._10_Chemical_status_of_surface_water_bodies_by_category(working_directory, conn, file)
        write.writerow(empty_line)

        functions._10_surfaceWaterBodyChemicalStatusPoor(working_directory, conn, file)
        write.writerow(empty_line)

        functions._11_Surface_water_bodies_ecological_status_or_potential_and_chemical_status_by_country(working_directory, conn, file)
        write.writerow(empty_line)

        functions._11_EcologicalStatus(working_directory, conn, file)
        write.writerow(empty_line)

        functions._12_Ecological_Status_or_Potential(working_directory, conn, file)
        write.writerow(empty_line)

        functions._12_Chemical_Status(working_directory, conn, file)
        write.writerow(empty_line)

        functions._13_Groundwater_bodies_quantitative_status_Area_km2(working_directory, conn, file)
        write.writerow(empty_line)

        functions._14_Groundwater_bodies_chemical_status_Area_km2(working_directory, conn, file)
        write.writerow(empty_line)

        functions._15_Groundwater_bodies_pollutants_and_pollutants_reported_as_other(working_directory, conn, file)
        write.writerow(empty_line)

        functions._16_Chemical_Status(working_directory, conn, file)
        write.writerow(empty_line)

        functions._16_Quantitative_Status(working_directory, conn, file)
        write.writerow(empty_line)

        functions._17_Groundwater_bodies_at_risk_of_failing_to_achieve_good_quantitative_status_and_reasons_for_failure_Area_km2(working_directory,conn, file)
        write.writerow(empty_line)

        functions._17_Quantitative_Reasons_For_Failure_Area_km2(working_directory,conn, file)
        write.writerow(empty_line)

        functions._18_Groundwater_bodies_at_risk_of_failing_to_achieve_good_chemical_status_and_reasons_for_failure_Area_km2(working_directory,conn, file)
        write.writerow(empty_line)

        functions._18_Chemical_Reasons_For_Failure_Area_km2(working_directory,conn, file)
        write.writerow(empty_line)

        functions._19_Groundwater_bodies_good_quantitative_expected_date_Area_km2(working_directory, conn, file)
        write.writerow(empty_line)

        functions._20_Groundwater_bodies_good_chemical_expected_date_Area_km2(working_directory, conn, file)
        write.writerow(empty_line)

        functions._21_gwQuantitativeAssessmentConfidence(working_directory, conn, file)
        write.writerow(empty_line)

        functions._22_gwChemicalAssessmentConfidence(working_directory, conn, file)
        write.writerow(empty_line)

        functions._23_Number_of_groundwater_bodies_by_geological_formation(working_directory, conn, file)
        write.writerow(empty_line)

        functions._24_Chemical_assessment_using_monitoring_grouping_or_expert_Number(working_directory, conn, file)
        write.writerow(empty_line)

        functions._25_Specific_pollutants_Number(working_directory, conn, file)
        write.writerow(empty_line)

        functions._25_RBSP_Other_Number_(working_directory, conn, file)
        write.writerow(empty_line)

        functions._26_Surface_water_bodies_biological_quality_elements_status(working_directory, conn, file)
        write.writerow(empty_line)

        functions._27_swEcologicalStatusOrPotentialExpectedAchievementDate(working_directory, conn, file)
        write.writerow(empty_line)

        functions._28_swChemicalStatusExpectedAchievementDate2022(working_directory, conn, file)
        write.writerow(empty_line)


        functions._29_Surface_water_bodies_delineation_of_the_management_units_in_the_3rd_RBMP(working_directory, conn, file)
        write.writerow(empty_line)

        functions._29_Surface_water_bodies_evolution_type_by_category_3rd_Cycle(working_directory, conn, file)
        write.writerow(empty_line)

        functions._29_Surface_water_bodies_evolution_type_by_country_3rd_Cycle(working_directory, conn, file)
        write.writerow(empty_line)

        functions._30_Groundwater_bodies_delineation_and_evolution_type(working_directory, conn, file)
        write.writerow(empty_line)


        functions._30_Evolution_Type(working_directory, conn, file)
        write.writerow(empty_line)

        functions._31_Ecological_Monitoring(working_directory, conn, file)
        write.writerow(empty_line)

        functions._31_Chemical_Monitoring(working_directory, conn, file)


        functions._31_Quantitative_Monitoring(working_directory, conn, file)

        functions._32_Surface_water_bodies_broad_types(working_directory, conn, file)
        write.writerow(empty_line)

def correct_highlight_map(val):
    color = 'white'
    absval=abs(float(val))
    if absval is None:
        color = 'white'
    if absval == 0:
        color = 'lightgrey'
    elif absval <= 25: #good
        color = 'green'
    elif 25 < absval <= 50: #moderate
        color = 'orange'
    elif 50 < absval <= 75:
        color = 'yellow'
    elif 75 < absval: #bad
        color = 'red'

    return 'background-color: {}'.format(color)

file = 'Outliers - ' + code
extention = '.csv'
with open(final_Excel + file + extention, 'r', newline='', encoding='utf-8') as f:
    print("filename", f)

    df = pd.read_csv(f)
    print(df)
    dfstyled = df.style.applymap(correct_highlight_map, subset='Difference (%)')

    print(dfstyled.to_html())

    dfstyled.to_excel(final_Excel + file + '.xlsx', engine='openpyxl', index=False)
