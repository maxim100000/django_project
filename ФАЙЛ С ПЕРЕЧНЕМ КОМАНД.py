import functools
import django
django.setup()
from news_paper.models import Post, Author, User, Category, Comment

User.objects.create_user('miha')
User.objects.create_user('dimon')

Author.objects.create(user=User.objects.get(username='dimon'), rating=0)
Author.objects.create(user=User.objects.get(username='miha'), rating=0)

Category.objects.create(name='Politic')
Category.objects.create(name='Sport')
Category.objects.create(name='Kino')
Category.objects.create(name='Pop-music')

article1 = 'С учетом возрастающей политической напряженности неудивительно,' \
           ' что ученые некоторых стран задумываются о последствиях ядерного конфликта. ' \
           'На этот раз пара новозеландских исследователей решила оценить последствия резкого ' \
           'снижения уровня солнечной освещенности для сельскохозяйственного производства в ' \
           '38 островных государствах по всему миру. ' \
           'Результаты их анализа опубликованы в журнале Risk Analysis. Согласно выводам ученых, ' \
           'только четыре островных государства смогут обеспечить себя продуктами питания в условиях ' \
           'сниженной освещенности и более прохладного климата: Исландия, Новая Зеландия, ' \
           'Вануату и Соломоновы Острова. Их результаты в отношении Новой Зеландии по большей части' \
           ' повторяют выводы 1980-х годов, хотя с тех пор устойчивость страны снизилась' \
           ' в силу возросшей зависимости от импортного топлива и цифровой инфраструктуры.'

Post.objects.create(text=article1, title='Ученые назвали одно из немногих островных государств, которое переживет ядерную зиму', 
                    record='A', rating=0, author=Author.objects.get(user_id=3))

article2 = 'Хотя интуитивно люди склонны думать, что занятия музыкой полезны для' \
           ' их психического здоровья, научные исследования указывают на более сложную и' \
           ' неочевидную связь. В новой работе международная группа ученых обнаружила генетическую' \
           ' корреляцию между увлечением музыкой и психическим здоровьем на примере нескольких тысяч' \
           ' близнецов. Результаты исследования показывают, что у музыкально активных людей' \
           ' существенно повышен генетический риск развития депрессии и биполярного расстройства.' 

Post.objects.create(text=article2, title='Увлечение музыкой связали с повышенным риском развития психических заболеваний', 
                    record='A', rating=0, author=Author.objects.get(user_id=4))

news = 'Ученые из Гринвича (США) обнаружили на пляже в Новой Зеландии окаменелые останки крупнейшего' \
       ' пингвина, когда-либо жившего на планете, их исследование опубликовано в научном' \
       ' в журнале Journal of Paleontology. "Недавние находки окаменелостей в Новой Зеландии выявили удивительное разнообразие ' \
       'сообщества пингвинов. Самый крупный экземпляр отнесен к новому виду Kumimanu fordycein.' \
       ' Этот пингвин был самым большим из когда-либо живших на Земле", - говорится в исследовании'

Post.objects.create(text=news, title='На пляже в Новой Зеландии нашли останки 154-килограммового пингвина', 
                    record='N', rating=0, author=Author.objects.get(user_id=3))

Post.objects.get(id=1).category.add(Category.objects.get(id=1), Category.objects.get(id=3))
Post.objects.get(id=2).category.add(Category.objects.get(id=3), Category.objects.get(id=4))
Post.objects.get(id=3).category.add(Category.objects.get(id=2), Category.objects.get(id=3))

Comment.objects.create(post_id=1, user_id=3, text='Круто', rating=0)
Comment.objects.create(post_id=2, user_id=4, text='Дизлайк', rating=0)
Comment.objects.create(post_id=3, user_id=3, text='Неплохо', rating=0)
Comment.objects.create(post_id=2, user_id=4, text='Хорошо', rating=0)

Post.objects.get(id=1).like()
Post.objects.get(id=2).like()
Post.objects.get(id=3).like()

Comment.objects.get(id=1).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=1).dislike()

print(sum([x.rating for x in Author.objects.get(id=1).post_set.filter()]))
print(sum(functools.reduce(lambda x, y: x + y, [[i['rating'] for i in x.comment_set.values('rating')] for x in Author.objects.get(id=2).post_set.filter()])))
print([i.comment_set.filter().values('rating') for i in Author.objects.get(id=2).post_set.filter()])

a = Author.objects.get(id=1)
a.update_rating()
a.save()

a = Author.objects.get(id=2)
a.update_rating()
a.save()

rating, username =  Author.objects.values('rating', 'user__username').order_by('-rating')[0].items()
print(f'Пользователь {username[1]}, рейтинг {rating[1]}') 

result_set = Post.objects.filter(record='A').order_by('-rating').values('author__user__username', 'title', 
                                                                        'date_time', 'rating', 'id')
print('Лучшая статья\nАвтор {}\nЗаголовок{}\nВремя добавления {}\nРейтинг {}\n'.format
      (*[v for i, v  in result_set[0].items()]), Post.objects.get(rating=result_set[0]['rating']).preview(), sep='')

all_comments = Post.objects.filter(record='A').order_by('-rating')[0].comment_set.values('date_time', 'text', 'rating', 'user__username')
print('Дата комментария {}\nТекст комментария {}\nРейтинг {}\nПользователь {}\n'.
      format(*[j for i, j in all_comments[0].items()]), sep='')
