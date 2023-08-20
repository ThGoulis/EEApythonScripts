import matplotlib.pyplot as plt
from itertools import zip_longest
import re
import os


working_directory = 'C:\\Users\\Theofilos Goulis\\Documents\\BaselineAllData\\AT\\'
imagepath = 'C:\\Users\\Theofilos Goulis\\Documents\\BaselineAllData\\AT\\output\\'

if not os.path.isdir(imagepath):
    os.makedirs(imagepath)
    print("Directory %s was created." % imagepath)



def rbdCodeNames (df,country, outfile):
    html_string = '''<h3>RBD Code and names </h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))


def _1_surfaceWaterBodyNumberAndSite2016(df, country, outfile):
    html_string = '''<h3>1. Number and size of surface water bodies </h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Country', 'Number']].plot.bar('Country', 'Number', rot=0)
        plt.title('Surface Waters bodies\nNumber')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '1.surfaceWaterBodyNumberAndSite2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'

    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _2_GroundWaterBodyCategory2016(df, country, outfile):
    html_string = '''<h3>2. Number and size of groundwater bodies</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Country', 'Number']].plot.bar('Country', 'Number', rot=0, color="#653700")
        plt.title('Groundwater bodies\nNumber')
        plt.xlabel('')
        plt.ylabel('Total Number of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '2.GroundWaterBodyCategory2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _3_surfaceWaterBodyCategory2016(df, country, outfile):
    html_string = '''<h3>3. Number of surface water bodies by category and type</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        # temp['Wrap Values'] = df['Type'].str.wrap(20)
        categories = ["RW", "LW", "TW","CW", "TeW"]
        for categ in categories:
            if not temp.loc[(temp['Surface Water Body Category'] == categ)].empty:
                temp1 = temp.loc[(temp['Surface Water Body Category'] == categ)]
                temp1['Wrap Values'] = temp1['Type'].str.wrap(20)
                temp1[['Wrap Values', 'Total']].plot.bar('Wrap Values', 'Total', rot=65)
                plt.title('Number of surface water bodies by category and type\n(' + categ  + ')' )
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '3.surfaceWaterBodyCategory2016' + country + categ + '.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _4_SOW_SWB_SWB_swSignificantImpactType_Table2016(df, country, outfile):
    html_string = '''<h3>4. Surface water bodies significant pressures and impacts</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp['Wrap Values'] = temp['Significant Impact Type'].str.wrap(30)
        temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], rot=65, figsize=(12,4))
        plt.title('Surface water bodies\nsignificant impacts')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nsurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '4.SOW_SWB_SWB_swSignificantImpactType_Table2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _4_SOW_SWB_SWB_swSignificantImpactType_Table_Other2016(df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _4_SOW_SWB_SWB_swSignificant_Pressure_Type_Table2016(df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _4_SOW_SWB_SWB_swSignificantPressureType_Table_Other(df, country, outfile):
    df.dropna()
    values = df.loc[(df['Country'] == country)]
    if not values.empty:
        html_string = '''<br>'''
        html_string += values.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _4_SOW_SWB_SWB_swSignificantImpactType_Table_Overall2016(df, country, outfile):
    html_string = '''<br>'''
    html_string += df.to_html()
    df.plot(x='Significant Impact Type', y='Number',
            kind="bar", xlabel="",
            ylabel="Total Number of\nSurface water bodies", title="Surface water bodies\nSignificant impacts type", rot=85)
    plt.gcf()
    plt.draw()
    figfilename = imagepath + '4.SOW_SWB_SWB_swSignificantImpactType_Table_Overall2016' + country + '.png'
    plt.savefig(figfilename, bbox_inches='tight')
    html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _4_SOW_SWB_SWB_swSignificant_Pressure_Type_Table_Overall2016(df, country, outfile):
    try:
        html_string = '''<br>'''
        temp = df.loc[df['Significant Pressure Type Group']].unique()
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))
    except:
        pass

def _5_SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country(df, country, outfile):
    html_string = '''<h3>5. Groundwater bodies significant pressures and impacts</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Number of Impacts', 'Area (km^2)']].plot.bar('Number of Impacts', 'Area (km^2)', rot=0, color="#653700")
        plt.title('Groundwater bodies\nNumber of impacts')
        plt.xlabel('Number of impacts')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _5_gwSignificantImpactType2016(df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Significant Impact Type'].str.wrap(25)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)', rot=0, color="#653700")

        else:
            temp['Wrap Values'] = temp['Significant Impact Type'].str.wrap(30)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                                     figsize=(12, 4), rot=80, color="#653700")

        plt.title('Groundwater bodies of\nSignificant impacts')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.gwSignificantImpactType2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _5_gwSignificantImpactType_Other(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        temp = df.loc[(df['Country'] == country)]

        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Significant Impact Other'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                                      rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Significant Impact Other'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                                      figsize=(15, 4), rot=0, color="#653700")
        plt.title('Groundwater bodies of\nSignificant impact reported as "Other"')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.gwSignificantImpactType_Other' + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _5_SOW_GWB_gwSignificantPressureType_OtherTable2016(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)

        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Significant Pressure Other'].str.wrap(25)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', y=['Area (km^2)'],
                                                                        rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Significant Pressure Other'].str.wrap(25)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', y=['Area (km^2)'],
                                                                        figsize=(12, 4), rot=80, color="#653700")

        plt.title('Groundwater bodies of\nSignificant pressure reported as "Other"')
        plt.xlabel('')
        plt.ylabel('total Area (km^2) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.SOW_GWB_gwSignificantPressureType_OtherTable2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _5_gwSignificantPressureType2016(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)

        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Significant Pressure Type'].str.wrap(25)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)', rot=0, color="#653700")

        else:
            temp['Wrap Values'] = temp['Significant Pressure Type'].str.wrap(30)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)', figsize=(12, 4), rot=80, color="#653700")

        plt.title('Groundwater bodies of\nSignificant pressure')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.gwSignificantPressureType2016' + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _6_SWB_Chemical_exemption_type2016(df, country, outfile):
    html_string = '''<h3>6. Surface water bodies exemptions and pressures</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Exemption Type', 'Area (km^2)']].plot.bar('Chemical Exemption Type', 'Area (km^2)',
                                                                 rot=15)
        plt.title('Surface water bodies\nChemical exemption type')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '6. SWB_Chemical_exemption_type2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _6_Surface_water_bodies_Ecological_exemptions_Type2016(df, country, outfile):
    html_string = '''<br>
            '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[(df['Country'] == country)].count()
        if Arguments['Country'] < 2:
            temp['Wrap Values'] = temp['Ecological Exemption Type'].str.wrap(25)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', 'Number', rot=0)

        else:
            temp['Wrap Values'] = temp['Ecological Exemption Type'].str.wrap(30)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', 'Number',
                                                     figsize=(15, 4), rot=15)

        plt.title('Surface water body\nEcological exemption')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '6.Surface_water_bodies_Quality_element_exemptions_Type2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _6_Surface_water_bodies_Ecological_exemptions_and_pressures2016(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _6_Surface_water_bodies_Quality_element_exemptions_Type2016(df, country, outfile):
    EETGList = df['Quality Element Exemption Type Group'].unique().tolist()
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        for group in EETGList:
            temp = df.loc[(df['Country'] == country) & (df['Quality Element Exemption Type Group'] == group)]
            if not temp.empty:
                html_string += temp.to_html(index=False)

                Arguments = df.loc[(df['Country'] == country) & (df['Quality Element Exemption Type Group'] == group)].count()
                if Arguments['Country'] < 2:
                    temp['Wrap Values'] = temp['Quality Element Exemption Type'].str.wrap(25)
                    temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', 'Number', rot=0)

                else:
                    temp['Wrap Values'] = temp['Quality Element Exemption Type'].str.wrap(30)
                    temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', 'Number',
                                                                           figsize=(12, 4), rot=15)

                plt.title('Surface water bodies\nQuality element exemption type')
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '6.Surface_water_bodies_Quality_element_exemptions_Type2016' + country + group +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _7_Groundwater_bodies_Chemical_Exemption_Type2016(df, country, outfile):
    html_string = '''<h3>7. Groundwater bodies exemptions and pressures</h3>'''

    if not df.loc[(df['Country'] == country)].empty:
        try:
            temp = df.loc[(df['Country'] == country)]
            html_string += temp.to_html(index=False)
            temp['Wrap Values'] = temp['Chemical Exemption Type'].str.wrap(25)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                                     rot=45, color="#653700")
            plt.title('Groundwater bodies\nChemical exemption type')
            plt.xlabel('')
            plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '7.Groundwater_bodies_Chemical_Exemption_Type2016' + country + '.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
        except:
            pass
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _7_Groundwater_bodies_Quantitative_Exemption_Type2016(df, country, outfile):
    EETGList = df['Quantitative Exemption Type Group'].unique().tolist()
    EETList = df['Quantitative Exemption Type'].unique().tolist()
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        for types, group in zip(EETList, EETGList):
            if not df.loc[(df['Country'] == country) & (df['Quantitative Exemption Type Group'] == group)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Quantitative Exemption Type Group'] == group)]
                html_string += temp.to_html(index=False)
                temp[['Quantitative Exemption Type', 'Area (km^2)']].plot.bar('Quantitative Exemption Type',
                                                                             'Area (km^2)', rot=15, color="#653700")
                plt.title('Groundwater bodies\nQuantitative exemption type')
                plt.xlabel('')
                plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '7.Groundwater_bodies_Quantitative_Exemption_Type2016' + country + group +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _7_Groundwater_bodies_Quantitative_exemptions_and_pressures2016(df, country, outfile):
    html_string = '''<br>'''

    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _7_gwChemicalExcemptionPressures (df, country, outfile):
    html_string = '''<br>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _8_Surface_water_bodies_Ecological_status_or_potential_group_Failing(df, country, outfile):
    html_string = '''<h3>8. Number and percent of surface water bodies at good or high and failling to achieve good ecological status or potential</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Country', 'Number']].plot.bar('Country', y=['Number'], rot=0)
        plt.title('Surface water bodies\nFailing to achieve good ecological status or potential')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '8.Surface_water_bodies_Ecological_status_or_potential_group_Failing' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _8_Surface_water_bodies_Ecological_status_or_potential_group_Good_High(df, country, outfile):
    html_string = '''<br>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Country', 'Number']].plot.bar('Country', y=['Number'], rot=0)
        plt.title('Surface water bodies\nHigh-Good')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _8_swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2016(df, country, outfile):
    categories = ["RW", "LW", "TW", "CW", "TeW"]
    ESOPV = df['Ecological Status Or Potential Value'].unique().tolist()
    if not df.loc[(df['Country'] == country) ].empty:
        html_string = '''<br>
        '''
        for categ, esopv in zip(categories, ESOPV):

            if not df.loc[(df['Country'] == country) & (df['Surface Water Body Category'] == categ)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Surface Water Body Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                                  'Number', rot=0)
                plt.title('Surface water bodies\n(' + categ +')')
                plt.xlabel('Values')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '8.Surface_water_bodies_Ecological_status_or_potential_group_Good_High' + country + categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _9_swEcologicalStatusOrPotential_All_Category2ndRBMP2016(df, country, outfile):
    categories = ["RW", "LW", "TW", "CW", "TeW"]
    ESOPV = df['Ecological Status Or Potential Value'].unique().tolist()
    if not df.loc[(df['Country'] == country)].empty:
        for categ, esopv in zip(categories, ESOPV):
            html_string = '''<h3>9. Surface water body category and ecological status</h3>
            '''
            if not df.loc[(df['Country'] == country) & (df['Surface Water Body Category'] == categ)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Surface Water Body Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Ecological Status Or Potential Value', 'Number']].plot.bar(
                    'Ecological Status Or Potential Value', 'Number', rot=0)
                plt.title('Surface water bodies\nEcological status or potential (' + categ + ')')
                plt.xlabel('Type')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '9.swEcologicalStatusOrPotential_All_Category2ndRBMP2016' + country + categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _10_swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016(df, country, outfile):
    html_string = '''<h3>9. Number of surface water bodies at unknown ecological status by category</h3>
    '''
    categories = ["RW", "LW", "TW", "CW"]
    if not df.loc[(df['Country'] == country)].empty:
        for categ in categories:
            if not df.loc[(df['Country'] == country) & (df['Surface Water Body Category'] == categ)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Surface Water Body Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Ecological Status Or Potential Value', 'Number']].plot.bar(
                    'Ecological Status Or Potential Value', 'Number', rot=0)
                plt.title('Surface Water Bodies Categories\nEcological status of potential (' + categ + ')')
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '10.swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2016' + country + categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _11_swEcologicalStatusOrPotential_by_Category_Total_By_Category2ndRBMP2016(df, country, outfile):
    ESOPV = df['Ecological Status Or Potential Value'].unique().tolist()
    categories = df['Surface Water Body Category'].unique().tolist()
    #if not df.loc[(df['Country'] == country)].empty:
    for categ, esopv in zip(categories, ESOPV):
        html_string = '''<h3>11. Surface water bodies ecological status or potential</h3>
        '''
        try:
            temp = df.loc[(df['Surface Water Body Category'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                              'Number', rot=0)
            plt.title('Surface water bodies categories\nEcological status or potential (' + categ + ')')
            plt.xlabel('')
            plt.ylabel('Total Number')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '11.swEcologicalStatusOrPotential_by_Category_Total_By_Category2ndRBMP2016' + country + categ +'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
            outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))
        except:
            pass


def _11_swEcologicalStatusOrPotential_by_Country_Total_Status2ndRBMP(df, country, outfile):
    ESOPV = df['Ecological Status Or Potential Value'].unique().tolist()
    categories = df['Surface Water Body Category'].unique().tolist()
    if not df.loc[(df['Country'] == country)].empty:
        for categ, esopv in zip(categories, ESOPV):
            html_string = '''<br>
            '''
            try:
                temp = df.loc[(df['Surface Water Body Category'] == categ) & (df['Country'] == country)]
                html_string += temp.to_html(index=False)
                temp[['Ecological Status Or Potential Value', 'Number']].plot.bar(
                    'Ecological Status Or Potential Value', 'Number', rot=0)
                plt.title('Surface water bodies categories\nEcological status or potential (' + categ + ')')
                plt.xlabel('')
                plt.ylabel('Total Number')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '11.swEcologicalStatusOrPotential_by_Country_Total_Status2ndRBMP' + country + categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
                outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))
            except:
                pass

def _12_SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016(df, country, outfile):
    categories = df['Surface Water Body Category'].unique().tolist()
    html_string = '''<h3>10. Chemical status of surface water bodies by category</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        for categ in categories:
            if not df.loc[(df['Surface Water Body Category'] == categ) & (df['Country'] == country)].empty:
                temp = df.loc[(df['Surface Water Body Category'] == categ) & (df['Country'] == country)]
                html_string += temp.to_html(index=False)
                temp[['Chemical Status Value', 'Number']].plot.bar('Chemical Status Value', 'Number', rot=0)
                plt.title('Surface water bodies Categories\n' + categ)
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '12.SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2016' + country + categ+ '.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))


def _12_surfaceWaterBodyChemicalStatusGood2016(df, country, outfile):
    html_string = '''<br>
        '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Number']].plot.bar('Chemical Status Value', y=['Number'], rot=0)
        plt.title('Surface water bodies\nChemical status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water body')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '12.surfaceWaterBodyChemicalStatusGood2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _12_swChemicalStatusValue_by_Country2016(df, country, outfile):
    html_string = '''<br>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        try:
            temp = df.loc[(df['Country'] == country)]
            html_string += temp.to_html(index=False)
            temp[['Chemical Status Value', 'Percent']].plot.bar('Chemical Status Value', 'Percent', rot=0)
            plt.title('Surface water bodies categories\nChemical status')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.xlabel('')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '12.swChemicalStatusValue_by_Country2016' + country + '.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
            outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))
        except:
            pass

