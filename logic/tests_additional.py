from logic.tests_services import ServiceBaseTest, BaseModelTest
from datamodel.models import Game, Move, GameStatus
from django.urls import reverse

from django.contrib.auth.models import User


class WinServiceTests(BaseModelTest):
    def setUp(self):
        super().setUp()
        self.user1 = User.objects.get_or_create(username='foo10', id=10)[0]
        self.user1.save()

        self.user2 = User.objects.get_or_create(username='foo11', id=11)[0]
        self.user2.save()

    def tearDown(self):
        super().tearDown()

    def test0(self):
        """ Validación de la actualización del juego al ganar el gato"""
        game = Game(cat_user=self.user1)
        game.save()

        game.cat1 = 41
        game.cat2 = 50
        game.mouse = 48
        game.mouse_user = self.user2
        game.save()

        move = Move(origin=50, target=57, player=self.user1, game=game)
        move.save()

        self.assertEqual(game.status, GameStatus.FINISHED)
    
    def test1(self):
        """ Validación de la actualización del juego al ganar el raton"""
        game = Game(cat_user=self.user1)
        game.save()

        game.cat1 = 57
        game.cat2 = 59
        game.cat3 = 61
        game.cat4 = 63
        game.mouse = 18
        game.mouse_user = self.user2
        game.cat_turn = False
        game.save()

        move = Move(origin=18, target=11, player=self.user2, game=game)
        move.save()

        self.assertEqual(game.status, GameStatus.FINISHED)


