from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from datamodel import tests


class GameStatus(models.Model):
    CREATED = 'Created'
    ACTIVE = 'Active'
    FINISHED = 'Finished'

    CHOICE = [(CREATED, 'CREATED'),
              (ACTIVE, 'ACTIVE'),
              (FINISHED, 'FINISHED')]


# Create your models here.
class Game(models.Model):
    MIN_CELL = 0
    MAX_CELL = 63

    cat_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_as_cat")
    mouse_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_as_mouse", null=True, blank=True)

    cat1 = models.IntegerField(null=False, default=0, validators=[
            MaxValueValidator(MAX_CELL),
            MinValueValidator(MIN_CELL)
        ])
    cat2 = models.IntegerField(null=False, default=2, validators=[
            MaxValueValidator(MAX_CELL),
            MinValueValidator(MIN_CELL)
        ])
    cat3 = models.IntegerField(null=False, default=4, validators=[
            MaxValueValidator(MAX_CELL),
            MinValueValidator(MIN_CELL)
        ])
    cat4 = models.IntegerField(null=False, default=6, validators=[
            MaxValueValidator(MAX_CELL),
            MinValueValidator(MIN_CELL)
        ])
    mouse = models.IntegerField(null=False, default=59, validators=[
            MaxValueValidator(MAX_CELL),
            MinValueValidator(MIN_CELL)
        ])
    cat_turn = models.BooleanField(null=False, default=True)

    status = models.CharField(max_length=15, default=GameStatus.CREATED, choices=GameStatus.CHOICE)

    def __str__(self):
        string = "({}, {})".format(self.id, self.status)

        if self.cat_turn:
            string = string + '\tCat [X] {}({}, {}, {}, {})'.format(self.cat_user, self.cat1,
                                                                    self.cat2, self.cat3, self.cat4)
        else:
            string = string + '\tCat [ ] {}({}, {}, {}, {})'.format(self.cat_user, self.cat1,
                                                                    self.cat2, self.cat3, self.cat4)

        if hasattr(self, 'mouse_user') and self.mouse_user != None:
            if self.cat_turn:
                string = string + ' --- Mouse [ ] {}({})'.format(self.mouse_user, self.mouse)
            else:
                string = string + ' --- Mouse [X] {}({})'.format(self.mouse_user, self.mouse)

        return string

    def save(self, *args, **kwargs):

        if (hasattr(self, 'mouse_user') and self.mouse_user != None) and (self.status == GameStatus.CREATED):
            self.status = GameStatus.ACTIVE

        list_white = []
        for i in range(0, 8):
            if i % 2 == 0:
                for j in range(0, 8, 2):
                    list_white.append(i*8+j)
            else:
                for j in range(1, 9, 2):
                    list_white.append(i*8+j)

        if self.cat1 not in list_white:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.cat2 not in list_white:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.cat3 not in list_white:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.cat4 not in list_white:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.mouse not in list_white:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        super(Game, self).save(*args, **kwargs)


