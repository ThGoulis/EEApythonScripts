from argparse import Namespace
import sqlite3
import time
from sqlite3 import Error
import functions
import os
import argparse


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    print("Success connection with database")
    return conn


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A script to extract information from WISE database and create reports per country for the MS assesors')
    parser.add_argument('db', help='Path to SQLite DB file')
    parser.add_argument('country', help='Country Code to extract information from')
    parser.add_argument('outputdir', help='The directory to extract the CSVs to. It must NOT end with a backslash character \\')
    args: Namespace = parser.parse_args()

    countryCode = [args.country]

    country = ' '.join(countryCode)
    output_dir = args.outputdir  # .strip("\\")

    working_directory = output_dir + '\\' + country + '\\'

    if not os.path.isdir(working_directory):
        os.makedirs(working_directory)
        print("Directory %s was created." % working_directory)

    # create a database connection
    database = args.db
    conn = create_connection(database)
    st = time.time()
    print("Generated output files")

    scripts = {
        # functions.swNumberAndSize(working_directory, conn, countryCode, 2022),
               # functions.gwNumberAndSize(working_directory, conn, countryCode, 2022),
               # functions.swWater_body_category_and_Type(working_directory, conn, countryCode, 2022),
               # functions.swSignificantPressureType(working_directory, conn, countryCode, 2022),
               # functions.swSignificant_pressures_reported_as_Other(working_directory, conn, countryCode, 2022),
               # functions.swSignificant_impacts(working_directory, conn, countryCode, 2022),
               # functions.swNumber_of_impacts_by_country(working_directory, conn, countryCode, 2022),
               # functions.gwSignificantImpactTypeByCountry2022(working_directory, conn, countryCode, 2022),
               # functions.gwSignificant_impacts(working_directory, conn, countryCode, 2022),
               # functions.gwSignificantImpactType_Other(working_directory, conn, countryCode, 2022),
               # functions.gwSignificantPressureType_Table(working_directory, conn, countryCode, 2022),
               # functions.gwSignificantPressureType_OtherTable(working_directory, conn, countryCode, 2022),
               # functions.swSignificantImpactType_Table_Other(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_Quality_element_exemptions_Type(working_directory, conn, countryCode, 2022),
               # functions.swEcologicalexemptionandpressure(working_directory, conn, countryCode, 2022),
               # functions.swEcologicalexemption(working_directory, conn, countryCode, 2022),
               # functions.swEcologicalStatusOrPotential_by_Category(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_Ecological_status_or_potential_groupGood(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_Ecological_status_or_potential_groupFailing(working_directory, conn, countryCode, 2022),
               # functions.swEcologicalStatusOrPotential_Unknown_Category(working_directory, conn, countryCode, 2022),
               # functions.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category(working_directory, conn, countryCode, 2022),
               # functions.SurfaceWaterBody_ChemicalStatus_Table_by_Category(working_directory, conn, countryCode, 2022),
               # functions.surfaceWaterBodyChemicalStatusGood(working_directory, conn, countryCode, 2022),
               # functions.swEcologicalStatusOrPotentialChemical_by_Country(working_directory, conn, countryCode, 2022),
               # functions.swEcological_status_or_potential_and_chemical_status_by_category(working_directory, conn, countryCode, 2022),
               # functions.GroundWaterBodyCategoryChemical_status(working_directory, conn, countryCode, 2022),
               # functions.Groundwater_bodies_quantitative_status(working_directory, conn, countryCode, 2022),
               # functions.SOW_GWB_gwChemicalReasonsForFailure_Table(working_directory, conn, countryCode, 2022),
               # functions.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status(working_directory, conn, countryCode, 2022),
               # functions.gwChemical_status(working_directory, conn, countryCode, 2022),
               # functions.gwChemicalStatusValue_Table(working_directory, conn, countryCode, 2022),
               # functions.gwQuantitativeAssessmentConfidence(working_directory, conn, countryCode, 2022),
               # functions.gwChemicalAssessmentConfidence(working_directory, conn, countryCode, 2022),
               # functions.geologicalFormation(working_directory, conn, countryCode, 2022),
               # functions.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_River_basin_specific_pollutants(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_QE1__assessment(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_QE2_assessment(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_QE3_assessment(working_directory, conn, countryCode, 2022),
               # functions.Surface_water_bodies_QE3_3_assessment(working_directory, conn, countryCode, 2022),
               # functions.gwQuantitativeStatusExpectedAchievementDate(working_directory, conn, countryCode, 2022),
               # functions.gwChemicalStatusExpectedGoodIn2022(working_directory, conn, countryCode, 2022),
               # functions.gwChemicalStatusExpectedAchievementDate(working_directory, conn, countryCode, 2022),
               # functions.gwQuantitativeStatusValue_gwChemicalStatusValue(working_directory, conn, countryCode, 2022),
               # functions.swEcologicalStatusOrPotentialExpectedAchievementDate(working_directory, conn, countryCode, 2022),
               # functions.swChemicalStatusExpectedAchievementDate(working_directory, conn, countryCode, 2022),
               # functions.gwQuantitativeReasonsForFailure_Table(working_directory, conn, countryCode, 2022),
               # functions.SWB_Chemical_exemption_type(working_directory, conn, countryCode, 2022),
               # functions.gwChemical_Exemption_Type(working_directory, conn, countryCode, 2022),
               # functions.gwChemical_exemptions_and_pressures(working_directory, conn, countryCode, 2022),
               # # functions.generate_quantitivetypeandpressure_table(conn),
               # functions.gwQuantitiveTypeAndPressure(working_directory, conn, countryCode, 2022),
               # functions.gwPollutantOther(working_directory, conn, countryCode, 2022),
               # functions.gwPollutant(working_directory, conn, countryCode, 2022),
               # functions.ecologicalMonitoring(working_directory, conn, countryCode, 2022),
               # functions.chemicalMonitoring(working_directory, conn, countryCode, 2022),
               # functions.quantitativeMonitoring(working_directory, conn, countryCode, 2022),
               # functions.rbdCodeNames(working_directory, conn, countryCode, 2022),
               # functions.surfaceWaterBodyTypeCode(working_directory, conn, countryCode, 2022),
               # functions.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, 2022),
               # functions.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, 2022),
               # functions.sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, 2022),
               # functions.gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, 2022),
               # functions.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP(working_directory, conn, countryCode, 2022),
               functions.per_RBD_ExemptionType(working_directory, conn, countryCode, 2022),
               }

    with conn:
        scripts

    conn.close()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

    print("Connection close...")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
