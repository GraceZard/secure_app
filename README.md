# Secure App

A small Django-based secure e-commerce example application with accounts, inventory, cart, and auditing components.

## Features

- User registration, login and profile management
- Inventory management (items, images, categories)
- Shopping cart and checkout flow
- Order history and audit logging

## Requirements

- Python 3.8+ (use the version in your environment)
- See `requirements.txt` for exact Python package pins

## Quick start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. (Optional) Create a superuser to access the admin:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Tests

Run the project's tests with:

```bash
python manage.py test
```
## Media / Product images

Product images are stored under `media/` and `product_images/` in the project workspace. When running locally, Django serves these files only in `DEBUG=True`.

## Notes

- This project is intended as an example and learning resource. Before deploying to production, review settings in `secure_app/settings.py`, especially `DEBUG`, `ALLOWED_HOSTS`, database, and static/media handling.
- Configure a proper production-ready database, static file serving, and media storage for deployments.

## Contributing

If you'd like to contribute, fork the repo, make changes on a feature branch, add tests, and submit a pull request.

## License

See repository or project owner for license information.
# secure_app
SSD PROJECT
