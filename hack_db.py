import random
from datacenter.models import Schoolkid, Lesson, Subject, Mark, Commendation, Chastisement


def check_schoolkid_exists(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем. Пожалуйста, уточните запрос и попробуйте заново.')
        exit(1)
    except Schoolkid.DoesNotExist:
        print('Указанный пользователь не существует. Отправьте запрос заново.')
        exit(1)
    return schoolkid

def fix_marks(name):
    schoolkid = check_schoolkid_exists(name)
    bad_marks = Mark.objects.filter(schoolkid__full_name=schoolkid.full_name, points__in=[2, 3])
    for bad_mark in bad_marks:
        good_mark = random.randint(4, 5)
        bad_mark.points = good_mark
        bad_mark.save()
    return Mark.objects.filter(schoolkid__full_name=schoolkid.full_name, points__in=[2, 3])


def remove_chastisements(name):
    schoolkid = check_schoolkid_exists(name)
    child_chastisements = Chastisement.objects.filter(schoolkid__full_name=schoolkid.full_name)
    return child_chastisements.delete()


def create_commendation(name, subject):
    schoolkid = check_schoolkid_exists(name)
    praise = random.choice(praises)
    try:
        lesson = Lesson.objects.filter(group_letter='А', year_of_study=6, subject__title=subject).order_by('-date').first()
        commendation = Commendation.objects.create(text='Хвалю!', created=lesson.date, schoolkid=schoolkid,
                                               subject=lesson.subject, teacher=lesson.teacher)
    except AttributeError:
        print('Указанная дисциплина не найдена, попробуйте ввести еще раз!')
        exit(1)
    return commendation


praises = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
         'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
         'Сказано здорово – просто и ясно!',
         'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!',
         'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!', 'Прекрасное начало!',
         'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
         'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
         'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
         'Теперь у тебя точно все получится!']
