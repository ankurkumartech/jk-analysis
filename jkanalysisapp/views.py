from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
import pandas as pd
from django.utils.encoding import smart_str
import numpy as np
import json
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from django.views.decorators.csrf import csrf_exempt

def get_data(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"Message":"Success"})

def get_columns(start_year, end_year, first_month=None, second_month=None, quarter_req=None, percent_filter=None, end_quarter=None):
    
    df = pd.read_csv("jkanalysisapp/jkdata.csv", header=3)
    
    q1 = ['APR', 'MAY', 'JUN']
    q2 = ['JUL', 'AUG', 'SEP']
    q3 = ['OCT', 'NOV', 'DEC']
    q4 = ['JAN', 'FEB', 'MAR']

    quarters = [q1, q2, q3, q4]
    start_year_second = start_year[-2:]
    start_year_first = int(start_year_second) - 1
    
    end_year_second = end_year[-2:]
    end_year_first = int(end_year_second) - 1
    
    start_year_all_months = []
    end_year_all_months = []
    
    for quarter in quarters:
        if quarter != ['JAN', 'FEB', 'MAR']:
            for month in quarter:
                start_year_all_months.append(month + str(start_year_first))
        else:
            for month in quarter:
                start_year_all_months.append(month + str(start_year_second))
                
    df_all_columns_start_year = []
    
    for month in start_year_all_months:
        for df_month in df.columns:
            if month in df_month and 'TO' not in df_month and 'ACTI' not in df_month and 'Clu' not in df_month and 'PCR' in df_month and 'SAS' not in df_month:
                df_all_columns_start_year.append(df_month)
    
    for quarter in quarters:
        if quarter != ['JAN', 'FEB', 'MAR']:
            for month in quarter:
                end_year_all_months.append(month + str(end_year_first))
        else:
            for month in quarter:
                end_year_all_months.append(month + str(end_year_second))
                
    df_all_columns_end_year = []
    
    for month in end_year_all_months:
        for df_month in df.columns:
            if month in df_month and 'TO' not in df_month and 'ACTI' not in df_month and 'Clu' not in df_month and 'PCR' in df_month and 'SAS' not in df_month:
                df_all_columns_end_year.append(df_month)
    
    if quarter_req == 'q1': 
        df_all_columns_start_year = [item for item in df_all_columns_start_year if any(value in item for value in q1)]
        
    if end_quarter == 'q1':
        df_all_columns_end_year = [item for item in df_all_columns_end_year if any(value in item for value in q1)]
        
    if quarter_req == 'q2':
        df_all_columns_start_year = [item for item in df_all_columns_start_year if any(value in item for value in q2)]
    
    if end_quarter == 'q2':
        df_all_columns_end_year = [item for item in df_all_columns_end_year if any(value in item for value in q2)]
        
    if quarter_req == 'q3':
        df_all_columns_start_year = [item for item in df_all_columns_start_year if any(value in item for value in q3)]
        
    if end_quarter == 'q3':
        df_all_columns_end_year = [item for item in df_all_columns_end_year if any(value in item for value in q3)]
        
    if quarter_req == 'q4':
        df_all_columns_start_year = [item for item in df_all_columns_start_year if any(value in item for value in q4)]
        
    if end_quarter == 'q4':
        df_all_columns_end_year = [item for item in df_all_columns_end_year if any(value in item for value in q4)]
    
    if first_month:
        for column in df_all_columns_start_year.copy():
            if first_month.upper() not in column:
                df_all_columns_start_year.remove(column)
                
    if second_month:
        for column in df_all_columns_end_year.copy():
            if second_month.upper() not in column:
                df_all_columns_end_year.remove(column)
    print(df_all_columns_start_year)
    print(df_all_columns_end_year)
    
                
    return df, df_all_columns_start_year, df_all_columns_end_year

# def yoy(request, start_year, end_year):
#     df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year)
                
#     start_year_apm_value = df[df_all_columns_start_year].sum().sum()/12
#     end_year_apm_value = df[df_all_columns_end_year].sum().sum()/12
    
