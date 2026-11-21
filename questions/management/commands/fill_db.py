import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from faker import Faker

from core.models import *
from questions.models import *

User = get_user_model()
fake = Faker()

BATCH_SIZE = 5000  


class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными. Использование: python manage.py fill_db <ratio>"

    def add_arguments(self, parser):
        parser.add_argument(
            "ratio",
            type=int,
            help="Коэффициент заполнения: users=ratio, questions=ratio*10, "
                 "answers=ratio*100, tags=ratio, likes=ratio*200",
        )

    def handle(self, *args, **options):
        ratio = options["ratio"]
        if ratio <= 0:
            self.stderr.write("ratio должен быть положительным числом")
            return

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write(self.style.WARNING(
            f"Генерация: users={num_users}, questions={num_questions}, "
            f"answers={num_answers}, tags={num_tags}, likes={num_likes}"
        ))

        # ------------------------------------------------------------------
        # 1. Пользователи + профили
        # ------------------------------------------------------------------
        self.stdout.write("Создание пользователей и профилей...")

        # Генерируем уникальные username/email заранее, чтобы избежать коллизий
        existing_usernames = set(
            User.objects.values_list("username", flat=True)
        )
        usernames = set()
        while len(usernames) < num_users:
            usernames.add(fake.user_name() + str(random.randint(0, 10**9)))
        usernames -= existing_usernames
        usernames = list(usernames)[:num_users]

        emails = [f"{u}@example.com" for u in usernames]

        users = [
            User(username=u, email=e)
            for u, e in zip(usernames, emails)
        ]
        # bulk_create возвращает объекты с заполненными pk (на PostgreSQL / SQLite 3.35+)
        users = User.objects.bulk_create(users, batch_size=BATCH_SIZE)

        # Профили
        profiles = [
            Profile(
                user_id=u.pk,
                name=fake.name()[:150],
            )
            for u in users
        ]
        profiles = Profile.objects.bulk_create(profiles, batch_size=BATCH_SIZE)
        profile_ids = [p.pk for p in profiles]

        # ------------------------------------------------------------------
        # 2. Теги
        # ------------------------------------------------------------------
        self.stdout.write("Создание тегов...")

        existing_tags = set(Tag.objects.values_list("name", flat=True))
        tag_names = set()
        while len(tag_names) < num_tags:
            # короткие "слова" как названия тегов (max_length=20)
            tag_names.add(fake.word()[:20] + str(random.randint(0, 999)))
        tag_names -= existing_tags
        tag_names = list(tag_names)[:num_tags]

        tags = [Tag(name=n, slug=n) for n in tag_names]
        tags = Tag.objects.bulk_create(tags, batch_size=BATCH_SIZE)
        tag_ids = [t.pk for t in tags]

        # ------------------------------------------------------------------
        # 3. Вопросы + связи M2M с тегами через through-таблицу
        # ------------------------------------------------------------------
        self.stdout.write("Создание вопросов...")

        now = timezone.now()
        questions = [
            Question(
                profile_id=random.choice(profile_ids),
                title=fake.sentence(nb_words=5)[:50],
                description=fake.text(max_nb_chars=1000),
                created_at=now - timedelta(
                    days=random.randint(0, 365),
                    seconds=random.randint(0, 86400),
                ),
            )
            for _ in range(num_questions)
        ]
        questions = Question.objects.bulk_create(questions, batch_size=BATCH_SIZE)
        question_ids = [q.pk for q in questions]

        # M2M через through-таблицу (Question.tags.through)
        QuestionTag = Question.tags.through
        through_rows = []
        for qid in question_ids:
            # каждому вопросу 1-3 случайных тега
            n_tags = random.randint(1, 3)
            for tid in random.sample(tag_ids, min(n_tags, len(tag_ids))):
                through_rows.append(QuestionTag(question_id=qid, tag_id=tid))

        # bulk_create для M2M
        for i in range(0, len(through_rows), BATCH_SIZE):
            QuestionTag.objects.bulk_create(
                through_rows[i:i + BATCH_SIZE], batch_size=BATCH_SIZE, ignore_conflicts=True
            )

        # ------------------------------------------------------------------
        # 4. Ответы
        # ------------------------------------------------------------------
        self.stdout.write("Создание ответов...")

        answers = [
            Answer(
                question_id=random.choice(question_ids),
                profile_id=random.choice(profile_ids),
                content=fake.text(max_nb_chars=1000),
                is_correct=random.random() < 0.15,
                created_at=now - timedelta(
                    days=random.randint(0, 365),
                    seconds=random.randint(0, 86400),
                ),
            )
            for _ in range(num_answers)
        ]
        answers = Answer.objects.bulk_create(answers, batch_size=BATCH_SIZE)
        answer_ids = [a.pk for a in answers]

        # ------------------------------------------------------------------
        # 5. Лайки пользователей (QuestionLike + AnswerLike)
        # ------------------------------------------------------------------
        self.stdout.write("Создание оценок пользователей...")

        # Делим общее количество лайков примерно поровну
        n_q_likes = num_likes // 2
        n_a_likes = num_likes - n_q_likes

        # ---- QuestionLike ----
        # Уникальный constraint (profile, question) — избегаем дублей
        seen_q = set()
        q_like_rows = []
        attempts = 0
        max_attempts = n_q_likes * 3
        while len(q_like_rows) < n_q_likes and attempts < max_attempts:
            attempts += 1
            pid = random.choice(profile_ids)
            qid = random.choice(question_ids)
            key = (pid, qid)
            if key in seen_q:
                continue
            seen_q.add(key)
            q_like_rows.append(
                QuestionLike(
                    profile_id=pid,
                    question_id=qid,
                    value=random.choice([1, 1, 1, -1]),
                )
            )
        for i in range(0, len(q_like_rows), BATCH_SIZE):
            QuestionLike.objects.bulk_create(
                q_like_rows[i:i + BATCH_SIZE], batch_size=BATCH_SIZE,
                ignore_conflicts=True,
            )

        # ---- AnswerLike ----
        seen_a = set()
        a_like_rows = []
        attempts = 0
        max_attempts = n_a_likes * 3
        while len(a_like_rows) < n_a_likes and attempts < max_attempts:
            attempts += 1
            pid = random.choice(profile_ids)
            aid = random.choice(answer_ids)
            key = (pid, aid)
            if key in seen_a:
                continue
            seen_a.add(key)
            a_like_rows.append(
                AnswerLike(
                    profile_id=pid,
                    answer_id=aid,
                    value=random.choice([1, 1, 1, -1]),
                )
            )
        for i in range(0, len(a_like_rows), BATCH_SIZE):
            AnswerLike.objects.bulk_create(
                a_like_rows[i:i + BATCH_SIZE], batch_size=BATCH_SIZE,
                ignore_conflicts=True,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Готово. Создано: "
            f"users={len(users)}, profiles={len(profiles)}, "
            f"tags={len(tags)}, questions={len(questions)}, "
            f"answers={len(answers)}, "
            f"q_likes={len(q_like_rows)}, a_likes={len(a_like_rows)}"
        ))