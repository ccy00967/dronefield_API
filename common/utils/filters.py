import django_filters
from trade.models import Request

class RequestFilter(django_filters.FilterSet):
    # 클라이언트가 endDate=YYYY-MM, startDate=YYYY-MM 형식으로 전달할 경우 처리하는 필터
    endDate = django_filters.CharFilter(method='filter_date')
    startDate = django_filters.CharFilter(method='filter_date')

    class Meta:
        model = Request
        fields = ['orderId', 'exterminateState', 'checkState', 'startDate', 'endDate']

    def filter_date(self, queryset, name, value):
        """
        value 예시: "2024-02"
        """
        try:
            year_str, month_str = value.split('-')
            year = int(year_str)
            month = int(month_str)
        except ValueError:
            # 올바른 형식이 아닐 경우 필터링 없이 원래 queryset 반환
            return queryset

        # 전달된 필드 이름(name)에 맞춰서 필터 조건을 구성합니다.
        filter_kwargs = {
            f"{name}__year": year,
            f"{name}__month": month,
        }
        return queryset.filter(**filter_kwargs)