#     return JsonResponse({'APM-' + start_year:start_year_apm_value, 'APM-' + end_year:end_year_apm_value})


# def qoq(request, start_year, end_year, quarter):
#     df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year, quarter_req=quarter)
    
#     start_year_apm_value = df[df_all_columns_start_year].sum().sum()/12
#     end_year_apm_value = df[df_all_columns_end_year].sum().sum()/12
    
#     return JsonResponse({quarter.upper() + '-' + start_year:start_year_apm_value, quarter.upper() + '-' +  end_year:end_year_apm_value})
    
# def mom(request, start_year, end_year, first_month=None, second_month=None):
    
#     df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year, first_month=first_month.upper(), second_month=second_month.upper())
    
#     start_year_apm_value = df[df_all_columns_start_year].sum().sum()/12
#     end_year_apm_value = df[df_all_columns_end_year].sum().sum()/12
    
#     return JsonResponse({first_month.upper() + '-' + start_year:start_year_apm_value, second_month.upper() + '-' + end_year:end_year_apm_value})


def percent_filter_func(percent_filter, start_year, end_year,quarter=None, end_quarter=None, first_month=None, second_month=None):
    
    df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year, first_month=first_month, second_month=second_month, quarter_req=quarter, end_quarter=end_quarter)
    
    df_start_year = df[df_all_columns_start_year].astype('float')
    df_end_year = df[df_all_columns_end_year].astype('float')
    
    try:
        df_start_year['difference %'] = ((df_start_year[df_all_columns_start_year[0]] - df_end_year[df_all_columns_end_year [0]]) / df_end_year[df_all_columns_end_year[0]]) * 100
    except:
        return Response({"Error":"Please try again"}, status=status.HTTP_404_NOT_FOUND)
    
        
    df_start_year.replace([np.inf, -np.inf], np.nan)

    df_start_year.dropna(inplace=True)
    
    df_end_year.replace([np.inf, -np.inf], np.nan)

    df_end_year.dropna(inplace=True)
    
    percent_filter_more_count = df_start_year[(df_start_year['difference %'] > float(percent_filter)) & (df_start_year['difference %'] != float('inf'))].shape[0]
    
    percent_filter_less_count = df_start_year[(df_start_year['difference %'] < float(percent_filter)) & (df_start_year['difference %'] != float('inf'))].shape[0]
    
    return JsonResponse({"dealers count with less than {}".format(str(percent_filter) + '%'):percent_filter_less_count, "dealers count with more than {}".format(str(percent_filter) + "%"):percent_filter_more_count})

def download_excel(request, percent_filter, start_year, end_year,type=None, quarter=None, first_month=None, second_month=None):
    
    df, df_all_columns_start_year, df_all_columns_end_year = get_columns(percent_filter=percent_filter, start_year=start_year, end_year=end_year, quarter_req=quarter, first_month=first_month, second_month=second_month)
    df_start_year = df[df_all_columns_start_year]
    df_end_year = df[df_all_columns_end_year]
    
    df_start_year['difference %'] = ((df_start_year[df_all_columns_start_year[0]] - df_end_year[df_all_columns_end_year[0]]) / df_end_year[df_all_columns_end_year[0]]) * 100
    
    df_start_year[second_month.upper()+ '-' +str(end_year)] = df_end_year[df_end_year.columns[0]]
    
    if type == 'more':
        df_start_year = df_start_year[(df_start_year['difference %'] > float(percent_filter)) & (df_start_year['difference %'] != float('inf'))]
    else:
        df_start_year = df_start_year[(df_start_year['difference %'] < float(percent_filter)) & (df_start_year['difference %'] != float('inf'))]
        
    final_df = df_start_year.copy()
    final_df['Name of Account'] = df['Name of Account']
    final_df['SAP Code'] = df['SAP Code']
    final_df['Region'] = df['Region']
    final_df['Zone'] = df['Zone']
    final_df['DOJ'] = df['DOJ']

    excel_file = "dealers_details.xlsx"
    final_df.to_excel(excel_file)

    file_path = '/home/lenovo/Desktop/projects/jkmatplot/jkanalysis/' + excel_file

    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(excel_file)        
        return response
    else:
        return JsonResponse({"Error":"Please try again"}, status=status.HTTP_503_SERVICE_NOT_AVAILABLE)


