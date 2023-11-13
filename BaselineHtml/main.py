import os
import pandas as pd
import eeafunctions
import shutil
import argparse
from argparse import Namespace


parser = argparse.ArgumentParser(description='A script to extract information from WISE database and create reports per country for the MS assesors')
parser.add_argument('csvpath', help='The directory of saving csv files')
parser.add_argument('country', help='Country Code to extract information from')
parser.add_argument('outputpath', help='The directory to extract the html and css file to. It must NOT end with a backslash character \\')
args: Namespace = parser.parse_args()

countryCode = [args.country]
country = ''.join(countryCode)

csv_path = args.csvpath

output_path = args.outputpath
working_directory = output_path + '\\' + country + '\\'

if not os.path.isdir(working_directory):
    os.makedirs(working_directory)
    print("Directory %s was created." % working_directory)

graphs = {
    'rbdCodeNames2016.csv': eeafunctions.rbdCodeNames,
    '1.surfaceWaterBodyNumberAndSite2016.csv': eeafunctions._1_surfaceWaterBodyNumberAndSite2016,
    '2.GroundWaterBodyCategory2016.csv': eeafunctions._2_GroundWaterBodyCategory2016,
    '3.surfaceWaterBodyCategory2016.csv': eeafunctions._3_surfaceWaterBodyCategory2016,
    '4.SignificantImpactType_Table2016.csv': eeafunctions._4_SOW_SWB_SWB_swSignificantImpactType_Table2016,
    '4.swSignificantImpactType_Table_Other2016.csv': eeafunctions._4_SOW_SWB_SWB_swSignificantImpactType_Table_Other2016,
    '4.swSignificant_Pressure_Type_Table2016.csv': eeafunctions._4_SOW_SWB_SWB_swSignificant_Pressure_Type_Table2016,
    '4.swSignificantPressureType_Table_Other.csv': eeafunctions._4_SOW_SWB_SWB_swSignificantPressureType_Table_Other,
    '5.SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country.csv': eeafunctions._5_SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country,
    '5.gwSignificantImpactType2016.csv': eeafunctions._5_gwSignificantImpactType2016,
    '5.gwSignificantImpactType_Other.csv': eeafunctions._5_gwSignificantImpactType_Other,
    '5.gwSignificantPressureType2016.csv': eeafunctions._5_gwSignificantPressureType2016,
    '5.gwSignificantPressureType_OtherTable2016.csv': eeafunctions._5_SOW_GWB_gwSignificantPressureType_OtherTable2016,
    '6.swChemical_exemption_type2016.csv': eeafunctions._6_SWB_Chemical_exemption_type2016,
    '6.Surface_water_bodies_Ecological_exemptions_Type2016.csv': eeafunctions._6_Surface_water_bodies_Ecological_exemptions_Type2016,
    '6.Surface_water_bodies_Ecological_exemptions_and_pressures2016.csv': eeafunctions._6_Surface_water_bodies_Ecological_exemptions_and_pressures2016,
    '6.Surface_water_bodies_Quality_element_exemptions_Type2016.csv': eeafunctions._6_Surface_water_bodies_Quality_element_exemptions_Type2016,
    '7.Groundwater_bodies_Chemical_Exemption_Type2016.csv': eeafunctions._7_Groundwater_bodies_Chemical_Exemption_Type2016,
    '7.Groundwater_bodies_Quantitative_Exemption_Type2016.csv': eeafunctions._7_Groundwater_bodies_Quantitative_Exemption_Type2016,
    '7.Groundwater_bodies_Quantitative_exemptions_and_pressures2016.csv': eeafunctions._7_Groundwater_bodies_Quantitative_exemptions_and_pressures2016,
    '7.gwChemical_exemptions_and_pressures.csv': eeafunctions._7_gwChemicalExcemptionPressures,
    '8.Surface_water_bodies_Ecological_status_or_potential_group_Failing.csv': eeafunctions._8_Surface_water_bodies_Ecological_status_or_potential_group_Failing,
    '8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High.csv': eeafunctions._8_Surface_water_bodies_Ecological_status_or_potential_group_Good_High,
    '8.swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016.csv': eeafunctions._8_swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016,
    '9.swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016.csv': eeafunctions._10_swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016,
    '12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016.csv': eeafunctions._12_SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016,
    '12.surfaceWaterBodyChemicalStatusGood2016.csv': eeafunctions._12_surfaceWaterBodyChemicalStatusGood2016,
    '14.swChemical_by_Country.csv': eeafunctions._14_swChemical_by_Country,
    '15.swEcologicalStatusOrPotential_by_Country2016.csv': eeafunctions._14_swEcologicalStatusOrPotential_by_Country,
    '15.swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ.csv': eeafunctions._15_swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ,
    '15.swChemicalStatusValue_by_Country_by_Categ2016.csv': eeafunctions._15_swChemicalStatusValue_by_Country_by_Categ2016,
    '16.Surface_water_bodies_Failing_notUnknown_by_Country2016.csv': eeafunctions._16_Surface_water_bodies_Failing_notUnknown_by_Country2016,
    '17.Surface_water_bodies_Failing_notUnknown_by_RBD2016.csv': eeafunctions._17_Surface_water_bodies_Failing_notUnknown_by_RBD2016,
    '18.GroundWaterBodyCategoryQuantitative_status2016.csv': eeafunctions._18_GroundWaterBodyCategoryQuantitative_status2016,
    '20.GroundWaterBodyCategoryChemical_status2016.csv': eeafunctions._20_GroundWaterBodyCategoryChemical_status2016,
    '21.SOW_GWB_gwPollutant_Table2016.csv': eeafunctions._21_SOW_GWB_gwPollutant_Table2016,
    '21.SOW_GWB_gwPollutant_Table2016_Other.csv': eeafunctions._21_SOW_GWB_gwPollutant_Table2016_Other,
    '20.GroundWaterBodyCategoryChemical_status2016.csv': eeafunctions._22_GroundWaterBodyCategoryChemical_status2016,
    '22.gwQuantitativeStatusValue_Percent_Country_2016.csv': eeafunctions._22_gwQuantitativeStatusValue_Percent_Country_2016,
    '23.Ground_water_bodies_Failing_notUnknown_by_Country2016.csv': eeafunctions._23_Ground_water_bodies_Failing_notUnknown_by_Country2016,
    '24.Ground_water_bodies_Failing_notUnknown_by_RBD2016.csv': eeafunctions._24_Ground_water_bodies_Failing_notUnknown_by_RBD2016,
    '25.Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016.csv': eeafunctions._25_Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016,
    '25.SOW_GWB_gwQuantitativeReasonsForFailure_Table2016.csv': eeafunctions._25_SOW_GWB_gwQuantitativeReasonsForFailure_Table2016,
    '26.gwChemicalStatusValue_Table2016.csv': eeafunctions._26_gwChemicalStatusValue_Table2016,
    '26.gwChemicalReasonsForFailure_Table2016.csv': eeafunctions._26_SOW_GWB_gwChemicalReasonsForFailure_Table2016,
    '29.gwQuantitativeStatusExpectedGoodIn2015.csv': eeafunctions._29_gwQuantitativeStatusExpectedGoodIn2015,
    '30.gwQuantitativeStatusExpectedAchievementDate2016.csv': eeafunctions._30_gwQuantitativeStatusExpectedAchievementDate2016,
    '31.gwChemicalStatusExpectedGoodIn2015.csv': eeafunctions._31_gwChemicalStatusExpectedGoodIn2015,
    '32.gwChemicalStatusExpectedAchievementDate2016.csv': eeafunctions._32_gwChemicalStatusExpectedAchievementDate2016,
    '35.gwQuantitativeAssessmentConfidence2016.csv': eeafunctions._35_gwQuantitativeAssessmentConfidence2016,
    '36.gwChemicalAssessmentConfidence2016.csv': eeafunctions._36_gwChemicalAssessmentConfidence2016,
    '37.Number_of_groundwater_bodies_failing_to_achieve_good_status.csv': eeafunctions._37_Number_of_groundwater_bodies_failing_to_achieve_good_status,
    '38.GWB_geologicalFormation2016.csv': eeafunctions._38_GWB_geologicalFormation2016,
    '39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016.csv': eeafunctions._39_swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016,
    '40.swRBsPollutants.csv': eeafunctions._40_swRBsPollutants,
    '40.Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016.csv': eeafunctions._40_Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016,
    '42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016.csv': eeafunctions._42_Surface_water_bodies_QE1_Biological_quality_elements_assessment2016,
    '42.Surface_water_bodies_QE2_assessment2016.csv':eeafunctions._42_Surface_water_bodies_QE2_assessment2016,
    '42.Surface_water_bodies_QE3_assessment2016.csv': eeafunctions._42_Surface_water_bodies_QE3_assessment2016,
    '42.Surface_water_bodies_QE3_3_assessment2016.csv': eeafunctions._42_Surface_water_bodies_QE3_3_assessment2016,
    '44.swEcologicalStatusOrPotentialExpectedGoodIn2015.csv': eeafunctions._44_swEcologicalStatusOrPotentialExpectedGoodIn2015,
    '45.swEcologicalStatusOrPotentialExpectedAchievementDate2016.csv': eeafunctions._45_swEcologicalStatusOrPotentialExpectedAchievementDate2016,
    '46.swChemicalStatusExpectedGoodIn2015.csv': eeafunctions._46_swChemicalStatusExpectedGoodIn2015,
    '47.swChemicalStatusExpectedAchievementDate2016.csv': eeafunctions._47_swChemicalStatusExpectedAchievementDate2016
}


