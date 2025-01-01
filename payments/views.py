from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from payments.serializers import TossPaymentsUpdateSerializer
from payments.serializers import TossPaymentsSerializer

from payments.permissions import CheckUser
from payments.permissions import CheckAmount
from payments.permissions import CheckPaymentKey
from payments.permissions import CheckStatusMatching

from trade.models import CustomerRequest

import json
from payments.models import TossPayments
import requests
from rest_framework.response import Response


# 시크릿키를 base64로 인코딩 했다 - 토스 권장사항
# 터미널에 아래 명령어를 입력하면 인코딩된 값이 반환된다 - base64 임포트하거나 해서 사용하기
# echo -n 'test_sk_L~~~' | base64
HEADERS = {
            'Authorization': "Basic dGVzdF9za19Ma0tFeXBOQXJXV1lveEs5eldKQXJsbWVheFlHOg==",
            'Content-Type': "application/json"
        }

# 신청서와 예약금 2개 만들기
# 이때 신청서를 여러개 받을 수 있다.
class TossPaymentsUpdateDeleteWithRequestView(generics.CreateAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = TossPaymentsUpdateSerializer
    #lookup_field = 'orderid' # 토스페이 orderid를 받음
    name = "tosspayments-update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        CheckStatusMatching,
        CheckUser,
        #CheckAmount,
    )

    #def perform_update(self, serializer):
    def create(self, serializer):
        # 사용자로부터 받음
        PAYMENT_KEY = self.request.data.get('paymentKey')
        #AMOUNT = self.request.data.get('amount')
        ORDERID = self.request.data.get('orderId')
        orderIdList = self.request.data.get('orderidlist')
        #orderIdList = self.request.data.getlist('orderIdList')
        for orderid in orderIdList:
            AMOUNT = self.request.data.get('amount')

        # 값 검증하기
        url = 'https://api.tosspayments.com/v1/payments/confirm'
        data = {
            "paymentKey": PAYMENT_KEY,
            "orderId": ORDERID,
            "amount": AMOUNT
        }
        payload = json.dumps(data)
        response = requests.post(url, headers=HEADERS, data=payload)

        if(400 <= response.status_code < 500) :
            error = response.json()
            return Response({"code": error['code'] , "message" : error['message']}, status = response.status_code)
        
        # 토스 결제확인 데이터
        tosspayData = response.json()

        # 토스 결제확인 데이터 저장
        tosspaymentsObj = TossPayments.objects.create(
            orderId = tosspayData["orderId"],
            paymentKey = tosspayData["paymentKey"],
            method = tosspayData["method"],
            totalAmount = tosspayData["totalAmount"],
            status = tosspayData["status"],
        )

        # 해당하는 신청서 save 실행하기
        for orderid in orderIdList:
            print(orderid)
            if(self.request.user.role == 3):
                CustomerRequest.objects.filter(orderid=orderid).update(reservateTosspayments=tosspaymentsObj, reservateDepositState=1)
            if(self.request.user.role == 4):
                CustomerRequest.objects.filter(orderid=orderid).update(requestTosspayments=tosspaymentsObj, requestDepositState=1)
        return Response({"message" : "결제가 완료되었습니다."}, status = status.HTTP_201_CREATED)


# 수정 필요
# 결제 취소등 정보수정
class TossPaymentsUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = TossPaymentsSerializer
    lookup_field = 'orderid'
    name = "tosspayments-cancel"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        CheckPaymentKey,
        CheckStatusMatching,
    )

    def perform_update(self, serializer):
        #PAYMENT_KEY = self.request.data.get('paymentKey')
        PAYMENT_KEY = serializer.data['paymentKey']
        #cancelAmount = self.request.data.get('cancelAmount')
        cancelAmount = CustomerRequest.objects.get(orderid=self.kwargs.get('orderid'))
        
        # 부분 환불하기
        url = 'https://api.tosspayments.com/v1/payments/' + PAYMENT_KEY + '/cancel'
        data = {
            "cancelAmount": cancelAmount,
        }
        payload = json.dumps(data)
        headers = HEADERS
        response = requests.post(url, headers=headers, data=payload)

        if(400 <= response.status_code < 500) :
            error = response.json()
            return Response({"code": error['code'] , "message" : error['message']}, status = response.status_code)
        
        tosspayData = response.json()

        serializer.save(requestDepositState=0, requestCancelTransactionKey=tosspayData['transactionKey'])

