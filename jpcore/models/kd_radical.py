from django.db import models


class KDRadical(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdradical')

    # The radical number, in the range 1 to 214.     
    classical = models.TextField()
    nelson = models.TextField()

    def __str__(self):
        return f'classical: {self.classical}, nelson: {self.nelson}, names: {self.names}'
