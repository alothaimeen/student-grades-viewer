# Student Grades Viewer - AI Coding Instructions

## Project Overview
Static web app for searching student grades by ID number. Built for Arabic-speaking schools with **dual-period grading system** (period1 + period2) and behavioral notes. Deployed via GitHub Pages with automated updates.

## Architecture

### Data Flow
```
Excel files → Python converters → JSON → Static HTML/JS → GitHub Pages
الفترة 1.xlsx → convert_excel_to_json.py → period1.json
‏‏الفترة 2.xlsx → convert_excel_to_json_period2.py → period2.json
الملاحظات.xlsx → convert_notes_to_json.py → notes.json
Current date/time → save_update_date.py → last_update.json
```

### Key Components
- **`index.html`**: Main student search (by ID number), fetches both period JSONs + notes + last update date
- **`admin.html`**: Admin interface with password protection, search by student name
- **Python converters**: Transform Excel → JSON with Arabic text normalization
- **`save_update_date.py`**: Saves current update timestamp in both Gregorian and Hijri calendars
- **`umm_alqura_calendar.py`**: Hijri (Islamic) calendar conversion library for date formatting

## Critical Workflows

### Update Data Workflow
**Primary method**: Use `update_all.ps1` (PowerShell) or `update_all.bat` (Batch)
- Converts all 3 Excel files → JSON automatically
- Commits changes to `main` branch
- Merges to `gh-pages` branch for deployment
- **Deployment time**: 1-2 minutes after push

**Individual updates**: Use specific scripts (`update.ps1`, `update_period2.ps1`, `update_notes.ps1`)

### Deployment
- Uses dual-branch strategy: `main` (development) + `gh-pages` (production)
- `deploy.ps1`: Automated deployment script
- Live URL: `https://alothaimeen.github.io/student-grades-viewer/`

## Arabic Text Handling (CRITICAL)

### Name Normalization Pattern
Used across Python and JavaScript to match student names:
```javascript
function normalizeArabicName(name) {
    return name
        .trim()                         // Remove whitespace
        .replace(/\s+/g, ' ')           // Normalize multiple spaces
        .replace(/[ًٌٍَُِّْ]/g, '');    // Remove Arabic diacritics
}
```

**Python equivalent** in `convert_notes_to_json.py` and test files - must stay synchronized.

### Excel Column Names
All Excel columns use **Arabic names**:
- `الهوية` (ID), `الطالب` (Student name), `الصف` (Grade/class)
- `الواجبات` (Homework), `أنشطة` (Activities), `تطبيقات صفية` (Classwork)
- `المشاركة` (Participation), `الاختبار التحريري` (Written test), `الشفوي` (Oral test)
- `مجموع الغياب` (Total absence)

**When modifying converters**, preserve exact column name matching including Arabic characters.

## Project-Specific Conventions

### File Naming
- Excel files have **Arabic names with special characters**: `الفترة 1.xlsx`, `‏‏الفترة 2.xlsx`, `الملاحظات.xlsx`
- JSON outputs use **English names**: `period1.json`, `period2.json`, `notes.json`, `last_update.json`
- Scripts use descriptive English: `convert_excel_to_json.py`, `update_all.ps1`, `save_update_date.py`

### PowerShell vs Batch Scripts
Maintain **both** PowerShell (`.ps1`) and Batch (`.bat`) versions for Windows compatibility:
- PowerShell: Modern, better error handling, colored output
- Batch: Fallback for restricted environments

### JSON Data Structure
Period JSON structure (each student object):
```json
{
  "الرقم التسلسلي": 1,
  "الهوية": 1159456654,
  "الصف": 5,
  "الطالب": "الاسم الكامل",
  "مجموع الغياب": 8,
  "الواجبات": 1,
  "أنشطة": 3,
  "تطبيقات صفية": 3,
  "المشاركة": 0,
  "الاختبار التحريري": 2,
  "الشفوي": 0,
  "المجموع": 9
}
```

Notes JSON groups by student name with array of violations.

### Hijri Calendar Integration
`umm_alqura_calendar.py` provides official Saudi Hijri calendar conversion:
- Uses `hijridate` library (see `requirements.txt`)
- Converts Excel dates → formatted Arabic Hijri dates
- Format: `"الأربعاء, 5 جمادى الأولى, 1447"`
- Called by `convert_notes_to_json.py` for date formatting

## Testing

### Manual Testing
- `test_matching.py`: Tests Arabic name normalization between period data and notes
- `test_notes.html`: Browser-based test for notes display
- Live preview: Use Python's `http.server` or VS Code Live Server

### Deployment Verification
After pushing updates:
1. Wait 1-2 minutes for GitHub Actions
2. Check live site: `https://alothaimeen.github.io/student-grades-viewer/`
3. Test search with known student IDs from `period1.json`

## Common Gotchas

1. **Excel file encoding**: Files must be UTF-8 compatible. If conversion fails, check for corrupted Arabic characters.
2. **PowerShell execution policy**: If `.ps1` scripts don't run, user may need: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
3. **Branch sync**: Always merge `main` → `gh-pages` for deployments (automated in `deploy.ps1`)
4. **JSON caching**: Admin search uses cache-busting (`?v=timestamp`) for notes.json to force refresh
5. **Student ID matching**: Uses exact integer match on `الهوية` field, not string comparison

## Key Files Reference
- Update workflow: `QUICK_UPDATE_GUIDE.md`, `UPDATE_GUIDE.md`
- Admin features: `ADMIN_GUIDE.md`
- Hijri calendar: `UMM_ALQURA_GUIDE.md`, `HIJRI_UPDATE.md`
- Notes feature: `NOTES_GUIDE.md`
- Last update feature: `LAST_UPDATE_FEATURE.md`
