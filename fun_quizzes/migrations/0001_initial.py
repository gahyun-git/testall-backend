# Generated by Django 5.1.7 on 2025-04-03 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('name', models.CharField(max_length=50, verbose_name='카테고리명')),
                ('slug', models.SlugField(unique=True, verbose_name='URL용 이름')),
                ('description', models.TextField(blank=True, verbose_name='설명')),
                ('icon', models.ImageField(upload_to='category_icons/', verbose_name='아이콘')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='정렬 순서')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리 목록',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='PastLifeTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('title', models.CharField(max_length=100, verbose_name='테스트 제목')),
                ('slug', models.SlugField(unique=True, verbose_name='URL용 이름')),
                ('description', models.TextField(verbose_name='테스트 설명')),
                ('thumbnail', models.ImageField(upload_to='test_thumbnails/', verbose_name='썸네일')),
                ('participant_count', models.PositiveIntegerField(default=0, verbose_name='참여자 수')),
                ('share_count', models.PositiveIntegerField(default=0, verbose_name='공유 수')),
                ('prompt_template', models.TextField(blank=True, help_text='생년월일, 시간 등의 변수는 {birth_date}, {birth_time} 형식으로 입력', verbose_name='AI 프롬프트 템플릿')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fun_quizzes.category', verbose_name='카테고리')),
            ],
            options={
                'verbose_name': '전생 테스트',
                'verbose_name_plural': '전생 테스트 목록',
            },
        ),
        migrations.CreateModel(
            name='PastLifeResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(verbose_name='생년월일')),
                ('birth_time', models.TimeField(verbose_name='태어난 시간')),
                ('past_life_name', models.CharField(blank=True, max_length=100, verbose_name='전생 이름')),
                ('past_life_story', models.TextField(blank=True, verbose_name='전생 이야기')),
                ('result_image', models.ImageField(blank=True, upload_to='past_life_results/', verbose_name='결과 이미지')),
                ('story_response', models.JSONField(blank=True, null=True, verbose_name='이야기 AI 응답')),
                ('image_response', models.JSONField(blank=True, null=True, verbose_name='이미지 AI 응답')),
                ('ad_shown', models.BooleanField(default=False, verbose_name='광고 노출 여부')),
                ('ad_shown_at', models.DateTimeField(blank=True, null=True, verbose_name='광고 노출 시간')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fun_quizzes.pastlifetest', verbose_name='테스트')),
            ],
            options={
                'verbose_name': '전생 테스트 결과',
                'verbose_name_plural': '전생 테스트 결과 목록',
                'ordering': ['-created_at'],
            },
        ),
    ]
