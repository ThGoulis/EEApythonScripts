import matplotlib.pyplot as plt


def rbdCodeNames(df, country, outfile, imagepath):
    html_string = '''<h3>RBD Code and names </h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))
    
    
def _1_swNumberAndSize2022(df, country, outfile, imagepath):
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
        figfilename = imagepath + '_1_swNumberAndSize2022' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'

    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _2_gwNumberAndSize2022(df, country, outfile, imagepath):
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
        figfilename = imagepath + '_2_gwNumberAndSize2022' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _3_surfaceWaterBodyCategory2022(df, country, outfile, imagepath):
    html_string = '''<h3>3. Number of surface water bodies by category and type</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
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
                figfilename = imagepath + '_3_surfaceWaterBodyCategory2022' + country + categ + '.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _4_swSignificantPressureType_NumberOfImpact_by_country2022(df, country, outfile, imagepath):
    html_string = '''<h3>4. Surface water bodies significant pressures and impacts</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp.plot(x="Country", y=["Impact 0 - Number", "Impact 1 - Number", 'Impact 2 - Number', 'Impact 3 - Number', 'Impact 4+ - Number'], kind='bar',
                  rot=0, label=["0", "1", "2", "3", "4+"])

        plt.title('Surface water bodies\nNumber of impacts')
        plt.legend(title="Number of Impacts")
        plt.xlabel('Number of impacts')
        plt.ylabel('Total Number')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_4_swSignificantPressureType_NumberOfImpact_by_country2022' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _NewDash_8_swNumber_of_impacts_by_country_by_category2022(df, country, outfile, imagepath):
    html_string = '''<h3>8. Surface water bodies significant pressures and impacts</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        categories = ["RW", "LW", "TW", "CW", "TeW"]
        for categ in categories:
            if not df.loc[(df['Category'] == categ) & (df['Country'] == country)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Category'] == categ)]
                html_string += temp.to_html(index=False)
                temp.plot(x="Country", y=["Impact 0 - Number", "Impact 1 - Number", 'Impact 2 - Number', 'Impact 3 - Number', 'Impact 4+ - Number'], kind='bar',
                          rot=0, label=["0", "1", "2", "3", "4+"])
                plt.title('Surface water bodies\nNumber of impacts by category - '+categ)
                plt.legend(title="Number of Impacts")
                plt.xlabel('Number of impacts')
                plt.ylabel('Total Number')
                plt.gcf()
                plt.draw()
                figfilename = imagepath + '_NewDash_8_swNumber_of_impacts_by_country_by_category2022' + country + ''+ categ +'.png'
                plt.savefig(figfilename, bbox_inches='tight')
                html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _4_SOW_SWB_SWB_swSignificantImpactType_Table2022(df, country, outfile, imagepath):
    html_string = '''<br>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _4_SOW_SWB_SWB_swSignificantImpactType_Table_Other2022(df, country, outfile, imagepath):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _4_SOW_SWB_SWB_swSignificant_Pressure_Type_Table2022(df, country, outfile, imagepath):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _4_SOW_SWB_SWB_swSignificantPressureType_Table_Other2022(df, country, outfile, imagepath):
    df.dropna()
    values = df.loc[(df['Country'] == country)]
    if not values.empty:
        html_string = '''<br>'''
        html_string += values.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))
# .replace('.0', '')

def _5_SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country2022(df, country, outfile, imagepath):
    html_string = '''<h3>5. Groundwater bodies significant pressures and impacts</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp.plot(x="Country", y=["Impact 0 - Area (km^2)", "Impact 1 - Area (km^2)", 'Impact 2 - Area (km^2)', 'Impact 3 - Area (km^2)', 'Impact 4+ - Area (km^2)'], kind='bar',
                  rot=0, label=["0", "1", "2", "3", "4+"])
        plt.title('Groundwater bodies\nNumber of impacts')
        plt.legend(title="Number of Impacts")
        plt.xlabel('Number of impacts')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.SOW_GWB_gwSignificantPressureType_NumberOfImpact_by_country' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _5_gwSignificant_impacts2022(df, country, outfile, imagepath):
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
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)', figsize=(12, 4), rot=80, color="#653700")

        plt.title('Groundwater bodies of\nSignificant impacts')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '5.gwSignificantImpactType2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _5_gwSignificantImpactType_Other(df, country, outfile, imagepath):
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _5_SOW_GWB_gwSignificantPressureType_OtherTable2022(df, country, outfile, imagepath):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _5_gwSignificantPressureType2022(df, country, outfile, imagepath):
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
        figfilename = imagepath + '5.gwSignificantPressureType2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _6_SWB_Chemical_exemption_type2022(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _6_Surface_water_bodies_Ecological_exemptions_Type2022(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _6_Surface_water_bodies_Ecological_exemptions_and_pressures2022(df, country, outfile, imagepath):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _6_Surface_water_bodies_Quality_element_exemptions_Type2022(df, country, outfile, imagepath):
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _7_Groundwater_bodies_Chemical_Exemption_Type2022(df, country, outfile, imagepath):
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


