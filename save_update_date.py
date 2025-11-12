#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت حفظ تاريخ آخر تحديث
يتم تشغيله تلقائياً بعد تحويل الملفات لحفظ تاريخ التحديث الحالي
"""

import json
from datetime import datetime
from umm_alqura_calendar import gregorian_to_hijri, format_hijri_date

def save_update_date():
    """حفظ تاريخ التحديث الحالي (ميلادي وهجري)"""
    
    # الحصول على التاريخ والوقت الحالي
    now = datetime.now()
    
    # التاريخ الميلادي
    gregorian_date = now.strftime("%Y-%m-%d")
    gregorian_time = now.strftime("%H:%M")
    gregorian_full = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # التاريخ الهجري
    hijri = gregorian_to_hijri(now.year, now.month, now.day)
    hijri_date = format_hijri_date(hijri)
    
    # إنشاء البيانات
    update_info = {
        "last_update": {
            "gregorian": {
                "date": gregorian_date,
                "time": gregorian_time,
                "full": gregorian_full,
                "display": f"{gregorian_date} - {gregorian_time}"
            },
            "hijri": {
                "date": hijri_date,
                "display": hijri_date
            },
            "timestamp": int(now.timestamp())
        }
    }
    
    # حفظ في ملف JSON
    with open('last_update.json', 'w', encoding='utf-8') as f:
        json.dump(update_info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم حفظ تاريخ التحديث:")
    print(f"   📅 ميلادي: {gregorian_full}")
    print(f"   🌙 هجري: {hijri_date}")

if __name__ == "__main__":
    try:
        save_update_date()
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        exit(1)
