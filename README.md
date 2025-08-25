# Muranga University Management System

A comprehensive full-stack university management system built with Django REST Framework (backend) and React (frontend). This system handles all aspects of university operations including student management, academic records, attendance tracking, fee management, and library services.

## 🚀 Features

### 📚 Academic Management
- **Faculty & Department Management**: Hierarchical academic structure with deans and heads
- **Course Management**: Programs from Certificate to PhD level
- **Unit Management**: Course units with prerequisites and credit hours
- **Student Enrollment**: Semester-based registration system
- **Academic Calendar**: Year and semester management with deadlines

### 👥 User Management
- **Student Profiles**: Complete academic and personal information
- **Lecturer Management**: Faculty profiles with ranks and specializations
- **Role-based Access**: Different permissions for students, lecturers, and administrators

### 📊 Assessment & Grading
- **Multiple Assessment Types**: CATs, Assignments, Exams with customizable weights
- **Grade Management**: Letter grades with automatic GPA calculation
- **Academic Performance Tracking**: Student progress monitoring
- **Result Processing**: Comprehensive grade analysis

### 📋 Attendance System
- **Session Management**: Structured attendance tracking by week and session type
- **Multiple Session Types**: Lectures, tutorials, practicals, seminars
- **Attendance Analytics**: Real-time attendance rate calculation
- **Lecturer Dashboard**: Easy attendance marking interface

### 💰 Financial Management
- **Fee Structure**: Configurable fee breakdown by course and semester
- **Payment Tracking**: Multiple payment methods with verification
- **Receipt Generation**: Automatic receipt numbering
- **Financial Reports**: Payment history and outstanding balances

### 📖 Library Management
- **Book Catalog**: Comprehensive book database with availability tracking
- **Borrowing System**: Student book loans with due date management
- **Fine Calculation**: Automatic overdue fine computation
- **Library Analytics**: Book utilization and borrowing statistics

## 🛠 Tech Stack

### Backend
- **Django 4.x** - Web framework
- **Django REST Framework** - API development
- **SQLite/PostgreSQL** - Database
- **django-cors-headers** - CORS handling
- **Python 3.8+** - Programming language

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling (optional)

## 📁 Project Structure

```
muranga-university/
├── backend/
│   ├── manage.py
│   ├── backend/                    # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── attendance/                 # Main Django app
│       ├── models.py              # All database models
│       ├── admin.py               # Admin interface configuration
│       ├── serializers.py         # DRF serializers
│       ├── views.py               # API views
│       ├── urls.py                # URL routing
│       └── migrations/            # Database migrations
└── frontend/
    ├── index.html
    ├── .env                       # Environment variables
    ├── package.json
    └── src/
        ├── main.jsx               # App entry point
        ├── App.jsx                # Main app component
        ├── components/            # Reusable components
        ├── pages/                 # Page components
        ├── services/              # API services
        └── utils/                 # Utility functions
```

## 🗄️ Database Models

### Core Academic Models
- **Faculty** - University faculties with deans
- **Department** - Academic departments with heads
- **Course** - Degree programs (Certificate to PhD)
- **Unit** - Course units with prerequisites
- **AcademicYear** & **Semester** - Academic calendar

### User Models
- **Student** - Student profiles with academic status
- **Lecturer** - Faculty member profiles with ranks
- **Enrollment** - Student-unit relationships

### Assessment Models
- **AssessmentType** - Types of assessments (CAT, Assignment, Exam)
- **Assessment** - Specific assessments for units
- **Grade** - Student grades with GPA calculation

### Attendance Models
- **AttendanceSession** - Structured attendance sessions
- **AttendanceRecord** - Individual attendance records

### Financial Models
- **FeeStructure** - Fee breakdown by course/semester
- **FeePayment** - Payment tracking with verification

### Library Models
- **Library** - Library locations
- **Book** - Book catalog with availability
- **BookBorrowing** - Book lending with fines

## 🚦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git
- Virtual environment tool (venv)

### Backend Setup

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd muranga-university
   
   # Create and activate virtual environment
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

3. **Configure Django settings** (backend/settings.py):
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'rest_framework',
       'corsheaders',
       'attendance',  # Your main app
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       # ... other middleware
   ]
   
   CORS_ALLOW_ALL_ORIGINS = True  # For development only
   
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 20
   }
   ```

4. **Run migrations:**
   ```bash
   cd backend
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional):**
   ```bash
   python manage.py loaddata sample_data.json
   ```

7. **Start development server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Create React app (if not exists):**
   ```bash
   npm create vite@latest . -- --template react
   ```

3. **Install dependencies:**
   ```bash
   npm install
   npm install axios react-router-dom
   ```