def _7_Groundwater_bodies_Quantitative_Exemption_Type2022(df, country, outfile, imagepath):
    EETGList = df['Quantitative Exemption Type Group'].unique().tolist()
    EETList = df['Quantitative Exemption Type'].unique().tolist()
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        for types, group in zip(EETList, EETGList):
            if not df.loc[(df['Country'] == country) & (df['Quantitative Exemption Type Group'] == group)].empty:
                temp = df.loc[(df['Country'] == country) & (df['Quantitative Exemption Type Group'] == group)]
                html_string += temp.to_html(index=False)
                html_string += '''<br><br>'''
                # temp[['Quantitative Exemption Type', 'Area (km^2)']].plot.bar('Quantitative Exemption Type',
                #                                                              'Area (km^2)', rot=15, color="#653700")
                # plt.title('Groundwater bodies\nQuantitative exemption type')
                # plt.xlabel('')
                # plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
                # plt.gcf()
                # plt.draw()
                # figfilename = imagepath + '7.Groundwater_bodies_Quantitative_Exemption_Type2016' + country + group +'.png'
                # plt.savefig(figfilename, bbox_inches='tight')
                # html_string += '<br><img src = "' + figfilename + '"><br>'
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _7_Groundwater_bodies_Quantitative_exemptions_and_pressures2022(df, country, outfile, imagepath):
    html_string = '''<br>'''

    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _7_gwChemicalExcemptionPressures2022 (df, country, outfile, imagepath):
    html_string = '''<br>
    '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _8_Surface_water_bodies_Ecological_status_or_potential_group_Failing(df, country, outfile, imagepath):
    html_string = '''<h3>8. Number and percent of surface water bodies at good or high and failling to achieve good ecological status or potential</h3>
    <p>Number and percent of surface water bodies failing to achieve good ecological status or potential</p>
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _8_Surface_water_bodies_Ecological_status_or_potential_group_Good_High(df, country, outfile, imagepath):
    html_string = '''<br>
    <p>Number and percent of surface water bodies at good or high ecological status or potential</p>
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _8_swEcologicalStatusOrPotential_RW_LW_Category2ndRBMP2022(df, country, outfile, imagepath):
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _9_swEcologicalStatusOrPotential_Unknown_Category2ndRBMP2022(df, country, outfile, imagepath):
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


def _10_SurfaceWaterBody_SWB_ChemicalStatus_Table_by_Category2022(df, country, outfile, imagepath):
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


def _10_surfaceWaterBodyChemicalStatusGood2022(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _11_swChemical_by_Country(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _11_swEcologicalStatusOrPotential_by_Country (df, country, outfile, imagepath):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _12_swEcologicalStatusOrPotentialValue_swChemicalStatusValue_by_Country_by_Categ2022(df, country, outfile, imagepath):
    html_string = '''<h3>12. Surface water bodies ecological status or potential and chemical status by category</h3>
    '''
    categories = ["RW", "LW", "TW", "CW", "TeW"]
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _12_swChemicalStatusValue_by_Country_by_Categ2022(df, country, outfile, imagepath):
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _13_GroundWaterBodyCategoryQuantitative_status2022(df, country, outfile, imagepath):
    html_string = '''<h3>13. Groundwater bodies quantitative status</h3>
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
        figfilename = imagepath + '_13_GroundWaterBodyCategoryQuantitative_status2022' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _14_GroundWaterBodyCategoryChemical_status2022(df, country, outfile, imagepath):
    df.dropna()
    html_string = '''<h3>14. Groundwater bodies chemical status</h3>
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _15_SOW_GWB_gwPollutant_Table2022(df, country, outfile, imagepath):
    html_string = '''<h3>15. Groundwater bodies pollutants and pollutants reported as 'other'</h3>
        '''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _15_SOW_GWB_gwPollutant_Table2022_Other(df, country, outfile, imagepath):
    df.dropna()
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>
        '''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>'))


