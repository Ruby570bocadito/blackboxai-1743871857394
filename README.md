
Built by https://www.blackbox.ai

---

```markdown
# SocialPhantom

SocialPhantom is a web application built with Flask that allows users to create and manage marketing campaigns, clone websites for testing purposes, and send emails with tracking features. This project is aimed at facilitating the management of various campaign types while providing insightful analytics on their performance.

## Project Overview

The application offers functionality such as:

- Campaign creation and management
- Website cloning
- Email sending with tracking capabilities
- Payload generation for various exploit types
- Comprehensive dashboards for campaign analytics

## Installation

To get started with SocialPhantom, follow the steps below:

1. **Clone the repository**:
   ```bash
   git clone https://your-repo-link.git
   cd your-repo-name
   ```

2. **Create a Python virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root directory and define the following variables:
   ```plaintext
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///app.db
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@example.com
   MAIL_PASSWORD=your_email_password
   ADMIN_EMAIL=admin@example.com
   CLONE_DIR=path_to_clone_directory
   PAYLOAD_DIR=path_to_payload_directory
   ```

5. **Run the application**:
   Use the following command to start the server:
   ```bash
   python run.py
   ```

## Usage

You can access the application by navigating to `http://localhost:5000/` in your web browser. The main features are available through a user-friendly interface, allowing you to create, manage, and analyze your campaigns with ease.

### API Endpoints

Some of the available endpoints include:

- **Campaign Management**:
  - `GET /campaign/` - List all campaigns
  - `POST /campaign/` - Create a new campaign
  - `GET /campaign/<campaign_id>` - Retrieve specific campaign details
  - `PUT /campaign/<campaign_id>/status` - Update campaign status

- **Email Sending**:
  - `POST /email/send` - Send emails for a campaign

- **Web Cloning**:
  - `POST /cloner/clone` - Clone a website

- **Dashboard**:
  - `GET /dashboard/<campaign_id>` - View the dashboard for a specific campaign

## Features

- **User Authentication**: Secure access to campaign features.
- **Campaign Creation**: Create campaigns with custom vectors and targets.
- **Email Tracking**: Send emails with tracking capabilities.
- **Website Cloning**: Clone external websites to analyze and create targeted campaigns.
- **Payload Generation**: Generate payloads for security testing.
- **Dashboard Insights**: Visualize campaign performance with charts and metrics.

## Dependencies

SocialPhantom utilizes several packages for its operation, which are defined in `requirements.txt`. Key dependencies include:

- Flask
- Flask-SQLAlchemy
- Flask-Mail
- Flask-Login
- Selenium
- BeautifulSoup4
- Pandas
- Matplotlib
- python-dotenv

To install these dependencies, ensure to run the command `pip install -r requirements.txt` after activating your Python environment.

## Project Structure

Here’s a brief overview of the project structure:

```
socialphantom/
│
├── app.py               # Main application file
├── config.py            # Configuration settings
├── run.py               # Entry point to start the application
├── requirements.txt     # Required Python packages
│
├── database/            # Contains database-related files
│   ├── __init__.py
│   ├── models.py        # Database models
│
├── scenario_generator.py # Blueprint for scenario generation
├── web_cloner.py        # Blueprint for website cloning features
├── email_sender.py      # Blueprint for email campaign management
├── payload_generator.py  # Blueprint for payload generation features
├── campaign_manager.py   # Blueprint for managing campaigns
└── dashboard.py         # Blueprint for statistics and insights

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

Feel free to customize any section or text to better fit your project description or to provide more specific instructions.