4. **Configure environment variables:**
   ```bash
   # .env
   VITE_API_BASE_URL=http://127.0.0.1:8000/api
   VITE_ADMIN_URL=http://127.0.0.1:8000/admin
   ```

5. **Start development server:**
   ```bash
   npm run dev
   ```

## 🌐 API Endpoints

### Academic Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/faculties/` | List all faculties |
| GET | `/api/departments/` | List all departments |
| GET | `/api/courses/` | List all courses |
| GET | `/api/units/` | List all units |

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create new student |
| GET | `/api/students/{id}/` | Get student details |
| PUT | `/api/students/{id}/` | Update student |
| DELETE | `/api/students/{id}/` | Delete student |
| GET | `/api/lecturers/` | List all lecturers |

### Assessment & Grades
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/assessments/` | List assessments |
| GET | `/api/grades/` | List grades |
| GET | `/api/students/{id}/grades/` | Student grades |
| GET | `/api/students/{id}/gpa/` | Student GPA |

### Attendance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/attendance-sessions/` | List attendance sessions |
| POST | `/api/attendance-records/` | Mark attendance |
| GET | `/api/units/{id}/attendance/` | Unit attendance report |

### Financial
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/fee-structures/` | List fee structures |
| GET | `/api/payments/` | List payments |
| POST | `/api/payments/` | Record payment |

### Library
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List books |
| GET | `/api/borrowings/` | List borrowings |
| POST | `/api/borrowings/` | Borrow book |

## 🎯 Usage

### Accessing the System
1. **Frontend Application**: http://localhost:5173
2. **Admin Panel**: http://127.0.0.1:8000/admin
3. **API Documentation**: http://127.0.0.1:8000/api

### Admin Dashboard Features
- **Student Management**: Complete CRUD operations
- **Academic Structure**: Faculty, Department, Course management  
- **Attendance Monitoring**: Real-time attendance rates
- **Grade Management**: Assessment and grade processing
- **Financial Tracking**: Fee structure and payment verification
- **Library Operations**: Book catalog and borrowing management

### Student Features
- **Profile Management**: View and update personal information
- **Course Registration**: Enroll in units for semester
- **Grade Viewing**: Check assessment results and GPA
- **Attendance History**: View attendance records
- **Fee Payment**: Check fee structure and payment history
- **Library Access**: Search books and view borrowing history

### Lecturer Features
- **Unit Management**: View assigned units and enrolled students
- **Attendance Marking**: Mark student attendance for sessions
- **Grade Entry**: Record assessment marks and final grades
- **Student Analytics**: View student performance statistics

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Python linting
flake8 backend/
black backend/

# JavaScript linting  
cd frontend
npm run lint
npm run format
```

### Database Management
```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush
```

## 📊 Sample Data

### Academic Structure
- **Faculty of Computing**: Computer Science, IT, Software Engineering
- **Faculty of Business**: Business Administration, Economics, Accounting
- **Faculty of Education**: Primary Education, Secondary Education

### Sample Students
- Student profiles across different courses and years
- Enrollment records for current semester
- Grade history and GPA calculations

### Sample Units
- Core and elective units for each course
- Prerequisites mapping
- Lecturer assignments

## 🚀 Deployment

### Production Setup
1. **Environment Variables:**
   ```bash
   DEBUG=False
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **Static Files:**
   ```bash
   python manage.py collectstatic
   ```

3. **Production Server:**
   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn backend.wsgi:application
   ```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript
- Write tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## 🔒 Security Features

### Authentication & Authorization
- **JWT Token Authentication**: Secure API access
- **Role-based Permissions**: Different access levels for users
- **Session Management**: Secure user sessions
- **Password Security**: Django's built-in password hashing

### Data Protection
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: Django ORM protection
- **CSRF Protection**: Cross-site request forgery protection
- **XSS Prevention**: Output escaping and sanitization

### Access Control
- **Student Access**: Own records and enrolled units only
- **Lecturer Access**: Assigned units and enrolled students
- **Admin Access**: Full system access with audit trails

## 📈 Performance Optimization

### Database Optimization
- **Indexing**: Optimized database indexes for frequent queries
- **Query Optimization**: Select_related and prefetch_related usage
- **Connection Pooling**: Efficient database connections
- **Caching**: Redis/Memcached for frequently accessed data

### API Performance
- **Pagination**: Paginated responses for large datasets
- **Filtering**: Advanced filtering and search capabilities  
- **Compression**: Gzip compression for API responses
- **Rate Limiting**: API rate limiting to prevent abuse

## 📱 Mobile Responsiveness

The frontend is designed to be fully responsive and works seamlessly on:
- **Desktop**: Full feature access with optimal layout
- **Tablet**: Touch-optimized interface with adapted navigation
- **Mobile**: Mobile-first design with essential features accessible

## 🔍 Advanced Features

