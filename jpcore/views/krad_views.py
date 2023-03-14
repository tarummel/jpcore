from http import HTTPStatus
from django.db import connection
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Kanji, Radical
from jpcore.serializers import RadicalSerializer

RADICALS = ['一', '｜', '丶', 'ノ', '𠂉', '乙', '九', '亅', '二', '亠', '人', '⺅', '𠆢', '儿', '入', 'ハ', '丷', '冂', '冖', '冫', '几', '凵', '刀', '⺉', '力', '勹', '匕', '匚', '亡', '十', '卜', '卩', '厂', '厶', '又', '口', '品', '囗', '土', '士', '夂', '夊', '夕', '大', '女', '子', '宀', '寸', '小', '⺌', '尢', '尤', '尸', '屮', '山', '巛', '川', '工', '已', '巾', '干', '幺', '广', '廴', '廾', '弋', '弓', 'ヨ', '彑', '彡', '彳', '心', '⺖', '戈', '戸', '手', '扌', '支', '攵', '文', '斗', '斤', '方', '无', '無', '日', '曰', '月', '木', '欠', '止', '歹', '殳', '毋', '母', '比', '毛', '氏', '气', '水', '⺡', '火', '⺣', '爪', '父', '爻', '爿', '片', '牙', '牛', '犬', '⺨', '玄', '王', '瓜', '瓦', '甘', '生', '用', '田', '疋', '⽧', '癶', '白', '皮', '皿', '目', '矛', '矢', '石', '示', '⺭', '⽱', '禾', '穴', '立', '竹', '米', '糸', '缶', '⺲', '羊', '羽', '⺹', '而', '耒', '耳', '聿', '肉', '臣', '自', '至', '臼', '舌', '舛', '舟', '艮', '色', '⺾', '虍', '虫', '血', '行', '衣', '⻂', '西', '見', '角', '言', '谷', '豆', '豕', '豸', '貝', '赤', '走', '足', '身', '車', '辛', '辰', '⻌', '邑', '⻏', '酉', '釆', '里', '金', '長', '門', '⻖', '隶', '隹', '雨', '青', '非', '面', '革', '韋', '韭', '音', '頁', '風', '飛', '食', '首', '香', '馬', '骨', '高', '髟', '鬥', '鬯', '鬲', '鬼', '魚', '鳥', '鹵', '鹿', '麦', '麻', '黄', '黍', '黒', '黹', '黽', '鼎', '鼓', '鼠', '鼻', '齊', '斉', '歯', '竜', '亀', '龠', 'マ', 'ユ', '乃', '也', '及', '久', '元', '井', '勿', '五', '屯', '巴', '世', '巨', '冊', '奄', '岡', '免', '啇']
PAGE_LIMIT = 500
NO_KANJI_FIELDS = ['number', 'radical', 'strokes', 'meaning', 'reading', 'frequency', 'position', 'notes']
MAX_RADICALS_LIMIT = 27

def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)

# returns all Radicals
# option 'simple' maps the response to { strokes -> [rad1, rad2, ...] }
@require_GET
def list(request):
    queryset = Radical.objects.all().order_by('strokes')
    
    if request.GET.get('simple', None):
        output = {}
        for row in queryset.iterator():
            strokes, radical = row.strokes, row.radical
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(radical)
        return success(HTTPStatus.OK, output)

    serializer = RadicalSerializer(queryset, many = True, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

# returns the Radical object associated with the radical char
@require_GET
def getByRadical(request, radical):

    if len(radical) != 1:
        return error(HTTPStatus.BAD_REQUEST)
    
    try:
        queryset = Radical.objects.get(radical = radical)
    except:
        return error(HTTPStatus.NOT_FOUND, 'radical not found')
    
    serializer = RadicalSerializer(queryset, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

# returns a list of all viable Radicals from a given comma-delimited list of Radicals
@require_GET
def getRelatedRadicals(request, radicals):

    if len(radicals) > MAX_RADICALS_LIMIT:
        return error(HTTPStatus.BAD_REQUEST, 'either no radicals found or too many provided')

    split = [*set(radicals.split(','))]

    for s in split:
        if len(s) != 1:
            return error(HTTPStatus.BAD_REQUEST, 'one radical between commas only')

    queryset = Radical.objects.filter(
        kanji__in = Kanji.objects.annotate(c = Count('radicals', filter=Q(radicals__radical__in=split))).filter(c = len(split))
    ).exclude(radical__in = split).distinct().order_by('strokes')

    if not len(queryset):
        return error(HTTPStatus.NOT_FOUND, 'no matching entry found')

    if request.GET.get('simple', None):
        output = []
        for row in queryset.iterator():
            output.append(row.radical)

        if request.GET.get('invert', None):
            # list comprehension to preserve order
            output = [e for e in RADICALS if e not in output and e not in split]
        return success(HTTPStatus.OK, output)

    serializer = RadicalSerializer(queryset, many = True, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)
