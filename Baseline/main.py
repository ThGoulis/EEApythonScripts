import os
import sqlite3
import time
from sqlite3 import Error
import function


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def main():
    # countryCode = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE",
    #                "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT",
    #                "LT", "LU", "LV", "MT", "NL", "NO", "PL", "PT",
    #                "RO", "SE", "SI", "SK", "UK"]

    countryCode = ["FR"]

    country = ' '.join(countryCode)
    working_directory = 'C:\\Users\\Theofilos Goulis\\Documents\\BaselineAllData\\' + country + '\\'

    if not os.path.isdir(working_directory):
        os.makedirs(working_directory)
        print("Directory %s was created." % working_directory)

    database = r"C:\Users\Theofilos Goulis\Downloads\wise-wfd-database_v01_r04/WISE_SOW.sqlite"

    # create a database connection
    conn = create_connection(database)
    st = time.time()

    '''Surface water'''
    function.WISE_SOW_SurfaceWaterBody_SWB_Table(conn, countryCode, 2016, working_directory)

    function.WISE_SOW_SurfaceWaterBody_SWB_Category(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_Ecological_exemptions_and_pressures(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_Ecological_exemptions_Type(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_Quality_element_exemptions_Type(conn, countryCode, 2016, working_directory)

    function.SWB_Chemical_exemption_type(conn, countryCode, 2016, working_directory)

    function.WISE_SOW_SurfaceWaterBody_SWB_ChemicalStatus_Table(conn, countryCode, 2016, working_directory)

    function.SurfaceWaterBody_ChemicalStatus_Table_by_Category(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_Ecological_status_or_potential_groupGoodHigh(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_Ecological_status_or_potential_groupFailling(conn, countryCode, 2016, working_directory)

    function.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016(conn, countryCode, 2016, working_directory)

    function.swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016(conn, countryCode, 2016, working_directory)

    function.swEcologicalStatusOrPotentialChemical_by_Country(conn, countryCode, 2016, working_directory)

    function.swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_Failing_notUnknown_by_RBD2016(conn, countryCode, 2016, working_directory)

    function.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement(conn, countryCode, 2016, working_directory)

    function.swRBsPollutants(conn, countryCode, 2016, working_directory)

    function.swEcologicalStatusOrPotentialExpectedGoodIn2015(conn, countryCode, 2016, working_directory)

    function.swEcologicalStatusOrPotentialExpectedAchievementDate(conn, countryCode, 2016, working_directory)

    function.swChemicalStatusExpectedGoodIn2015(conn, countryCode, 2016, working_directory)

    function.swChemicalStatusExpectedAchievementDate(conn, countryCode, 2016, working_directory)
    '''Groundwater'''
    function.GroundWaterBodyCategory2016(conn, countryCode, 2016, working_directory)

    function.Groundwater_bodies_Chemical_Exemption_Type(conn, countryCode, 2016, working_directory)

    function.Groundwater_bodies_Quantitative_Exemption_Type(conn, countryCode, 2016, working_directory)

    function.gwChemical_exemptions_and_pressures(conn, countryCode, 2016, working_directory)

    function.Groundwater_bodies_Quantitative_exemptions_and_pressures(conn, countryCode, 2016, working_directory)

    function.SOW_GWB_GroundWaterBody_GWB_Chemical_status(conn, countryCode, 2016, working_directory)

    function.SOW_GWB_GroundWaterBody_GWB_Quantitative_status(conn, countryCode, 2016, working_directory)

    function.gwQuantitativeStatusValue_gwChemicalStatusValue(conn, countryCode, 2016, working_directory)

    function.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status(conn, countryCode, 2016, working_directory)

    function.SOW_GWB_gwQuantitativeReasonsForFailure_Table(conn, countryCode, 2016, working_directory)

    function.SOW_GWB_gwChemicalReasonsForFailure_Table(conn, countryCode, 2016, working_directory)

    function.gwChemicalStatusValue_Table(conn, countryCode, 2016, working_directory)

    function.gwQuantitativeStatusExpectedGoodIn2015(conn, countryCode, 2016, working_directory)

    function.gwQuantitativeStatusExpectedAchievementDate(conn, countryCode, 2016, working_directory)

    function.gwChemicalStatusExpectedGoodIn2015(conn, countryCode, 2016, working_directory)

    function.gwChemicalStatusExpectedAchievementDate(conn, countryCode, 2016, working_directory)

    function.gwQuantitativeAssessmentConfidence(conn, countryCode, 2016, working_directory)

    function.gwChemicalAssessmentConfidence(conn, countryCode, 2016, working_directory)

    function.Number_of_groundwater_bodies_failing_to_achieve_good_status(conn, countryCode, 2016, working_directory)

    function.geologicalFormation(conn, countryCode, 2016, working_directory)
    '''swSignificant'''
    function.swSignificant_Pressure_Type_Table2016(conn, countryCode, 2016, working_directory)

    function.SignificantImpactType_Table2016(conn, countryCode, 2016, working_directory)

    function.swSignificantImpactType_Table_Other2016(conn, countryCode, 2016, working_directory)

    function.swSignificantPressureType_Table_Other(conn, countryCode, 2016, working_directory)
    '''gwSignificant'''
    function.SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country(conn, countryCode, 2016, working_directory)

    function.gwSignificantImpactType2016(conn, countryCode, 2016, working_directory)

    function.gwSignificantImpactType_Other(conn, countryCode, 2016, working_directory)

    function.gwSignificantPressureType2016(conn, countryCode, 2016, working_directory)

    function.gwSignificantPressureType_OtherTable2016(conn, countryCode, 2016, working_directory)
    '''gwPollutant'''
    function.SOW_GWB_gwPollutant_Table(conn, countryCode, 2016, working_directory)

    function.SOW_GWB_gwPollutant_Table_Other(conn, countryCode, 2016, working_directory)
    '''swFailingRBSP'''
    function.Surface_water_bodies_Failing_notUnknown_by_Country(conn, countryCode, 2016, working_directory)

    function.swRiver_basin_specific_pollutants_reported_as_Other(conn, countryCode, 2016, working_directory)
    '''gwFailingRBSP'''
    function.Ground_water_bodies_Failing_notUnknown_by_Country(conn, countryCode, 2016, working_directory)

    function.Ground_water_bodies_Failing_notUnknown_by_RBD(conn, countryCode, 2016, working_directory)
    '''QualityElement'''
    function.Surface_water_bodies_QE1_Biological_quality_elements_assessment(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_QE2_assessment(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_QE3_assessment(conn, countryCode, 2016, working_directory)

    function.Surface_water_bodies_QE3_3_assessment(conn, countryCode, 2016, working_directory)

    conn.close()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

    print("Connection close...")


if __name__ == "__main__":
    main()