### Analytics Dashboard
- **Student Performance Analytics**: GPA trends and performance metrics
- **Attendance Analytics**: Unit and course-level attendance rates
- **Financial Analytics**: Fee collection and outstanding balances
- **Library Analytics**: Book utilization and borrowing patterns

### Reporting System
- **Academic Reports**: Transcripts, grade reports, attendance summaries
- **Financial Reports**: Fee statements, payment history, revenue reports
- **Administrative Reports**: Enrollment statistics, performance analytics
- **Export Options**: PDF, Excel, and CSV export capabilities

### Notification System
- **Email Notifications**: Assignment due dates, grade releases, fee reminders
- **SMS Integration**: Critical notifications via SMS
- **In-app Notifications**: Real-time system notifications
- **Bulk Messaging**: Announcements to groups of users

### Integration Capabilities
- **External APIs**: Integration with external services
- **LMS Integration**: Learning Management System connectivity
- **Payment Gateways**: Mobile money and bank integration
- **USSD Support**: Basic operations via USSD codes

## 🛠️ Maintenance & Monitoring

### Logging & Monitoring
- **Application Logs**: Comprehensive logging for debugging
- **Error Tracking**: Automated error reporting and tracking
- **Performance Monitoring**: Response time and resource usage monitoring
- **Health Checks**: System health monitoring endpoints

### Backup & Recovery
- **Automated Backups**: Daily database backups
- **File Backups**: Static file and media backups
- **Recovery Procedures**: Documented recovery processes
- **Disaster Recovery**: Multi-location backup strategy

### System Maintenance
- **Regular Updates**: Security patches and feature updates
- **Database Maintenance**: Regular optimization and cleanup
- **Performance Tuning**: Ongoing performance optimization
- **Capacity Planning**: Scalability assessment and planning

## 📚 Documentation

### API Documentation
- **OpenAPI/Swagger**: Interactive API documentation
- **Postman Collection**: Complete API collection for testing
- **Code Examples**: Sample code for common operations
- **Integration Guides**: Step-by-step integration tutorials

### User Guides
- **Student Manual**: Complete guide for student features
- **Lecturer Guide**: Faculty member user manual
- **Administrator Manual**: System administration guide
- **Quick Start Guide**: Getting started documentation

## 🔄 Version History

### v2.0.0 (Current)
- Complete university management system
- Enhanced attendance tracking
- Financial management integration
- Library management system
- Advanced analytics dashboard

### v1.0.0 (Initial)
- Basic student management
- Simple attendance tracking
- Grade management
- Basic reporting

## 🐛 Known Issues & Limitations

### Current Limitations
- **Single Campus Support**: Currently designed for single campus operation
- **Limited Mobile App**: Web-based responsive design (native apps planned)
- **Basic Workflow**: Advanced approval workflows not implemented
- **Limited Integrations**: External system integrations minimal

### Planned Improvements
- **Multi-campus Support**: Support for multiple university campuses
- **Mobile Applications**: Native iOS and Android apps
- **Advanced Workflows**: Approval processes for various operations
- **AI Integration**: Predictive analytics and intelligent recommendations

## 🆘 Troubleshooting

### Common Issues

**Database Connection Issues**
```bash
# Check database connectivity
python manage.py dbshell

# Reset migrations (development only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

**Frontend Build Issues**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear build cache
npm run build -- --force
```

**Permission Issues**
```bash
# Reset permissions (Linux/Mac)
chmod +x manage.py
sudo chown -R $USER:$USER .

# Windows permissions
icacls . /grant %USERNAME%:F /T
```

### Performance Issues
- **Slow Queries**: Check Django debug toolbar for query optimization
- **Memory Usage**: Monitor memory usage and implement caching
- **Load Testing**: Use tools like Apache Bench or Locust for load testing

## 📞 Support

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check comprehensive documentation
- **Community Forum**: Join discussions and get help
- **Email Support**: technical-support@muranga-university.edu

### Professional Support
- **Training Services**: On-site training for administrators
- **Customization**: Custom feature development
- **Hosting Services**: Managed hosting solutions
- **Maintenance Contracts**: Professional maintenance services

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Open Source Acknowledgments
- **Django**: Web framework
- **React**: Frontend library
- **Bootstrap**: UI components
- **Chart.js**: Data visualization
- **All Contributors**: Community contributors and maintainers

## 🌟 Acknowledgments

- **Muranga University**: For providing the requirements and testing environment
- **Development Team**: Dedicated developers and designers
- **Beta Testers**: Faculty and staff who provided valuable feedback
- **Open Source Community**: For the excellent tools and libraries used

---

**Made By steve  for Muranga University**

*For more information, visit our [documentation site](https://docs.muranga-university.edu) or contact our support team.*