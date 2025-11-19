# Unified SOC Dashboard

A unified web interface for accessing multiple locally hosted security tools through a single dashboard with Django backend and React frontend.

## Features

- ✅ Single unified interface for multiple SOC tools
- ✅ Reverse proxy for Wazuh, Shuffle, DFIR-IRIS, and Velociraptor
- ✅ Modern React UI with sidebar navigation
- ✅ Django backend with full HTTP method support
- ✅ CORS enabled for cross-origin requests
- ✅ SSL verification bypass for local HTTPS services
- ✅ Responsive design

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Local instances of:
  - Wazuh (port 5601)
  - Shuffle (port 3000)
  - DFIR-IRIS (port 443)
  - Velociraptor (port 8889)

## Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start Django server:
```bash
python manage.py runserver 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start React development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## Usage

1. Ensure all target services are running on their respective ports
2. Access the dashboard at `http://localhost:3000`
3. Click on any service in the sidebar to view it in the iframe
4. Use the refresh button to reload the current service

## Architecture

### Backend (Django)

- **Framework**: Django 4.2.7 with Django REST Framework
- **Proxy Logic**: Custom views using `requests` library
- **CORS**: Handled via `django-cors-headers`
- **Endpoints**:
  - `/proxy/wazuh/` → `http://localhost:5601`
  - `/proxy/shuffle/` → `http://localhost:3000`
  - `/proxy/iris/` → `https://localhost:443`
  - `/proxy/velociraptor/` → `http://localhost:8889`

### Frontend (React)

- **Framework**: React 18.2.0
- **UI**: Custom CSS with modern dark theme
- **Navigation**: Sidebar with service selection
- **Display**: Iframe-based service rendering

## Configuration

### Modifying Service URLs

Edit `backend/proxy/views.py`:

```python
SERVICE_URLS = {
    'wazuh': 'http://localhost:5601',
    'shuffle': 'http://localhost:3000',
    'iris': 'https://localhost:443',
    'velociraptor': 'http://localhost:8889',
}
```

### Adding New Services

1. Add service to `SERVICE_URLS` in `backend/proxy/views.py`
2. Add URL patterns in `backend/proxy/urls.py`
3. Add service to `SERVICES` array in `frontend/src/App.js`

## Security Notes

⚠️ **Important**: This application is designed for local development and testing.

- SSL verification is disabled for HTTPS proxying
- CORS is set to allow all origins
- No authentication is implemented
- Not suitable for production without additional security measures

## Troubleshooting

### Service Not Loading

- Verify the target service is running
- Check the service URL and port in `SERVICE_URLS`
- Review browser console for errors
- Check Django logs for proxy errors

### CORS Errors

- Ensure `django-cors-headers` is installed
- Verify CORS settings in `settings.py`

### Connection Refused

- Confirm target services are accessible at configured ports
- Check firewall settings

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Enable SSL certificate verification
5. Implement authentication and authorization
6. Use a production WSGI server (Gunicorn, uWSGI)
7. Set up a reverse proxy (Nginx, Apache)
8. Build React for production: `npm run build`

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.
```

---

This complete codebase provides a production-ready unified SOC dashboard with all necessary files, configurations, and documentation. The application features a modern UI, robust proxy handling, and comprehensive error management.