def _13_gwChemicalStatus_Table2016(df, country, outfile):
    html_string = '''<h3>13. Surface water bodies chemical status</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Country', 'Good', 'Unknown', 'Poor']].plot.bar('Country', y=['Good', 'Unknown', 'Poor'], rot=0, color="#653700")
        plt.title('Ground water bodies\nChemical status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nGround water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '13.gwChemicalStatus_Table2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _14_swEcologicalStatusOrPotential_by_Category_Total_Status2ndRBMP2016(df, country, outfile):

    html_string = '''<h3>14. Surface water bodies ecological status or potential and chemical status by country</h3>
    '''
    html_string += df.to_html()
    df[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value', 'Number',
                                                                    rot=0)
    plt.title('Surface Water Bodies\nEcological status or potential')
    plt.xlabel('')
    plt.ylabel('Total Number of\nSurface water bodies')
    plt.gcf()
    plt.draw()
    figfilename = imagepath + '14.swEcologicalStatusOrPotential_by_Category_Total_Status2ndRBMP2016' + country + '.png'
    plt.savefig(figfilename, bbox_inches='tight')
    html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _14_swChemical_by_Country(df, country, outfile):
    html_string = '''<h3>11. Surface water bodies ecological status or potential and chemical status by country</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Number']].plot.bar('Chemical Status Value', 'Number',
                                                                        rot=0)
        plt.title('Surface Water Bodies\nChemical Status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '14.swChemical_by_Country' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _14_swEcologicalStatusOrPotential_by_Country (df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value', 'Number',
                                                                        rot=0)
        plt.title('Surface Water Bodies\nEcological status or potential')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '14.swEcologicalStatusOrPotential_by_Country' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _15_swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ(df, country, outfile):
    html_string = '''<h3>12. Surface water bodies ecological status or potential and chemical status by category</h3>
    '''
    categories = ["RW", "LW", "TW", "CW","TeW"]
    if not df.loc[(df['Country'] == country)].empty:
        for categ in categories:
            if not df.loc[(df['Country'] == country) & (df['Categories'] == categ)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Categories'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Ecological Status Value', 'Number']].plot.bar('Ecological Status Value', 'Number', rot=0)
                plt.title('Surface water bodies Categories\nEcological status')
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface Water Bodies Category')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '_15_swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ' + country + categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _15_swChemicalStatusValue_by_Country_by_Categ2016(df, country,outfile):
    html_string = '''<br>'''
    categories = ["RW", "LW", "TW", "CW", "TeW"]
    if not df.loc[(df['Country'] == country)].empty:
        for categ in categories:
            if not df.loc[(df['Country'] == country) & (df['Categories'] == categ)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Categories'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Chemical Status Value', 'Number']].plot.bar('Chemical Status Value', 'Number', rot=0)
                plt.title('Surface water bodies Categories\n(' + categ + ')')
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface Water Bodies Category')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '_15_swChemicalStatusValue_by_Country_by_Categ2016' + country + categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _15_swEcologicalStatusOrPotentialValue_by_Country2016(df, country, outfile):
    html_string = '''<br>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Ecological Status or Potential Value', 'Number']].plot.bar('Ecological Status or Potential Value',
                                                                          y=['Number'], rot=0)
        plt.title('Surface water bodies Categories\nEcological status or potential')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface Water Bodies Category')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_15_swEcologicalStatusOrPotentialValue_by_Country2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _15_swEcologicalStatusOrPotential_ChemicalStatus_by_Category2016(df, country, outfile):
    categories = df['Surface Water Body Category'].unique().tolist()
    html_string = '''<br>'''
    for categ in categories:
        if not df.loc[(df['Categories'] == categ)].empty:
            temp = df.loc[(df['Surface Water Body Category'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                              y=['Number'], rot=0)
            plt.title('Surface water bodies categories\nEcological status or potential')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface Water Bodies Category')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '_15_swEcologicalStatusOrPotential_ChemicalStatus_by_Category2016' + country + categ +'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _15_swEcologicalStatusOrPotential_ChemicalStatus_by_Category_Chemical2016(df, country, outfile):
    ESOPV = df['Chemical Status Value'].unique().tolist()
    categories = df['Surface Water Body Category'].unique().tolist()
    html_string = '''<br>
    '''
    for categ, esopv in zip_longest(categories, ESOPV):
        if not df.loc[(df['Categories'] == categ)].empty:
            temp = df.loc[(df['Surface Water Body Category'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Surface Water Body Category', 'Chemical Status Value', 'Number']].plot.bar('Chemical Status Value',
                                                                                              y=[
                                                                                                  'Surface Water Body Category',
                                                                                                  'Number'], rot=0)
            plt.title('Surface water bodies Categories\n(' + categ +')')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface Water Bodies Category')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '15.swEcologicalStatusOrPotential_ChemicalStatus_by_Category_Chemical2016' + categ + '.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _15_swEcologicalStatusOrPotential_ChemicalStatus_by_Category_Ecological2016(df, country, outfile):
    ESOPV = df['Ecological Status Or Potential Value'].unique().tolist()
    categories = df['Surface Water Body Category'].unique().tolist()
    html_string = '''<br>
    '''
    for categ, esopv in zip_longest(categories, ESOPV):
        if not df.loc[(df['Categories'] == categ)].empty:
            temp = df.loc[(df['Surface Water Body Category'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Surface Water Body Category', 'Ecological Status Or Potential Value', 'Number']].plot.bar(
                'Ecological Status Or Potential Value', y=['Surface Water Body Category', 'Number'], rot=0)
            plt.title('Surface water bodies Categories \n(' + categ + ')')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface Water Bodies Category')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '_15_swEcologicalStatusOrPotential_ChemicalStatus_by_Category_Ecological2016' + categ + '.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _16_Surface_water_bodies_Failing_notUnknown_by_Country2016(df, country, outfile):
    html_string = '''<h3>13. % Surface water bodies failing to achieve good status by country</h3>'''
    temp = df.loc[(df['Country'] == country)]
    html_string += temp.to_html(index=False)
    if not df.loc[(df['Country'] == country)].empty:
        temp[['Country', 'Known Status', 'Failing status']].plot.bar('Country',
                                                                     y=['Known Status', 'Failing status'], rot=0)
        plt.title('Surface water bodies')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_16_Surface_water_bodies_Failing_notUnknown_by_Country2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _17_Surface_water_bodies_Failing_notUnknown_by_RBD2016(df, country, outfile):
    html_string = '''<h3>14. % Surface water bodies failing to achieve good status by country and RBD</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)

        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['RBD Name'].str.wrap(25)
            temp[['Country', 'Wrap Values', 'Known Status', 'Failing Status']].plot.bar('Wrap Values',
                                                                                     y=['Known Status', 'Failing Status'],
                                                                                     rot=0)
        else:
            temp['Wrap Values'] = temp['RBD Name'].str.wrap(30)
            temp[['Country', 'Wrap Values', 'Known Status', 'Failing Status']].plot.bar('Wrap Values',
                                                                                     y=['Known Status', 'Failing Status'],
                                                                                     figsize=(12, 4), rot=80)
        plt.title('Surface water bodies\nFailing status by RBD Name')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_17_Surface_water_bodies_Failing_notUnknown_by_RBD2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _18_GroundWaterBodyCategoryQuantitative_status2016(df, country, outfile):
    html_string = '''<h3>15. Groundwater bodies quantitative status</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Quantitative Status Value', 'Area (km^2)']].plot.bar('Quantitative Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nQuantitative status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_18_GroundWaterBodyCategoryQuantitative_status2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _19_GroundWaterBodyCategoryQuantitative_status2016(df, country, outfile):
    html_string = '''<h3>16. Groundwater bodies good quantitative status</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country) & (df['Quantitative Status Value'] == 'Good')]
        html_string += temp.to_html(index=False)
        temp[['Quantitative Status Value', 'Area (km^2)']].plot.bar('Quantitative Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nQuantitative status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGround water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_19_GroundWaterBodyCategoryQuantitative_status2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _20_GroundWaterBodyCategoryChemical_status2016(df, country, outfile):
    df.dropna()
    html_string = '''<h3>16. Groundwater bodies chemical status</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', 'Area (km^2)', rot=0, color="#653700")
        plt.title('Groundwater bodies\nChemical status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGround water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_20_GroundWaterBodyCategoryChemical_status2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _21_SOW_GWB_gwPollutant_Table2016(df, country, outfile):
    html_string = '''<h3>17. Groundwater bodies pollutants and pollutants reported as 'other'</h3>
        '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _21_SOW_GWB_gwPollutant_Table2016_Other(df, country, outfile):
    df.dropna()
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:

        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _22_GroundWaterBodyCategoryChemical_status2016(df, country, outfile):
    html_string = '''<h3>18. % Groundwater bodies quantitative and chemical status</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nChemical status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_22_GroundWaterBodyCategoryChemical_status2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _22_gwQuantitativeStatusValue_Percent_Country_2016(df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Quantitative Status Value', 'Area (km^2)']].plot.bar('Quantitative Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nQuantitative status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_22_gwQuantitativeStatusValue_Percent_Country_2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _23_Ground_water_bodies_Failing_notUnknown_by_Country2016(df, country, outfile):
    html_string = '''<h3>19. % Groundwater bodies failing to achieve good status-country</h3>
            '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Country', 'Known Status', 'Failing status']].plot.bar('Country', y=['Known Status', 'Failing status'], rot=0)
        plt.title('Groundwater bodies')
        plt.xlabel('')
        plt.ylabel('Total Number of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_23_Ground_water_bodies_Failing_notUnknown_by_Country2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _24_Ground_water_bodies_Failing_notUnknown_by_RBD2016(df, country, outfile):
    html_string = '''<h3>20. % Groundwater bodies failing to achieve good status-RBD</h3>
                    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)

        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Value'] = temp['RBD Code'].str.wrap(25)
            temp[['Country', 'Wrap Value', 'Known Status', 'Failing status']].plot.bar('Wrap Value', y=['Known Status', 'Failing status'],
                                                                                rot=0)

        else:
            temp['Wrap Value'] = temp['RBD Code'].str.wrap(30)
            temp[['Country', 'Wrap Value', 'Known Status', 'Failing status']].plot.bar('Wrap Value', y=['Known Status', 'Failing status'],
                                                                                figsize=(12, 4), rot=80)

        plt.title('Groundwater bodies')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_24_Ground_water_bodies_Failing_notUnknown_by_RBD2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _25_Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016(df, country, outfile):
    html_string = '''<h3>21. Groundwater bodies at risk of failing to achieve good quantitative status and reasons for failure</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Quantitative Status Value', 'Area (km^2)']].plot.bar('Quantitative Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nQuantitative status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGround water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_25_Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _25_SOW_GWB_gwQuantitativeReasonsForFailure_Table2016(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>
        '''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)

        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Quantitative Reasons For Failure'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', y=['Area (km^2)'], rot=0, color="#653700")

        else:
            temp['Wrap Values'] = temp['Quantitative Reasons For Failure'].str.wrap(30)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', y=['Area (km^2)'], figsize=(12, 4), rot=80, color="#653700")

        plt.title('Groundwater bodies\nQuantitative reasons for failure')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGround water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_25_SOW_GWB_gwQuantitativeReasonsForFailure_Table2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _26_gwChemicalStatusValue_Table2016(df, country, outfile):
    html_string = '''<h3>22. Groundwater bodies at risk of failing to achieve good chemical status and reasons for failure</h3>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nChemical status')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_26_gwChemicalStatusValue_Table2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _26_SOW_GWB_gwChemicalReasonsForFailure_Table2016(df, country, outfile):
    html_string = '''<br>'''

    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', y=['Area (km^2)'], rot=0, color="#653700")
        plt.title('Groundwater bodies\nChemical reasons for failure')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_26_SOW_GWB_gwChemicalReasonsForFailure_Table2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _29_gwQuantitativeStatusExpectedGoodIn2015(df, country, outfile):
    html_string = '''<h3>23. Groundwater bodies good quantitative status expected in 2015</h3>'''

    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:

            temp['Wrap Values'] = temp['Quantitative Status Expected Good In 2015'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Quantitative Status Expected Good In 2015'].str.wrap(20)

            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nQuantitative status expected good in 2015')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '29.gwQuantitativeStatusExpectedGoodIn2015' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _30_gwQuantitativeStatusExpectedAchievementDate2016(df, country, outfile):
    html_string = '''<h3>24. Groundwater bodies good quantitative expected date</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Quantitative Status Expected Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Quantitative Status Expected Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nQuantitative status expected date')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '30.gwQuantitativeStatusExpectedAchievementDate2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _31_gwChemicalStatusExpectedGoodIn2015(df, country, outfile):
    html_string = '''<h3>25. Groundwater bodies good chemical status expected in 2015</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Chemical Status Expected Achievement Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Chemical Status Expected Achievement Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nGood chemical status expected in 2015')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '31.gwChemicalStatusExpectedGoodIn2015' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _32_gwChemicalStatusExpectedAchievementDate2016(df, country, outfile):
    html_string = '''<h3>26. Groundwater bodies good chemical expected date</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Chemical Status Expected Achievement Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Chemical Status Expected Achievement Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nGood chemical status expected date')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '32.gwChemicalStatusExpectedAchievementDate2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _35_gwQuantitativeAssessmentConfidence2016(df, country, outfile):
    html_string = '''<h3>27. Groundwater bodies quantitative status assessment confidence</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Quantitative Assessment Confidence'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Quantitative Assessment Confidence'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nQuantitative assessment confidence')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '35.gwQuantitativeAssessmentConfidence2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _36_gwChemicalAssessmentConfidence2016(df, country, outfile):
    html_string = '''<h3>28. Groundwater bodies chemical status assessment confidence</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Chemical Assessment Confidence'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Chemical Assessment Confidence'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nChemical assessment confidence')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '36.gwChemicalAssessmentConfidence2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _38_GWB_geologicalFormation2016(df, country, outfile):
    html_string = '''<h3>29. Number of groundwater bodies by geological formation</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Geological Formation'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Geological Formation'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         figsize=(12, 4), rot=80, color="#653700")
        plt.title('Groundwater bodies\nGeological formation')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '38.GWB_geologicalFormation2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _39_swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016(df, country, outfile):
    CMS = df['Chemical Monitoring Results'].unique().tolist()
    CAC = df['Chemical Assessment Confidence'].unique().tolist()

    html_string = '<h3>30. Chemical assessment using monitoring, grouping or expert</h3>'
    for cac in CAC:
        if not df.loc[(df['Country'] == country) & (df['Chemical Assessment Confidence'] == cac)].empty:
            temp = df.loc[(df['Country'] == country) & (df['Chemical Assessment Confidence'] == cac)]
            html_string += temp.to_html(index=False)

            Arguments = df.loc[(df['Country'] == country) & (df['Chemical Assessment Confidence'] == cac)].count()
            if Arguments['Chemical Assessment Confidence'] < 3:
                temp['Wrap Values'] = temp['Chemical Monitoring Results'].str.wrap(25)
                temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'],
                                                       rot=0)
            else:
                temp['Wrap Values'] = temp['Chemical Monitoring Results'].str.wrap(30)
                temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'],
                                                       figsize=(12, 4), rot=80)

            plt.title('Surface water bodies\nChemical assessment confidence')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + '39.swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2016' + country + cac +'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))



