"""
دوال معالجة التشكيل في العربية
مبنية على منطق موقع Saheh بالكامل
"""

import re

# ========================================
# رموز التشكيل في العربية (Unicode)
# ========================================
ARABIC_DIACRITICS = {
    'shadda': '\u0651',           # الشدة (ّ)
    'tanween_fatha': '\u064B',    # تنوين فتح (ً)
    'tanween_damma': '\u064C',    # تنوين ضم (ٌ)
    'tanween_kasra': '\u064D',    # تنوين كسر (ٍ)
    'fatha': '\u064E',            # فتحة (َ)
    'damma': '\u064F',            # ضمة (ُ)
    'kasra': '\u0650',            # كسرة (ِ)
    'sukun': '\u0652',            # سكون (ْ)
    'alif_khanjari': '\u0670',    # ألف خنجرية
    'madda': '\u0653',            # مدة
    'hamza_above': '\u0654',
    'hamza_below': '\u0655',
    'sila': '\u0670',
    'alif_wasl': '\u0671',
    'wasla_small': '\u06E1'
}

# ========================================
# الحروف الشمسية
# ========================================
SHAMSI_LETTERS = 'ت ث د ذ ر ز س ش ص ض ط ظ ل ن'

# ========================================
# دوال إزالة التشكيل الأساسية
# ========================================

def remove_diacritics(text, keep_list=None):
    """
    تزيل كل التشكيل ما عدا الذي في keep_list
    """
    if keep_list is None:
        keep_list = []
    
    all_marks = list(ARABIC_DIACRITICS.values())
    marks_to_remove = [mark for mark in all_marks if mark not in keep_list]
    
    if not marks_to_remove:
        return text
    
    pattern = '[' + ''.join(marks_to_remove) + ']'
    text = re.sub(pattern, '', text)
    
    return text

# ========================================
# معالجة التشديد الشمسي
# ========================================

def remove_shamsi_tashdid(text):
    """
    تزيل الشدة من الحروف الشمسية بعد "ال"
    """
    # حالة "ال" العادية
    pattern1 = r'(ال)([' + SHAMSI_LETTERS + r'])\u0651'
    text = re.sub(pattern1, r'\1\2', text)
    
    # حالة "لل" (مثل في "اللَّهُ")
    pattern2 = r'(لل)([' + SHAMSI_LETTERS + r'])\u0651'
    text = re.sub(pattern2, r'\1\2', text)
    
    return text

# ========================================
# معالجة الأسماء الموصولة والكلمات الخاصة
# ========================================

def process_special_words(text):
    """
    معالجة الأسماء الموصولة والكلمات الخاصة
    """
    special_cases = {
        # المفرد
        r'الَّذِي': 'الذي',
        r'الَّتِي': 'التي',
        
        # المثنى المذكر
        r'اللَّذَانِ': 'اللذان',
        r'اللَّذَيْنِ': 'اللذين',
        r'اللَّذَان': 'اللذان',
        r'اللَّذَيْن': 'اللذين',
        
        # المثنى المؤنث
        r'اللَّتَانِ': 'اللتان',
        r'اللَّتَيْنِ': 'اللتين',
        r'اللَّتَان': 'اللتان',
        r'اللَّتَيْن': 'اللتين',
        
        # جمع المذكر
        r'الَّذِينَ': 'الذين',
        r'الَّذِين': 'الذين',
        
        # جمع المؤنث
        r'اللَّاتِي': 'اللاتي',
        r'اللَّوَاتِي': 'اللواتي',
        r'اللَّائِي': 'اللائي',
        
        # كلمة الجلالة
        r'اللَّه': 'الله',
    }
    
    for pattern, replacement in special_cases.items():
        text = re.sub(pattern, replacement, text)
    
    return text

# ========================================
# معالجة الأفعال المبنية للمجهول
# ========================================

def is_majhool_verb(word):
    """تتحقق إذا كانت الكلمة فعلاً مبنياً للمجهول"""
    majhool_patterns = [
        r'^ضُ[عر]', r'^قُ[تل]', r'^أُ[كل]', r'^إُ[كل]',
        r'^حُ[وص]', r'^سُ[مع]', r'^وُ[جد]', r'^كُ[تب]',
    ]
    
    for pattern in majhool_patterns:
        if re.search(pattern, word):
            return True
    return False

def preserve_majhool_damma(text, keep_damma_default=False):
    """تحافظ على ضمة أول الكلمة إذا كانت فعلاً مبنياً للمجهول"""
    if keep_damma_default:
        return text
    
    words = text.split()
    result = []
    
    for word in words:
        if is_majhool_verb(word):
            result.append(word)
        else:
            result.append(word)
    
    return ' '.join(result)

# ========================================
# الدالة الرئيسية الموحدة
# ========================================

def clean_tashkeel(text, 
                   keep_shadda=True,
                   keep_tanween_fatha=True,
                   keep_tanween_damma=True,
                   keep_tanween_kasra=True,
                   keep_fatha=False,
                   keep_damma=False,
                   keep_kasra=False,
                   keep_shamsi=False,
                   keep_majhool=True):
    """
    الدالة الرئيسية لمعالجة التشكيل
    """
    # 1. تجهيز قائمة ما سنحتفظ به
    keep_list = []
    
    if keep_shadda:
        keep_list.append(ARABIC_DIACRITICS['shadda'])
    if keep_tanween_fatha:
        keep_list.append(ARABIC_DIACRITICS['tanween_fatha'])
    if keep_tanween_damma:
        keep_list.append(ARABIC_DIACRITICS['tanween_damma'])
    if keep_tanween_kasra:
        keep_list.append(ARABIC_DIACRITICS['tanween_kasra'])
    if keep_fatha:
        keep_list.append(ARABIC_DIACRITICS['fatha'])
    if keep_damma:
        keep_list.append(ARABIC_DIACRITICS['damma'])
    if keep_kasra:
        keep_list.append(ARABIC_DIACRITICS['kasra'])
    
    # 2. معالجة الكلمات الخاصة أولاً
    text = process_special_words(text)
    
    # 3. إزالة التشكيل غير المرغوب
    text = remove_diacritics(text, keep_list)
    
    # 4. معالجة التشديد الشمسي
    if not keep_shamsi:
        text = remove_shamsi_tashdid(text)
    
    # 5. الحفاظ على ضمة المبني للمجهول
    if keep_majhool:
        text = preserve_majhool_damma(text, keep_damma)
    
    return text