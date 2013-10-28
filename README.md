# Flask Webapp

Flask Webapp 是一個提供 Mobile backend components 的平台，目前提供的服務如下

* in-app-purchase

## Requirements

* Python 3.3.2
* Flask 0.10

## Getting Started

確認您有 Python 的正確版本

    #install python 3.3
    sudo apt-get install python3.3
    #check python version
    python --version

確認您有 Flask 的正確版本

    #install Flask latest version (0.10)
    pip install Flask

安裝 Flask Webapp

    #install Flask Webapp
    git clone : git@rtd.softstar.com.tw:wes/flask_webapp.git
    cd flask_webapp
    python setup.py install

Create new webapp project

    flask_webapp-quickstart project_name
    ...
    Welcome to the Webapp 0.1 quickstart utility.
    Selected root path: project_name
    Open In-App Purchases (Y/N).
    > Open In-App Purchases [N]: y
    Open push notification (Y/N).
    > Open push notification [N]: y

## IN_APP_PURCHASE

提供 iOS in-app purchase receipt verification endpoints

| endpoints             | method    | description |
| --------              | --------  | --------    |
| /iap/receipts/verify  | post      | 傳送 data : receipt_data = 'Base64-encoded 的 ios store receipt-data' |