def get_regions(request):
    if request.method == 'GET':
        query_param = request.GET.get('zone')
        df = pd.read_csv("jkanalysisapp/jkdata.csv", header=3)
        if query_param:
            zone_regions = df[df['Zone'] == query_param]['Region'].unique()
        else:
            pass
        return JsonResponse({query_param:zone_regions.tolist()})
    else:
        return JsonResponse({"Error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
def get_zones(request):
    if request.method == 'GET':
        df = pd.read_csv("jkanalysisapp/jkdata.csv", header=3)
        all_regions = df['Zone'].unique()
        return JsonResponse({"Zone":all_regions.tolist()})
    else:
        return JsonResponse({"Error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def yoy_new(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_year = data['first_year']
        end_year = data['sec_year']
        percent_filter = data['perc_filter']
        
        df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year, percent_filter=percent_filter)
        
        start_year_apm_value = df[df_all_columns_start_year].sum().sum()/12
        end_year_apm_value = df[df_all_columns_end_year].sum().sum()/12
        
        if percent_filter:
            result = percent_filter_func(start_year=start_year, end_year=end_year, percent_filter=percent_filter)
            
            if result.status_code == 404:
                return JsonResponse({"Error": "Please try again"}, status=status.HTTP_404_NOT_FOUND)
            res = json.loads(result.content)
            return JsonResponse(res)
        
        return JsonResponse({'APM-' + start_year:start_year_apm_value, 'APM-' + end_year:end_year_apm_value})
    else:
        return JsonResponse({"Error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def qoq_new(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_year = data['first_year']
        end_year = data['sec_year']
        percent_filter = data['perc_filter']
        quarter_req = data['first_quarter']
        end_quarter = data['sec_quarter']

        df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year, percent_filter=percent_filter, quarter_req=quarter_req, end_quarter=end_quarter)
        
        start_year_apm_value = df[df_all_columns_start_year].sum().sum()/12
        end_year_apm_value = df[df_all_columns_end_year].sum().sum()/12
        
        if percent_filter:
            result = percent_filter_func(start_year=start_year, end_year=end_year, percent_filter=percent_filter, quarter=quarter_req, end_quarter=end_quarter)
            
        if result.status_code == 404:
            return JsonResponse({"Error": "Please try again"}, status=status.HTTP_404_NOT_FOUND)
        res = json.loads(result.content)

        return JsonResponse(res)
        
        
        return JsonResponse({quarter_req.upper() + '-' + start_year:start_year_apm_value, end_quarter.upper() + '-' +  end_year:end_year_apm_value})

    else:
        return JsonResponse({"Error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def mom_new(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_year = data['first_year']
        end_year = data['sec_year']
        percent_filter = data['perc_filter']
        first_month = data['first_month']
        second_month = data['sec_month']
        
        df, df_all_columns_start_year, df_all_columns_end_year = get_columns(start_year=start_year, end_year=end_year, percent_filter=percent_filter, first_month=first_month, second_month=second_month)
        
        start_year_apm_value = df[df_all_columns_start_year].sum().sum()/12
        end_year_apm_value = df[df_all_columns_end_year].sum().sum()/12
        
        if percent_filter:
            result = percent_filter_func(start_year=start_year, end_year=end_year, percent_filter=percent_filter, first_month=first_month, second_month=second_month)
            if result.status_code == 404:
                return JsonResponse({"Error": "Please try again"}, status=status.HTTP_404_NOT_FOUND)
            res = json.loads(result.content)
            return JsonResponse(res)
        return JsonResponse({first_month.upper() + '-' + start_year:start_year_apm_value, second_month.upper() + '-' + end_year:end_year_apm_value})
    else:
        return JsonResponse({"Error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)