from django.db import models

# Aux model for KDKanji that makes it easier to grab the related kanji
# The Visual Closeness auxillery model that defines a numerical "visual closeness" between two kanji
class VisualCloseness(models.Model):

    # The first, base kanji
    left = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'vcloseness')
    # The second, related kanji
    right = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'vrelated')

    # Stroke Edit Distance which measures the OVERALL visual closeness between the left/right kanji with expected values 0.000 through 1.000
    # Closeness value as defined in "strokeEditDistance.csv"
    sed = models.DecimalField(max_digits = 4, decimal_places = 3)
    
    # "yenAndLi" which measures the RADICAL closeness between the left/right kanji with expected values 0.000 through 1.000
    # Closeness value as defined in "yehAndLiRadical.csv"
    # ynl = models.DecimalField(max_digits = 4, decimal_places = 3)

    def __str__(self):
        return f'{self.left.kanji}-{self.right.kanji} sed: {self.sed}'
