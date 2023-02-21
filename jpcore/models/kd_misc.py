from django.contrib.postgres.fields import ArrayField
from django.db import models


class KDMisc(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdmisc')

    # The kanji grade level:
    # 1 through 6 indicates a Kyouiku kanji and the grade in which the kanji is taught in Japanese schools. 
    # 8 indicates it is one of the remaining Jouyou Kanji to be learned in junior high school. 
    # 9 indicates it is a Jinmeiyou (for use in names) kanji which in addition to the Jouyou kanji are approved for use 
    #   in family name registers and other official documents. 
    # 10 also indicates a Jinmeiyou kanji which is a variant of a Jouyou kanji.
    grade = models.TextField(blank = True)

    # The (former) Japanese Language Proficiency test level for this kanji. Values range from 1 (most advanced) to 
    # 4 (most elementary). This field does not appear for kanji that were not required for any JLPT level.
	# Note that the JLPT test levels changed in 2010, with a new 5-level system (N1 to N5) being introduced. No official
    # kanji lists are available for the new levels. The new levels are regarded as being similar to the old levels 
    # except that the old level 2 is now divided between N2 and N3.
    jlpt = models.TextField(blank = True)

    # The stroke count of the kanji, including the radical.
    # NOTE: does not contain the common miscounts if listed
    strokes = models.TextField()

    # A frequency-of-use ranking. The 2,500 most-used characters have a ranking; those characters that lack this field 
    # are not ranked. The frequency is a number from 1 to 2,500 that expresses the relative frequency of occurrence of a
    # character in modern Japanese. (Actually there are 2,501 kanji ranked as there was a tie.)
    frequency = models.TextField(blank = True)

    # When the kanji is itself a radical and has a name, this element contains the name (in hiragana.)
    radical_names = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'grade: {self.kanji}, jlpt: {self.jlpt}, strokes: {self.strokes}, freq: {self.frequency}'
