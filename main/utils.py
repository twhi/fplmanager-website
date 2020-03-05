OPT_PARAM_CHOICES = [
    ('assists', 'Assists'),
    ('bonus', 'Bonus Points'),
    ('bps', 'BPS'),
    ('creativity', 'Creativity'),
    ('dreamteam_count', 'Dreamteam Count'),
    ('ep_next', 'xP (Next GW)'),
    ('ep_this', 'xP (Last GW)'),
    ('xg_season', 'xG (Season)'),
    ('form', 'Form'),
    ('goals_scored', 'Goals Scored'),
    ('ict_index', 'ICT Index'),
    ('influence', 'Influence'),
    ('kpi', 'KPI'),
    ('event_points', 'Points (Last GW)'),
    ('total_points', 'Points (Total)'),
    ('minutes', 'Mins Played'),
    ('points_per_game', 'Points/Game'),
    ('price_change', 'Price Change Measure'),
    ('selected_by_percent', 'Selected By %'),
    ('threat', 'Threat'),
    ('top_50_count', 'Top 50 Team Count'),
    ('transfers_in_event', 'Transfers in GW'),
    ('transfers_in', 'Transfers in Total'),
    ('value_form', 'Value Form'),
    ('value_season', 'Value Season'),
]

stats_url = 'http://www.fplstatistics.co.uk/Home/AjaxStatsHandler?sEcho=1&iColumns=16&sColumns=,web_name,PClubName,Position,Status,Cost,MinsperGame,Points,Ptsper90Min,Form,PosFormFPLpts,GWsGT5,WeightedPoints,KPI1,KPI1V,PId&iDisplayStart=0&iDisplayLength=1000&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=false&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=true&mDataProp_9=9&sSearch_9=&bRegex_9=false&bSearchable_9=true&bSortable_9=true&mDataProp_10=10&sSearch_10=&bRegex_10=false&bSearchable_10=true&bSortable_10=true&mDataProp_11=11&sSearch_11=&bRegex_11=false&bSearchable_11=true&bSortable_11=true&mDataProp_12=12&sSearch_12=&bRegex_12=false&bSearchable_12=true&bSortable_12=true&mDataProp_13=13&sSearch_13=&bRegex_13=false&bSearchable_13=true&bSortable_13=true&mDataProp_14=14&sSearch_14=&bRegex_14=false&bSearchable_14=true&bSortable_14=true&mDataProp_15=15&sSearch_15=&bRegex_15=false&bSearchable_15=false&bSortable_15=true&sSearch=&bRegex=false&iSortCol_0=13&sSortDir_0=desc&iSortingCols=1&PosSelect=&MaxPrice=14.0'

top_50_url = 'http://www.fplstatistics.co.uk/Home/AjaxTop50Handler?sEcho=1&iColumns=11&sColumns=TimesinTop50%2Cweb_name%2CPClubName%2CPosition%2CStatus%2CPoints%2CCost%2CForm%2Cunlockdt%2CNTIDelta%2CNTIPERCENTNJD&iDisplayStart=0&iDisplayLength=1000&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=false&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=true&mDataProp_9=9&sSearch_9=&bRegex_9=false&bSearchable_9=true&bSortable_9=true&mDataProp_10=10&sSearch_10=&bRegex_10=false&bSearchable_10=true&bSortable_10=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1572860326251'