class Move(models.Model):
    origin = models.IntegerField(null=False)
    target = models.IntegerField(null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, auto_now=True)

    def save(self, *args, **kwargs):
        if self.game.status != GameStatus.ACTIVE:
            raise ValidationError(tests.MSG_ERROR_MOVE)

        if self.game.cat_turn and self.player == self.game.cat_user:
            if self.target > Game.MAX_CELL or self.target < Game.MIN_CELL:
                raise ValidationError(tests.MSG_ERROR_MOVE)
            elif not self.valid(self.game, self.game.cat_user, self.origin, self.target):
                raise ValidationError(tests.MSG_ERROR_MOVE)
            if self.origin == self.game.cat1:
                if self.target == self.game.mouse or self.target == self.game.cat2 or self.target == self.game.cat3 or self.target == self.game.cat4:
                    raise ValidationError(tests.MSG_ERROR_MOVE)
                self.game.cat1 = self.target
                self.game.save()
                if self.win():
                    self.game.status = GameStatus.FINISHED
                    self.game.save()
                    super(Move, self).save(*args, **kwargs)
                self.game.cat_turn = False
                self.game.save()
            elif self.origin == self.game.cat2:
                if self.target == self.game.mouse or self.target == self.game.cat1 or self.target == self.game.cat3 or self.target == self.game.cat4:
                    raise ValidationError(tests.MSG_ERROR_MOVE)
                self.game.cat2 = self.target
                self.game.save()
                if self.win():
                    self.game.status = GameStatus.FINISHED
                    self.game.save()
                    super(Move, self).save(*args, **kwargs)
                self.game.cat_turn = False
                self.game.save()
            elif self.origin == self.game.cat3:
                if self.target == self.game.mouse or self.target == self.game.cat2 or self.target == self.game.cat1 or self.target == self.game.cat4:
                    raise ValidationError(tests.MSG_ERROR_MOVE)
                self.game.cat3 = self.target
                self.game.save()
                if self.win():
                    self.game.status = GameStatus.FINISHED
                    self.game.save()
                    super(Move, self).save(*args, **kwargs)
                self.game.cat_turn = False
                self.game.save()
            elif self.origin == self.game.cat4:
                if self.target == self.game.mouse or self.target == self.game.cat2 or self.target == self.game.cat3 or self.target == self.game.cat1:
                    raise ValidationError(tests.MSG_ERROR_MOVE)
                self.game.cat4 = self.target
                self.game.save()
                if self.win():
                    self.game.status = GameStatus.FINISHED
                    self.game.save()
                    super(Move, self).save(*args, **kwargs)
                self.game.cat_turn = False
                self.game.save()
            else:
                raise ValidationError(tests.MSG_ERROR_MOVE)
        elif not self.game.cat_turn and self.player == self.game.mouse_user:
            if self.target > Game.MAX_CELL or self.target < Game.MIN_CELL:
                raise ValidationError(tests.MSG_ERROR_MOVE)
            if not self.valid(self.game, self.game.mouse_user, self.origin, self.target):
                raise ValidationError(tests.MSG_ERROR_MOVE)
            if self.target == self.game.cat1 or self.target == self.game.cat2 or self.target == self.game.cat3 or self.target == self.game.cat4:
                raise ValidationError(tests.MSG_ERROR_MOVE)
            self.game.mouse = self.target
            self.game.save()
            if self.win():
                self.game.status = GameStatus.FINISHED
                self.game.save()
                super(Move, self).save(*args, **kwargs)
            self.game.cat_turn = True
            self.game.save()
        else:
            raise ValidationError(tests.MSG_ERROR_MOVE)

        super(Move, self).save(*args, **kwargs)

    def win(self):
        if self.game.cat_turn:
            for target in [self.game.mouse + 7, self.game.mouse + 9, self.game.mouse - 7, self.game.mouse - 9]:
                if target == self.game.cat1 or target == self.game.cat2 or target == self.game.cat3 or target == self.game.cat4:
                    continue
                if self.valid(self.game, self.game.mouse_user, self.game.mouse, target):
                    return False
            return True
        else:
            for target in [self.game.cat1 + 7, self.game.cat1 + 9]:
                if self.valid(self.game, self.game.cat_user, self.game.cat1, target):
                    return False
            for target in [self.game.cat2 + 7, self.game.cat2 + 9]:
                if self.valid(self.game, self.game.cat_user, self.game.cat2, target):
                    return False
            for target in [self.game.cat3 + 7, self.game.cat3 + 9]:
                if self.valid(self.game, self.game.cat_user, self.game.cat3, target):
                    return False
            for target in [self.game.cat4 + 7, self.game.cat4 + 9]:
                if self.valid(self.game, self.game.cat_user, self.game.cat4, target):
                    return False
            return True

    def valid(self, game, player, origin, target):
        origin = int(origin)
        target = int(target)

        if origin == game.cat1 or origin == game.cat2 or origin == game.cat3 or origin == game.cat4 or origin == game.mouse:
            if origin == game.mouse and player == game.mouse_user:
                if target == origin - 9 or target == origin - 7 or target == origin + 7 or target == origin + 9 or target == origin:
                    if int(target / 8) != int(origin / 8) - 1 and int(target / 8) != int(origin / 8) + 1:
                        return False
                    if target < 64:
                        return True
                return False

            elif player == game.cat_user:
                if target == origin + 7 or target == origin + 9 or target == origin:
                    if int(target / 8) != int(origin / 8) + 1:
                        return False
                    if target < 64:
                        return True

        return False

    def valid_nogame(self, target, origin):
        if target == origin - 9 or target == origin - 7 or target == origin + 7 or target == origin + 9 or target == origin:
            if int(target / 8) == int(origin / 8) and target != origin:
                return False
            if target < 64:
                return True

        return False


COUNTER_ERROR = "Insert not allowed|Inseción no permitida"


class CounterManager(models.Manager):

    def create(self, *args, **kwargs):
        raise ValidationError(COUNTER_ERROR)

    @classmethod
    def __createCounter(cls, int):
        counter = Counter(value=int)
        super(Counter, counter).save()
        return counter

    def inc(self):
        try:
            c = Counter.objects.all()[0]

        except IndexError:
            c = CounterManager.__createCounter(1)
            return c.value

        c.value += 1
        super(Counter, c).save()
        return c.value

    def get_current_value(self):
        try:
            c = Counter.objects.all()[0]

        except IndexError:
            c = CounterManager.__createCounter(0)

        return c.value


class Counter(models.Model):
    value = models.IntegerField(default=0)
    objects = CounterManager()

    def save(self, *args, **kwargs):
        raise ValidationError(COUNTER_ERROR)
