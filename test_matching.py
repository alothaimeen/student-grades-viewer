import json
import re

# دالة التنظيف من JavaScript
def normalizeArabicName(name):
    if not name:
        return ''
    
    name = str(name).strip()
    # توحيد المسافات المتعددة
    name = re.sub(r'\s+', ' ', name)
    # إزالة التشكيل العربي
    name = re.sub(r'[ًٌٍَُِّْ]', '', name)
    
    return name

# قراءة البيانات
with open('period1.json', 'r', encoding='utf-8') as f:
    students = json.load(f)

with open('notes.json', 'r', encoding='utf-8') as f:
    notes = json.load(f)

# البحث عن الطالب
student_id = 1152684930
student = next((s for s in students if s['الهوية'] == student_id), None)

if student:
    print(f"الطالب في ملف الدرجات:")
    print(f"  الاسم: '{student['الطالب']}'")
    print(f"  الاسم المنظف: '{normalizeArabicName(student['الطالب'])}'")
    print()
    
    # البحث عن الملاحظات
    student_name = normalizeArabicName(student['الطالب'])
    student_notes = [n for n in notes if normalizeArabicName(n['اسم_الطالب']) == student_name]
    
    print(f"عدد الملاحظات المطابقة: {len(student_notes)}")
    print()
    
    # فحص أول 3 ملاحظات
    if student_notes:
        print("أول 3 ملاحظات:")
        for i, note in enumerate(student_notes[:3], 1):
            print(f"  {i}. {note['المشكلة']} - {note['التاريخ']}")
    
    # فحص المطابقة
    print("\n=== فحص المطابقة ===")
    for note in notes[:5]:
        note_name = normalizeArabicName(note['اسم_الطالب'])
        match = note_name == student_name
        if 'ناصر' in note_name:
            print(f"ملاحظة: '{note['اسم_الطالب']}'")
            print(f"  منظف: '{note_name}'")
            print(f"  مطابق: {match}")
