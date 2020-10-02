# Create your views here.
import json

from django.http import request, HttpResponse, JsonResponse

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import IncidentStatusTypeMaster, IncidentCategoryMaster, ServerMaster, SmsManager, SmsLog, ContactUs, Hint
import requests
import random
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.datastructures import MultiValueDictKeyError
import os

from master.models import UserMaster, UserMasterDetails

from master.models import EducationMaster, AccessTypeMaster, UserTypeMaster

from logs.models import RegLog, UserLogs, PaymentLog
from config.utils import create_log
from django.contrib.auth import authenticate
from config.utils import create_log
import re
# import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from .models import NotificationLog, TockenUser, BankList, BankTransactionPRD, BillConfirmation, BankTransaction, \
    IncidentMaster, IncidentCommentDetail, IncidentFeedbackDetail

from calendar import monthrange
from django.db.models import Count

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.cache import add_never_cache_headers, patch_response_headers, patch_vary_headers


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
# @method_decorator(cache_page(60))
def dashboard_data_IH(request, BPCODE):
    dash = None
    lastmonth_year = ""
    lastmonth_year_Bill_Amt = ""
    YTDData = ""
    MTDData = ""
    HintCount = ""
    Open_count = 0
    Closed_Count = 0
    Noti_Count = 0
    response = None

    try:

        IC = GETIncident_Count_Dashboard(BPCODE)

        IC = json.loads(IC.content)
        Open_count = IC['Open_count']
        Closed_Count = IC['Closed_Count']
        Noti_Count = NotificationLog.objects.filter(status=1, BP_Code=BPCODE, Read_Status=0).count()
        try:
            userm = UserMaster.objects.get(username=BPCODE)
        except UserMaster.DoesNotExist as ex:
            userm = None
            dash_f = GETSAP_Dashboard(request, BPCODE)
            if dash_f[0]:
                dash = dash_f[1]
                del dash['__metadata']

            ll = Last_Bill_Month(request, BPCODE)
            ll_j = json.loads(ll.content)
            lastmonth_year = ll_j['lastmonth_year']
            lastmonth_year_Bill_Amt = ll_j['lastmonth_year_Bill_Amt']

            ytd = Last_Seven_Days_Copy(request, BPCODE)
            YTDData = json.loads(ytd.content)

            mtd = Last_Six_Month_Bill(request, BPCODE)
            MTDData = json.loads(mtd.content)

        cu = Hint.objects.filter(Hint_Status=1, Hint_Leng='EN').count()
        HintCount = str(cu)

        if userm:
            # user_type = UserTypeMaster.objects.get(
            #     user_type='EU')
            try:
                ud = UserMasterDetails.objects.get(usermaster=userm)
            except UserMasterDetails.DoesNotExist as ex:
                ud = None
                dash_f = GETSAP_Dashboard(request, BPCODE)
                if dash_f[0]:
                    dash = dash_f[1]
                    del dash['__metadata']

            if ud:
                if ud.user_type.user_type == "EU":
                    dash_f = GETSAP_Dashboard(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]
                        del dash['__metadata']

                else:
                    dash_f = GETSAP_Dashboard_DBUser(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]

                        del dash['__metadata']
                        dash_new = {"Partner": BPCODE,
                                    "GrossCopy": dash['PaidCopy'],
                                    "FreeCopy": "",
                                    "PaidCopy": dash['PaidCopy'],
                                    "Zlao": "",
                                    "Zcoo": "",
                                    "OutStd": round(float(float(dash['OutStd']) / 100000), 2),
                                    "Asd": round(float(float(dash['Asd']) / 100000), 2),

                                    }
                        lastmonth_year_Bill_Amt = round(
                            float(float(dash['Billing']) / 100000), 2)
                        dash = dash_new
                ll = Last_Bill_Month(request, BPCODE)
                ll_j = json.loads(ll.content)
                lastmonth_year = ll_j['lastmonth_year']
                if ud.user_type.user_type == "EU":
                    lastmonth_year_Bill_Amt = ll_j['lastmonth_year_Bill_Amt']
                # else:
                #     lastmonth_year_Bill_Amt = dash['Billing']

                ytd = Last_Seven_Days_Copy(request, BPCODE)
                YTDData = json.loads(ytd.content)

                mtd = Last_Six_Month_Bill(request, BPCODE)
                MTDData = json.loads(mtd.content)

            # else:
            #     dash_f = GETSAP_Dashboard(request, BPCODE)

        ul = user_log(request, BPCODE, 'Dashboard', 'Dashboard Open')
        response = JsonResponse(
            {'data': dash, 'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt,
             'YTDData': YTDData, 'MTDData': MTDData, 'HintCount': HintCount, "Open_count": Open_count,
             "Closed_Count": Closed_Count, 'Noti_Count': Noti_Count, 'reply': 'User Dashboard Data'})
        # response['Cache-Control'] = f'max-age={60*60*24}'
        # response.RawResponse(headers={"content-type": "application/json"})
        # response.headers['Cache-Control'] = 'max-age=60'
        # if ud.user_type.user_type == "EU":
        # patch_response_headers(response, cache_timeout=300)

        return response

    except Exception as e:
        ul = user_log(request, BPCODE, 'Dashboard',
                      'Dashboard Open with Error')
        response = JsonResponse(
            {'data': None, 'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt,
             'YTDData': YTDData, 'MTDData': MTDData, 'HintCount': HintCount, "Open_count": Open_count,
             "Closed_Count": Closed_Count, 'Noti_Count': Noti_Count, 'reply': str(e)})
        return response


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def user_len(request):
    request_data = json.loads(request.body)
    try:
        if request.method == 'POST':
            DeviceTokenId = ""
            Bp_code = request_data['Bp_code']
            Notification_Leng = request_data['Leng']
            device_id = request_data['device_id']
            if "DeviceTokenId" in request_data:
                DeviceTokenId = request_data['DeviceTokenId']
            data_msg = 'Notification_Leng update'
            try:
                um = UserMaster.objects.get(username=Bp_code)
                TU = TockenUser.objects.filter(usermaster=um, Tocken_code=DeviceTokenId, device_id=device_id).update(
                    Notification_Leng=Notification_Leng)
                if TU:
                    # TU.Notification_Leng = Notification_Leng
                    # TU.Tocken_code = DeviceTokenId
                    # TU.device_id = device_id
                    # TU.save()
                    TU = None
                else:
                    TU = TockenUser()
                    TU.usermaster = um
                    TU.Tocken_code = DeviceTokenId
                    TU.device_id = device_id
                    TU.Notification_Leng = Notification_Leng
                    TU.save()



            except UserMaster.DoesNotExist as ex:
                um = None
                data_msg = 'BP Code not found'

            ul = user_log(request, Bp_code, 'Login', 'Notification_Leng')

            return JsonResponse({'data': data_msg, 'reply': 'Notification_Leng Successful '})


    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Notification_Read(request, BP_Code):
    try:

        # Incident_data = NotificationLog.objects.filter(status=1,BP_Code=BP_Code,Read_Status=0).update(Read_Status=1,Read_On=datetime.now())

        return JsonResponse({'data': {'BP_Code': BP_Code, 'Read': 'T'}, 'reply': 'Notification Read'})
    except Exception as e:

        return JsonResponse({'data': None, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Notification_Read_ID(request, Nitification_Id):
    try:

        Incident_data = NotificationLog.objects.filter(status=1, Nitification_Id=Nitification_Id).update(Read_Status=1,
                                                                                                         Read_On=datetime.now())

        return JsonResponse({'data': {'Nitification_Id': Nitification_Id, 'Read': 'T'}, 'reply': 'Notification Read'})
    except Exception as e:

        return JsonResponse({'data': None, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Notification_List(request, BP_Code):
    try:
        Incident_data = None
        indidata_new = []
        Incident_data = NotificationLog.objects.filter(status=1, BP_Code=BP_Code, Read_Status=0)
        if Incident_data:
            for item in Incident_data:
                tt = {
                    'Nitification_Id': item.Nitification_Id,
                    'usermaster': item.usermaster.adalias,
                    'Notification_Category': item.Notification_Category,
                    'State': item.State,
                    'Notification_Leng': item.Notification_Leng,
                    'SalseOrg': item.SalseOrg,
                    'BP_Code': item.BP_Code,
                    'Notification_Title': item.Notification_Title,
                    # Notification_Body = models.TextField(max_length=255, blank=True, null=True)
                    'Notification_To': item.Notification_To,
                    'Notification_body': item.Notification_body,
                    'Screen_Name': item.Screen_Name,
                    'Sent_Status': item.Sent_Status,
                    'Sent_On': item.Sent_On,
                    'Read_Status': item.Read_Status,
                    'Read_On': item.Read_On,
                    'googleapis_Request_Body': item.googleapis_Request_Body,
                    'googleapis_Response_Code': item.googleapis_Response_Code,
                    'googleapis_Response_Body': item.googleapis_Response_Body,

                    'status': item.status,
                    'create_date': item.create_date,
                    'update_date': item.update_date,
                    'create_user': item.create_user,
                    'update_user': item.update_user

                }
                indidata_new.append(tt)

            # indidata_new = serializers.serialize(
            #     'python', Incident_data, use_natural_foreign_keys=True, use_natural_primary_keys=True)

        return JsonResponse({'data': indidata_new, 'reply': 'Notification List'})
    except Exception as e:

        return JsonResponse({'data': None, 'reply': str(e)})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def send_noti(request):
    try:
        request_data = json.loads(request.body)

        serverToken = 'AAAAga-7N00:APA91bHrOFit0sWc9LsxR9L1Cujl8Pk7_AG66XpElQlNrQadIJM-QrnjfpGPhTg0CjTLEh3zjzJK8yWgp8PB56diMN9Dm2hvLNz9eyg3vN04LBsxCTozhKDAnUU4fyZcq07dfij3FDXG'
        deviceToken = request_data['deviceToken']
        msg_title = request_data['msg_title']
        msg_body = request_data['msg_body']

        try:
            um = UserMaster.objects.get(username=request_data['BP_Code'])
        except UserMaster.DoesNotExist as ex:
            um = None
        NL = NotificationLog()
        NL.usermaster = um
        NL.Notification_Category = 'Test'
        NL.BP_Code = request_data['BP_Code']

        NL.Screen_Name = request_data['screen_name']

        NL.save()

        dataPayLoad = {
            "screen_name": request_data['screen_name'], "BP_Code": request_data['BP_Code'],
            "notification_id": NL.Nitification_Id,
            'title': msg_title,
            'body': msg_body}

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }

        body = {

            'to': deviceToken,

            'priority': 'high',
            'data': dataPayLoad,
        }
        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

        NL.Notification_Title = msg_title
        NL.Notification_To = deviceToken
        NL.Notification_body = msg_body
        NL.googleapis_Request_Body = body
        NL.Sent_Status = 1
        NL.Sent_On = datetime.now()
        NL.googleapis_Response_Code = response.status_code
        NL.save()

        # print(response.status_code)
        if response.status_code == 200:
            NL.googleapis_Response_Body = response.json()
            NL.save()
            return JsonResponse({'data': response.json(), 'reply': response.status_code})
        else:
            # return HttpResponse( + '   '  + str(response))
            NL.googleapis_Response_Body = 'Not Sent'
            NL.save()
            return JsonResponse({'data': 'Not Sent', 'reply': response.status_code})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
def send_push_notification(request):
    try:
        serverToken = 'AAAAga-7N00:APA91bHrOFit0sWc9LsxR9L1Cujl8Pk7_AG66XpElQlNrQadIJM-QrnjfpGPhTg0CjTLEh3zjzJK8yWgp8PB56diMN9Dm2hvLNz9eyg3vN04LBsxCTozhKDAnUU4fyZcq07dfij3FDXG'
        deviceToken = 'cDLGh1DnT-WHPJbw6xLW2L:APA91bEJsmXJ0-IZ9bvKQCivAUL4Xq1HG0RQ0phDnZfpMKMnzDnFOE7byN0R09BGoO7nZcCQYSmTudmEelGVGoX-9VNYryACxdLo2O0k83uhB-gE9gprenz2kJQ9JFbPdAHWdCmUHoAP'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }

        body = {
            'notification': {'title': 'Welcome to DB Samriddhi App',
                             'body': 'Welcome to DB Samriddhi App to view your transaction detail'
                             },
            'to': deviceToken,

            'priority': 'high',
            #   'data': dataPayLoad,
        }
        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        # print(response.status_code)
        if response.status_code == 200:
            return JsonResponse({'data': response.json(), 'reply': response.status_code})
        else:
            return HttpResponse(str(response.status_code) + '   ' + str(response))

    except Exception as e:

        return JsonResponse({'data': None, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Bank_List(request):
    try:
        Incident_data = None
        indidata_new = []
        Incident_data = BankList.objects.filter(status=1)
        if Incident_data:
            for item in Incident_data:
                tt = {'Bank_Name': item.Bank_Name,
                      'Bank_Type': item.Bank_Type,
                      'Bank_URL': item.Bank_URL,
                      'status': item.status,
                      'create_date': item.create_date,
                      'update_date': item.update_date,
                      'create_user': item.create_user,
                      'update_user': item.update_user

                      }
                indidata_new.append(tt)

            # indidata_new = serializers.serialize(
            #     'python', Incident_data, use_natural_foreign_keys=True, use_natural_primary_keys=True)

        return JsonResponse({'data': indidata_new, 'reply': 'Bank List'})
    except Exception as e:

        return JsonResponse({'data': None, 'reply': str(e)})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def POSTIDBIUTRSAP(request):
    return_toBank = {"status": "failed", "utr": None, "reason": "NA"}
    try:

        request_data = json.loads(request.body)
        utr = request_data['utr']
        return_toBank = {"status": "failed", "utr": utr, "reason": "NA"}
        pan = request_data['pan']
        van = request_data['van']
        tranAmt = request_data['tranAmt']

        trandate = request_data['trandate']

        Rem_name = request_data['Rem_name']
        Rem_name_rbi = request_data['Rem_name_rbi']

        mode = request_data['mode']
        Sender_receiver_info = request_data['Sender_receiver_info']
        ifsc = request_data['ifsc']
        RemitterAcctNo = request_data['RemitterAcctNo']

        if request.user.username == "idbiapi":

            if request.method == 'POST':
                try:
                    BT = BankTransactionPRD.objects.get(utr=utr, status=1)
                    return_toBank = {"status": "duplicate", "utr": utr,
                                     "reason": "All ready transaction is received"}
                    return JsonResponse(return_toBank)

                except BankTransactionPRD.DoesNotExist as e:
                    BT_new = BankTransactionPRD()
                    BT_new.pan = pan
                    BT_new.van = van
                    BT_new.tranAmt = tranAmt
                    BT_new.trandate = trandate
                    BT_new.Rem_name = Rem_name
                    BT_new.Rem_name_rbi = Rem_name_rbi
                    BT_new.utr = utr
                    BT_new.mode = mode
                    BT_new.Sender_receiver_info = Sender_receiver_info
                    BT_new.ifsc = ifsc
                    BT_new.RemitterAcctNo = RemitterAcctNo
                    BT_new.create_user = request.user.username
                    BT_new.save()
                    ul = user_log(request, 'IDBI Bank', 'Bank Transaction',
                                  'Insert IDBI Bank PRD UTR #: ' + str(utr))
                    return_toBank['status'] = "success"
                    return_toBank['reason'] = "NA"
                    return_toBank['utr'] = utr
                    BT_new.Response_To_Bank = 1
                    BT_new.Bank_Response_Json = return_toBank
                    BT_new.save()
                    rr = POST_BANK_TRID(request, BT_new.Transaction_ID, 'PAY')
                    return JsonResponse(return_toBank)
        else:

            return_toBank = {"status": "failed", "utr": utr,
                             "reason": "User not authorized to post data"}
            return JsonResponse(return_toBank)

    except Exception as e:
        return_toBank['status'] = "failed"
        return_toBank['reason'] = str(e)
        # ul = user_log(request, 'IDBI Bank', 'Bank Transaction',
        #                          'Insert Error IDBI Bank PRD UTR #: ' + return_toBank)
        return JsonResponse(return_toBank)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def BillConfirm(request):
    request_data = json.loads(request.body)
    Bill_Period = request_data['Bill_Period']
    Bill_No = request_data['Bill_No']
    Confirm_Remark = request_data['Confirm_Remark']
    Confirm_By = request_data['Confirm_By']

    device_id = request_data['device_id']
    BP_Code = request_data['BP_Code']
    Bill_Amount = request_data['Bill_Amount']
    Bill_copies = request_data['Bill_copies']
    try:
        data = {}
        if request.method == 'POST':
            try:
                BC = BillConfirmation.objects.get(Bill_No=Bill_No)
                return_toBank = {
                    "reply": "You have confirmed already this bill"}
                return JsonResponse(return_toBank)

            except BillConfirmation.DoesNotExist as e:
                BT_new = BillConfirmation()
                BT_new.Bill_Period = Bill_Period
                BT_new.Bill_No = Bill_No
                BT_new.BP_Code = BP_Code
                BT_new.Confirm_Remark = Confirm_Remark
                BT_new.Confirm_By = Confirm_By
                BT_new.Device_On = device_id
                BT_new.Bill_Amount = Bill_Amount
                BT_new.Bill_copies = Bill_copies

                BT_new.save()
                ul = user_log(request, BP_Code, 'Billing',
                              'Bill Confirmation Done Bill no. #: ' + str(Bill_No))
                return_toBank = {
                    "reply": "The Transactions in the Bill are confirmed"}
                return JsonResponse(return_toBank)

    except Exception as e:
        return JsonResponse({"reply: ": "Bill Confirmation Error: " + str(e)})


def POST_BANK_TRID(request, Tr_ID, serverCode):
    try:
        pots_body = {
            "Van": None,
            "Amount": None,
            "TrnDate": None,
            "Utr": None,
            "TrType": None,
            "Ifsc": None
        }
        BT = None
        if serverCode == "QEC":
            BT = BankTransaction.objects.get(Transaction_ID=Tr_ID)
        if serverCode == "PAY":
            BT = BankTransactionPRD.objects.get(Transaction_ID=Tr_ID)

        if BT:
            pots_body = {
                "Van": BT.van,
                "Amount": BT.tranAmt,
                "TrnDate": BT.trandate.strftime("%Y-%m-%d") + "T01:00:00.000000",
                "Utr": BT.utr,
                "TrType": BT.mode,
                "Ifsc": BT.ifsc
            }
            if BT.Post_To_SAP == 0:
                res = SAP_BANK_POST_QEC(request, pots_body, serverCode)
                if res[0]:
                    BT.Post_To_SAP = 1
                    BT.Post_To_SAP_on = datetime.now()
                    BT.SAP_sent_Json = pots_body
                    BT.SAP_response_Json = res[1]
                    BT.save()
                    ul = user_log(request, 'IDBI Bank', 'Bank Transaction SAPPOST',
                                  'POST Sucess IDBI Bank UTR #: ' + str(BT.utr))
                else:
                    BT.Post_To_SAP = 0
                    BT.Post_To_SAP_on = datetime.now()
                    BT.SAP_sent_Json = pots_body
                    BT.SAP_response_Json = res[1]
                    BT.save()
                    ul = user_log(request, 'IDBI Bank', 'Bank Transaction SAPPOST',
                                  'POST Fail IDBI Bank UTR #: ' + str(BT.utr))
                return JsonResponse({"message": res[0]})
            else:
                return JsonResponse({"message": "Already Posted to SAP"})

        else:
            return JsonResponse({"message": "Tr ID Not Found"})

    except Exception as ex:
        return JsonResponse({"message": str(ex)})


def SAP_BANK_POST_QEC(request, pots_body=None, serverCode='PRD'):
    try:

        sapuser = ''
        sappassword = ''
        sapurl = ''

        try:

            res = ServerMaster.objects.get(
                server_text=serverCode, server_status='1')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"

                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_IDBI_SRV/BANKSet" % (
                    res.server_host)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))
        headers = {"content-type": "application/json",
                   "X-Requested-With": "X", "Accept": "application/json"}
        auth_values = (sapuser, sappassword)
        body_json = pots_body
        response = requests.post(
            sapurl, auth=auth_values, data=json.dumps(body_json), headers=headers)
        flag = None
        fresult = None
        # if response.status_code == 201:
        appdata = (response.json())
        # else:
        # appdata = {'msg':response.json()}

        if len(appdata) >= 1:
            if response.status_code == 201:
                fresult = response.headers
                # else:
                # results = appdata['d']
                # if fresult == "Message Send: Successfully":
                flag = True
            else:
                flag = False
                fresult = appdata
            # if len(results) >0:
            #     fresult = results

            # else:
            #     pass

            if flag:

                return (flag, fresult)
            else:

                return (flag, fresult)

        else:

            return (flag, "No Response Get From SAP!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def POSTIDBIUTR(request):
    return_toBank = {"status": "failed", "utr": None, "reason": "NA"}
    try:

        request_data = json.loads(request.body)
        utr = request_data['utr']
        return_toBank = {"status": "failed", "utr": utr, "reason": "NA"}
        pan = request_data['pan']
        van = request_data['van']
        tranAmt = request_data['tranAmt']

        trandate = request_data['trandate']

        Rem_name = request_data['Rem_name']
        Rem_name_rbi = request_data['Rem_name_rbi']

        mode = request_data['mode']
        Sender_receiver_info = request_data['Sender_receiver_info']
        ifsc = request_data['ifsc']
        RemitterAcctNo = request_data['RemitterAcctNo']

        if request.user.username == "idbiapi":

            if request.method == 'POST':
                try:
                    BT = BankTransaction.objects.get(utr=utr)
                    return_toBank = {"status": "duplicate", "utr": utr,
                                     "reason": "All ready transaction is received"}
                    return JsonResponse(return_toBank)

                except BankTransaction.DoesNotExist as e:
                    BT_new = BankTransaction()
                    BT_new.pan = pan
                    BT_new.van = van
                    BT_new.tranAmt = tranAmt
                    BT_new.trandate = trandate
                    BT_new.Rem_name = Rem_name
                    BT_new.Rem_name_rbi = Rem_name_rbi
                    BT_new.utr = utr
                    BT_new.mode = mode
                    BT_new.Sender_receiver_info = Sender_receiver_info
                    BT_new.ifsc = ifsc
                    BT_new.RemitterAcctNo = RemitterAcctNo
                    BT_new.create_user = request.user.username
                    BT_new.save()
                    ul = user_log(request, 'IDBI Bank', 'Bank Transaction',
                                  'Insert IDBI Bank QEC UTR #: ' + str(utr))
                    return_toBank['status'] = "success"
                    return_toBank['reason'] = "NA"
                    return_toBank['utr'] = utr
                    BT_new.Response_To_Bank = 1
                    BT_new.Bank_Response_Json = return_toBank
                    BT_new.save()

                    return JsonResponse(return_toBank)
        else:

            return_toBank = {"status": "failed", "utr": utr,
                             "reason": "User not authorized to post data"}
            return JsonResponse(return_toBank)

    except Exception as e:
        return_toBank['status'] = "failed"
        return_toBank['reason'] = str(e)
        return JsonResponse(return_toBank)


def GETIncident_Count_Dashboard(BPCODE):
    try:
        Open_count = 0
        Closed_Count = 0
        try:
            um = UserMaster.objects.get(username=BPCODE)
        except UserMaster.DoesNotExist as ex:
            um = None
        if um:
            try:
                ud = UserMasterDetails.objects.get(usermaster=um)
            except UserMasterDetails.DoesNotExist as ex:
                ud = None
        if ud:
            Incident_Status_open = IncidentStatusTypeMaster.objects.get(pk=2)
            Incident_Status_close = IncidentStatusTypeMaster.objects.get(pk=3)
            if ud.access_type.access_type == 'AG':
                Open_count = Open_count + IncidentMaster.objects.filter(
                    Incident_Status=Incident_Status_open, status=1, Incident_BP_CODE=BPCODE).count()
                Closed_Count = Closed_Count + IncidentMaster.objects.filter(
                    Incident_Status=Incident_Status_close, status=1, Incident_BP_CODE=BPCODE).count()

            else:

                dash_f = GETSAP_DBUser_Outstanding_Count(
                    request, BPCODE, 'S', '*')

                dash = None
                if dash_f[0]:
                    dash = dash_f[1]
                    # del dash['__metadata']
                    for num in dash['results']:
                        del num['__metadata']

                        Open_count = Open_count + IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_open, status=1, Incident_STATE=num['State']).count()
                        Closed_Count = Closed_Count + IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_close, status=1, Incident_STATE=num['State']).count()

        return JsonResponse(
            {'BPCODE': BPCODE, 'Open_count': Open_count, 'Closed_Count': Closed_Count, 'reply': 'GETIncident_Count'})

    except Exception as e:
        return JsonResponse({'BPCODE': BPCODE, 'Open_count': Open_count, 'Closed_Count': Closed_Count, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GETIncident_Count(request, BPCODE, GrpBy, Search_Key):
    try:
        inci_count = []

        dash_f = GETSAP_DBUser_Outstanding_Count(
            request, BPCODE, GrpBy, Search_Key)
        Open_count = 0
        Closed_Count = 0
        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']
                inci_data = {'InHouse_Code': BPCODE, 'State': '', 'Vkorg': '', 'SoldToParty': '',
                             'Location': '', 'CustName': '', 'Open_Count': '', 'Closed_Count': ''}
                inci_data['State'] = num['State']
                inci_data['Vkorg'] = num['Vkorg']
                inci_data['Location'] = num['Location']
                inci_data['SoldToParty'] = num['SoldToParty']
                Incident_Status_open = IncidentStatusTypeMaster.objects.get(
                    pk=2)
                Incident_Status_close = IncidentStatusTypeMaster.objects.get(
                    pk=3)
                if GrpBy == 'S':
                    Open_count = IncidentMaster.objects.filter(
                        Incident_Status=Incident_Status_open, status=1, Incident_STATE=num['State']).count()
                    Closed_Count = IncidentMaster.objects.filter(
                        Incident_Status=Incident_Status_close, status=1, Incident_STATE=num['State']).count()
                if GrpBy == 'C':
                    Open_count = IncidentMaster.objects.filter(
                        Incident_Status=Incident_Status_open, status=1, Incident_VKORG=num['Vkorg']).count()
                    Closed_Count = IncidentMaster.objects.filter(
                        Incident_Status=Incident_Status_close, status=1, Incident_VKORG=num['Vkorg']).count()

                if GrpBy == 'A':
                    inci_data['CustName'] = num['CustName']
                    Open_count = IncidentMaster.objects.filter(
                        Incident_Status=Incident_Status_open, status=1, Incident_BP_CODE=num['SoldToParty']).count()
                    Closed_Count = IncidentMaster.objects.filter(
                        Incident_Status=Incident_Status_close, status=1, Incident_BP_CODE=num['SoldToParty']).count()

                inci_data['Open_Count'] = Open_count
                inci_data['Closed_Count'] = Closed_Count
                if Open_count == 0 and Closed_Count == 0:
                    pass
                else:
                    inci_count.append(inci_data)

        return JsonResponse({'data': {'results': inci_count}, 'reply': 'GETIncident_Count'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def get_agentVKORG(request, BPCODE):
    try:
        VKORG = None
        State = None
        Partner = None
        Type = None
        Name = None
        dash_f = GETSAP_Agent_Hirarchy(request, BPCODE)

        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            for num in dash['results']:
                if num['Type'] == 'CE':
                    VKORG = num['Vkorg']
                    State = num['State']
                    Partner = num['Partner']
                    Type = num['Type']
                    Name = num['Name']
                    break

                if num['Type'] == 'UE':
                    VKORG = num['Vkorg']
                    State = num['State']
                    Partner = num['Partner']
                    Type = num['Type']
                    Name = num['Name']
                    break

        return JsonResponse(
            {'BPCODE': BPCODE, 'VKORG': VKORG, 'State': State, 'Partner': Partner, 'Type': Type, 'Name': Name,
             'reply': 'GETAgent_Hirarchy'})

    except Exception as e:
        return JsonResponse(
            {'BPCODE': BPCODE, 'VKORG': VKORG, 'State': State, 'Partner': Partner, 'Type': Type, 'Name': Name,
             'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GETAgent_Hirarchy(request, BPCODE):
    try:

        dash_f = GETSAP_Agent_Hirarchy(request, BPCODE)

        dash = None
        if dash_f[0]:
            dash = dash_f[1]

        return JsonResponse({'data': dash, 'reply': 'GETAgent_Hirarchy'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def GETSAP_Agent_Hirarchy(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_HIRERCHY_SRV/HIRSet?$format=json&$filter=Partner eq '%s'" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
                for num in results['results']:
                    del num['__metadata']

            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def UpdateIncidentComment(request):
    request_data = json.loads(request.body)
    incident_number = request_data['Incident_Number']
    incident_status = request_data['Incident_Status_Code']
    incident_comment_text = request_data['incident_comment_text']

    incident_device_id = request_data['device_id']
    Bp_code = request_data['Bp_code']
    try:
        data = {}
        if request.method == 'POST':
            IncidentComment_By_Name = None
            IncidentComment_By_Level = None
            try:
                IM = IncidentMaster.objects.get(pk=incident_number)
                IS = IncidentStatusTypeMaster.objects.get(pk=incident_status)
                IM.Incident_Status = IS  # incident_status
                IM.Incident_Last_Comment = incident_comment_text
                IM.Incident_Last_Comment_By = Bp_code
                IM.Incident_Last_Comment_On = datetime.now()

                IM.save()

                IF = IncidentCommentDetail()
                IF.Incident_Number = IM
                try:
                    uu = UserMaster.objects.get(
                        username=request_data['Bp_code'])
                    IncidentComment_By_Name = uu.first_name
                    ud = UserMasterDetails.objects.get(usermaster=uu)
                    IncidentComment_By_Level = ud.access_type
                except UserMaster.DoesNotExist as ex:
                    pass
                except UserMasterDetails.DoesNotExist as ex:
                    pass

                IF.IncidentComment_Text = incident_comment_text
                Incident_Status = IS
                IF.IncidentComment_By = Bp_code
                IF.IncidentComment_On = datetime.now()
                IF.create_user = Bp_code
                IF.IncidentComment_By_Name = IncidentComment_By_Name
                IF.IncidentComment_By_Level = IncidentComment_By_Level
                IF.save()
                ul = user_log(request, Bp_code, 'Incident',
                              'Incident Update #: ' + str(incident_number))
                return JsonResponse({'reply': "Incident Comment Saved Successfully #: " + str(incident_number)})

            except IncidentMaster.DoesNotExist as e:
                return JsonResponse({"reply: ": "Incident not found"})

            except IncidentStatusTypeMaster.DoesNotExist as e:
                return JsonResponse({"reply: ": "Invalid Status Code"})

            # return JsonResponse({'reply': "Incident Create #: "+str(Incident_Number)})

    except Exception as e:
        return JsonResponse({"reply: ": "Incident Create Error: " + str(e)})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def UpdateFeedback(request):
    request_data = json.loads(request.body)
    incident_number = request_data['Incident_Number']
    incident_status = request_data['Incident_Status_Code']
    incident_feedback_text = request_data['incident_feedback_text']
    incident_rating = request_data['incident_rating']
    incident_device_id = request_data['device_id']
    Bp_code = request_data['Bp_code']
    try:
        data = {}
        if request.method == 'POST':

            try:
                IM = IncidentMaster.objects.get(pk=incident_number)
                IS = IncidentStatusTypeMaster.objects.get(pk=incident_status)
                IM.Incident_Status = IS  # incident_status
                IM.Incident_Last_Feedback = incident_feedback_text
                IM.Incident_Last_Feedback_By = Bp_code
                IM.Incident_Last_Feedback_On = datetime.now()

                IM.save()

                IF = IncidentFeedbackDetail()
                IF.Incident_Number = IM
                IF.IncidentFeedback_Rating = incident_rating
                IF.IncidentFeedback_Text = incident_feedback_text
                IF.IncidentFeedback_By = Bp_code
                IF.create_user = Bp_code
                IF.save()

                return JsonResponse({'reply': "Incident Update Successfully #: " + str(incident_number)})

            except IncidentMaster.DoesNotExist as e:
                return JsonResponse({"reply: ": "Incident not found"})

            except IncidentStatusTypeMaster.DoesNotExist as e:
                return JsonResponse({"reply: ": "Invalid Status Code"})

            ul = user_log(request, Bp_code, 'Incident',
                          'Incident Update #: ' + str(incident_number))

            return JsonResponse({'reply': "Incident Create #: " + str(Incident_Number)})

    except Exception as e:
        return JsonResponse({"reply: ": "Incident Create Error: " + str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetIncidentComments(request, Incident_Number):
    try:
        IncidentCommnets = None

        try:

            IM = IncidentMaster.objects.get(pk=Incident_Number)

        except IncidentMaster.DoesNotExist as ex:
            return JsonResponse({'data': None, 'reply': "No Incident Comments Found"})

        Incident_data = IncidentCommentDetail.objects.filter(
            status=1, Incident_Number=IM)

        if Incident_data:

            # Incident_data1 = json.dumps(list(Incident_data))
            indidata_new = serializers.serialize(
                'python', Incident_data, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            for incidata in indidata_new:
                incidata['fields']['create_date'] = incidata['fields']['create_date'].date()

            return JsonResponse({'data': indidata_new, 'reply': 'GetIncidentComments'})
        else:
            return JsonResponse({'data': None, 'reply': "No Incident Comments Found"})
    except IncidentCommentDetail.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "No Incident Comments Found"})

    except Exception as ex:
        return JsonResponse({'data': None, 'reply': str(ex)})


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetIncidentList(request, BPCODE, Status_CODE, CATEGORY_CODE):
    try:
        IncidentCommentList = []
        IncidentFeedbackList = []
        IncidentStatus = None
        IncidentCategory = None
        if Status_CODE != '*':
            try:

                IncidentStatus = IncidentStatusTypeMaster.objects.get(
                    pk=Status_CODE)

            except IncidentStatusTypeMaster.DoesNotExist as ex:
                return JsonResponse({'data': None, 'reply': "No Status Code Found"})

        if CATEGORY_CODE != '*':
            try:

                IncidentCategory = IncidentCategoryMaster.objects.get(
                    pk=CATEGORY_CODE)

            except IncidentCategoryMaster.DoesNotExist as ex:
                return JsonResponse({'data': None, 'reply': "No Category Code Found"})

        if Status_CODE == '*':
            if CATEGORY_CODE == '*':
                Incident_data = IncidentMaster.objects.filter(
                    status=1, Incident_BP_CODE=BPCODE)
            else:
                Incident_data = IncidentMaster.objects.filter(
                    status=1, Incident_BP_CODE=BPCODE, Incident_Cat=IncidentCategory)
        else:
            if CATEGORY_CODE == '*':
                Incident_data = IncidentMaster.objects.filter(
                    status=1, Incident_BP_CODE=BPCODE, Incident_Status=IncidentStatus)
            else:
                Incident_data = IncidentMaster.objects.filter(
                    status=1, Incident_BP_CODE=BPCODE, Incident_Status=IncidentStatus, Incident_Cat=IncidentCategory)

        if Incident_data:

            for incidata in Incident_data:
                # datetime_str = incidata['create_date']
                # old_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                # new_format = '%d-%m-%Y %H:%M:%S'
                # incidata['create_date'] = incidata['create_date']
                com = incidata.getallcomments()
                if com:
                    for comdata in com:
                        com_jj = {'Incident_Number': incidata.Incident_Number,
                                  'IncidentComment_Number': comdata.IncidentComment_Number,
                                  'IncidentComment_Text': comdata.IncidentComment_Text,
                                  'IncidentComment_By': comdata.IncidentComment_By,
                                  'IncidentComment_On': comdata.IncidentComment_On}
                        IncidentCommentList.append(com_jj)

                fed = incidata.getallfeedback()
                if fed:
                    for feddata in fed:
                        fed_jj = {'Incident_Number': incidata.Incident_Number,
                                  'IncidentFeedback_Number': feddata.IncidentFeedback_Number,
                                  'IncidentFeedback_Rating': feddata.IncidentFeedback_Rating,
                                  'IncidentFeedback_Text': feddata.IncidentFeedback_Text,
                                  'IncidentFeedback_By': feddata.IncidentFeedback_By,
                                  'IncidentFeedback_On': feddata.IncidentFeedback_On}
                        IncidentFeedbackList.append(fed_jj)

            indidata_new = serializers.serialize(
                'python', Incident_data, use_natural_foreign_keys=True, use_natural_primary_keys=True, cls=LazyEncoder)
            for incidata in indidata_new:
                incidata['fields']['create_date'] = incidata['fields']['create_date'].date()

            return JsonResponse({'data': {'Incidentlist': indidata_new, 'Comments': IncidentCommentList,
                                          'Feedback': IncidentFeedbackList}, 'reply': 'GetIncidentList'})
        else:
            if Status_CODE == "2":
                return JsonResponse({'data': None, 'reply': "No Open Incidents"})
            else:
                return JsonResponse({'data': None, 'reply': "No Clsed Incidents"})

    except IncidentMaster.DoesNotExist as ex:
        if Status_CODE == "2":
            return JsonResponse({'data': None, 'reply': "No Open Incidents"})
        else:
            return JsonResponse({'data': None, 'reply': "No Clsed Incidents"})

    except Exception as ex:
        return JsonResponse({'data': None, 'reply': str(ex)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetIncidentReportCATWISE(request, BPCODE, Status_CODE):
    Cat_Inci_List = []
    Cat_Inci_item = {'Incident_category_Code': '',
                     'Incident_category_Text': '', 'Total Incident': ''}

    try:
        IncidentStatus = None
        if Status_CODE != '*':
            try:

                IncidentStatus = IncidentStatusTypeMaster.objects.get(
                    pk=Status_CODE)

            except IncidentStatusTypeMaster.DoesNotExist as ex:
                return JsonResponse({'data': None, 'reply': "No Status Code Found"})

        if Status_CODE == '*':
            Incident_data = IncidentMaster.objects.filter(status=1, Incident_BP_CODE=BPCODE).values(
                'Incident_Cat').annotate(total=Count('Incident_Number')).order_by('Incident_Cat')
            # Incident_data = IncidentMaster.objects.annotate(total=Count('Incident_Number')).order_by('Incident_Cat')
        else:
            Incident_data = IncidentMaster.objects.filter(status=1, Incident_BP_CODE=BPCODE,
                                                          Incident_Status=IncidentStatus).values(
                'Incident_Cat').order_by('Incident_Cat').annotate(count=Count('Incident_Cat'))
            # Incident_data = IncidentMaster.objects.annotate(total=Count('Incident_Number')).order_by('Incident_Cat')

        if Incident_data:
            for inct in Incident_data:
                cat_code = inct['Incident_Cat']
                try:

                    IncidentCategory = IncidentCategoryMaster.objects.get(
                        pk=cat_code)
                    cat_text = IncidentCategory.IncidentCategory_Text

                except IncidentCategoryMaster.DoesNotExist as ex:
                    cat_text = ""

                Cat_Inci_item = {'BP_Code': BPCODE, 'Status_CODE': Status_CODE,
                                 'Status_Text': IncidentStatus.IncidentStatus_Text,
                                 'Incident_category_Code': inct['Incident_Cat'], 'Incident_category_Text': cat_text,
                                 'Total Incident': inct['count']}
                Cat_Inci_List.append(Cat_Inci_item)

            # Incident_data1 = json.dumps(list(Incident_data))
            return JsonResponse({'data': Cat_Inci_List, 'reply': 'GetIncidentReportCATWISE'})
        else:
            if Status_CODE == "2":
                return JsonResponse({'data': None, 'reply': "No Open Incidents"})
            else:
                return JsonResponse({'data': None, 'reply': "No Clsed Incidents"})
            # return JsonResponse({'data': None, 'reply': "No Incident Found"})
    except IncidentMaster.DoesNotExist as ex:
        if Status_CODE == "2":
            return JsonResponse({'data': None, 'reply': "No Open Incidents"})
        else:
            return JsonResponse({'data': None, 'reply': "No Clsed Incidents"})
        # return JsonResponse({'data': None, 'reply': "No Incident Found"})

    except Exception as ex:
        return JsonResponse({'data': None, 'reply': str(ex)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetIncidentReport(request, BPCODE, CATEGORY_CODE):
    try:
        IncidentStatus = None
        if CATEGORY_CODE != '*':
            try:

                IncidentStatus = IncidentStatusTypeMaster.objects.get(
                    pk=CATEGORY_CODE)

            except IncidentStatusTypeMaster.DoesNotExist as ex:
                return JsonResponse({'data': None, 'reply': "No Status Code Found"})

        if CATEGORY_CODE == '*':
            Incident_data = IncidentMaster.objects.filter(
                status=1, Incident_BP_CODE=BPCODE)
        else:
            Incident_data = IncidentMaster.objects.filter(
                status=1, Incident_BP_CODE=BPCODE, Incident_Status=IncidentStatus)

        if Incident_data:

            return JsonResponse({'data': serializers.serialize('python', Incident_data, use_natural_foreign_keys=True,
                                                               use_natural_primary_keys=True),
                                 'reply': 'GetIncidentReport'})
        else:
            return JsonResponse({'data': None, 'reply': "No Incident Found"})

    except IncidentMaster.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "No Incident Found"})

    except Exception as ex:
        return JsonResponse({'data': None, 'reply': str(ex)})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def CreateIncident(request):
    request_data = json.loads(request.body)
    try:
        data = {}
        if request.method == 'POST':
            # ul = user_log(request, request_data['Bp_code'], 'Payment',
            #               'Payment Status Saved: '+request_data['Payment_Status'])
            Incident_Cat_val = request_data['Incident_Cat_Code']
            try:
                Incident_Cat = IncidentCategoryMaster.objects.get(
                    pk=Incident_Cat_val)
            except IncidentCategoryMaster.DoesNotExist as e:
                Incident_Cat = IncidentCategoryMaster.objects.get(pk=10)

            Incident_Status_val = request_data['Incident_Status_Code']
            try:
                Incident_Status = IncidentStatusTypeMaster.objects.get(
                    pk=2)
            except IncidentStatusTypeMaster.DoesNotExist as e:
                Incident_Status = IncidentStatusTypeMaster.objects.get(pk=2)

            Incident_Text = request_data['Incident_Text']
            Incident_BP_CODE = request_data['Bp_code']
            Incident_Last_Comment = request_data['Incident_Text']
            Incident_Last_Comment_By = request_data['Bp_code']
            create_user = request_data['Bp_code']
            update_user = request_data['Bp_code']

            vk = get_agentVKORG(request, Incident_BP_CODE)
            vk = json.loads(vk.content)

            im = IncidentMaster()
            im.Incident_Cat = Incident_Cat
            im.Incident_Status = Incident_Status
            im.Incident_Text = Incident_Text
            im.Incident_BP_CODE = Incident_BP_CODE
            im.Incident_Last_Comment = Incident_Last_Comment
            im.Incident_Last_Comment_By = Incident_Last_Comment_By
            im.create_user = create_user
            im.update_user = update_user
            im.Incident_VKORG = vk['VKORG']
            im.Incident_STATE = vk['State']
            im.Incident_Last_assigned_to_code = vk['Partner']
            im.Incident_Last_assigned_to_Name = vk['Name']
            im.Incident_Last_assigned_to_Level = vk['Type']

            im.save()
            Incident_Number = im.Incident_Number

            ul = user_log(request, request_data['Bp_code'], 'Incident',
                          'Incident Create #: ' + str(Incident_Number))

            return JsonResponse({'reply': "Incident Create #: " + str(Incident_Number)})

    except Exception as e:
        return JsonResponse({"reply: ": "Incident Create Error: " + str(e)})


def GetIncidentStatusType(request):
    try:

        IncidentStatusType = IncidentStatusTypeMaster.objects.filter(
            IncidentStatus_Status=1)

        return JsonResponse(
            {'data': serializers.serialize('python', IncidentStatusType), 'reply': 'IncidentStatusType'})

    except IncidentStatusTypeMaster.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "No Data Found"})

    except Exception as ex:
        return JsonResponse({'data': None, 'reply': str(ex)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetIncidentCategory(request):
    try:

        IncidentCategory = IncidentCategoryMaster.objects.filter(
            IncidentCategory_Status=1)

        return JsonResponse({'data': serializers.serialize('python', IncidentCategory), 'reply': 'IncidentCategory'})

    except IncidentCategoryMaster.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "IncidentCategory"})

    except Exception as ex:
        return JsonResponse({'data': None, 'reply': str(ex)})


def GETSAP_AGChields_DATA(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_VERIFY_SRV/AGNconfSet?$format=json&$filter=(Parent eq '%s')" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetAGChield(request, BPCODE):
    try:

        Chielddata_f = GETSAP_AGChields_DATA(request, BPCODE)
        Chielddata = None
        if Chielddata_f[0]:
            Chielddata = Chielddata_f[1]
            # del dash['__metadata']
            for num in Chielddata['results']:
                del num['__metadata']
        return JsonResponse({'data': Chielddata, 'reply': 'GetAGChield'})

    except Exception as ex:
        return JsonResponse({'data': str(ex), 'reply': "GetAGChield"})


def GETSAP_DBUser_Outstanding_Count(request, BPCODE, GrpBy=None, Search_Key='*'):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_EXE_OUTST_SRV/OUTSTSet?$format=json&$filter=Adid eq '%s'" % (
                    res.server_host, BPCODE)
                if GrpBy:
                    sapurl = sapurl + " and Fltr  eq '%s' " % (GrpBy.upper())
                # if edi:
                #     if edi != "*":
                #         sapurl = sapurl + "  and Pva eq '%s' " % (edi)

                # if fromdt and todt:
                #     sapurl = sapurl + \
                #         "and (OrdDate ge datetime'%sT00:00:00' and OrdDate le datetime'%sT00:00:00')" % (
                #             fromdt, todt)

                if GrpBy == 'C':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                if GrpBy == 'A':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkorg eq '%s'" % (Search_Key.upper())

                # and AgType eq 'MA' and (OrdDate ge datetime'2019-12-01T00:00:00' and OrdDate le datetime'2020-03-01T00:00:00')
            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                # for num in results['results']:
                # OrdDate = re.split(
                #     '\(|\)', num['OrdDate'])[1][:10]
                # # num['OrdDate'] = datetime.datetime.fromtimestamp(
                # # int(OrdDate))
                # num['OrdDate'] = OrdDate
                # num['Partner'] = num['SoldToParty']

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def DBUser_Outstanding_Count_KEY(request, BPCODE, GrpBy, Search_Key=None):
    try:
        ul = user_log(request, BPCODE, 'Outstanding',
                      'Outstanding Open with Group and Key:' + GrpBy + " " + Search_Key)
        # if Search_Key == '*':
        dash_f = GETSAP_DBUser_Outstanding_Count(
            request, BPCODE, GrpBy, Search_Key)

        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']

                # for num1 in num['NavSubagentSet']['results']:
                #     del num1['__metadata']
                # for num2 in num['NavEdtnSet']['results']:
                #     del num2['__metadata']

        return JsonResponse({'data': dash, 'reply': 'DBUser_Outstanding_Count'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def GETSAP_DBUser_Billing_Count(request, BPCODE, GrpBy=None, fromdt=None, todt=None, Search_Key='*'):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_EXE_BILLING_SRV/BILLSet?$format=json&$filter=Adid eq '%s'" % (
                    res.server_host, BPCODE)
                if GrpBy:
                    sapurl = sapurl + " and Fltr  eq '%s' " % (GrpBy.upper())
                # if edi:
                #     if edi != "*":
                #         sapurl = sapurl + "  and Pva eq '%s' " % (edi)

                if fromdt and todt:
                    sapurl = sapurl + \
                             "and (OrdDate ge datetime'%sT00:00:00' and OrdDate le datetime'%sT00:00:00')" % (
                                 fromdt, todt)

                if GrpBy == 'C':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                if GrpBy == 'A':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkorg eq '%s'" % (Search_Key.upper())

                # and AgType eq 'MA' and (OrdDate ge datetime'2019-12-01T00:00:00' and OrdDate le datetime'2020-03-01T00:00:00')
            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                for num in results['results']:
                    OrdDate = re.split(
                        '\(|\)', num['OrdDate'])[1][:10]
                    # num['OrdDate'] = datetime.datetime.fromtimestamp(
                    # int(OrdDate))
                    num['OrdDate'] = OrdDate
                    # num['Partner'] = num['SoldToParty']

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def DBUser_Billing_Count_KEY(request, BPCODE, GrpBy, fromdt, todt, Search_Key=None):
    try:
        ul = user_log(request, BPCODE, 'Billing',
                      'Billing Open with Group and Key:' + GrpBy + " " + Search_Key)
        # if Search_Key == '*':
        dash_f = GETSAP_DBUser_Billing_Count(
            request, BPCODE, GrpBy, fromdt, todt, Search_Key)

        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']

                # for num1 in num['NavSubagentSet']['results']:
                #     del num1['__metadata']
                # for num2 in num['NavEdtnSet']['results']:
                #     del num2['__metadata']

        return JsonResponse({'data': dash, 'reply': 'DBUser_Billing_Count'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def SAP_Payment_POST(request, pots_body=None):
    try:

        sapuser = ''
        sappassword = ''
        sapurl = ''

        try:

            res = ServerMaster.objects.get(
                server_text='PAY', server_status='1')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"

                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AMT_POSTING_SRV/PAYSet" % (
                    res.server_host)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))
        headers = {"content-type": "application/json",
                   "X-Requested-With": "X", "Accept": "application/json"}
        auth_values = (sapuser, sappassword)
        body_json = request.session['post_body']
        response = requests.post(
            sapurl, auth=auth_values, data=json.dumps(body_json), headers=headers)
        flag = None
        fresult = None
        # if response.status_code == 201:
        appdata = (response.json())
        # else:
        # appdata = {'msg':response.json()}

        if len(appdata) >= 1:
            if response.status_code == 201:
                fresult = response.headers
                # else:
                # results = appdata['d']
                # if fresult == "Message Send: Successfully":
                flag = True
            else:
                flag = False
                fresult = appdata
            # if len(results) >0:
            #     fresult = results

            # else:
            #     pass

            if flag:

                return (flag, fresult)
            else:

                return (flag, fresult)

        else:

            return (flag, "No Response Get From SAP!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
def SAPFIPOST(request, PaymentLog_id):
    try:
        SAPPOST_status = 0
        SAP_Request = ''
        SAP_Response = ''
        post_body = {
            "Vkorg": "",
            "Kunnr": "",
            "Xblnr": "",
            "Dmshb": ""
        }
        try:
            paylog1 = PaymentLog.objects.get(pk=PaymentLog_id)
        except PaymentLog.DoesNotExist:
            paylog1 = None

        if paylog1.Payment_Status == 'Success':
            # Payment_Response_Json = json.dumps(paylog1.Payment_Response)
            TransactionID = PaymentLog_id
            post_body['Kunnr'] = paylog1.username
            post_body['Xblnr'] = TransactionID
            post_body['Dmshb'] = paylog1.Payment_Amount
            post_body['Vkorg'] = ''

            post_body['Kunnr'] = str(post_body['Kunnr'])
            post_body['Xblnr'] = str(post_body['Xblnr'])
            post_body['Dmshb'] = str(post_body['Dmshb'])

            request.session['post_body'] = post_body
            SAP_Request = post_body
            try:
                ss = SAP_Payment_POST(request, post_body)
                if ss[0]:
                    SAPPOST_status = 1
                    SAP_Response = ss[1]
                else:
                    SAPPOST_status = 0
                    SAP_Response = ss[1]
            except Exception as e:
                SAPPOST_status = 0
                SAP_Response = str(e)

            # try:
            # paylog = PaymentLog.objects.get(pk=PaymentLog_id)
            paylog1.SAPPOST_status = SAPPOST_status
            paylog1.SAP_Request = SAP_Request
            paylog1.SAP_Response = SAP_Response
            paylog1.save()
            # except PaymentLog.DoesNotExist:
            #     pass
            return JsonResponse({'reply': "Payment Status Saved TRUE: " + PaymentLog_id})

        else:
            return JsonResponse({'reply': "Payment Status Saved FALSE: " + PaymentLog_id})

    except Exception as ex:

        return JsonResponse({'reply': "Error:- " + str(ex)})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def Update_PaymentStatus(request):
    request_data = json.loads(request.body)
    try:
        data = {}
        if request.method == 'POST':
            ul = user_log(request, request_data['Bp_code'], 'Payment',
                          'Payment Status Saved: ' + request_data['Payment_Status'])
            post_body = {
                "Vkorg": "",
                "Kunnr": "",
                "Xblnr": "",
                "Dmshb": ""
            }
            # data = {'username': request_data['BpCode'],'Payment_Amount': request_data['Bp_code'], 'Password': request_data['Password'], 'device_id': request_data['device_id']}
            SAPPOST_status = 0
            SAP_Request = ''
            SAP_Response = ''
            PaymentLog_id = '0'

            uu = PaymentLog()
            uu.username = request_data['Bp_code']
            uu.Payment_Amount = request_data['Payment_Amount']
            uu.Payment_Request = request_data['Payment_Request']
            uu.Payment_Response = request_data['Payment_Response']
            uu.Payment_diviceID = request_data['Payment_diviceID']
            uu.Payment_Status = request_data['Payment_Status']
            uu.SAPPOST_status = SAPPOST_status
            uu.SAP_Request = SAP_Request
            uu.SAP_Response = SAP_Response
            uu.save()
            PaymentLog_id = uu.PaymentLog_id
            # try:
            #     paylog1 = PaymentLog.objects.get(pk=PaymentLog_id)
            # except PaymentLog.DoesNotExist:
            #     paylog1 = None

            ul = user_log(request, request_data['Bp_code'], 'Payment',
                          'paymentId Found from PAYUMoney: ' + str(PaymentLog_id))

            SAPFIPOST(request, PaymentLog_id)

            ul = user_log(request, request_data['Bp_code'], 'Payment', 'SAP POST Status ' + str(
                SAPPOST_status) + ' for paymentId: ' + str(PaymentLog_id))

            # if paylog1.Payment_Status == 'Success':
            #     #Payment_Response_Json = json.dumps(paylog1.Payment_Response)
            #     TransactionID = PaymentLog_id #Payment_Response_Json['result']['paymentId'] #request_data['Payment_Response']['result']['paymentId']
            #     ul = user_log(request, request_data['Bp_code'], 'Payment',
            #               'paymentId Found from PAYUMoney: '+TransactionID)
            #     # post_body['Kunnr'] = str(request_data['Bp_code'])
            #     # post_body['Xblnr'] = str(
            #     #     request_data['Payment_Response']['result']['paymentId'])
            #     # post_body['Dmshb'] = str(request_data['Payment_Amount'])
            #     # post_body['Vkorg'] = ''

            #     post_body['Kunnr'] = paylog1.username
            #     post_body['Xblnr'] = TransactionID
            #     post_body['Dmshb'] = paylog1.Payment_Amount
            #     post_body['Vkorg'] = ''

            #     post_body['Kunnr'] = str(post_body['Kunnr'])
            #     post_body['Xblnr'] = str(post_body['Xblnr'])
            #     post_body['Dmshb'] = str(post_body['Dmshb'])

            #     request.session['post_body'] = post_body
            #     SAP_Request = post_body
            #     try:
            #         ss = SAP_Payment_POST(request, post_body)
            #         if ss[0]:
            #             SAPPOST_status = 1
            #             SAP_Response = ss[1]
            #         else:
            #             SAPPOST_status = 0
            #             SAP_Response = ss[1]
            #     except Exception as e:
            #         SAPPOST_status = 0
            #         SAP_Response = str(e)

            #     try:
            #         paylog = PaymentLog.objects.get(pk=PaymentLog_id)
            #         paylog.SAPPOST_status = SAPPOST_status
            #         paylog.SAP_Request = SAP_Request
            #         paylog.SAP_Response = SAP_Response
            #         paylog.save()
            #     except PaymentLog.DoesNotExist:
            #         pass
            #     ul = user_log(request, request_data['Bp_code'], 'Payment',
            #               'SAP POST Status '+ SAPPOST_status +' for paymentId: '+TransactionID)

            return JsonResponse({'reply': "Payment Status Saved: " + request_data['Payment_Status']})

    except Exception as e:
        return JsonResponse({"reply: ": "Payment Status Saved: " + request_data['Payment_Status'] + " " + str(e)})


def mobileotp_FPWD(request, mbileno, bpcode):
    # if 'userdata' not in request.session:
    #     return HttpResponseRedirect(reverse(''))
    try:
        # mbileno = str(request.GET.get('mbileno', None))
        mbileno = "91" + mbileno
        optval = str(random.randint(1000, 9999))
        # smshost = None
        smsurl = ""
        try:
            smshost = SmsManager.objects.get(sms_for='signup', sms_status='1')
            request.session["mobileOTP"] = optval
            smsval = smshost.sms_body_first + " " + optval + " ." + \
                     smshost.sms_body_second + smshost.sms_body_third
            smsurl = "%s&to=%s&text=%s%s" % (
                smshost.sms_host, mbileno, smsval, smshost.sms_from)
        except ServerMaster.DoesNotExist as EX:
            data = {'data': None, 'reply': str(EX)}
            return JsonResponse(data)
        # return HttpResponse("<script>alert('hi')</script>")
        except Exception as ex:
            # return HttpResponse("<script>alert('hi')</script>")
            data = {'data': None, 'reply': str(EX)}
            return JsonResponse(data)
        response = requests.get(smsurl)
        smsresponse = response.json()
        smslogobj = SmsLog()
        smslogobj.sms_body = smsval
        smslogobj.sms_from_page = "SignUp Page"
        smslogobj.sms_response = smsresponse
        # smslogobj.sms_send_on
        smslogobj.sms_to = mbileno
        smslogobj.save()

        data = {
            'mobileotpsent': 'T',
            'mobileno': mbileno,
            'otp': optval,
            'Bp_code': bpcode,

        }
        return JsonResponse({'data': data, 'reply': ''})
    except Exception as ex:
        # return HttpResponse(str(ex))
        {'data': None, 'reply': str(EX)}
        return JsonResponse({'data': data})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def Update_PWD(request):
    request_data = json.loads(request.body)
    try:
        data = {}
        if request.method == 'POST':

            data = {'Verified': request_data['isOtpVerified'], 'BpCode': request_data['Bp_code'],
                    'Password': request_data['Password'], 'device_id': request_data['device_id']}
            if data['Verified'] == True:
                uu = UserMaster.objects.get(username=request_data['Bp_code'])
                if uu:
                    # uu.password = request_data['Password']
                    uu.set_password(request_data['Password'])
                    uu.save()
                    ul = user_log(
                        request, data['BpCode'], 'UpdatePWD', 'Update Password Done')
                    return JsonResponse({'reply': "Your Passowrd is Update Successfully."})
            else:
                return JsonResponse({'reply': "Please enter valid OTP"})
    except Exception as e:
        return JsonResponse({"reply: ": str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def User_Reg_Mob_Forgot(request, BPMOBILE_NO):
    try:
        ud = UserMasterDetails.objects.get(mobile_no=BPMOBILE_NO)
        uu = UserMaster.objects.get(username=ud.usermaster)
        if uu:
            sent_opt = mobileotp_FPWD(request, BPMOBILE_NO, uu.username)
            return HttpResponse(sent_opt)
        else:
            ul = user_log(request, BPMOBILE_NO, 'ForgotPwd',
                          'Mobile Number is not matched:' + BPMOBILE_NO)
            return JsonResponse({'data': None, 'reply': "Mobile Number is not matched."})

    except UserMaster.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "Mobile Number Not Found"})
    except UserMasterDetails.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "Mobile Number Not Found"})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_log(request, userid, logkey, log_action):
    try:

        ul = UserLogs()
        # userid request.session["userdata"]["Username"]
        ul.username = userid
        ul.log_key = logkey
        ul.log_action = log_action

        # try:
        #     ip = get_client_ip(request)
        # except Exception as ex:
        #     ip = " On Mobile/Tablet"

        # ul.log_ip = ip

        # try:
        #     ul.log_host = request.META['HTTP_HOST']
        # except Exception as ex:
        #     ul.log_host = " On Mobile/Tablet"

        # try:
        #     ul.platform = request.META['HTTP_USER_AGENT']
        # except Exception as ex:
        #     ul.platform = " On Mobile/Tablet"

        # try:
        #     ul.browser_type = request.META['PATH_INFO']
        # except Exception as ex:
        #     ul.browser_type = " On Mobile/Tablet"

        ul.save()
        return (True, 'Log Saved')
    except Exception as ex:
        ul = UserLogs()
        ul.userid = userid
        ul.log_key = logkey
        ul.log_action = "Error on: " + log_action + " " + str(ex)
        ul.save()
        return (False, str(ex))


def SAP_Profile_POST(request, pots_body=None):
    try:

        sapuser = ''
        sappassword = ''
        sapurl = ''

        try:

            res = ServerMaster.objects.get(
                server_text='PRD', server_status='1')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"

                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_PROFILE_UPD_SRV/PRFSet" % (
                    res.server_host)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))
        headers = {"content-type": "application/json",
                   "X-Requested-With": "X", "Accept": "application/json"}
        auth_values = (sapuser, sappassword)
        body_json = request.session['post_body']
        response = requests.post(
            sapurl, auth=auth_values, data=json.dumps(body_json), headers=headers)
        flag = None
        fresult = None
        # if response.status_code == 201:
        appdata = (response.json())
        # else:
        # appdata = {'msg':response.json()}

        if len(appdata) >= 1:
            if response.status_code == 201:
                fresult = appdata
                # else:
                # results = appdata['d']
                # if fresult == "Message Send: Successfully":
                flag = True
            else:
                flag = False

            # if len(results) >0:
            #     fresult = results

            # else:
            #     pass

            if flag:

                return (flag, fresult)
            else:

                return (flag, fresult)

        else:

            return (flag, "No Response Get From SAP!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def Profile_Update(request):
    request_data = json.loads(request.body)
    post_body = {
        "BpCode": "",
        "BpMob1": "",
        "BpGndr": "",
        "BpEmail": "",
        "MarrAnvi": None,
        "WorkingWithDb": None,
        "Dob": None,
        "MaritalStatus": "",
        "State": "",
        "City": "",
        "Pincode": "",
        "Unit": "",
        "Addr": "",
        "Religion": "",
        "NoChild": "",
        "PolicyNo": "",
        "Aadhar": "",
        "Pan": "",
        "SpName": "",
        "SpDob": None,
        "MotName": "",
        "MotDob": None,
        "FatName": "",
        "FatDob": None,
        "Bro1Name": "",
        "Bro1Dob": None,
        "Bro2Name": "",
        "Bro2Dob": None,
        "Sis1Name": "",
        "Sis1Dob": None,
        "Sis2Name": "",
        "Sis2Dob": None,
        "Kid1Name": "",
        "Kid1Dob": None,
        "Kid1Edu": "",
        "Kid1Gndr": "",
        "Kid2Name": "",
        "Kid2Dob": None,
        "Kid2Edu": "",
        "Kid2Gndr": "",
        "Kid3Name": "",
        "Kid3Dob": None,
        "Kid3Edu": "",
        "Kid3Gndr": "",
        "Kid4Name": "",
        "Kid4Dob": None,
        "Kid4Edu": "",
        "Kid4Gndr": "",
        "Kid5Name": "",
        "Kid5Dob": None,
        "Kid5Edu": "",
        "Kid5Gndr": "",
    }

    try:
        if request.method == 'POST':
            req_data = request_data  # request_data['data']

            req_usermaster = req_data['usermaster']
            req_userdetail = req_data['userdetail']
            req_usercrm = req_data['usercrm']['results'][0]

            if req_usercrm:
                post_body['BpCode'] = req_usercrm['BpCode']
                post_body['BpMob1'] = req_usercrm['Mobile1']
                # if req_usercrm['Gender'] == "Male"
                post_body['BpGndr'] = req_usercrm['Gender'][:1]
                post_body['BpEmail'] = req_usercrm['Email']
                if req_usercrm['MarrAnni'] != "":
                    post_body['MarrAnvi'] = "/Date(" + \
                                            req_usercrm['MarrAnni'] + ")/"

                if req_usercrm['WorkingWithDb'] != "":
                    post_body['WorkingWithDb'] = "/Date(" + \
                                                 req_usercrm['WorkingWithDb'] + ")/"

                if req_usercrm['Dob'] != "":
                    post_body['Dob'] = "/Date(" + req_usercrm['Dob'] + ")/"

                post_body['MaritalStatus'] = req_usercrm['MaritalStatus']
                post_body['State'] = req_usercrm['State']
                post_body['City'] = req_usercrm['City']
                post_body['Pincode'] = req_usercrm['Pincode']
                post_body['Unit'] = req_usercrm['Unit']
                post_body['Addr'] = req_usercrm['Addr']
                post_body['Religion'] = req_usercrm['Religion']
                post_body['NoChild'] = req_usercrm['NoChild']
                post_body['PolicyNo'] = req_usercrm['PolicyNo']
                post_body['Aadhar'] = req_usercrm['Aadhar']
                post_body['Pan'] = req_usercrm['Pan']

                post_body['SpName'] = req_usercrm['WIFESet'][0]['Name']
                if req_usercrm['WIFESet'][0]['Dob'] != "":
                    post_body['SpDob'] = "/Date(" + \
                                         req_usercrm['WIFESet'][0]['Dob'] + ")/"

                post_body['MotName'] = req_usercrm['MOTSet'][0]['Name']
                if req_usercrm['MOTSet'][0]['Dob'] != "":
                    post_body['MotDob'] = "/Date(" + \
                                          req_usercrm['MOTSet'][0]['Dob'] + ")/"

                post_body['FatName'] = ""
                post_body['FatDob'] = None

                post_body['Bro1Name'] = req_usercrm['BROSet'][0]['Name']
                if req_usercrm['BROSet'][0]['Dob'] != "":
                    post_body['Bro1Dob'] = "/Date(" + \
                                           req_usercrm['BROSet'][0]['Dob'] + ")/"

                post_body['Bro2Name'] = req_usercrm['BROSet'][1]['Name']
                if req_usercrm['BROSet'][1]['Dob'] != "":
                    post_body['Bro2Dob'] = "/Date(" + \
                                           req_usercrm['BROSet'][1]['Dob'] + ")/"

                post_body['Sis1Name'] = req_usercrm['SISSet'][1]['Name']
                if req_usercrm['SISSet'][1]['Dob'] != "":
                    post_body['Sis1Dob'] = "/Date(" + \
                                           req_usercrm['SISSet'][1]['Dob'] + ")/"

                post_body['Sis2Name'] = req_usercrm['SISSet'][1]['Name']
                if req_usercrm['SISSet'][1]['Dob'] != "":
                    post_body['Sis2Dob'] = "/Date(" + \
                                           req_usercrm['SISSet'][1]['Dob'] + ")/"

                if len(req_usercrm['KIDSet']) > 0:

                    post_body['Kid1Name'] = req_usercrm['KIDSet'][0]['Name']
                    if req_usercrm['KIDSet'][0]['Dob'] != "":
                        post_body['Kid1Dob'] = "/Date(" + \
                                               req_usercrm['KIDSet'][0]['Dob'] + ")/"
                    post_body['Kid1Edu'] = req_usercrm['KIDSet'][0]['Education']
                    post_body['Kid1Gndr'] = req_usercrm['KIDSet'][0]['Gender'][:1]
                if len(req_usercrm['KIDSet']) > 1:

                    post_body['Kid2Name'] = req_usercrm['KIDSet'][1]['Name']
                    if req_usercrm['KIDSet'][1]['Dob'] != "":
                        post_body['Kid2Dob'] = "/Date(" + \
                                               req_usercrm['KIDSet'][1]['Dob'] + ")/"
                    post_body['Kid2Edu'] = req_usercrm['KIDSet'][1]['Education']
                    post_body['Kid2Gndr'] = req_usercrm['KIDSet'][1]['Gender'][:1]

                if len(req_usercrm['KIDSet']) > 2:
                    post_body['Kid3Name'] = req_usercrm['KIDSet'][2]['Name']
                    if req_usercrm['KIDSet'][2]['Dob'] != "":
                        post_body['Kid3Dob'] = "/Date(" + \
                                               req_usercrm['KIDSet'][2]['Dob'] + ")/"
                    post_body['Kid3Edu'] = req_usercrm['KIDSet'][2]['Education']
                    post_body['Kid3Gndr'] = req_usercrm['KIDSet'][2]['Gender'][:1]

                if len(req_usercrm['KIDSet']) > 3:
                    post_body['Kid4Name'] = req_usercrm['KIDSet'][3]['Name']
                    if req_usercrm['KIDSet'][3]['Dob'] != "":
                        post_body['Kid4Dob'] = "/Date(" + \
                                               req_usercrm['KIDSet'][3]['Dob'] + ")/"
                    post_body['Kid4Edu'] = req_usercrm['KIDSet'][3]['Education']
                    post_body['Kid4Gndr'] = req_usercrm['KIDSet'][3]['Gender'][:1]
                if len(req_usercrm['KIDSet']) > 4:
                    post_body['Kid5Name'] = req_usercrm['KIDSet'][4]['Name']
                    if req_usercrm['KIDSet'][4]['Dob'] != "":
                        post_body['Kid5Dob'] = "/Date(" + \
                                               req_usercrm['KIDSet'][4]['Dob'] + ")/"
                    post_body['Kid5Edu'] = req_usercrm['KIDSet'][4]['Education']
                    post_body['Kid5Gndr'] = req_usercrm['KIDSet'][4]['Gender'][:1]

                request.session['post_body'] = post_body
                ss = SAP_Profile_POST(request, post_body)
                if ss[0]:
                    ul = user_log(
                        request, post_body['BpCode'], 'Profile', 'Profile update request sent')
                    return JsonResponse({'data': post_body, 'reply': 'Profile update request sent succesfully.'})
                else:
                    ul = user_log(
                        request, post_body['BpCode'], 'Profile', 'Profile update request with Error')
                    return JsonResponse({'data': post_body, 'reply': 'Error on Profile Update'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def GETSAP_USER_MOBILE_VARIFY(request, BPCODE, MOBILE_NO):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_AGENT_VRF_SRV/VRFSet?$format=json&$filter=(Partner eq '%s' and Mobile eq '%s')" % (
                    res.server_host, BPCODE, MOBILE_NO)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "Agent Code or Mobile Number is invalid")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Get_Hint(request, Lan='EN'):
    try:
        cu = Hint.objects.filter(Hint_Status=1, Hint_Leng=Lan)
        # ul = user_log(request,post_body['BpCode'],'Profile','Profile update request with Error')
        return JsonResponse({'data': serializers.serialize('python', cu), 'reply': 'Hint'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Ledger_data(request, BPCODE, fromdt, todt, trantype):
    try:

        Outstanding = ""
        AgencyName = ""
        try:
            userm = UserMaster.objects.get(username=BPCODE)
            if userm:
                AgencyName = userm.first_name
            else:
                AgencyName = ""
        except UserMaster.DoesNotExist as ex:
            AgencyName = ""

        if not trantype:
            trantype = '*'

        dash_f = GETSAP_Ledger(request, BPCODE, fromdt, todt, trantype)
        dash = None
        if dash_f[0]:
            dash = dash_f[1]
        # del dash['__metadata']
        # for num in dash['results']:
        #     del num['__metadata']

        # Outstanding = get_outstanding(BPCODE)
        ul = user_log(request, BPCODE, 'Ledger',
                      'Show Ledger Data for Start Date: ' + fromdt + ' End Date:' + todt)
        return JsonResponse({'data': dash, 'AgencyName': AgencyName, 'reply': 'Ledger Data'})

    except Exception as e:
        ul = user_log(request, BPCODE, 'Ledger',
                      'Show Ledger Data for Start Date: ' + fromdt + ' End Date:' + todt)
        return JsonResponse({'data': None, 'AgencyName': AgencyName, 'reply': str(e)})


def GETSAP_Ledger(request, BPCODE, fromdt=None, todt=None, trantype=None):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_LEDGER_SRV/HeaderSet?$filter=Kunnr eq '%s'" % (
                    res.server_host, BPCODE)
                # if AgType:
                #     sapurl = sapurl + " and AgType eq '%s' " % (AgType)
                if trantype:
                    if trantype != "*":
                        sapurl = sapurl + "  and Blart eq '%s' " % (trantype)

                if fromdt and todt:
                    sapurl = sapurl + " and (Budat ge datetime'%sT00:00:00' and Budat le datetime'%sT00:00:00')" % (
                        fromdt, todt)

                sapurl = sapurl + "&$expand=TRNSet&$format=json"

                # and AgType eq 'MA' and (OrdDate ge datetime'2019-12-01T00:00:00' and OrdDate le datetime'2020-03-01T00:00:00')
            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                for num in results['results']:
                    del num['__metadata']
                    Budat = re.split(
                        '\(|\)', num['Budat'])[1][:10]
                    # num['OrdDate'] = datetime.datetime.fromtimestamp(
                    # int(OrdDate))
                    num['Budat'] = Budat
                    for num1 in num['TRNSet']['results']:
                        del num1['__metadata']
                        Budat1 = re.split(
                            '\(|\)', num1['Budat'])[1][:10]
                        # num['OrdDate'] = datetime.datetime.fromtimestamp(
                        # int(OrdDate))
                        num1['Budat'] = Budat1
                        if num1['Blart'] == 'DZ':
                            num1['Blart'] = 'Collection'
                        if num1['Blart'] == 'RW':
                            num1['Blart'] = 'Invoice'
                        if num1['Blart'] == 'RX':
                            num1['Blart'] = 'CreditNote'
                        if num1['Blart'] == 'IC':
                            num1['Blart'] = 'Adjustment'

                    num['TRNSet'] = num['TRNSet']['results']

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


def get_outstanding(BPCODE):
    try:
        dash = None

        try:
            userm = UserMaster.objects.get(username=BPCODE)
        except UserMaster.DoesNotExist as ex:
            userm = None
        if userm:
            # user_type = UserTypeMaster.objects.get(
            #     user_type='EU')
            try:
                ud = UserMasterDetails.objects.get(usermaster=userm)
            except UserMaster.DoesNotExist as ex:
                ud = None

            if ud:
                if ud.user_type.user_type == "EU":
                    dash_f = GETSAP_Dashboard(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]
                        del dash['__metadata']

                else:
                    dash_f = GETSAP_Dashboard_DBUser(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]
                        del dash['__metadata']
                        dash_new = {"Partner": BPCODE,
                                    "GrossCopy": dash['PaidCopy'],
                                    "FreeCopy": "",
                                    "PaidCopy": dash['PaidCopy'],
                                    "Zlao": "",
                                    "Zcoo": "",
                                    "OutStd": "",
                                    "Asd": ""}
                        dash = dash_new

            else:
                dash_f = GETSAP_Dashboard(request, BPCODE)
                if dash_f[0]:
                    dash = dash_f[1]
                    del dash['__metadata']

        else:
            dash_f = GETSAP_Dashboard(request, BPCODE)
            if dash_f[0]:
                dash = dash_f[1]
                del dash['__metadata']

        return dash['OutStd']

    except Exception as e:
        return str(e)


def Last_Six_Month_Bill(request, BPCODE):
    dash = None
    todate = datetime.today()
    frmdate = todate + relativedelta(months=-6)
    try:
        dash = None
        cur = todate
        cur_1 = todate + relativedelta(months=-1)
        cur_2 = todate + relativedelta(months=-2)
        cur_3 = todate + relativedelta(months=-3)
        cur_4 = todate + relativedelta(months=-4)
        cur_5 = todate + relativedelta(months=-5)
        cur_6 = todate + relativedelta(months=-6)

        cur_1_month = str(cur_1.month)
        cur_2_month = str(cur_2.month)
        cur_3_month = str(cur_3.month)
        cur_4_month = str(cur_4.month)
        cur_5_month = str(cur_5.month)
        cur_6_month = str(cur_6.month)

        if cur_1.month < 9:
            cur_1_month = "0" + cur_1_month

        if cur_2.month < 9:
            cur_2_month = "0" + cur_2_month
        if cur_3.month < 9:
            cur_3_month = "0" + cur_3_month
        if cur_4.month < 9:
            cur_4_month = "0" + cur_4_month
        if cur_5.month < 9:
            cur_5_month = "0" + cur_5_month
        if cur_6.month < 9:
            cur_6_month = "0" + cur_6_month
        # todate = str(todate.year) + "-" + str(todate.month) + "-" + str(todate.day)
        # frmdate = str(frmdate.year) + "-" + str(frmdate.month) + "-" + str(frmdate.day)

        usercrm_f = GETSAP_Bill_Month(request, BPCODE)
        usercrm = None
        if usercrm_f[0]:
            dash = usercrm_f[1]['results']

            dash.pop(0)
            dash.pop(0)
            dash.pop(0)
            dash.pop(0)
            dash.pop(0)
            dash.pop(0)
            dash.pop(0)
            dash.pop(0)

            for num in dash:

                if num['Gjahr'] == "0000":
                    num['Gjahr'] = "2020"

                mr = monthrange(int(num['Gjahr']), int(num['Monat']))

                # num['BillNo'] = mr

                if num['SoldCopies'] == "":
                    num['SoldCopies'] = 0

                num['SoldCopies'] = int(int(num['SoldCopies']) / int(mr[1]))

            #     # del num['__metadata']
            #     if num['Monat'] == cur_1_month and num['Gjahr'] == cur_1.year :
            #         pass
            #     elif num['Monat'] == cur_2_month and num['Gjahr'] == cur_2.year :
            #         pass
            #     elif num['Monat'] == cur_3_month and num['Gjahr'] == cur_3.year :
            #         pass
            #     elif num['Monat'] == cur_4_month and num['Gjahr'] == cur_4.year :
            #         pass
            #     elif num['Monat'] == cur_5_month and num['Gjahr'] == cur_5.year :
            #         pass
            #     elif num['Monat'] == cur_6_month and num['Gjahr'] == cur_6.year :
            #         pass
            #     else:
            #         dash.remove(num)

            # ,'pe':[cur_1_month + str(cur_1.year),cur_2_month + str(cur_2.year),cur_3_month + str(cur_3.year),cur_4_month + str(cur_4.year),cur_5_month + str(cur_5.year),cur_6_month + str(cur_6.year) ]
        return JsonResponse({'MTDdata': dash, 'todate': todate, 'frmdate': frmdate, 'reply': 'Last_Seven_Days_Copy'})
    except Exception as e:
        return JsonResponse({'MTDdata': dash, 'todate': todate, 'frmdate': frmdate, 'reply': str(e)})


# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
def Last_Seven_Days_Copy(request, BPCODE):
    dash = None
    todate = datetime.today()
    frmdate = todate + timedelta(days=-6)
    try:

        dash = None
        todate = datetime.today()
        frmdate = todate + timedelta(days=-6)
        todate = str(todate.year) + "-" + \
                 str(todate.month) + "-" + str(todate.day)
        frmdate = str(frmdate.year) + "-" + \
                  str(frmdate.month) + "-" + str(frmdate.day)

        # datetime.datetime(todate.year, todate.month, todate.day-6)
        dash_f = GETSAP_NoOfCopies(request, BPCODE, 'MA', frmdate, todate, "*")

        if dash_f[0]:
            dash = dash_f[1]['results']
            # del dash['__metadata']
            for num in dash:
                del num['__metadata']

        return JsonResponse({'YTDdata': dash, 'todate': todate, 'frmdate': frmdate, 'reply': 'Last_Seven_Days_Copy'})
    except Exception as e:
        return JsonResponse({'YTDdata': dash, 'todate': todate, 'frmdate': frmdate, 'reply': str(e)})


def Last_Bill_Month(request, BPCODE):
    try:

        today = datetime.today()
        # datem = datetime.datetime(today.year, today.month-1, 1)
        lastmonth = today.month - 1
        lastmonth_str = str(lastmonth)
        curyear = today.year
        if lastmonth < 9:
            lastmonth_str = "0" + lastmonth_str
        lastmonth_year = lastmonth_str + "-" + str(curyear)
        lastmonth_year_Bill_Amt = ""

        usercrm_f = GETSAP_Bill_Month(request, BPCODE)
        usercrm = None
        if usercrm_f[0]:
            usercrm = usercrm_f[1]
            for num in usercrm['results']:
                if num['Monat'] == lastmonth_str and num['Gjahr'] == str(curyear):
                    lastmonth_year_Bill_Amt = str(num['NetBilling'])

        return JsonResponse({'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt,
                             'reply': 'Last_Bill_Month'})

    except Exception as e:
        return JsonResponse(
            {'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt, 'reply': str(e)})


# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
def GETBillPDF(request, Billno):
    try:
        # usernameval = userid  #request.POST['username']
        sapuser = ''
        sappassword = ''
        sapurl = ''
        try:
            # complexQuery = ServerMaster(server_text='PRD') & ServerMaster(server_status='1')

            # res = ServerMaster.objects.filter(complexQuery)
            res = ServerMaster.objects.get(
                server_text='PRD', server_status='1')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"

                # sapurl = "http://%s/sap/opu/odata/SAP/ZJO_ADVT_PORTAL_BILL_STATEMENT_SRV/BILL_STATSet?$format=json&$filter=AgCode eq '%s' and Vkorg eq '%s'" %(res.server_host,Partner,Vkorg)
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_INVOICE_FILE_SRV/INVSet(Vbeln='%s')/$value" % (
                    res.server_host, Billno)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)

        # appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:

            fresult = response

            flag = True
            return HttpResponse(fresult, content_type='application/pdf')

        else:
            return HttpResponse("Error While downlod E-Invoice")
            # return (flag,"User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        return HttpResponse("Runtime Error: " + str(ex))
        # return (False,"Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Get_ContactUs(request):
    try:
        cu = ContactUs.objects.filter(ContactUs_Status=1)

        return JsonResponse({'data': serializers.serialize('python', cu), 'reply': 'ContactUs'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def GETSAP_Bill_Month(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_BILL_STAT_SRV/BILL_STATSet?$format=json&$filter=(SoldToPty eq '%s')&$format=json" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                for num in results['results']:
                    del num['__metadata']
                    if num['Fkdat']:
                        WorkingWithDb = re.split(
                            '\(|\)', num['Fkdat'])[1][:10]
                        num['Fkdat'] = WorkingWithDb
                        # num['WorkingWithDb'] = datetime.datetime.fromtimestamp(
                        #     int(WorkingWithDb))

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def Bill_Month(request, BPCODE):
    try:
        Outstanding = ""
        usercrm_f = GETSAP_Bill_Month(request, BPCODE)
        usercrm = None
        if usercrm_f[0]:
            usercrm = usercrm_f[1]

        Outstanding = get_outstanding(BPCODE)
        ul = user_log(request, BPCODE, 'Bill_Month',
                      'Show Bill Monthly Report')
        return JsonResponse(
            {'data': usercrm, 'Outstanding': Outstanding, 'reply': 'Bill Monthly Report', 'PayUMoney': False,
             'BankList': True})

    except Exception as e:
        ul = user_log(request, BPCODE, 'Bill_Month',
                      'Show Bill Monthly Report with Error')
        return JsonResponse(
            {'data': None, 'Outstanding': Outstanding, 'reply': str(e), 'PayUMoney': False, 'BankList': True})


def GETSAP_BP_CRM(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                # sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_CRM_SRV/HeaderSet?$filter=(BpCode eq '%s')&$expand=NavItemSet&$format=json" % (
                #     res.server_host, BPCODE)

                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_PROFILE_SRV/HeaderSet?$filter=(BpCode eq '%s')&$expand=BROSet,KIDSet,MOTSet,SISSet,WIFESet,FATSet&$format=json" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                for num in results['results']:
                    del num['__metadata']
                    # if num['WorkingWithDb']:
                    #     WorkingWithDb = re.split(
                    #         '\(|\)', num['WorkingWithDb'])[1][:10]
                    #     num['WorkingWithDb'] = WorkingWithDb
                    #     # num['WorkingWithDb'] = datetime.datetime.fromtimestamp(
                    #     #     int(WorkingWithDb))

                    # for num1 in num['NavItemSet']['results']:
                    #     del num1['__metadata']
                    #     if num1['EventDate']:
                    #         EventDate = re.split(
                    #             '\(|\)', num1['EventDate'])[1][:10]
                    #         num1['EventDate'] = EventDate
                    #         # num1['EventDate'] = datetime.datetime.fromtimestamp(
                    #         #     int(EventDate))
                    #     else:
                    #         num1['EventDate'] = ""

                    WorkingWithDb = re.split(
                        '\(|\)', num['WorkingWithDb'])[1][:10]
                    num['WorkingWithDb'] = WorkingWithDb

                    Dob = re.split(
                        '\(|\)', num['Dob'])[1][:10]
                    num['Dob'] = Dob

                    MarrAnni = re.split(
                        '\(|\)', num['MarrAnni'])[1][:10]
                    num['MarrAnni'] = MarrAnni

                    for num1 in num['MOTSet']['results']:
                        del num1['__metadata']
                        if num1['Dob']:
                            Dob = re.split(
                                '\(|\)', num1['Dob'])[1][:10]
                            num1['Dob'] = Dob
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['Dob'] = ""
                        if num1['MarrAnni']:
                            MarrAnni = re.split(
                                '\(|\)', num1['MarrAnni'])[1][:10]
                            num1['MarrAnni'] = MarrAnni
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['MarrAnni'] = ""

                    num['MOTSet'] = num['MOTSet']['results']

                    for num1 in num['BROSet']['results']:
                        del num1['__metadata']
                        if num1['Dob']:
                            Dob = re.split(
                                '\(|\)', num1['Dob'])[1][:10]
                            num1['Dob'] = Dob
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['Dob'] = ""
                        if num1['MarrAnni']:
                            MarrAnni = re.split(
                                '\(|\)', num1['MarrAnni'])[1][:10]
                            num1['MarrAnni'] = MarrAnni
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['MarrAnni'] = ""

                    num['BROSet'] = num['BROSet']['results']

                    for num1 in num['SISSet']['results']:
                        del num1['__metadata']
                        if num1['Dob']:
                            Dob = re.split(
                                '\(|\)', num1['Dob'])[1][:10]
                            num1['Dob'] = Dob
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['Dob'] = ""
                        if num1['MarrAnni']:
                            MarrAnni = re.split(
                                '\(|\)', num1['MarrAnni'])[1][:10]
                            num1['MarrAnni'] = MarrAnni
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['MarrAnni'] = ""

                    num['SISSet'] = num['SISSet']['results']

                    for num1 in num['WIFESet']['results']:
                        del num1['__metadata']
                        if num1['Dob']:
                            Dob = re.split(
                                '\(|\)', num1['Dob'])[1][:10]
                            num1['Dob'] = Dob
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['Dob'] = ""
                        if num1['MarrAnni']:
                            MarrAnni = re.split(
                                '\(|\)', num1['MarrAnni'])[1][:10]
                            num1['MarrAnni'] = MarrAnni
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['MarrAnni'] = ""

                    num['WIFESet'] = num['WIFESet']['results']

                    for num1 in num['KIDSet']['results']:
                        del num1['__metadata']
                        if num1['Dob']:
                            Dob = re.split(
                                '\(|\)', num1['Dob'])[1][:10]
                            num1['Dob'] = Dob
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['Dob'] = ""
                        if num1['MarrAnni']:
                            MarrAnni = re.split(
                                '\(|\)', num1['MarrAnni'])[1][:10]
                            num1['MarrAnni'] = MarrAnni
                            # num1['EventDate'] = datetime.datetime.fromtimestamp(
                            #     int(EventDate))
                        else:
                            num1['MarrAnni'] = ""

                    num['KIDSet'] = num['KIDSet']['results']

                    num['FATSet'] = num['FATSet']['results']

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def User_Profile(request, BPCODE):
    try:
        userm = UserMaster.objects.filter(username=BPCODE)
        usermqq = UserMaster.objects.get(username=BPCODE)
        # EducationMaster.objects.filter(status='1')
        EducationList = ['Primary', 'Secondary',
                         'Sr. Secondary', 'Graduation', 'Post Graduation']
        userdetail = UserMasterDetails.objects.filter(usermaster=usermqq)
        usercrm_f = GETSAP_BP_CRM(request, BPCODE)
        usercrm = None
        if usercrm_f[0]:
            usercrm = usercrm_f[1]
        ul = user_log(request, BPCODE, 'Profile', 'Show User Profile')
        return JsonResponse({'data': {'usermaster': serializers.serialize('python', userm),
                                      'userdetail': serializers.serialize('python', userdetail), 'usercrm': usercrm,
                                      'EducationList': EducationList}, 'isedit': True, 'reply': 'User Profile'})

    except Exception as e:
        ul = user_log(request, BPCODE, 'Profile',
                      'Show User Profile with Error')
        return JsonResponse({'data': None, 'isedit': True, 'reply': str(e)})


def getSAPUserDetail(request, server_text_val):
    ss = ServerMaster.objects.get(server_text=server_text_val, server_status=1)
    return ss


def WebAPI_Get_SAP_PATH(request, client):
    try:
        ss = getSAPUserDetail(request, client)
        data = {'data': {
            'server_text': ss.server_text,
            'server_host': ss.server_host,
            'server_username': ss.server_username,
            'server_password': ss.server_password,
            'screenshot': False
        }}
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


def GETSAP_REG_DATA(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_VERIFY_SRV/AGNconfSet?$format=json&$filter=(Partner eq '%s')" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


def mobileotp(request, mbileno):
    # if 'userdata' not in request.session:
    #     return HttpResponseRedirect(reverse(''))
    try:
        # mbileno = str(request.GET.get('mbileno', None))
        mbileno = "91" + mbileno
        optval = str(random.randint(1000, 9999))
        # smshost = None
        smsurl = ""
        try:
            smshost = SmsManager.objects.get(sms_for='signup', sms_status='1')
            request.session["mobileOTP"] = optval
            smsval = smshost.sms_body_first + " " + optval + " ." + \
                     smshost.sms_body_second + smshost.sms_body_third
            smsurl = "%s&to=%s&text=%s%s" % (
                smshost.sms_host, mbileno, smsval, smshost.sms_from)
        except ServerMaster.DoesNotExist as EX:
            data = {'data': None, 'reply': str(EX)}
            return JsonResponse(data)
        # return HttpResponse("<script>alert('hi')</script>")
        except Exception as ex:
            # return HttpResponse("<script>alert('hi')</script>")
            data = {'data': None, 'reply': str(EX)}
            return JsonResponse(data)
        response = requests.get(smsurl)
        smsresponse = response.json()
        smslogobj = SmsLog()
        smslogobj.sms_body = smsval
        smslogobj.sms_from_page = "SignUp Page"
        smslogobj.sms_response = smsresponse
        # smslogobj.sms_send_on
        smslogobj.sms_to = mbileno
        smslogobj.save()

        data = {
            'mobileotpsent': 'T',
            'mobileno': mbileno,
            'otp': optval,

        }
        return JsonResponse({'data': data, 'reply': ''})
    except Exception as ex:
        # return HttpResponse(str(ex))
        {'data': None, 'reply': str(EX)}
        return JsonResponse({'data': data})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def User_Reg_Mob(request, BPCODE, BPMOBILE_NO):
    uu = UserMaster.objects.filter(
        username=BPCODE).count()
    if uu > 0:
        return JsonResponse({'data': None, 'reply': "user already exist"})
    else:
        Usr_reg_sap = GETSAP_REG_DATA(request, BPCODE)

        # sent_otp = mobileotp(request,Usr_reg_sap.Mobile)
        if Usr_reg_sap[0]:

            rr = Usr_reg_sap[1]
            if rr['results'][0]['ReqsentFlag'] == 'X':

                if rr['results'][0]['Mobile'] == BPMOBILE_NO:
                    sent_opt = mobileotp(request, rr['results'][0]['Mobile'])
                    return HttpResponse(sent_opt)
                else:
                    ul = user_log(request, BPCODE, 'SignUp',
                                  'Mobile Number is not matched:' + BPMOBILE_NO)
                    return JsonResponse({'data': None, 'reply': "Mobile Number is not matched."})
            else:
                ul = user_log(request, BPCODE, 'SignUp',
                              'You are not authorized to use this application:' + BPMOBILE_NO)
                return JsonResponse({'data': None, 'reply': "!! You are not authorized to use this application !!"})

        else:
            user_veri = GETSAP_USER_MOBILE_VARIFY(request, BPCODE, BPMOBILE_NO)
            if user_veri[0]:
                rr1 = user_veri[1]
                sent_opt = mobileotp(request, BPMOBILE_NO)
                ul = user_log(request, BPCODE, 'SignUp',
                              'OPT Sent to:' + BPMOBILE_NO)
                return HttpResponse(sent_opt)
            else:
                ul = user_log(request, BPCODE, 'SignUp',
                              str(user_veri[1]) + BPMOBILE_NO)
                return JsonResponse({'data': None, 'reply': user_veri[1]})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def User_Reg(request, BPCODE):
    uu = UserMaster.objects.filter(
        username=BPCODE).count()
    if uu > 0:
        return JsonResponse({'data': None, 'reply': "user already exist"})
    else:
        Usr_reg_sap = GETSAP_REG_DATA(request, BPCODE)

        # sent_otp = mobileotp(request,Usr_reg_sap.Mobile)
        if Usr_reg_sap[0]:

            rr = Usr_reg_sap[1]
            if rr['results'][0]['ReqsentFlag'] == 'X':

                sent_opt = mobileotp(request, rr['results'][0]['Mobile'])
                ul = user_log(request, BPCODE, 'SignUp',
                              'OPT Sent to:' + rr['results'][0]['Mobile'])
                return HttpResponse(sent_opt)
            else:
                return JsonResponse({'data': None, 'reply': "!! You are not authorized to use this application !!"})

        else:
            return JsonResponse({'data': None, 'reply': "!! You are not authorized to use this application !!"})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def Verify_OTP(request):
    request_data = json.loads(request.body)
    try:
        data = {}
        print(request)
        if request.method == 'POST':
            data = {'Verified': request_data['isOtpVerified'],
                    'BpCode': request_data['Bp_code'], 'Password': request_data['Password'],
                    'device_id': request_data['device_id']}
        if data['Verified'] == True:
            # is_bp = 0
            # is_adalias = 0
            # res = getSAPUserDetail(request, 'PRD')
            # if res:
            #     sapuser = res.server_username  # "DBITMGT"
            #     sappassword = res.server_password  # "Dbitmgt1$"
            #     sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_VERIFY_SRV/AGNconfSet?$format=json&$filter=(Partner eq '%s')" % (
            #         res.server_host, data['BpCode'])
            #     auth_values = (sapuser, sappassword)
            #     response = requests.get(sapurl, auth=auth_values)
            #     appdata = response.json()

            #     if response.status_code == 200:
            #         results = appdata['d']
            #         if len(results) > 0:
            #             fresult = results['results'][0]
            #             mobile_no = fresult["Mobile"]
            #             email = fresult['Email'] if fresult['Email'] else fresult['Partner'] + "@gmail.com"
            #             type = fresult['Type']
            #             partner = fresult['Partner']
            #             request_sent_flag = fresult['ReqsentFlag']
            #             first_name = fresult['Name1']
            #             last_name = fresult['Name2']
            #             active_flag = fresult['ActiveFlag']
            #             device_id = fresult['Deviceid']
            #             device_type = ''

            Usr_reg_sap = GETSAP_REG_DATA(request, data['BpCode'])
            ul = user_log(request, data['BpCode'],
                          'SignUp', 'User Activation Done')
            # sent_otp = mobileotp(request,Usr_reg_sap.Mobile)
            if Usr_reg_sap[0]:

                fresult = Usr_reg_sap[1]["results"][0]
                mobile_no = fresult["Mobile"]
                # fresult['Email'] if fresult['Email'] else
                email = fresult['Partner'] + "@gmail.com"
                utype = fresult['Type']
                partner = fresult['Partner']
                request_sent_flag = fresult['ReqsentFlag']
                first_name = fresult['Name1']
                last_name = fresult['Name2']
                active_flag = fresult['ActiveFlag']
                device_id = data['device_id']  # fresult['Deviceid']
                device_type = ''

                if utype != '' and utype != None:
                    access_type = AccessTypeMaster.objects.filter(
                        access_type=utype).first()
                else:
                    access_type = AccessTypeMaster.objects.filter(
                        access_type='AG').first()
                if utype == 'AG':
                    user_type = UserTypeMaster.objects.filter(
                        user_type='EU').first()
                else:
                    user_type = UserTypeMaster.objects.filter(
                        user_type='DB').first()

                uu = UserMaster.objects.filter(
                    username=partner).count()
                if uu > 0:
                    return JsonResponse({'reply': "user already exist"})
                else:
                    rs = SAPPOSTROCHAT(request, partner, device_id, 'X')
                    dct = {
                        "UserMasterDetails": {
                            '_access_type': access_type,
                            '_user_type': user_type,
                            '_mobile': mobile_no,
                        }
                    }
                    res = UserMaster.objects.create_user(first_name=first_name, last_name=last_name,
                                                         email=email,
                                                         username=partner, password=request_data['Password'], **dct)

                    ul = user_log(request, partner, 'SignUp',
                                  'User Creation Done')
                    if isinstance(res, dict):
                        if res.get('error'):
                            return JsonResponse({"ERROR: ": res.get('error', "Can't create user profile")})
                    reg_log_details = RegLog(PARTNER=partner, adalias=partner,
                                             mobile_no=mobile_no,
                                             reg_device_id=device_id, platform=device_type)
                    reg_log_details.save()
                    create_log({'username': partner, 'log_action': '', 'log_host': '',
                                'log-ip': '', 'browser_type': '', 'platform': device_type})

            return JsonResponse({'reply': "Your Account activation request submit succesfuly, Thanks.!"})
        else:
            return JsonResponse({'reply': "Please enter valid OTP"})
    except Exception as e:
        return JsonResponse({"reply: ": str(e)})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def user_login(request):
    request_data = json.loads(request.body)
    loginflag = True
    try:
        if request.method == 'POST':
            DeviceTokenId = ""
            Bp_code = request_data['Bp_code']
            Password = request_data['Password']
            device_id = request_data['device_id']
            if "DeviceTokenId" in request_data:
                DeviceTokenId = request_data['DeviceTokenId']

            UserSAPStatus = ''
            user = authenticate(username=Bp_code, password=Password)
            if user is not None:

                userm = UserMaster.objects.filter(username=Bp_code)
                userm_ll = UserMaster.objects.get(username=Bp_code)
                usermqq = UserMaster.objects.get(username=Bp_code)
                userdetail = UserMasterDetails.objects.filter(
                    usermaster=usermqq)

                if str(userdetail[0].user_type) == 'DB User':
                    RL = RegLog.objects.filter(PARTNER=Bp_code, reg_device_id=device_id).count()
                    if RL == 0:
                        ul = user_log(request, Bp_code, 'Login', 'another device:' + str(device_id))
                        return JsonResponse({'data': None,
                                             'reply': 'Your activation was done on another device, Please use the same device to access this application',
                                             'showprofile': False})

                if DeviceTokenId is not "":
                    TU = TockenUser.objects.filter(usermaster=usermqq, device_id=device_id).update(
                        Tocken_code=DeviceTokenId)
                    if TU:

                        # TU = TockenUser()
                        # TU.usermaster = usermqq
                        # TU.Tocken_code = DeviceTokenId
                        # TU.device_id = device_id
                        # TU.save()
                        TU = None
                    else:
                        TU1 = TockenUser()
                        TU1.usermaster = usermqq
                        TU1.Tocken_code = DeviceTokenId
                        TU1.device_id = device_id
                        TU1.save()

                Usr_reg_sap = GETSAP_REG_DATA(request, Bp_code)
                if Usr_reg_sap[0]:
                    UserSAPStatus = Usr_reg_sap[1]

                ul = user_log(request, Bp_code, 'Login', 'Login Done')

                return JsonResponse({'data': {'usermaster': serializers.serialize('python', userm),
                                              'userdetail': serializers.serialize('python', userdetail),
                                              'UserSAPStatus': UserSAPStatus},
                                     'reply': 'Login Successful ' + str(userdetail[0].user_type), 'showprofile': True})

            else:
                return JsonResponse({'data': None, 'reply': 'User  ID or Password is Not Correct', 'showprofile': True})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e), 'showprofile': False})


# @check_session
def SAPPOSTROCHAT(request, Partner=None, Deviceid=None, ActiveFlag=None):
    try:

        sapuser = ''
        sappassword = ''
        sapurl = ''

        try:

            res = ServerMaster.objects.get(
                server_text='PRD', server_status='1')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"

                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_REGISTRATION_SRV/AGN_REGSet" % (
                    res.server_host)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))
        headers = {"content-type": "application/json",
                   "X-Requested-With": "X", "Accept": "application/json"}
        auth_values = (sapuser, sappassword)
        body_json = {
            "Partner": Partner,
            "ActiveFlag": ActiveFlag,
            "Deviceid": Deviceid
        }
        response = requests.post(
            sapurl, auth=auth_values, data=json.dumps(body_json), headers=headers)
        flag = None
        fresult = None
        # if response.status_code == 201:
        appdata = (response.json())['error']['message']
        # else:
        # appdata = {'msg':response.json()}

        if len(appdata) >= 1:
            if response.status_code == "201":
                fresult = appdata['value']
                # else:
                # results = appdata['d']
                # if fresult == "Message Send: Successfully":
                flag = True
            else:
                flag = False

            # if len(results) >0:
            #     fresult = results

            # else:
            #     pass

            if flag:

                return (flag, fresult)
            else:

                return (flag, fresult)

        else:

            return (flag, "No Response Get From SAP!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


def GETSAP_Dashboard(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_AGENT_DSB_SRV/AGN_DSBSet(Partner='%s')?$format=json" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


def GETSAP_Dashboard_DBUser(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_EXE_DSB_SRV/EXE_DSBSet(Adid='%s')?$format=json" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
# @method_decorator(cache_page(60))
def dashboard_data(request, BPCODE):
    dash = None
    lastmonth_year = ""
    lastmonth_year_Bill_Amt = ""
    YTDData = ""
    MTDData = ""
    HintCount = ""
    Open_count = 0
    Closed_Count = 0
    Noti_Count = 0
    response = None

    try:

        # IC = GETIncident_Count_Dashboard(BPCODE)

        # IC = json.loads(IC.content)
        Open_count = 0  # IC['Open_count']
        Closed_Count = 0  # IC['Closed_Count']
        Noti_Count = NotificationLog.objects.filter(status=1, BP_Code=BPCODE, Read_Status=0).count()
        try:
            userm = UserMaster.objects.get(username=BPCODE)
        except UserMaster.DoesNotExist as ex:
            userm = None
            dash_f = GETSAP_Dashboard(request, BPCODE)
            if dash_f[0]:
                dash = dash_f[1]
                del dash['__metadata']

            ll = Last_Bill_Month(request, BPCODE)
            ll_j = json.loads(ll.content)
            lastmonth_year = ll_j['lastmonth_year']
            lastmonth_year_Bill_Amt = ll_j['lastmonth_year_Bill_Amt']

            # ytd = Last_Seven_Days_Copy(request, BPCODE)
            YTDData = None  # json.loads(ytd.content)

            mtd = Last_Six_Month_Bill(request, BPCODE)
            MTDData = json.loads(mtd.content)

        # cu = Hint.objects.filter(Hint_Status=1, Hint_Leng='EN').count()
        HintCount = 0  # str(cu)

        if userm:
            # user_type = UserTypeMaster.objects.get(
            #     user_type='EU')
            try:
                ud = UserMasterDetails.objects.get(usermaster=userm)
            except UserMasterDetails.DoesNotExist as ex:
                ud = None
                dash_f = GETSAP_Dashboard(request, BPCODE)
                if dash_f[0]:
                    dash = dash_f[1]
                    del dash['__metadata']

            if ud:
                if ud.user_type.user_type == "EU":
                    dash_f = GETSAP_Dashboard(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]
                        del dash['__metadata']

                else:
                    dash_f = GETSAP_Dashboard_DBUser(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]

                        del dash['__metadata']
                        dash_new = {"Partner": BPCODE,
                                    "GrossCopy": dash['PaidCopy'],
                                    "FreeCopy": "",
                                    "PaidCopy": dash['PaidCopy'],
                                    "Zlao": "",
                                    "Zcoo": "",
                                    "OutStd": round(float(float(dash['OutStd']) / 100000), 2),
                                    "Asd": round(float(float(dash['Asd']) / 100000), 2),

                                    }
                        lastmonth_year_Bill_Amt = round(
                            float(float(dash['Billing']) / 100000), 2)
                        dash = dash_new
                ll = Last_Bill_Month(request, BPCODE)
                ll_j = json.loads(ll.content)
                lastmonth_year = ll_j['lastmonth_year']
                if ud.user_type.user_type == "EU":
                    lastmonth_year_Bill_Amt = ll_j['lastmonth_year_Bill_Amt']
                # else:
                #     lastmonth_year_Bill_Amt = dash['Billing']

                # ytd = Last_Seven_Days_Copy(request, BPCODE)
                YTDData = None  # json.loads(ytd.content)

                mtd = Last_Six_Month_Bill(request, BPCODE)
                MTDData = json.loads(mtd.content)

            # else:
            #     dash_f = GETSAP_Dashboard(request, BPCODE)

        ul = user_log(request, BPCODE, 'Dashboard', 'Dashboard Open')
        response = JsonResponse(
            {'data': dash, 'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt,
             'YTDData': YTDData, 'MTDData': MTDData, 'HintCount': HintCount, "Open_count": Open_count,
             "Closed_Count": Closed_Count, 'Noti_Count': Noti_Count, 'reply': 'User Dashboard Data'})
        # response['Cache-Control'] = f'max-age={60*60*24}'
        # response.RawResponse(headers={"content-type": "application/json"})
        # response.headers['Cache-Control'] = 'max-age=60'
        # if ud.user_type.user_type == "EU":
        patch_response_headers(response, cache_timeout=300)

        return response

    except Exception as e:
        ul = user_log(request, BPCODE, 'Dashboard',
                      'Dashboard Open with Error')
        response = JsonResponse(
            {'data': None, 'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt,
             'YTDData': YTDData, 'MTDData': MTDData, 'HintCount': HintCount, "Open_count": Open_count,
             "Closed_Count": Closed_Count, 'Noti_Count': Noti_Count, 'reply': str(e)})
        return response


def GETSAP_NoOfCopies(request, BPCODE, AgType=None, fromdt=None, todt=None, edi=None):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_COPIES_SRV/AGN_CPSet?$format=json&$filter=Partner eq '%s'" % (
                    res.server_host, BPCODE)
                if AgType:
                    sapurl = sapurl + " and AgType eq '%s' " % (AgType)
                if edi:
                    if edi != "*":
                        sapurl = sapurl + "  and Pva eq '%s' " % (edi)

                if fromdt and todt:
                    sapurl = sapurl + \
                             "and (OrdDate ge datetime'%sT00:00:00' and OrdDate le datetime'%sT00:00:00')" % (
                                 fromdt, todt)

                # and AgType eq 'MA' and (OrdDate ge datetime'2019-12-01T00:00:00' and OrdDate le datetime'2020-03-01T00:00:00')
            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                for num in results['results']:
                    OrdDate = re.split(
                        '\(|\)', num['OrdDate'])[1][:10]
                    # num['OrdDate'] = datetime.datetime.fromtimestamp(
                    # int(OrdDate))
                    num['OrdDate'] = OrdDate

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def NoOfCopies_data(request, BPCODE, AgType, fromdt, todt, edi):
    try:

        Outstanding = ""
        if AgType == 'AG':
            AgType = 'MA'

        dash_f = GETSAP_NoOfCopies(request, BPCODE, AgType, fromdt, todt, edi)
        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']

        Outstanding = get_outstanding(BPCODE)
        ul = user_log(request, BPCODE, 'Copies', 'Copies Open')
        return JsonResponse({'data': dash, 'Outstanding': Outstanding, 'reply': 'Number of Copies'})

    except Exception as e:
        ul = user_log(request, BPCODE, 'Copies', 'Copies Open with Error')
        return JsonResponse({'data': None, 'Outstanding': Outstanding, 'reply': str(e)})


def GETSAP_EditionList(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_EDTN_MASTER_SRV/HeaderSet?$filter=(SoldToParty eq '%s')&$expand=NavSubagentSet,NavEdtnSet&$format=json" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def EditionList_data(request, BPCODE):
    try:

        dash_f = GETSAP_EditionList(request, BPCODE)
        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']
                del num['SoldToParty']
                for num1 in num['NavSubagentSet']['results']:
                    del num1['__metadata']
                for num2 in num['NavEdtnSet']['results']:
                    del num2['__metadata']

        return JsonResponse({'data': dash, 'reply': 'Edition and Sub Agent List'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


def GETSAP_DBUser_Copies_Count(request, BPCODE, GrpBy=None, fromdt=None, todt=None, Search_Key='*', Search_Key2='*',
                               Search_Key3='*', Search_Key4='*', Search_Key5='*'):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_EXE_COPY_SRV/EXE_COPYSet?$format=json&$filter=Adid eq '%s'" % (
                    res.server_host, BPCODE)
                if GrpBy:
                    sapurl = sapurl + " and Fltr  eq '%s' " % (GrpBy.upper())
                # if edi:
                #     if edi != "*":
                #         sapurl = sapurl + "  and Pva eq '%s' " % (edi)

                if fromdt and todt:
                    sapurl = sapurl + \
                             "and (OrdDate ge datetime'%sT00:00:00' and OrdDate le datetime'%sT00:00:00')" % (
                                 fromdt, todt)

                if GrpBy == 'C':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                if GrpBy == 'A':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkorg eq '%s'" % (Search_Key.upper())

                if GrpBy == 'S':
                    pass

                if GrpBy == 'P':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                if GrpBy == 'G':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                    if Search_Key2 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vtweg eq '%s'" % (Search_Key2.upper())

                    if Search_Key3 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkorg  eq '%s'" % (Search_Key3.upper())

                # if GrpBy == 'L':
                #     if Search_Key == '*':
                #         pass
                #     else:
                #         sapurl = sapurl + \
                #             "and State eq '%s'" % (Search_Key.upper())

                #     if Search_Key2 == '*':
                #         pass
                #     else:
                #         sapurl = sapurl + \
                #             "and Vtweg eq '%s'" % (Search_Key2.upper())
                if GrpBy == 'L':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                    if Search_Key2 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vtweg eq '%s'" % (Search_Key2.upper())

                    if Search_Key3 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkgrp eq '%s'" % (Search_Key3.upper())

                if GrpBy == 'D':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                    if Search_Key2 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vtweg eq '%s'" % (Search_Key2.upper())

                    if Search_Key3 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkgrp eq '%s'" % (Search_Key3.upper())

                    if Search_Key4 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkorg eq '%s'" % (Search_Key4.upper())

                if GrpBy == 'N':
                    if Search_Key == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and State eq '%s'" % (Search_Key.upper())

                    if Search_Key2 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vtweg eq '%s'" % (Search_Key2.upper())

                    if Search_Key3 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkgrp eq '%s'" % (Search_Key3.upper())

                    if Search_Key4 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Vkorg eq '%s'" % (Search_Key4.upper())

                    if Search_Key5 == '*':
                        pass
                    else:
                        sapurl = sapurl + \
                                 "and Bzirk eq '%s'" % (Search_Key5.upper())

                # and AgType eq 'MA' and (OrdDate ge datetime'2019-12-01T00:00:00' and OrdDate le datetime'2020-03-01T00:00:00')
            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:

                for num in results['results']:
                    OrdDate = re.split(
                        '\(|\)', num['OrdDate'])[1][:10]
                    # num['OrdDate'] = datetime.datetime.fromtimestamp(
                    # int(OrdDate))
                    num['OrdDate'] = OrdDate
                    num['Partner'] = num['SoldToParty']

                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def DBUser_Copies_Count(request, BPCODE, GrpBy, fromdt, todt):
    try:
        ul = user_log(request, BPCODE, 'Copies', 'Copies Open Group: ' + GrpBy)
        dash_f = GETSAP_DBUser_Copies_Count(
            request, BPCODE, GrpBy, fromdt, todt)
        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']

                # for num1 in num['NavSubagentSet']['results']:
                #     del num1['__metadata']
                # for num2 in num['NavEdtnSet']['results']:
                #     del num2['__metadata']

        return JsonResponse({'data': dash, 'reply': 'DBUser_Copies_Count'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def DBUser_Copies_Count_KEY(request, BPCODE, GrpBy, fromdt, todt, Search_Key=None, Search_Key2=None, Search_Key3=None,
                            Search_Key4=None, Search_Key5=None):
    try:
        ul = user_log(request, BPCODE, 'Copies',
                      'Copies Open with Group and Key:' + str(GrpBy) + " " + str(Search_Key) + " " + str(
                          Search_Key2) + " " + str(Search_Key3) + " " + str(Search_Key4) + " " + str(Search_Key5))
        if Search_Key == '*':
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt)
        elif Search_Key2 == None and Search_Key3 == None and Search_Key4 == None and Search_Key5 == None:
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt, Search_Key)

        elif Search_Key2 and Search_Key3 == None and Search_Key4 == None and Search_Key5 == None:
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt, Search_Key, Search_Key2)

        elif Search_Key2 and Search_Key3 and Search_Key4 == None and Search_Key5 == None:
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt, Search_Key, Search_Key2, Search_Key3)

        elif Search_Key2 and Search_Key3 and Search_Key4 and Search_Key5 == None:
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt, Search_Key, Search_Key2, Search_Key3, Search_Key4)

        elif Search_Key2 and Search_Key3 and Search_Key4 and Search_Key5:
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt, Search_Key, Search_Key2, Search_Key3, Search_Key4, Search_Key5)

        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            # del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']

                # for num1 in num['NavSubagentSet']['results']:
                #     del num1['__metadata']
                # for num2 in num['NavEdtnSet']['results']:
                #     del num2['__metadata']

        return JsonResponse({'data': dash, 'reply': 'DBUser_Copies_Count'})

    except Exception as e:
        return JsonResponse({'data': None, 'reply': str(e)})
