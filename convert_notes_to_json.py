#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحويل ملف الملاحظات السلوكية من Excel إلى JSON
يقرأ ملف "الملاحظات.xlsx" ويحوله إلى "notes.json"
"""

import pandas as pd
import json
import os
from pathlib import Path
import re

def normalize_name(name):
    """
    تنظيف وتوحيد الأسماء العربية للمطابقة الصحيحة
    - إزالة المسافات الزائدة
    - توحيد المسافات المتعددة
    - إزالة التشكيل (اختياري)
    """
    if pd.isna(name):
        return ""
    
    name = str(name).strip()
    # توحيد المسافات المتعددة إلى مسافة واحدة
    name = re.sub(r'\s+', ' ', name)
    # إزالة التشكيل العربي
    name = re.sub(r'[ًٌٍَُِّْ]', '', name)
    
    return name

def convert_excel_to_json():
    """تحويل ملف Excel الملاحظات إلى JSON"""
    
    # المسار الحالي للسكريبت
    script_dir = Path(__file__).parent
    
    # مسارات الملفات
    excel_file = script_dir / "الملاحظات.xlsx"
    json_file = script_dir / "notes.json"
    
    print("🔄 جاري تحويل ملف الملاحظات من Excel إلى JSON...")
    print(f"📂 قراءة الملف: {excel_file.name}")
    
    # التحقق من وجود الملف
    if not excel_file.exists():
        print(f"❌ خطأ: الملف '{excel_file.name}' غير موجود!")
        print(f"📍 تأكد من وجود الملف في المجلد: {script_dir}")
        print("💡 الملف المتوقع يجب أن يحتوي على الأعمدة التالية:")
        print("   - م (الرقم التسلسلي)")
        print("   - اسم الطالب")
        print("   - التاريخ")
        print("   - المشكلة")
        print("   - الصف")
        print("   - الإجراء")
        return False
    
    try:
        # قراءة ملف Excel
        # نحدد header=1 لأن الصف الأول عنوان والصف الثاني يحتوي على أسماء الأعمدة
        df = pd.read_excel(excel_file, header=1)
        
        # عرض معلومات الملف
        print(f"✅ تم قراءة الملف بنجاح!")
        print(f"📊 عدد الملاحظات: {len(df)}")
        print(f"📋 الأعمدة الموجودة: {', '.join(df.columns.tolist())}")
        print()
        
        # تنظيف البيانات
        print("🧹 جاري تنظيف البيانات...")
        
        # التحقق من وجود الأعمدة المطلوبة
        required_columns = ['اسم الطالب', 'المشكلة']
        for col in required_columns:
            if col not in df.columns:
                print(f"❌ خطأ: العمود '{col}' غير موجود في الملف!")
                print(f"الأعمدة الموجودة: {', '.join(df.columns.tolist())}")
                return False
        
        # تنظيف الأسماء
        if 'اسم الطالب' in df.columns:
            df['اسم الطالب'] = df['اسم الطالب'].apply(normalize_name)
            print(f"   ✓ تم تنظيف أسماء الطلاب")
        
        # تحويل التاريخ إلى نص (لتجنب مشاكل التنسيق)
        if 'التاريخ' in df.columns:
            # تحويل التاريخ مع معالجة القيم الفارغة والخاطئة
            df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
            df['التاريخ'] = df['التاريخ'].apply(
                lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else ''
            )
            print(f"   ✓ تم تنسيق التواريخ")
        
        # إزالة الصفوف الفارغة
        df = df.dropna(subset=['اسم الطالب', 'المشكلة'], how='all')
        print(f"   ✓ تم إزالة الصفوف الفارغة")
        
        # إنشاء البيانات المنظمة
        notes_data = []
        for idx, row in df.iterrows():
            note = {
                "اسم_الطالب": normalize_name(row.get('اسم الطالب', '')),
                "التاريخ": row.get('التاريخ', ''),
                "المشكلة": str(row.get('المشكلة', '')).strip(),
                "الصف": int(row.get('الصف', 0)) if pd.notna(row.get('الصف')) else None,
                "الإجراء": str(row.get('الإجراء', '')).strip() if pd.notna(row.get('الإجراء')) else ""
            }
            
            # إضافة الملاحظة فقط إذا كان لها اسم طالب ومشكلة
            if note["اسم_الطالب"] and note["المشكلة"]:
                notes_data.append(note)
        
        print(f"📝 عدد الملاحظات الصالحة: {len(notes_data)}")
        
        # إحصائيات إضافية
        if notes_data:
            unique_students = len(set(note["اسم_الطالب"] for note in notes_data))
            print(f"👥 عدد الطلاب المذكورين: {unique_students}")
            
            # عرض نماذج من الطلاب
            print("\n📌 نماذج من الطلاب:")
            sample_students = list(set(note["اسم_الطالب"] for note in notes_data))[:5]
            for student in sample_students:
                student_notes_count = sum(1 for note in notes_data if note["اسم_الطالب"] == student)
                print(f"   - {student} ({student_notes_count} ملاحظة)")
        
        # حفظ البيانات كـ JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(notes_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 تم حفظ الملف: {json_file.name}")
        print(f"✨ تم التحويل بنجاح! 🎉")
        
        return True
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التحويل: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 70)
    print("📋 برنامج تحويل الملاحظات السلوكية من Excel إلى JSON")
    print("=" * 70)
    print()
    
    success = convert_excel_to_json()
    
    print()
    print("=" * 70)
    
    if success:
        print("✅ اكتمل التحويل بنجاح!")
        print("💡 يمكنك الآن استخدام ملف notes.json في الموقع")
        print("🔗 ملاحظة: تأكد من تحديث الموقع ليستخدم ملف الملاحظات الجديد")
    else:
        print("⚠️ فشل التحويل، راجع الأخطاء أعلاه")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
