
## 🚀 Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 6.0 | Backend MVC Framework |
| SQLite | Built-in | Relational Database (Development) |
| HTML5/CSS3 | — | Frontend User Interfaces |
| JavaScript | ES6+ | Client-side Interactivity |
| Font Awesome | 6.x | UI Iconography |
| Google Gemini API | 2.5 Flash | AI-powered Injury Analysis |

## 📋 User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Student** | Register, respond to invitations, confirm return, report injuries, use AI analysis, view digital card |
| **Service Manager** | Approve registrations, receive competition notifications, send invitations, generate reports |
| **Department Head** | View approved students, monitor absences, access AI injury insights |
| **Vice President** | View students and justified absences, receive final competition reports |

## 🔄 System Workflow

1. **Student Registration** → Student submits personal info, activity category, schedule
2. **Service Manager Review** → Approves registration; system auto-creates user account
3. **Competition Submission** → Official submits competition via public form
4. **Invitation Dispatch** → System auto-identifies eligible students and sends invitations
5. **Student Response** → Accept or decline participation
6. **Absence Registration** → System auto-generates justified absence records
7. **Return Confirmation** → Student confirms return and reports health status
8. **AI Injury Analysis** → System analyzes uploaded medical documents
9. **Reporting** → Department Head and VP access real-time dashboards

## 🤖 AI-Powered Injury Analysis

Upon returning from a competition, students can:

- Upload medical images (X-rays, reports)
- Provide text description of injury
- Receive structured AI analysis including:
  - Injury type and severity percentage
  - Required rest days
  - Rehabilitation exercises
  - Nutritional advice
  - Return prediction timeline
  - Medical warnings
  - Academic impact assessment

## 🗄️ Database Models

```python
class Student(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=5)
    category = models.CharField(max_length=20)  # sports/cultural
    activity_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')

class Competition(models.Model):
    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

class Participation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')

class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    is_justified = models.BooleanField(default=True)
    injury_status = models.CharField(max_length=20, null=True, blank=True)
