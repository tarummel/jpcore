from django.contrib.postgres.fields import ArrayField
from django.db import models


class KDQueryCode(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdquerycode')
    
    # These codes contain information relating to the glyph, and can be used for finding a required kanji.
    sh_descriptor = models.TextField()
    four_corner = models.TextField()
    deroo = models.TextField()

    # use these for representation, skip_codes for calculations
    skip = models.TextField()

    # SKIP code misclassifications:
	# a mistake in the division of the kanji
    misclass_pos = ArrayField(models.TextField(), blank = True)

    # a mistake in the number of strokes
    misclass_strokes = ArrayField(models.TextField(), blank = True)
    
    # mistakes in both division and strokes
    misclass_strokes_diff = ArrayField(models.TextField(), blank = True)

    # ambiguous stroke counts depending on glyph
    misclass_strokes_pos = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'skip: {self.skip}, sh: {self.sh_descriptor}, 4corner: {self.four_corner}, deroo: {self.deroo}'
