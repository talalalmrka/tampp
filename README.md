# PyTabs — TAMP Server Manager

A lightweight, cross-platform terminal-based server management application built with [Python](https://www.python.org/) and [Textual](https://textual.textualize.io/).

PyTabs provides a unified terminal interface for managing PHP and MariaDB development environments, monitoring server status, accessing configuration files, and working with server resources without constantly switching between terminal commands.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Application Interface](#application-interface)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [PHP Management](#php-management)
- [MariaDB Management](#mariadb-management)
- [Log Viewer](#log-viewer)
- [Configuration](#configuration)
- [Development](#development)
- [Architecture](#architecture)
- [Supported Platforms](#supported-platforms)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

PyTabs is designed to simplify local PHP and MariaDB server management through a modern Terminal User Interface (TUI).

Instead of manually navigating configuration files, checking processes, and remembering multiple commands, PyTabs brings essential server information and management tools together in one application.

The application is built using Textual, providing an interactive interface with tabs, widgets, keyboard navigation, clickable links, and dynamic status indicators.

### Project Goals

- Provide a simple interface for managing PHP and MariaDB.
- Make server configuration accessible and editable.
- Provide quick access to important directories and resources.
- Centralize application and server logs.
- Support multiple operating systems and development environments.
- Keep the application lightweight and easy to extend.

---

## Features

### General

- Modern terminal-based user interface.
- Tab-based navigation.
- Keyboard-driven interaction.
- Interactive widgets and status cards.
- Clickable filesystem paths and URLs.
- Centralized application and server logs.
- Modular and extensible architecture.

### PHP

- Display PHP server information.
- Configure server host and port.
- Display the PHP executable path.
- Display the document root.
- Access PHP configuration files.
- Edit and save `php.ini` directly from the application.
- Quick access to PHP server URLs and related resources.
- Access dashboard and phpMyAdmin.

### MariaDB

- Dedicated MariaDB management interface.
- Access database server information and resources.
- Centralized access to MariaDB-related logs.
- Dedicated controls and configuration interface.

### Application

- Unified PHP and MariaDB status overview.
- Start All and Stop All controls.
- Individual service status indicators.
- Dedicated settings interface.
- Live log viewing.

---

## Screenshots

Screenshots will be added as the interface evolves.

<!-- Add screenshots here.
Example:

![Home Screen](docs/screenshots/home.png)
![PHP Management](docs/screenshots/php.png)
![MariaDB Management](docs/screenshots/mariadb.png)
-->

---

## Application Interface

PyTabs organizes its functionality into five main tabs.

| Tab | Description |
|---|---|
| Log | Displays application and server logs. |
| Home | Provides an overview of PHP and MariaDB services. |
| PHP | Displays PHP server information and configuration. |
| MariaDB | Provides access to MariaDB management. |
| Settings | Contains application settings. |

### Home

The Home tab provides a centralized overview of the managed services.

It includes:

- PHP Server status.
- MariaDB Server status.
- Individual service controls.
- Start All action.
- Stop All action.

Service status indicators:

| Status | Description |
|---|---|
| ON | Service is running. |
| OFF | Service is stopped. |
| PENDING | Service operation is in progress. |

### PHP

The PHP tab provides access to the PHP development server configuration.

It displays information such as:

| Property | Default |
|---|---|
| Host | `0.0.0.0` |
| Port | `8000` |
| Executable | Detected PHP executable |
| Document Root | Configured project directory |
| Dashboard | Dashboard directory |
| Temporary Directory | Temporary files directory |
| Router | PHP router script |
| Log File | PHP server log |
| PID File | PHP server process ID |

Filesystem paths are interactive and can be opened directly.

Available browser links include:

- PHP development server.
- PHP information (`phpinfo()`).
- Dashboard.
- phpMyAdmin.

#### PHP Configuration Editor

PyTabs provides an integrated editor for `php.ini`.

The editor allows you to:

1. Open the PHP configuration file.
2. Modify configuration directives.
3. Save changes directly.
4. Restart PHP when necessary to apply the changes.

**Note:** Some PHP configuration changes require restarting the PHP server before they take effect.

### MariaDB

The MariaDB tab provides a dedicated interface for database server management.

It is designed to centralize access to:

- Database server information.
- MariaDB configuration.
- Database-related resources.
- Server logs.
- Service management.

The exact availability of individual controls depends on the configured MariaDB environment.

### Log

The Log tab provides a centralized view of application and server logs.

It brings together relevant output from:

- PyTabs application.
- PHP server.
- MariaDB server.

This makes it easier to inspect errors and troubleshoot development environment issues without switching between multiple terminal sessions.

### Settings

The Settings tab provides a dedicated location for application-level configuration and future customization.

---

## Project Structure

The project follows a modular Python package structure.

```text
tampp/
├── tampp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   │
│   ├── models/
│   │
│   ├── tabs/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── php.py
│   │   ├── mariadb.py
│   │   └── settings.py
│   │
│   └── ...
│
├── tests/
│
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

The exact tree may evolve as new components and services are introduced.

### Main Components

| Component | Responsibility |
|---|---|
| `app.py` | Main Textual application. |
| `__main__.py` | Python module entry point. |
| `models/` | Application data models. |
| `tabs/` | Individual application tabs. |
| `tests/` | Automated tests. |
| `pyproject.toml` | Project metadata and dependencies. |

---

## Requirements

- Python 3.8 or newer (as declared in the project metadata).
- PHP installed and accessible through the system environment.
- MariaDB installed for database management.
- pip.
- A supported terminal emulator.

PHP and MariaDB are external services and must be installed separately.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/talalalmrka/tampp.git

cd tampp
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

**Linux / macOS / Termux**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip

python -m pip install textual

python -m pip install -e .
```

### 4. Run PyTabs

```bash
python -m tampp
```

---

## Usage

After installation, launch the application:

```bash
python -m tampp
```

Use the keyboard to navigate between tabs and interact with the available controls.

The application provides a unified interface for accessing PHP and MariaDB management features.

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Q` | Quit the application. |
| `←` | Navigate to the previous tab. |
| `→` | Navigate to the next tab. |

Additional shortcuts may be available depending on the active tab and widget.

---

## PHP Management

PyTabs is designed to work with an existing PHP installation.

The application provides access to PHP server settings and related filesystem resources.

### Default Server Settings

```text
Host: 0.0.0.0
Port: 8000
```

The document root can be configured to point to your PHP projects directory.

### Configuration File

The PHP configuration editor provides direct access to:

```text
php.ini
```

Changes can be saved from inside the application.

Remember that PHP may need to be restarted after editing configuration directives.

---

## MariaDB Management

MariaDB is managed as a separate service from PHP.

PyTabs provides a dedicated interface for accessing database server management functionality.

The application is intended to support different MariaDB installation environments rather than relying exclusively on a single installation method.

---

## Configuration

PyTabs is designed to work with different development environments.

PHP and MariaDB executable locations, configuration paths, and server directories depend on the local installation.

Make sure the required executables are accessible and that the application has sufficient permissions to access the relevant configuration files and directories.

---

## Development

Contributions and improvements are welcome.

### 1. Clone the Repository

```bash
git clone https://github.com/talalalmrka/tampp.git

cd tampp
```

### 2. Create a Development Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install the Project

```bash
python -m pip install --upgrade pip

python -m pip install textual

python -m pip install -e .
```

### 4. Run the Application

```bash
python -m tampp
```

### 5. Run Tests

```bash
python -m pytest
```

### Development Recommendations

- Keep application components modular.
- Use separate modules for individual tabs.
- Keep server management logic separate from UI components.
- Use reusable widgets for shared interface elements.
- Follow Python type-hinting conventions.
- Add tests when introducing new functionality.

---

## Architecture

PyTabs uses a modular architecture based on Textual.

The application is organized into separate responsibilities:

```text
Application
    |
    +-- Log Tab
    |
    +-- Home Tab
    |      |
    |      +-- PHP Status
    |      |
    |      +-- MariaDB Status
    |      |
    |      +-- Service Controls
    |
    +-- PHP Tab
    |      |
    |      +-- Server Configuration
    |      +-- PHP Information
    |      +-- Configuration Editor
    |      +-- Filesystem Resources
    |
    +-- MariaDB Tab
    |
    +-- Settings Tab
```

This structure makes it easier to add new services, widgets, and management features without unnecessarily coupling them to the main application.

---

## Supported Platforms

PyTabs is intended to support multiple environments.

| Platform | Target |
|---|---|
| macOS | Supported development target |
| Linux | Supported development target |
| Windows | Supported development target |
| Termux | Supported development target |
| Debian (proot) | Supported development target |

Platform-specific executable paths and service commands may require environment-specific configuration.

---

## Dependencies

### Runtime

- [Python](https://www.python.org/) — Programming language.
- [Textual](https://textual.textualize.io/) — Terminal User Interface framework.

### External Services

- [PHP](https://www.php.net/) — PHP runtime and development server.
- [MariaDB](https://mariadb.org/) — Relational database server.

### Development

- [pytest](https://docs.pytest.org/) — Testing framework.
- [Hatchling](https://hatch.pypa.io/latest/) — Python build backend.

---

## Contributing

Contributions are welcome!

If you would like to improve PyTabs, fix bugs, or introduce new features:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the available tests.
5. Submit a Pull Request.

Example:

```bash
git checkout -b feature/my-feature

git add .

git commit -m "Add my feature"

git push origin feature/my-feature
```

Please keep contributions consistent with the project's modular architecture and coding conventions.

---

## License

PyTabs is released under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## Author

**talalalmrka**

GitHub: [@talalalmrka](https://github.com/talalalmrka)

Repository: [github.com/talalalmrka/tampp](https://github.com/talalalmrka/tampp)

---

<p align="center">
  Built with Python and Textual.
</p>