def _40_swRBsPollutants(df, country, outfile):
    html_string = '''<h3>31. River basin specific pollutants and pollutants reported as 'Other'</h3>            '''
    if not df.loc[(df['Country'] == country)].empty:

        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _40_Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016(df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _40_swPollutants(df, country, outfile):
    html_string = '''<br>'''
    temp = df.loc[(df['Country'] == country)]
    html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))


def _40_swRBsPollutantsOther(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>
                '''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _42_Surface_water_bodies_QE1_Biological_quality_elements_assessment2016(df, country, outfile):
    html_string = '<h3>32. Surface water bodies biological quality elements status</h3>'
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Code', 'Number']].plot.bar('Code', y=['Number'], figsize=[15, 4], rot=80)
        plt.title('Surface water bodies\nBiological quality elements status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '42.Surface_water_bodies_QE1_Biological_quality_elements_assessment2016' \
                      + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _42_Surface_water_bodies_QE2_assessment2016(df, country, outfile):
    html_string = '<br>'
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Code', 'Number']].plot.bar('Code', y=['Number'], figsize=[15, 4], rot=80)
        plt.title('Surface water bodies\nHydromorphological quality elements status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_42_Surface_water_bodies_QE2_assessment2016' \
                      + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _42_Surface_water_bodies_QE3_assessment2016(df, country, outfile):
    html_string = '<br>'
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Code', 'Number']].plot.bar('Code', y=['Number'], figsize=[15, 4], rot=80)
        plt.title('Surface water bodies\nChemical and physico-chemical quality elements status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_42_Surface_water_bodies_QE3_assessment2016' \
                      + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _42_Surface_water_bodies_QE3_3_assessment2016(df, country, outfile):
    html_string = '<br>'
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Code', 'Number']].plot.bar('Code', y=['Number'], figsize=[15, 4], rot=80)
        plt.title('Surface water bodies\nRiver Basin Specific Pollutants status ')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_42_Surface_water_bodies_QE3_3_assessment2016' \
                      + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _44_swEcologicalStatusOrPotentialExpectedGoodIn2015(df, country, outfile):
    html_string = '''<h3>33. Surface water bodies good ecological status expected in 2015</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Ecological Status Or Potential Expected Good In 2015'].str.wrap(20)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], rot=0)
        else:
            temp['Wrap Values'] = temp['Failing RBSP Other'].str.wrap(20)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], figsize=(12, 4), rot=80)
        plt.title('Surface water bodies\nEcological status or potential expected good in 2015')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '44.swEcologicalStatusOrPotentialExpectedGoodIn2015' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _45_swEcologicalStatusOrPotentialExpectedAchievementDate2016(df, country, outfile):
    html_string = '''<h3>34. Surface water bodies good ecological status expected date</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Ecological Status Or Potential Expected Achievement Date'].str.wrap(25)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], rot=0)
        else:
            temp['Wrap Values'] = temp['Ecological Status Or Potential Expected Achievement Date'].str.wrap(30)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], figsize=(12, 4), rot=80)
        plt.title('Surface water bodies\nEcological status or potential expected achievement date')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '45.swEcologicalStatusOrPotentialExpectedAchievementDate2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _46_swChemicalStatusExpectedGoodIn2015(df, country, outfile):
    html_string = '''<h3>35. Surface water bodies good chemical status expected in 2015</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Chemical Status Expected Good In 2015'].str.wrap(25)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], rot=0)
        else:
            temp['Wrap Values'] = temp['Chemical Status Expected Good In 2015'].str.wrap(30)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], figsize=(12, 4), rot=80)
        plt.title('Surface water bodies\nChemical status expected good in 2015')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '46.swChemicalStatusExpectedGoodIn2015' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>'))