def _16_GroundWaterBodyCategoryChemical_status2022(df, country, outfile, imagepath):
    html_string = '''<h3>16. % Groundwater bodies quantitative and chemical status</h3>
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _16_gwQuantitativeStatusValue_Percent_Country_2022(df, country, outfile, imagepath):
    if not df.loc[(df['Country'] == country)].empty:
        html_string = '''<br>'''
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _17_Groundwater_bodies_At_risk_of_failing_to_achieve_good_quantitative_status2022(df, country, outfile, imagepath):
    html_string = '''<h3>17. Groundwater bodies at risk of failing to achieve good quantitative status and reasons for failure</h3>
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _17_SOW_GWB_gwQuantitativeReasonsForFailure_Table2022(df, country, outfile, imagepath):
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _18_SOW_GWB_gwChemicalReasonsForFailure_Table2022(df, country, outfile, imagepath):
    html_string = '''<h3>18. Groundwater bodies at risk of failing to achieve good chemical status and reasons for failure</h3>'''

    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp[['Chemical Status Value', 'Area (km^2)']].plot.bar('Chemical Status Value', 'Area (km^2)', rot=0, color="#653700")
        plt.title('Groundwater bodies\nChemical reasons for failure')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$) of\nGroundwater bodies')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_26_SOW_GWB_gwChemicalReasonsForFailure_Table2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _18_gwChemicalStatusValue_Table2022(df, country, outfile, imagepath):
    html_string = '''<br>
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
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _19_gwQuantitativeStatusExpectedAchievementDate2022(df, country, outfile, imagepath):
    html_string = '''<h3>19. Groundwater bodies good quantitative expected date</h3>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _20_gwChemicalStatusExpectedAchievementDate2022(df, country, outfile, imagepath):
    html_string = '''<h3>20. Groundwater bodies good chemical expected date</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        Arguments = df.loc[df['Country'] == country].count()
        if Arguments['Country'] < 3:
            temp['Wrap Values'] = temp['Good Chemical Status Expected Date'].str.wrap(20)
            temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)',
                                                         rot=0, color="#653700")
        else:
            temp['Wrap Values'] = temp['Good Chemical Status Expected Date'].str.wrap(20)
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
# .replace('.0', '')

def _21_gwQuantitativeAssessmentConfidence2022(df, country, outfile, imagepath):
    html_string = '''<h3>21. Groundwater bodies quantitative status assessment confidence</h3>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _22_gwChemicalAssessmentConfidence2022(df, country, outfile, imagepath):
    html_string = '''<h3>22. Groundwater bodies chemical status assessment confidence</h3>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _23_GWB_geologicalFormation2022(df, country, outfile, imagepath):
    html_string = '''<h3>23. Number of groundwater bodies by geological formation</h3>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _24_swb_Chemical_assessment_using_monitoring_grouping_or_expert_judgement2022 (df, country, outfile, imagepath):
    CAC = df['Chemical Assessment Confidence'].unique().tolist()

    html_string = '<h3>24. Chemical assessment using monitoring, grouping or expert</h3>'
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


def _25_swRBsPollutants(df, country, outfile, imagepath):
    html_string = '''<h3>25. River basin specific pollutants and pollutants reported as 'Other'</h3>'''
    if not df.loc[(df['Country'] == country)].empty:

        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _25_Surface_water_bodies_River_basin_specific_pollutants_reported_as_Other2016(df, country, outfile, imagepath):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _26_Surface_water_bodies_QE1_assessment2022(df, country, outfile, imagepath):
    html_string = '<h3>26. Surface water bodies biological quality elements status</h3>'
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _26_Surface_water_bodies_QE2_assessment2016(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _26_Surface_water_bodies_QE3_assessment2016(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _26_Surface_water_bodies_QE3_3_assessment2016(df, country, outfile, imagepath):
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _27_swEcologicalStatusOrPotentialExpectedAchievementDate2022(df, country, outfile, imagepath):
    html_string = '''<h3>27. Surface water bodies good ecological status expected date</h3>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _28_swChemicalStatusExpectedAchievementDate2022(df, country, outfile, imagepath):
    html_string = '''<h3>28. Surface water bodies good chemical status expected date</h3>'''
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
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _9_1_sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_2022(df, country, outfile, imagepath):
    html_string = '''<h3>29. Surface water bodies: delineation of the management units in the 3<sup STYLE="font-size:75%">rd</sup> RBMP</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        html_string += '''<br>'''
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string)


def _9_1_sw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Other_2022(df, country, outfile, imagepath):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string)


