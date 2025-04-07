from django.db import models

from TestAll.backend.fun_quizzes.models.category import Category
from .base import TimeStampModel

class Test(TimeStampModel):
    """
    테스트 기본 정보 모델
    """
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="카테고리")
    # TextField 는 긴 텍스트를 저장할 때 사용
    # CharField 는 짧은 텍스트를 저장할 때 사용
    # 최대 길이를 지정해줄 수 있음 지정안하면 255 지정하면 데이터베이스에서 최적화된 인덱스를 사용할 수 있음
    title = models.CharField(max_length=100, verbose_name="테스트 제목")
    slug = models.SlugField(unique=True, verbose_name="URL용 이름")
    decription = models.TextField(verbose_name="테스트 설명")
    thumbnail = models.ImageField(upload_to="test/thumbnail", verbose_name="썸네일")

    # 통계필드
    participant_count = models.PositiveIntegerField(default=0, verbose_name="참여자 수")
    share_count = models.PositiveIntegerField(default=0, verbose_name="공유 수")

    # AI 이미지 생성 관련 설정
    is_ai_image = models.BooleanField(default=False, verbose_name="AI 이미지 생성 여부")
    prompt_template = models.TextField(
        blank=True,
        verbose_name="AI 이미지 생성 프롬프트 템플릿",
        help_text="생년월일, 시간 등의 변수는 {birth_date}, {birth_time} 형식으로 입력"
    )

    class Meta:
        verbose_name = "테스트"
        verbose_name_plural = "테스트 목록"

    def __str__(self):
        return self.title
