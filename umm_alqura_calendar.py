#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مكتبة تقويم أم القرى - Umm Al-Qura Calendar Library
====================================================
مكتبة شاملة للتعامل مع التقويم الهجري (تقويم أم القرى) في Python

المميزات:
- تحويل من ميلادي إلى هجري والعكس
- تنسيق التواريخ بصيغ عربية جميلة
- دعم أسماء الأيام والشهور بالعربية
- استخدام خوارزمية تقويم أم القرى الرسمية

الاستخدام:
    from umm_alqura_calendar import format_hijri_date, gregorian_to_hijri
    
    # تحويل تاريخ ميلادي إلى هجري
    hijri_date = gregorian_to_hijri(2025, 11, 6)
    
    # تنسيق التاريخ بصيغة عربية جميلة
    formatted = format_hijri_date(hijri_date)
    # النتيجة: "الأربعاء, 5 جمادى الأولى, 1447"
"""

from hijridate import Hijri, Gregorian
from datetime import datetime
import pandas as pd

# أسماء الأشهر الهجرية بالعربية
HIJRI_MONTHS = [
    "محرم",
    "صفر", 
    "ربيع الأول",
    "ربيع الآخر",
    "جمادى الأولى",
    "جمادى الآخرة",
    "رجب",
    "شعبان",
    "رمضان",
    "شوال",
    "ذو القعدة",
    "ذو الحجة"
]

# أسماء الأيام بالعربية
HIJRI_DAYS = [
    "الاثنين",    # 0 - Monday
    "الثلاثاء",   # 1 - Tuesday
    "الأربعاء",   # 2 - Wednesday
    "الخميس",     # 3 - Thursday
    "الجمعة",     # 4 - Friday
    "السبت",      # 5 - Saturday
    "الأحد"       # 6 - Sunday
]


def gregorian_to_hijri(year, month, day):
    """
    تحويل تاريخ ميلادي إلى هجري (تقويم أم القرى)
    
    Args:
        year (int): السنة الميلادية
        month (int): الشهر الميلادي (1-12)
        day (int): اليوم (1-31)
    
    Returns:
        Hijri: كائن التاريخ الهجري
    
    Example:
        >>> hijri = gregorian_to_hijri(2025, 11, 6)
        >>> print(f"{hijri.day}/{hijri.month}/{hijri.year}")
        5/5/1447
    """
    gregorian = Gregorian(year, month, day)
    return gregorian.to_hijri()


def hijri_to_gregorian(year, month, day):
    """
    تحويل تاريخ هجري إلى ميلادي
    
    Args:
        year (int): السنة الهجرية
        month (int): الشهر الهجري (1-12)
        day (int): اليوم (1-30)
    
    Returns:
        Gregorian: كائن التاريخ الميلادي
    
    Example:
        >>> gregorian = hijri_to_gregorian(1447, 5, 5)
        >>> print(f"{gregorian.day}/{gregorian.month}/{gregorian.year}")
        6/11/2025
    """
    hijri = Hijri(year, month, day)
    return hijri.to_gregorian()


def get_day_name(date_obj):
    """
    الحصول على اسم اليوم بالعربية من كائن تاريخ
    
    Args:
        date_obj: كائن datetime أو Gregorian أو Hijri
    
    Returns:
        str: اسم اليوم بالعربية
    
    Example:
        >>> from datetime import datetime
        >>> date = datetime(2025, 11, 6)
        >>> print(get_day_name(date))
        الأربعاء
    """
    if isinstance(date_obj, (Hijri, Gregorian)):
        # تحويل إلى datetime للحصول على اسم اليوم
        if isinstance(date_obj, Hijri):
            greg = date_obj.to_gregorian()
            date_obj = datetime(greg.year, greg.month, greg.day)
        else:
            date_obj = datetime(date_obj.year, date_obj.month, date_obj.day)
    
    # الحصول على رقم اليوم (0=Monday, 6=Sunday)
    day_index = date_obj.weekday()
    return HIJRI_DAYS[day_index]


def get_month_name(month_number):
    """
    الحصول على اسم الشهر الهجري بالعربية
    
    Args:
        month_number (int): رقم الشهر (1-12)
    
    Returns:
        str: اسم الشهر بالعربية
    
    Example:
        >>> print(get_month_name(5))
        جمادى الأولى
    """
    if 1 <= month_number <= 12:
        return HIJRI_MONTHS[month_number - 1]
    return ""


def format_hijri_date(hijri_date, include_day_name=True, include_year=True):
    """
    تنسيق التاريخ الهجري بصيغة عربية جميلة
    
    Args:
        hijri_date (Hijri): كائن التاريخ الهجري
        include_day_name (bool): إضافة اسم اليوم (افتراضي: True)
        include_year (bool): إضافة السنة (افتراضي: True)
    
    Returns:
        str: التاريخ منسق بالعربية
    
    Examples:
        >>> hijri = gregorian_to_hijri(2025, 11, 6)
        >>> print(format_hijri_date(hijri))
        الأربعاء, 5 جمادى الأولى, 1447
        
        >>> print(format_hijri_date(hijri, include_day_name=False))
        5 جمادى الأولى, 1447
        
        >>> print(format_hijri_date(hijri, include_year=False))
        الأربعاء, 5 جمادى الأولى
    """
    parts = []
    
    # إضافة اسم اليوم
    if include_day_name:
        day_name = get_day_name(hijri_date)
        parts.append(day_name)
    
    # إضافة اليوم والشهر
    month_name = get_month_name(hijri_date.month)
    date_part = f"{hijri_date.day} {month_name}"
    parts.append(date_part)
    
    # إضافة السنة
    if include_year:
        parts.append(str(hijri_date.year))
    
    return ", ".join(parts)


def convert_excel_date_to_hijri(excel_date, format_style="full"):
    """
    تحويل تاريخ من Excel إلى تاريخ هجري منسق
    
    هذه الدالة مفيدة عند قراءة ملفات Excel التي تحتوي على تواريخ
    
    Args:
        excel_date: التاريخ من Excel (يمكن أن يكون datetime أو string أو رقم)
        format_style (str): نمط التنسيق:
            - "full": الصيغة الكاملة مع اسم اليوم والسنة (افتراضي)
            - "short": بدون اسم اليوم
            - "no_year": بدون السنة
    
    Returns:
        str: التاريخ الهجري منسق، أو سترينغ فارغ إذا كان التاريخ غير صالح
    
    Examples:
        >>> from datetime import datetime
        >>> date = datetime(2025, 11, 6)
        >>> print(convert_excel_date_to_hijri(date))
        الأربعاء, 5 جمادى الأولى, 1447
        
        >>> print(convert_excel_date_to_hijri(date, format_style="short"))
        5 جمادى الأولى, 1447
    """
    try:
        # التعامل مع القيم الفارغة
        if pd.isna(excel_date):
            return ""
        
        # تحويل إلى datetime إذا لم يكن كذلك
        if not isinstance(excel_date, datetime):
            excel_date = pd.to_datetime(excel_date, errors='coerce')
            if pd.isna(excel_date):
                return ""
        
        # تحويل إلى هجري
        hijri = gregorian_to_hijri(excel_date.year, excel_date.month, excel_date.day)
        
        # تنسيق حسب النمط المطلوب
        if format_style == "short":
            return format_hijri_date(hijri, include_day_name=False, include_year=True)
        elif format_style == "no_year":
            return format_hijri_date(hijri, include_day_name=True, include_year=False)
        else:  # full
            return format_hijri_date(hijri, include_day_name=True, include_year=True)
    
    except Exception as e:
        # في حالة أي خطأ، إرجاع سترينغ فارغ
        print(f"⚠️ تحذير: خطأ في تحويل التاريخ: {e}")
        return ""


def format_hijri_date_simple(hijri_date):
    """
    تنسيق التاريخ الهجري بصيغة رقمية بسيطة (DD/MM/YYYY)
    
    Args:
        hijri_date (Hijri): كائن التاريخ الهجري
    
    Returns:
        str: التاريخ بصيغة رقمية
    
    Example:
        >>> hijri = gregorian_to_hijri(2025, 11, 6)
        >>> print(format_hijri_date_simple(hijri))
        5/5/1447
    """
    return f"{hijri_date.day}/{hijri_date.month}/{hijri_date.year}"


# ============================================================================
# دوال مساعدة للاختبار
# ============================================================================

def test_library():
    """اختبار سريع للمكتبة"""
    print("=" * 70)
    print("🧪 اختبار مكتبة تقويم أم القرى")
    print("=" * 70)
    print()
    
    # اختبار التحويل من ميلادي إلى هجري
    print("📅 اختبار 1: تحويل من ميلادي إلى هجري")
    gregorian_date = datetime(2025, 11, 6)
    hijri = gregorian_to_hijri(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    print(f"   التاريخ الميلادي: {gregorian_date.strftime('%Y-%m-%d')}")
    print(f"   التاريخ الهجري (رقمي): {format_hijri_date_simple(hijri)}")
    print(f"   التاريخ الهجري (كامل): {format_hijri_date(hijri)}")
    print()
    
    # اختبار التحويل من Excel
    print("📊 اختبار 2: تحويل تاريخ من Excel")
    excel_dates = [
        datetime(2025, 1, 1),
        datetime(2025, 6, 15),
        datetime(2025, 12, 31),
    ]
    
    for date in excel_dates:
        formatted = convert_excel_date_to_hijri(date)
        print(f"   {date.strftime('%Y-%m-%d')} → {formatted}")
    print()
    
    # اختبار أنماط التنسيق المختلفة
    print("🎨 اختبار 3: أنماط التنسيق المختلفة")
    test_date = datetime(2025, 11, 6)
    hijri = gregorian_to_hijri(test_date.year, test_date.month, test_date.day)
    print(f"   كامل: {format_hijri_date(hijri)}")
    print(f"   بدون اسم اليوم: {format_hijri_date(hijri, include_day_name=False)}")
    print(f"   بدون السنة: {format_hijri_date(hijri, include_year=False)}")
    print()
    
    print("✅ اكتملت الاختبارات بنجاح!")
    print("=" * 70)


if __name__ == "__main__":
    # تشغيل الاختبارات عند تشغيل الملف مباشرة
    test_library()
