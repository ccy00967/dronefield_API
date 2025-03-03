# from celery import shared_task
# from django.utils.timezone import now
# from datetime import timedelta
# from .models import Request


# @shared_task
# def delete_expired_requests():
#     """24시간이 지나고 requestDepositState가 1이 아닌 신청서를 삭제"""
#     expired_requests = Request.objects.filter(
#         requestDepositState__ne=1,  # 1이 아닌 경우
#         created_at__lt=now() - timedelta(hours=24)  # 24시간 초과
#     )
#     deleted_count, _ = expired_requests.delete()
#     return f"{deleted_count}개의 만료된 신청서 삭제됨"
