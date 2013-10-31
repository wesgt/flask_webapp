from webapp import create_app


def main():
    app = create_app('config_production.cfg')
    from webapp import extensions

    app.run(host=app.config.get('SERVER_IP'),
            port=app.config.get('SERVER_PORT'),
            debug=app.config.get('DEBUG'))

if __name__ == '__main__':
    main()
