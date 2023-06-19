# WoW-Helper
WoW-Helper is a full-use Discord bot intended to help facilitate and integrate useful World of Warcraft features and
tools into Discord.

[comment]: <> (Screenshots and small demo to be added.)

## Table of Contents
- [ **Install** ](#install)
  -  [ **Local Setup** ](#install-local)
  - [ **Database Setup** ](#install-db)
  - [ **Configuration** ](#config)
- [ **Usage** ](#usage)

<a name="install"></a>
## Install
Currently, the bot is in early stages and is unable to be invited via link.
<a name="install-local"></a>
### Local Setup
1. Download from Git.
    ```shell
    git clone https://github.com/BrionGahl/wow-helper.git
    ```
2. Create a Python Virtual environment and activate the environment.
    ```shell
    python -m venv <name>
   
   # if on Windows
   <name>\Scripts\activate.bat
   
   # if on Unix/MacOS
   source <name>/bin/activate
    ```
3. Install dependencies via pip.
    ```shell
    pip install -r requirements.txt    
    ```
4. Create a `.env` file and populate it based on the variables seen within the `example.env` file.
5. Launch the bot via 
    ```shell
    python -m wow_helper`
    ```
<a name="install-db"></a>
### Database Setup
Currently, the bot supports PostgreSQL databases. So long as a valid PostgreSQL database is connected tables will be 
created automatically. Further support will be added in the future expanding upon this and added different acceptable
dialects.
   
<a name="config"></a>
### Configuration
W.I.P.

<a name="usage"></a>
## Usage

