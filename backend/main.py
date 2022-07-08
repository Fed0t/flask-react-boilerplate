from bootstrap import init_app

app = init_app()

def run_app():
    app.run(
        host     = app.config['HOST'],
        debug    = app.config['DEBUG'],
        threaded = True,
        port     = app.config['PORT']
    )

########## Run ##############
if __name__ == '__main__':
    run_app()
    