def _47_swChemicalStatusExpectedAchievementDate2016(df, country, outfile):
    html_string = '''<h3>36. Surface water bodies good chemical status expected date</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 4:
            temp['Wrap Values'] = temp['Chemical Status Expected Achievement Date'].str.wrap(20)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], rot=0)
        else:
            temp['Wrap Values'] = temp['Chemical Status Expected Achievement Date'].str.wrap(30)
            temp[['Wrap Values', 'Number']].plot.bar('Wrap Values', y=['Number'], figsize=(12, 4), rot=80)
        plt.title('Surface water bodies\nChemical status expected achievement date')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '47.swChemicalStatusExpectedAchievementDate2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))

def _37_Number_of_groundwater_bodies_failing_to_achieve_good_status(df, country, outfile):
    html_string = '''<br><h3>37. Number of groundwater bodies failing to achieve good status</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        print(temp)
        temp[['Country', 'Good', 'Failing']].plot.bar(x='Country', y=['Good', 'Failing'], rot=0)
        plt.title('Groundwater bodies\nNumber')
        plt.xlabel('')
        plt.ylabel('Total Number of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_37_Number_of_groundwater_bodies_failing_to_achieve_good_status' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))



def NewDash_5_swPrioritySubstanceCode2016(df, country, outfile):
    html_string = '''<br><h3>New Dashboard starts below<br>5. Priority substances</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_6_surfaceWaterBodyTypeCode2016(df, country, outfile):
    html_string = '''<br><h3>6. Surface water bodies broad types by category</h3></h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Category'] == categ) & (df['Country'] == country)]
                html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def _7_swNumber_of_Impacts_by_country(df, country, outfile):
    html_string = '''<h3>7. Surface water body number of impacts </h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Number of Impacts', 'Number']].plot.bar('Number of Impacts', 'Number', rot=0)
        plt.title('Surface Waters bodies\nNumber')
        plt.xlabel('Number of impacts')
        plt.ylabel('Total Number')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_7_swNumber_of_Impacts_by_country' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string)

def NewDash_8_swNumber_of_impacts_by_country_by_category2016(df, country, outfile):
    html_string = '''<br><h3>8. Surface water body number of impacts by country and category</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Country'] == country) & (df['Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp.plot(x="Country", y=["Impact 0 - Number", "Impact 1 - Number", 'Impact 2 - Number',
                                          'Impact 3 - Number', 'Impact 4 - Number'], kind='bar',
                          rot=0, label=["0", "1", "2", "3", "4+"])
                plt.title('Surface water bodies\nNumber of impacts - ' + categ)
                plt.legend(title="Number of Impacts")
                plt.xlabel('Number of impacts')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + 'NewDash_8_swNumber_of_impacts_by_country_by_category2016' + country + '_'+categ+'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def _9_1_sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2010(df, country, outfile):
    html_string = '''<h3>9. Surface water bodies delineation of the management units in the 1<sup STYLE="font-size:75%">st</sup> 
                        and 2<sup STYLE="font-size:75%">nd</sup>RBMP</h3>
                    <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))


def _9_1_sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016(df, country, outfile):
    html_string = '''<br>
                    <p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0', ''))

