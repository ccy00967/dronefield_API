from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from payments.serializers import RequestTossUpdateSerializer
from payments.serializers import TossPaymentsSerializer

from payments.permissions import CheckUser
from payments.permissions import CheckAmount
from payments.permissions import CheckPaymentKey
from payments.permissions import CheckStatusMatching

from trade.models import Request

import json
from payments.models import TossPayments
import requests
from rest_framework.response import Response


# 시크릿키를 base64로 인코딩 했다 - 토스 권장사항
# 터미널에 아래 명령어를 입력하면 인코딩된 값이 반환된다 - base64 임포트하거나 해서 사용하기
# echo -n 'test_sk_L~~~' | base64
HEADERS = {
    "Authorization": "Basic dGVzdF9za19Ma0tFeXBOQXJXV1lveEs5eldKQXJsbWVheFlHOg==",
    "Content-Type": "application/json",
}


# 신청서와 예약금 2개 만들기
# 이때 신청서를 여러개 받을 수 있다.
class RequestTossCreateAPIView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestTossUpdateSerializer
    name = "request-tosspayments-update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        CheckStatusMatching,
        CheckUser,
        # CheckAmount,
    )

    def post(self, request):
        # 사용자로부터 받음
        PAYMENT_KEY = request.data.get("paymentKey")
        ORDERID = request.data.get("orderId")
        orderIdList = request.data.get("orderidlist")
        TotalAMOUNT = 0

        for orderid in orderIdList:
            try:
                # orderid를 'orderId'로 수정하여 필드명 일치시킴
                request_instance = Request.objects.get(orderId=orderid)
            except Request.DoesNotExist:
                return Response(
                    {"message": f"Request with orderId {orderid} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # RequestSerializer 인스턴스 생성
            serializer = self.get_serializer(request_instance)

            # 사용자 타입에 따른 금액 계산
            if request.user.type == 3:
                TotalAMOUNT += serializer.data.get("reservateDepositAmount", 0)
            elif request.user.type == 4:
                TotalAMOUNT += serializer.data.get("requestAmount", 0)

        print(TotalAMOUNT)

        # 값 검증하기
        url = "https://api.tosspayments.com/v1/payments/confirm"
        data = {"paymentKey": PAYMENT_KEY, "orderId": ORDERID, "amount": TotalAMOUNT}
        payload = json.dumps(data)
        response = requests.post(url, headers=HEADERS, data=payload)

        if 400 <= response.status_code < 500:
            error = response.json()
            return Response(
                {"code": error["code"], "message": error["message"]},
                status=response.status_code,
            )

        # 토스 결제확인 데이터
        tosspayData = response.json()

        # 토스 결제확인 데이터 저장
        tosspaymentsObj = TossPayments.objects.create(
            orderId=tosspayData["orderId"],
            paymentKey=tosspayData["paymentKey"],
            method=tosspayData["method"],
            totalAmount=tosspayData["totalAmount"],
            status=tosspayData["status"],
        )

        # 해당 신청서들 업데이트
        for orderid in orderIdList:
            print(orderid)
            if request.user.type == 3:
                Request.objects.filter(orderId=orderid).update(
                    reservateTosspayments=tosspaymentsObj, reservateDepositState=1
                )
            elif request.user.type == 4:
                Request.objects.filter(orderId=orderid).update(
                    requestTosspayments=tosspaymentsObj, requestDepositState=1
                )

        return Response(
            {"message": "결제가 완료되었습니다."}, status=status.HTTP_201_CREATED
        )


# 수정 필요
# 결제 취소등 정보수정
class TossPaymentsUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = TossPaymentsSerializer
    lookup_field = "orderid"
    name = "tosspayments-cancel"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        CheckPaymentKey,
        CheckStatusMatching,
    )

    def perform_update(self, serializer):
        # PAYMENT_KEY = self.request.data.get('paymentKey')
        PAYMENT_KEY = serializer.data["paymentKey"]
        # cancelAmount = self.request.data.get('cancelAmount')
        cancelAmount = Request.objects.get(orderid=self.kwargs.get("orderid"))

        # 부분 환불하기
        url = "https://api.tosspayments.com/v1/payments/" + PAYMENT_KEY + "/cancel"
        data = {
            "cancelAmount": cancelAmount,
        }
        payload = json.dumps(data)
        headers = HEADERS
        response = requests.post(url, headers=headers, data=payload)

        if 400 <= response.status_code < 500:
            error = response.json()
            return Response(
                {"code": error["code"], "message": error["message"]},
                status=response.status_code,
            )

        tosspayData = response.json()

        serializer.save(
            requestDepositState=0,
            requestCancelTransactionKey=tosspayData["transactionKey"],
        )
