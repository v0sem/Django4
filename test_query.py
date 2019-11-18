import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')

import django
django.setup()

from datamodel.models import User, Game, Move

Game.objects.all().delete()

def main():
    user10 = User.objects.get_or_create(username='foo10', id=10)[0]
    user10.save()

    user11 = User.objects.get_or_create(username='foo11', id=11)[0]
    user11.save()

    game1 = Game(cat_user=user10)
    game1.save()

    game_query = Game.objects.filter(cat_user__username__contains='', mouse_user=None)
    print('Juegos donde solo hay un usuario: ')
    print(game_query)
    print('')
    game2 = game_query[0]
    game2.mouse_user = User.objects.get(id=11)
    game2.save()

    print('Juego con menor ID de los anteriores con el ratón añadido: ')
    print(game2)
    print('')

    move = Move(origin=2, target=11, player=user10, game=game2)
    move.save()

    print('Juego después del primer movimiento del gato: ')
    print(game2)
    print('')

    move = Move(origin=59, target=52, player=user11, game=game2)
    move.save()

    print('Juego después del primer movimiento del ratón: ')
    print(game2)
    print('')



if __name__ == "__main__":
    main()