def _9_2_sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2016(df, country, outfile):
    html_string = '''<br>'''
    category = ["RW","LW","CW", "TW", "TeW"]
    for categ in category:
        html_string += '''<p>Category: '''
        html_string += categ
        html_string += '''</p>'''
        temp = df.loc[(df['Category'] == categ)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))

def _9_4_sw_Evolution_type_by_Country_and_Category_in_the_1st_and_2nd_RBMP2010(df, country, outfile):
    html_string = '''<br>
                <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Category'] == categ) & (df['Country'] == country)]
                html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('.0',''))

def _9_4_sw_Evolution_type_by_Country_and_Category_in_the_1st_and_2nd_RBMP2016(df, country, outfile):
    html_string = '''<br>
                    <p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Category'] == categ) & (df['Country'] == country)]
                html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('.0',''))

def _9_3_sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2010 (df, country, outfile):
    html_string = '''<br>
                    <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))

def _9_3_sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016 (df, country, outfile):
    html_string = '''<br>
                    <p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))

def gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2010(df, country, outfile):
    html_string = '''<h3>10. Groundwater bodies delineation and evolution type 1<sup STYLE="font-size:75%">st</sup> 
                        and 2<sup STYLE="font-size:75%">nd</sup> RBMP</h3>
                        <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup>2</sup>').replace('.0', ''))

def gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2016(df, country, outfile):
    html_string = '''<br>
                    <p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        # temp[['Country', 'Unchanged Area (km^2)']].plot.bar('Country', 'Unchanged Area (km^2)', rot=0, color="#653700")
        # plt.title('Groundwater bodies\nUnchanged Area ($km^2$)')
        # plt.xlabel('')
        # plt.ylabel('Total Area($km^2$)')
        # plt.gcf()
        # plt.draw()
        # figfilename = imagepath + '_10_1_gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2016' + country + '.png'
        # plt.savefig(figfilename, bbox_inches='tight')
        # html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup>2</sup>').replace('.0',''))