f = open(working_directory + country + '.html', 'w', encoding=" iso-8859-1")
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
          </tbody></table><br>'''
f.write(html_string)


print("Generating html file...")
for csv in graphs:
    currentdf = pd.read_csv(csv_path + '\\' + csv, encoding="ISO-8859-1")
    graphs[csv](currentdf, country, f, working_directory + country)

f.write('</body></html>')

css_file = '''.dataframe {
    font-size: 11pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 1px solid silver;

    }

.dataframe td, th {
    padding: 5px;
    text-align: left;
}


.dataframe tr:nth-child(even) {
    background: #E0E0E0;
}

.dataframe tr:hover {
    background: silver;
    cursor: pointer;
}

.dataframe thead { 
    display: table-header-group; }
.dataframe tfoot { display: table-row-group }
.dataframe tr { page-break-inside: avoid }
* {
 font-size: 100%;
 font-family: Arial;
}'''

print("Creating CSS file...")

css = open(working_directory + 'dfstyle.css', 'w', encoding="UTF-8")
css.write(css_file)

# print("Generate PDF report...")
# options = {'enable-local-file-access': None}
# config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
# pdfkit.from_file(working_directory + country + '.html', working_directory + country + '.pdf', configuration=config, css=css, options=options)

print("Script completed.")

