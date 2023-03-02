import json
from django.core.management.base import BaseCommand

from jpcore.models import Radical

class Command(BaseCommand):

    def handle(self, *args, **options):
        data = {}
        freq_threshold = 45
        topQuery = Radical.objects.filter(position__in = ["top"], frequency__gte = freq_threshold).values_list("id", "strokes", "radical").order_by("id")
        encloseQuery = Radical.objects.filter(position__in = ["enclose", "top left", "bottom left"], frequency__gte = freq_threshold).values_list("id", "strokes", "radical").order_by("id")
        leftQuery = Radical.objects.filter(position__in = ["left"], frequency__gte = freq_threshold).values_list("id", "strokes", "radical").order_by("id")
        rightQuery = Radical.objects.all().values_list("id", "strokes", "radical").order_by("id")
        infreqQuery = Radical.objects.filter(frequency__lt = freq_threshold).values_list("id", "strokes", "radical").order_by("id")

        m = rightQuery.difference(topQuery)
        n = m.difference(leftQuery)
        o = n.difference(encloseQuery)
        right = o.difference(infreqQuery).order_by("id")

        data["t"] = self.rowToArray(topQuery)
        data["e"] = self.rowToArray(encloseQuery)
        data["l"] = self.rowToArray(leftQuery)
        data["r"] = self.rowToMap(right)
        data["u"] = self.rowToMap(infreqQuery)

        f = open("./jpcore/management/generated/multirad_output.txt", "w")
        f.write(json.dumps(data))
        f.close()

    def rowToArray(self, queryset):
        output = []
        for tuple in queryset.iterator():
            output.append(tuple[2])
        return output
    
    def rowToMap(self, queryset):
        output = {}
        for row in queryset.iterator():
            strokes, radical = row[1], row[2]
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(radical)
        return output
