import pandas as pd
import eeafunctions

countries = ['HR']
country = ''.join(countries)
working_directory = 'C:\\Users\\Theofilos Goulis\\Documents\\Screening' + country + '\\3rdReportCsv' + country + '\\'


graphs = {
    # '''Csv to Html'''
    'rbdCodeNames2022.csv': eeafunctions.rbdCodeNames,
    '1.swNumberAndSize2022.csv': eeafunctions._1_swNumberAndSize2022,
    '2.gwNumberAndSize2022.csv': eeafunctions._2_gwNumberAndSize2022,
    '3.swWater_body_category_and_Type2022.csv':eeafunctions._3_surfaceWaterBodyCategory2022,
    '4.swNumber_of_impacts_by_country2022.csv': eeafunctions._4_swSignificantPressureType_NumberOfImpact_by_country2022,
    '4.swSignificant_impacts2022.csv': eeafunctions._4_SOW_SWB_SWB_swSignificantImpactType_Table2022,
    '4.swSignificantImpactType_Table_Other2022.csv': eeafunctions._4_SOW_SWB_SWB_swSignificantImpactType_Table_Other2022,
    '4.swSignificantPressureType2022.csv': eeafunctions._4_SOW_SWB_SWB_swSignificant_Pressure_Type_Table2022,
    '4.swSignificant_pressures_reported_as_Other2022.csv': eeafunctions._4_SOW_SWB_SWB_swSignificantPressureType_Table_Other2022,
    '5.1.gwSignificantImpactTypeByCountry2022.csv': eeafunctions._5_SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country2022,
    '5.gwSignificant_impacts2022.csv': eeafunctions._5_gwSignificant_impacts2022,
    '5.gwSignificantImpactType_Other2022.csv': eeafunctions._5_gwSignificantImpactType_Other,
    '5.gwSignificantPressureType_Table2022.csv': eeafunctions._5_gwSignificantPressureType2022,
    '5.gwSignificantPressureType_OtherTable2022.csv': eeafunctions._5_SOW_GWB_gwSignificantPressureType_OtherTable2022,
    '6.swChemical_exemption_type2022.csv': eeafunctions._6_SWB_Chemical_exemption_type2022,
    '6.swEcologicalexemption2022.csv': eeafunctions._6_Surface_water_bodies_Ecological_exemptions_Type2022,
    '6.swEcologicalexemptionandpressure2022.csv': eeafunctions._6_Surface_water_bodies_Ecological_exemptions_and_pressures2022,
    '6.Surface_water_bodies_Quality_element_exemptions_Type2022.csv': eeafunctions._6_Surface_water_bodies_Quality_element_exemptions_Type2022,
    '7.gwChemical_Exemption_Type2022.csv': eeafunctions._7_Groundwater_bodies_Chemical_Exemption_Type2022,
    '7.gwQuantitiveTypeAndPressure2022.csv': eeafunctions._7_Groundwater_bodies_Quantitative_Exemption_Type2022,
    '7.gwChemical_exemptions_and_pressures2022.csv': eeafunctions._7_gwChemicalExcemptionPressures2022,
    '8.Surface_water_bodies_Ecological_status_or_potential_groupFailing2022.csv':eeafunctions._8_Surface_water_bodies_Ecological_status_or_potential_group_Failing,
    '8.Surface_water_bodies_Ecological_status_or_potential_groupGood2022.csv': eeafunctions._8_Surface_water_bodies_Ecological_status_or_potential_group_Good_High,
    '8.swEcologicalStatusOrPotential_by_Category2022.csv': eeafunctions._8_swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2022,
    '9.swEcologicalStatusOrPotential_Unknown_Category2022.csv': eeafunctions._9_swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2022,
    '10.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2022.csv': eeafunctions._10_SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2022,
    '10.surfaceWaterBodyChemicalStatusGood2022.csv': eeafunctions._10_surfaceWaterBodyChemicalStatusGood2022,
    '11.swChemical_by_Country2022.csv': eeafunctions._11_swChemical_by_Country,
    '11.swEcologicalStatusOrPotential_by_Country2022.csv': eeafunctions._11_swEcologicalStatusOrPotential_by_Country,
    '12.swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ2022.csv': eeafunctions._12_swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ2022,
    '12.swChemicalStatusValue_by_Country_by_Categ2022.csv': eeafunctions._12_swChemicalStatusValue_by_Country_by_Categ2022,
    '13.Groundwater_bodies_quantitative_status2022.csv': eeafunctions._13_GroundWaterBodyCategoryQuantitative_status2022,
    '14.GroundWaterBodyCategoryChemical_status2022.csv': eeafunctions._14_GroundWaterBodyCategoryChemical_status2022,
    '15.gwPollutant2022.csv': eeafunctions._15_SOW_GWB_gwPollutant_Table2022,
    '15.gwPollutantOther2022.csv': eeafunctions._15_SOW_GWB_gwPollutant_Table2022_Other,
    '16.gwChemical_status2022.csv':eeafunctions._16_GroundWaterBodyCategoryChemical_status2022,
    '16.gwQuantitativeStatusValue_Percent_Country2022.csv': eeafunctions._16_gwQuantitativeStatusValue_Percent_Country_2022,
    '17.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022.csv': eeafunctions._17_Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022,
    '17.GWB_gwQuantitativeReasonsForFailure_Table2022.csv': eeafunctions._17_SOW_GWB_gwQuantitativeReasonsForFailure_Table2022,
    '22.gwChemicalReasonsForFailure_Table2022.csv': eeafunctions._18_SOW_GWB_gwChemicalReasonsForFailure_Table2022,
    '22.gwChemicalStatusValue_Table2022.csv': eeafunctions._18_gwChemicalStatusValue_Table2022,
    '24.gwQuantitativeStatusExpectedAchievementDate2022.csv': eeafunctions._19_gwQuantitativeStatusExpectedAchievementDate2022,
    '26.gwChemicalStatusExpectedGoodIn2022.csv': eeafunctions._20_gwChemicalStatusExpectedAchievementDate2022,
    '27.gwQuantitativeAssessmentConfidence2022.csv': eeafunctions._21_gwQuantitativeAssessmentConfidence2022,
    '28.gwChemicalAssessmentConfidence2022.csv': eeafunctions._22_gwChemicalAssessmentConfidence2022,
    '29.GWB_geologicalFormation2022.csv': eeafunctions._23_GWB_geologicalFormation2022,
    '30.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022.csv': eeafunctions._24_swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022,
    '31.Surface_water_bodies_River_basin_specific_pollutants2022.csv': eeafunctions._25_swRBsPollutants,
    '31.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2022.csv': eeafunctions._25_Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016,
    '32.Surface_water_bodies_QE1_assessment2022.csv': eeafunctions._26_Surface_water_bodies_QE1_assessment2022,
    '32.Surface_water_bodies_QE2_assessment2022.csv': eeafunctions._26_Surface_water_bodies_QE2_assessment2016,
    '32.Surface_water_bodies_QE3_assessment2022.csv': eeafunctions._26_Surface_water_bodies_QE3_assessment2016,
    '32.Surface_water_bodies_QE3_3_assessment2022.csv': eeafunctions._26_Surface_water_bodies_QE3_3_assessment2016,
    '34.swEcologicalStatusOrPotentialExpectedAchievementDate2022.csv': eeafunctions._27_swEcologicalStatusOrPotentialExpectedAchievementDate2022,
    '36.swChemicalStatusExpectedAchievementDate2022.csv': eeafunctions._28_swChemicalStatusExpectedAchievementDate2022,
    '109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2022.csv': eeafunctions._9_1_sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2022,
    '109.1.sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2022.csv': eeafunctions._9_1_sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2022,
    '109.2.sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2022.csv': eeafunctions._9_2_sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2016,
    '109.3.sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022.csv': eeafunctions._9_3_sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016,
    '10.1.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022.csv': eeafunctions.gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022,
    '10.2.gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2022.csv': eeafunctions._10_2_gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016,
    '129.1.ecologicalMonitoring2022.csv': eeafunctions._29_1_EcologicalMonitoring_Map_data,
    '129.2.chemicalMonitoring2022.csv': eeafunctions._29_2_ChemicalMonitoring_Map_data,
    '129.3.quantitativeMonitoring2022.csv': eeafunctions._29_3_QuantitativeMonitoring_Map_data,
    'NewDash.6.surfaceWaterBodyTypeCode2022.csv': eeafunctions._6_surfaceWaterBodyTypeCode,

}