def _10_1_gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2016(df, country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        # temp[['Country', 'Other Area (km^2)']].plot.bar('Country', 'Other Area (km^2)', rot=0, color="#653700")
        # plt.title('Groundwater bodies\nOther Area ($km^2$)')
        # plt.xlabel('')
        # plt.ylabel('Total Area($km^2$)')
        # plt.gcf()
        # plt.draw()
        # figfilename = imagepath + '_10_1_gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2016' + country + '.png'
        # plt.savefig(figfilename, bbox_inches='tight')
        # html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup>2</sup>').replace('.0',''))

def _10_2_gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2010(df, country, outfile):
    html_string = '''<br>
                    <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup>2</sup>').replace('.0', ''))

def _10_2_gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016(df, country, outfile):
    html_string = '''<br>
                    <p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        # temp['Wrap Values'] = temp['Evolution Type'].str.wrap(25)
        # temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)', rot=45, color="#653700")
        # plt.title('Groundwater bodies\nEvolution Type')
        # plt.xlabel('')
        # plt.ylabel('Total Area($km^2$)')
        # plt.gcf()
        # plt.draw()
        # figfilename = imagepath + '_10_2_gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016' + country + '.png'
        # plt.savefig(figfilename, bbox_inches='tight')
        # html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup>2</sup>').replace('.0',''))

def NewDash_11_swEcologicalStatusOrPotential_by_Country2010(df, country, outfile):
    html_string = '''<br><h3>11. Surface water bodies: Ecological status or potential by country 1<sup STYLE="font-size:75%">st</sup> 
                    and 2<sup STYLE="font-size:75%">nd</sup> RBMP</h3>
                <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                          'Number',
                                                                          rot=0)
        plt.title('Surface Water Bodies\nEcological status or potential - 1$^s$$^t$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_11_swEcologicalStatusOrPotential_by_Country2010' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_11_swEcologicalStatusOrPotential_by_Country2016(df, country, outfile):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                          'Number',
                                                                          rot=0)
        plt.title('Surface Water Bodies\nEcological status or potential - 2$^n$$^d$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_11_swEcologicalStatusOrPotential_by_Country2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_12_swChemical_by_Country2010(df, country, outfile):
    html_string = '''<br><h3>12. Surface water bodies: Chemical status 1<sup STYLE="font-size:75%">st</sup>
                            and 2<sup STYLE="font-size:75%">nd</sup> RBMB by country</h3>
                <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Number']].plot.bar('Chemical Status Value', 'Number',rot=0)
        plt.title('Surface water bodies\nChemical status - 1$^s$$^t$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_12_swChemical_by_Country2010' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_12_swChemical_by_Country2016(df, country, outfile):
    html_string = '''<p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Number']].plot.bar('Chemical Status Value', 'Number',rot=0)
        plt.title('Surface water bodies\nChemical status - 2$^n$$^d$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_12_swChemical_by_Country2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_13_GroundWaterBodyCategoryQuantitative_status2010(df, country, outfile):
    html_string = '''<br><h3>13. Groundwater bodies: Quantitative status 1<sup STYLE="font-size:75%">st</sup> and 2<sup STYLE="font-size:75%">nd</sup> RBMB by country</h3>
    <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Quantitative Status Value', 'Area (km^2)']].plot.bar('Quantitative Status Value', 'Area (km^2)',rot = 0,color="#653700")
        plt.title('Groundwater bodies\nQuantitative status - 1$^s$$^t$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_13_GroundWaterBodyCategoryQuantitative_status2010' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_13_GroundWaterBodyCategoryQuantitative_status2016(df, country, outfile):
    html_string = '''<p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Quantitative Status Value', 'Area (km^2)']].plot.bar('Quantitative Status Value', 'Area (km^2)',rot = 0,color="#653700")
        plt.title('Groundwater bodies\nQuantitative status - 2$^n$$^d$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_13_GroundWaterBodyCategoryQuantitative_status2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_14_gwChemical_status_by_country2010(df, country, outfile):
    html_string = '''<br><h3>14. Groundwater bodies chemical status 1<sup STYLE="font-size:75%">st</sup> and 2<sup STYLE="font-size:75%">nd</sup> RBMP by country</h3>
                <p>1<sup STYLE="font-size:75%">st</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', 'Area (km^2)',rot = 0,color="#653700")
        plt.title('Groundwater bodies\nChemical status - 1$^s$$^t$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_14_gwChemical_status_by_country2010' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_14_gwChemical_status_by_country2016(df, country, outfile):
    html_string = '''<p>2<sup STYLE="font-size:75%">nd</sup> RBMP</p>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', 'Area (km^2)',rot = 0,color="#653700")
        plt.title('Groundwater bodies\nChemical status - 2$^n$$^d$ RBMP')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_14_gwChemical_status_by_country2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2','<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

#     category =
def NewDash_18_Surface_water_bodies_QE1_status2016(df, country,outfile):
    html_string = '''<h3>18. Surface water bodies quality element status QE1</h3>'''
    category = ['QE1-2-3 - Macrophytes','QE1-3 - Benthic invertebrates','QE1-2-4 - Phytobenthos','QE1-2-2 - Angiosperms',
                'QE1-4 - Fish','QE1-2 - Other aquatic flora','QE1-2-1 - Macroalgae','QE1-1 - Phytoplankton']
    for categ in category:
        if not df.loc[(df['Country'] == country) & (df['Code'] == categ)].empty:
            html_string += categ
            temp = df.loc[(df['Country'] == country) & (df['Code'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                              'Number', rot=0)
            plt.title('Surface water bodies\nEcological Status Or Potential Value')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + 'NewDash_18_Surface_water_bodies_QE1_status2016' \
                          + country + '' + categ + '.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))


def NewDash_18_Surface_water_bodies_QE2_status2016(df, country,outfile):
    html_string = '''<h3>18. Surface water bodies quality element status QE2</h3>'''
    category = ['QE2-3 - Morphological conditions','QE2-2 - River continuity conditions','QE2-1 - Hydrological or tidal regime']
    for categ in category:
        if not df.loc[(df['Country'] == country) & (df['Code'] == categ)].empty:
            html_string += categ
            temp = df.loc[(df['Country'] == country) & (df['Code'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                              'Number', rot=0)
            plt.title('Surface water bodies\nEcological Status Or Potential Value')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + 'NewDash_18_Surface_water_bodies_QE2_status2016' \
                          +country+''+categ+'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_18_Surface_water_bodies_QE3_status2016(df, country,outfile):
    html_string = '''<h3>Surface water bodies quality element status QE3</h3>'''
    category = ['QE3-1-2 - Thermal conditions','QE3-1-3 - Oxygenation conditions','QE3-1-5 - Acidification status',
                'QE3-1-6-2 - Phosphorus conditions','QE3-1-1 - Transparency conditions','QE3-1-6-1 - Nitrogen conditions',
                'QE3-1-4 - Salinity conditions']
    for categ in category:
        if not df.loc[(df['Country'] == country) & (df['Code'] == categ)].empty:
            html_string += categ
            temp = df.loc[(df['Country'] == country) & (df['Code'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                              'Number', rot=0)
            plt.title('Surface water bodies\nEcological Status Or Potential Value')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + 'NewDash_18_Surface_water_bodies_QE3_status2016' \
                          +country+ ''+categ+'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_18_Surface_water_bodies_QE3_3_status2016(df, country,outfile):
    html_string = '''<h3>Surface water bodies quality element status QE3-3</h3>'''
    category = ['QE3-3 - River Basin Specific Pollutants']
    for categ in category:
        if not df.loc[(df['Country'] == country) & (df['Code'] == categ)].empty:
            html_string += categ
            temp = df.loc[(df['Country'] == country) & (df['Code'] == categ)]
            html_string += temp.to_html(index=False)
            temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                              'Number', rot=0)
            plt.title('Surface water bodies\nEcological Status Or Potential Value')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + 'NewDash_18_Surface_water_bodies_QE3_3_status2016' \
                          +country+''+categ+'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_18_Surface_water_bodies_QE_status2016(df, country,outfile):
    html_string = '''<h3>18.Surface water bodies: Quality element status</h3>'''
    if not df.loc[(df['Country'] == country) ].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    html_string += '''<p>NOTE: five quality elements parameters (QE1, QE1-2, QE2, Q3 and QE3-1) appear in the dashboard ('''
    html_string += '''<a href="https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_QualityElement/SWB_QualityElementGroup?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no">link</a>'''
    html_string += ''') but not in the database (<a href="https://www.eea.europa.eu/data-and-maps/data/wise-wfd-4">link</a>)</p>'''
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))

def NewDash_19_swEcological_status_or_potential_by_intercalibration_type_overall2016(df, country,outfile):
    html_string = '''<h3>19. Surface water bodies ecological status or potential by intercalibration type</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value',
                                                                          'Number', rot=0)
        plt.title('Surface water bodies\nEcological status or potential')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_19_swEcological_status_or_potential_by_intercalibration_type2022.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_19_swEcological_status_or_potential_by_intercalibration_type2022(df, country,outfile):
    html_string = '''<h3><i>Surface water bodies ecological status or potential by intercalibration type and by category</i></h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Country'] == country) & (df['Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value', 'Number', rot=0)
                plt.title('Surface water bodies\nEcological status or potential - ' + categ)
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + 'NewDash_19_swEcological_status_or_potential_by_intercalibration_type2022' \
                              + country +'_'+categ+'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_19_swEcological_status_or_potential_by_intercalibration_type_by_Category2022(df, country,outfile):
    html_string = '''<h3><i>Surface water bodies ecological status or potential by intercalibration type</i></h3>'''

    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        IntercalibrationType = ["RW-R-A1", "RW-R-A2", "RW-R-C1", "RW-R-C2", "RW-R-C3", "RW-R-C4",
                                "RW-R-C5", "RW-R-C6", "RW-R-E1", "RW-R-E2", "RW-R-E3", "RW-R-E4", "RW-R-EX4",
                                "RW-R-EX5", "RW-R-EX6", "RW-R-EX7", "RW-R-EX8", "RW-R-L1",
                                "RW-R-L2", "RW-R-M1", "RW-R-M2", "RW-R-M3", "RW-R-M4", "RW-R-M5", "RW-R-N1", "RW-R-N2",
                                "RW-R-N3", "RW-R-N4", "RW-R-N5", "RW-R-N7", "RW-R-N9",
                                "LW-EC1", "LW-L-AL3", "LW-L-AL4", "LW-L-CB1", "LW-L-CB2", "LW-L-CB3", "LW-L-M5/7",
                                "LW-L-M8", "LW-L-N-BF1", "LW-L-N-BF2", "LW-L-N-F1", "LW-L-N-F2",
                                "LW-L-N-M 101", "LW-L-N-M 102", "LW-L-N-M 201", "LW-L-N-M 202", "LW-L-N-M 301a",
                                "LW-L-N-M 302a", "LW-L-N1", "LW-L-N2a", "LW-L-N2b", "LW-L-N3a",
                                "LW-L-N3b", "LW-L-N5", "LW-L-N6a", "LW-L-N6b", "LW-L-N7", "LW-L-N8a", "LW-L-N8b",
                                "CW-BC1", "CW-BC3", "CW-BC4", "CW-BC5", "CW-BC6", "CW-BC7", "CW-BC8", "CW-BC9",
                                "CW-BL1", "CW-NEA1/26", "CW-NEA10", "CW-NEA3/4", "CW-NEA7",
                                "CW-NEA8a", "CW-NEA8b", "CW-NEA9", "CW-Type_I", "CW-Type_IIA", "CW-Type_IIA_Adriatic",
                                "CW-Type_IIIE", "CW-Type_IIIW", "CW-Type_Island-W",
                                "TW-BT1", "TW-CoastalLagoonsMesohaline", "TW-CoastalLagoonsOligohaline",
                                "TW-CoastalLagoonsPolyeuhaline", "TW-Estuaries", "TW-NEA11",
                                "inapplicable", "unpopulated"]

        for categ in category:
            for Intercalibration in IntercalibrationType:
                if not df.loc[(df['Category'] == categ) & (df['Country'] == country) & (df['Intercalibration Type Code'] == Intercalibration)].empty:
                    html_string += '''<p>Category: '''
                    html_string += categ
                    html_string += '''</p>'''
                    temp = df.loc[(df['Category'] == categ) & (df['Country'] == country) & (df['Intercalibration Type Code'] == Intercalibration)]
                    html_string += temp.to_html(index=False)
                    temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value','Number', rot=0)
                    plt.title('Surface water bodies\nEcological status or potential - '+categ+' - '+Intercalibration)
                    plt.xlabel('')
                    plt.ylabel('Total Number of\nSurface water bodies')
                    plt.gcf()
                    plt.draw()
                    Intercalibration = re.sub(r"/","_",Intercalibration)
                    figfilename = imagepath + 'NewDash_19_swEcological_status_or_potential_by_intercalibration_type2022' \
                                  + country + '_'+categ+'_'+Intercalibration+'.png'
                    plt.savefig(figfilename, bbox_inches='tight')
                    html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_20_swEcologicalStatus_by_country2016(df, country, outfile):
    html_string = '''<h3>20. Surface water bodies ecological status or potential and chemical status assessment confidence</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Ecological status or potential', 'Number']].plot.bar('Ecological status or potential','Number', rot=0)
        plt.title('Surface water bodies\nEcological status or potential')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_20_swEcologicalStatus_by_country2022' + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_20_ChemicalStatus_Assessment_confidence_by_country2016(df,country, outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical status', 'Number']].plot.bar('Chemical status','Number', rot=0)
        plt.title('Surface water bodies\nChemical status')
        plt.xlabel('')
        plt.ylabel('Total Number of\nSurface water bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + 'NewDash_20_ChemicalStatus_Assessment_confidence_by_country2022' + country +'.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_20_swEcologicalStatus_by_country_by_category_overall2016(df,country,outfile):
    html_string = '''<h3>20. Surface water bodies ecological status assessment</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        if not df.loc[(df['Country'] == country)].empty:
            temp = df.loc[(df['Country'] == country)]
            html_string += temp.to_html(index=False)
            temp[['Ecological status or potential', 'Number']].plot.bar('Ecological status or potential','Number', rot=0)
            plt.title('Surface water bodies\nEcological status or potential')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + 'NewDash_20_swEcologicalStatus_by_country_by_category_overall2016' \
                          + country +'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_20_swEcologicalStatus_by_country_by_category2016(df,country,outfile):
    html_string = '''<h3>Surface water bodies ecological status or potential and chemical status assessment confidence by category</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Country'] == country) & (df['Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Ecological status or potential', 'Number']].plot.bar('Ecological status or potential','Number', rot=0)
                plt.title('Surface water bodies\nEcological status or potential')
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + 'NewDash_20_swEcologicalStatus_by_country_by_category2016' \
                              + country + '_'+categ+'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_20_ChemicalStatus_Assessment_confidence_by_country_by_category_overall2016(df,country,outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        if not df.loc[(df['Country'] == country)].empty:
            temp = df.loc[(df['Country'] == country)]
            html_string += temp.to_html(index=False)
            temp[['Chemical status', 'Number']].plot.bar('Chemical status','Number', rot=0)
            plt.title('Surface water bodies\nChemical status')
            plt.xlabel('')
            plt.ylabel('Total Number of\nSurface water bodies')
            plt.gcf()
            plt.draw()
            figfilename = imagepath + 'NewDash_20_ChemicalStatus_Assessment_confidence_by_country_by_category2022' \
                          + country +'.png'
            plt.savefig(figfilename, bbox_inches='tight')
            html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_20_ChemicalStatus_Assessment_confidence_by_country_by_category2016(df,country,outfile):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        for categ in category:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Category: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Country'] == country) & (df['Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp[['Chemical status', 'Number']].plot.bar('Chemical status','Number', rot=0)
                plt.title('Surface water bodies\nChemical status')
                plt.xlabel('')
                plt.ylabel('Total Number of\nSurface water bodies')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + 'NewDash_20_ChemicalStatus_Assessment_confidence_by_country_by_category2022' \
                              + country + '_'+categ+'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))


def NewDash_22_swPhysical_alterations_by_country2016(df, country, outfile):
    html_string = '''<h3>22. Surface water bodies physical alterations by country</h3>'''
    category = ['Artificial water body', 'Heavily modified water body', 'Natural water body']
    if not df.loc[(df['Country'] == country)].empty:
        for categ in category:
            if not df.loc[(df['Type'] == categ) & (df['Country'] == country)].empty:
                html_string += '''<p>Type: '''
                html_string += categ
                html_string += '''</p><br>'''
                temp = df.loc[(df['Country'] == country) & (df['Type'] == categ)]
                html_string += temp.to_html(index=False)
        #         temp['Wrap Values'] = temp['Physical Alteration'].str.wrap(25)
        #         temp[['Wrap Values', 'Number']].plot.bar('Wrap Values','Number', rot=0)
        #         plt.title('Surface water bodies\nPhysical Alteration')
        #         plt.xlabel('')
        #         plt.ylabel('Total Number of\nSurface water bodies')
        #         plt.gcf()
        #         plt.draw()
        #         figfilename = imagepath + 'NewDash_22_swPhysical_alterations_by_country2016' \
        #                       + country + '_'+categ+'.png'
        #         plt.savefig(figfilename, bbox_inches='tight')
        #         html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_23_swDesignated_water_uses_by_country2016(df, country, outfile):
    html_string = '''<h3>23. Surface water bodies water uses by country</h3>'''
    category = ['Artificial water body', 'Heavily modified water body', 'Natural water body']
    if not df.loc[(df['Country'] == country)].empty:
        for categ in category:
            if not df.loc[(df['Country'] == country) & (df['Type'] == categ)].empty:
                html_string += '''<p>Type: '''
                html_string += categ
                html_string += '''</p>'''
                temp = df.loc[(df['Country'] == country) & (df['Type'] == categ)]
                html_string += temp.to_html(index=False)
        #         temp['Wrap Values'] = temp['Designated water uses'].str.wrap(15)
        #         temp[['Wrap Values', 'Number']].plot.bar('Wrap Values','Number', rot=0)
        #         plt.title('Surface water bodies\nDesignated water uses')
        #         plt.xlabel('')
        #         plt.ylabel('Total Number of\nSurface water bodies')
        #         plt.gcf()
        #         plt.draw()
        #         figfilename = imagepath + 'NewDash_23_swDesignated_water_uses_by_country2016' \
        #                       + country + '_'+categ+'.png'
        #         plt.savefig(figfilename, bbox_inches='tight')
        #         html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))

def NewDash_24_swEcologicalstatusorpotential_by_broadtype_by_country2016(df, country, outfile):
    html_string = '''<h3>24. Surface water bodies ecological status or potential by broad type and category</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        category = ["RW", "LW", "CW", "TW", "TeW"]
        broadtype = ['RW-00', 'RW-01', 'RW-02', 'RW-03', 'RW-04', 'RW-04', 'RW-05','RW-06', 'RW-07','RW-08','RW-09',
                     'RW-10','RW-11','RW-012','LW-00', 'LW-01', 'LW-02', 'LW-03', 'LW-04','LW-05', 'LW-06', 'LW-07',
                       'LW-08', 'CW-00', 'TW-00',  'Not applicable']
        for categ in category:
            if not df.loc[(df['Country'] == country) & (df['Category'] == categ)].empty:
                for brtype in broadtype:
                    if not df.loc[(df['Country'] == country) & (df['Broad Type Code'] == brtype) & (df['Category'] == categ)].empty:
                        html_string += '<p>Category: ' + categ + ' Broad Type Code: ' + brtype + '</p>'
                        temp = df.loc[(df['Country'] == country) & (df['Broad Type Code'] == brtype) & (df['Category'] == categ)]
                        html_string += temp.to_html(index=False)
                        temp[['Ecological Status Or Potential Value', 'Number']].plot.bar('Ecological Status Or Potential Value','Number', rot=0)
                        plt.title('Surface water bodies\nBroad Type Code ' + categ + ' ' + brtype)
                        plt.xlabel('')
                        plt.ylabel('Total Number of\nSurface water bodies')
                        plt.gcf()
                        plt.draw()
                        figfilename = imagepath + 'NewDash_24_swEcologicalstatusorpotential_by_broadtype_by_country2016' \
                                      + country + '_'+brtype+'_'+categ+'.png'
                        plt.savefig(figfilename, bbox_inches='tight')
                        html_string += '<br><img src = "' + figfilename + '"><br>'
                        # if country == "AT":
                        #     html_string += '''<p><small>*Dashboard (link here) presents 24 water bodies. In the database of the 2nd cycle ('''
                        #     html_string += '''<a href="https://tableau.discomap.eea.europa.eu/t/Wateronline/views/WISE_SOW_BroadType_G/SWB_Status_BroadType_Country?:embed=y&:showShareOptions=true&:display_count=no&:showVizHome=no">link</a>'''
                        #     html_string += ''') only 11 water bodies are presented</small></p>'''
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0',''))


def _29_1_EcologicalMonitoring_Map_data (df, country, outfile):
    html_string = '''<h3>29.Number of Monitoring size</h3><p><b><i>Ecological Monitoring</i></b></p>'''
    if not df.loc[(df['Water body Code'].str.match(r'^' + str(country) + '.*') == True)].empty:
        temp = df.loc[(df['Water body Code'].str.match(r'^' + str(country) + '.*'))]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))

def _29_2_ChemicalMonitoring_Map_data (df, country, outfile):
    html_string = '''<br><p><b><i>Chemical Monitoring</i></b></p>'''
    if not df.loc[(df['Water body Code'].str.match(r'^' + str(country) + '.*') == True)].empty:
        temp = df.loc[(df['Water body Code'].str.match(r'^' + str(country) + '.*'))]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))

def _29_3_QuantitativeMonitoring_Map_data (df, country, outfile):
    html_string = '''<br><p><b><i>Quantitative Monitoring</i></b></p>'''
    if not df.loc[(df['Water body Code'].str.match(r'^' + str(country) + '.*') == True)].empty:
        temp = df.loc[(df['Water body Code'].str.match(r'^' + str(country) + '.*'))]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('.0',''))


