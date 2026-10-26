# AI-Based-Learning
The AI-based Learning Platform is an educational web app built with Python and Django. Content
creators turn a title and an idea into a learning script, and generate multiple-choice quizzes from
that script, using the OpenAI API. Generated scripts and quizzes can be edited after creation, and
learners can browse every published script.

## Setup

Requires Python 3.10+.

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
copy .env.example .env         # then fill in OPENAI_API_KEY (and DJANGO_SECRET_KEY outside development)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign up or log in.

## Roles

Only users in the **Content Creator** group can create, edit and delete scripts; everyone else is
sent to the script library. Create the group and add users to it from the admin site at `/admin/`.

## Configuration

All secrets are read from environment variables (or a `.env` file). See `.env.example`.

| Variable | Purpose |
| --- | --- |
| `DJANGO_DEBUG` | `True` for local development only |
| `DJANGO_SECRET_KEY` | Required when debug is off |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |
| `OPENAI_API_KEY` | Key used for script and quiz generation |
| `OPENAI_MODEL` | Model name, defaults to `gpt-4o-mini` |

## Tests

```bash
python manage.py test Learn
```
