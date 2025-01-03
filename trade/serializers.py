from rest_framework import serializers
from trade.models import CustomerRequest
from user.serializers import ProfileSerializer
from payments.serializers import TossPaymentsSerializer
from farmer.serializers import ArableLandInfoSerializer


# 신청서
class CustomerRequestSerializer(serializers.ModelSerializer):
    # 외래키인 owner.[내용물]로 값을 리턴받을 수 있다, 물론 아래 Meta클래스의 필드에도 추가해야한다
    #tosspaymentorderId = serializers.ReadOnlyField(source='owner.uuid')
    #requestownerName = serializers.ReadOnlyField(source="requestowner.name")
    #requestownerEmail = serializers.ReadOnlyField(source="requestowner.email")
    orderid = serializers.ReadOnlyField()
    owner = ProfileSerializer(read_only=True)
    exterminatorinfo = ProfileSerializer(read_only=True)
    landInfo = ArableLandInfoSerializer(read_only=True)
    # 유저가 수정하면 안되는 것들
    calculation = serializers.ReadOnlyField()
    requestAmount = serializers.ReadOnlyField()
    requestDepositState = serializers.ReadOnlyField()
    reservateDepositState = serializers.ReadOnlyField()

    #유저가 수정하는 목록
    '''
    exterminateState 오직 방제사용
    customerCheckState
    dealmothod
    startDate
    pesticide
    setAmount
    '''

    class Meta:
        model=CustomerRequest
        #fields='__all__'
        exclude=(
            'requestCancelTransactionKey',
            'depositCancelTransactionKey',
            'requestTosspayments',
            'reservateTosspayments',
        )


# 금액 정산 시리얼라이저 필요?
class RequestExterminateDoneSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()

    class Meta:
        model=CustomerRequest
        fields= (
            'orderid',
            'calculation',
        )


# 이렇게 정보 쪼개기가 여러개 필요예정?
class CustomerRequestBriefSerializer(serializers.ModelSerializer):
    # 이렇게 가능한가?
    address  = serializers.ReadOnlyField(source='common.Address')

    class Meta:
        model=CustomerRequest
        fields= (
            'orderid',
            'landInfo',
            'startDate',
            'endDate',
        )
        # fields = '__all__'


class CustomerCheckExterminateStateSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()
    class Meta:
        model=CustomerRequest
        fields=(
            'orderid',
            'customerCheckState',
        )