def _9_2_sw_Evolution_type_by_Category_in_the_1st_and_2nd_RBMP_2016(df, country, outfile, imagepath):
    html_string = '''<h3>Surface water bodies evolution type by category 3<sup STYLE="font-size:75%">rd</sup> Cycle</h3>'''
    category = ["RW","LW", "TW", "CW", "TeW"]
    for categ in category:
        if not df.loc[(df['Category'] == categ)].empty:
            html_string += '''<br>'''
            temp = df.loc[(df['Category'] == categ)]
            html_string += temp.to_html(index=False)
    outfile.write(html_string)


def _9_3_sw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016 (df, country, outfile, imagepath):
    html_string = '''<h3>Surface water bodies evolution type by country 3<sup STYLE="font-size:75%">rd</sup> Cycle</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string)


def gw_delineation_of_the_management_units_in_the_1st_and_2nd_RBMP_Unchanged_Other_2022(df, country, outfile, imagepath):
    html_string = '''<h3>30. Groundwater bodies delineation and evolution type 3<sup STYLE="font-size:75%">rd</sup> 
                        RBMP</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup>2</sup>').replace('.0', ''))


def _10_2_gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016(df, country, outfile, imagepath):
    html_string = '''<br>'''
    if not df.loc[(df['Country'] == country)].empty:
        temp = df.loc[(df['Country'] == country)]
        html_string += temp.to_html(index=False)
        temp['Wrap Values'] = temp['Evolution Type'].str.wrap(25)
        temp[['Wrap Values', 'Area (km^2)']].plot.bar('Wrap Values', 'Area (km^2)', rot=45, color="#653700")
        plt.title('Groundwater bodies\nEvolution Type')
        plt.xlabel('')
        plt.ylabel('Total Area($km^2$)')
        plt.gcf()
        plt.draw()
        figfilename = imagepath + '_10_2_gw_Evolution_type_by_Country_in_the_1st_and_2nd_RBMP_2016' + country + '.png'
        plt.savefig(figfilename, bbox_inches='tight')
        html_string += '<br><img src = "' + figfilename + '"><br>'
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _6_surfaceWaterBodyTypeCode(df, country, outfile, imagepath):
    html_string = '''<br><h3>32. Surface water bodies broad types</h3>'''
    if not df.loc[(df['Country'] == country)].empty:
        html_string += '''<br>'''
        if not df.loc[(df['Country'] == country)].empty:
            temp = df.loc[(df['Country'] == country)]
            html_string += temp.to_html(index=False)
    outfile.write(html_string.replace('^2', '<sup STYLE="font-size:75%">2</sup>').replace('.0', ''))


def _29_1_EcologicalMonitoring_Map_data (df, country, outfile, imagepath):
    html_string = '''<h3>31.Monitoring<br>Ecological Monitoring</h3>'''
    if not df.loc[(df['RBD Code'].str.match(r'^' + str(country) + '.*') == True)].empty:
        temp = df.loc[(df['RBD Code'].str.match(r'^' + str(country) + '.*'))]
        html_string += temp.to_html(index=False)
    outfile.write(html_string)


def _29_2_ChemicalMonitoring_Map_data (df, country, outfile, imagepath):
    html_string = '''<br><p><b>Chemical Monitoring</b></p>'''
    if not df.loc[(df['RBD Code'].str.match(r'^' + str(country) + '.*') == True)].empty:
        temp = df.loc[(df['RBD Code'].str.match(r'^' + str(country) + '.*'))]
        html_string += temp.to_html(index=False)
    outfile.write(html_string)


def _29_3_QuantitativeMonitoring_Map_data (df, country, outfile, imagepath):
    html_string = '''<br><p><b>Quantitative Monitoring</b></p>'''
    if not df.loc[(df['RBD Code'].str.match(r'^' + str(country) + '.*') == True)].empty:
        temp = df.loc[(df['RBD Code'].str.match(r'^' + str(country) + '.*'))]
        html_string += temp.to_html(index=False)
    outfile.write(html_string)