for country in countries:
    f = open(working_directory + 'output\\' + country + '.html', 'w', encoding=" iso-8859-1")
    html_string = '<html><head><meta charset="UTF-8"><title>'
    html_string += country
    html_string += '''</title></head>
       <link rel="stylesheet" type="text/css" href="dfstyle.css"/>
       <body>
       <h3>MS Baselines Country: '''
    html_string += country
    html_string += '''</h3><table border="1" class="dataframe">
              <thead>
                <tr style="text-align: right;"><th>Abbreviation</th><th>Description</th></tr></thead>
                <tbody>
                <tr><td colspan="2" align="center" font size="+1"><b>Surface water bodies</b></td></tr>
                <tr><td>RW</td><td>River water body</td></tr>
                <tr><td>LW</td><td>Lake water body</td></tr>
                <tr><td>TW</td><td>Transitional water body</td></tr>
                <tr><td>CW</td><td>Coastal water body</td></tr>
                <tr><td>TeW</td><td>Territorial water body</td></tr>
                <tr><td colspan="2" align="center" font size="+1"><b>Surface water bodies ecological status</b></td></tr>
                <tr><td>1</td><td>High</td></tr>
                <tr><td>2</td><td>Good</td></tr>
                <tr><td>3</td><td>Moderate</td></tr>
                <tr><td>4</td><td>Poor</td></tr>
                <tr><td>5</td><td>Bad</td></tr>
                <tr><td colspan="2" align="center" font size="+1"><b>Surface water bodies chemical status</b></td></tr>
                <tr><td>2</td><td>Good</td></tr>
                <tr><td>3</td><td>Poor</td></tr>
                <tr><td colspan="2" align="center" font size="+1"><b>Groundwater bodies quantitative and chemical status</b></td></tr>
                <tr><td>2</td><td>Good</td></tr>
                <tr><td>3</td><td>Poor</td></tr>
              </tbody></table><br>
     '''
    f.write(html_string)

    for csv in graphs:
        print(csv)
        currentdf = pd.read_csv(working_directory + csv, encoding="ISO-8859-1")
        graphs[csv](currentdf, country, f)

    f.write('</body></html>')
