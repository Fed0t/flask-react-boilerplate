from commands.blockchain import blockchain

def init_commands(app):
    app.cli.add_command(blockchain)
