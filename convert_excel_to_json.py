#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحويل ملف Excel إلى JSON
يقرأ ملف "الفترة 1.xlsx" ويحوله إلى "period1.json"
"""

import pandas as pd
import json
import os
from pathlib import Path

def convert_excel_to_json():
    """تحويل ملف Excel إلى JSON"""
    
    # المسار الحالي للسكريبت
    script_dir = Path(__file__).parent
    
    # مسارات الملفات
    excel_file = script_dir / "الفترة 1.xlsx"
    json_file = script_dir / "period1.json"
    
    print("🔄 جاري تحويل ملف Excel إلى JSON...")
    print(f"📂 قراءة الملف: {excel_file.name}")
    
    # التحقق من وجود الملف
    if not excel_file.exists():
        print(f"❌ خطأ: الملف '{excel_file.name}' غير موجود!")
        print(f"📍 تأكد من وجود الملف في المجلد: {script_dir}")
        return False
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        
        # عرض معلومات الملف
        print(f"✅ تم قراءة الملف بنجاح!")
        print(f"📊 عدد الطلاب: {len(df)}")
        print(f"📋 الأعمدة: {', '.join(df.columns.tolist())}")
        
        # تحويل DataFrame إلى قائمة من القواميس
        data = df.to_dict(orient='records')
        
        # حفظ البيانات كـ JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        
        print(f"💾 تم حفظ الملف: {json_file.name}")
        print(f"✨ تم التحويل بنجاح! 🎉")
        
        return True
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التحويل: {str(e)}")
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🎓 برنامج تحويل درجات الطلاب من Excel إلى JSON")
    print("=" * 60)
    print()
    
    success = convert_excel_to_json()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ اكتمل التحويل بنجاح!")
        print("💡 يمكنك الآن استخدام الموقع لعرض الدرجات المحدثة")
    else:
        print("⚠️ فشل التحويل، راجع الأخطاء أعلاه")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
