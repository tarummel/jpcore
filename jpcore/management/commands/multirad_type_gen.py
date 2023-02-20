import json
from django.core.management.base import BaseCommand

from jpcore.models import Radical

class Command(BaseCommand):

    def handle(self, *args, **options):
        data = {}
        freq_threshold = 45
        topQuery = Radical.objects.filter(position__in = ["top"], frequency__gte = freq_threshold).values_list("strokes", "radical").order_by("strokes")
        leftQuery = Radical.objects.filter(position__in = ["left"], frequency__gte = freq_threshold).values_list("strokes", "radical").order_by("strokes")
        encloseQuery = Radical.objects.filter(position__in = ["enclose", "top left", "bottom left"], frequency__gte = freq_threshold).values_list("strokes", "radical").order_by("strokes")
        infreqQuery = Radical.objects.filter(frequency__lt = freq_threshold).values_list("strokes", "radical").order_by("strokes")
        rightQuery = Radical.objects.all().values_list("strokes", "radical").order_by("strokes")

        m = rightQuery.difference(topQuery)
        n = m.difference(leftQuery)
        o = n.difference(encloseQuery)
        right = o.difference(infreqQuery).order_by("strokes")

        data["t"] = self.tuplesToArray(topQuery)
        data["l"] = self.tuplesToArray(leftQuery)
        data["e"] = self.tuplesToArray(encloseQuery)
        data["unc"] = self.tuplesToMap(infreqQuery)
        data["r"] = self.tuplesToMap(right)

        f = open("./jpcore/management/generated/multirad_output.txt", "w")
        f.write(json.dumps(data))
        f.close()

    def tuplesToArray(self, queryset):
        output = []
        for tuple in queryset.iterator():
            output.append(tuple[1])
        return output
    
    def tuplesToMap(self, queryset):
        output = {}
        for row in queryset.iterator():
            strokes, radical = row[0], row[1]
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(radical)
        return output
