#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from  heroes import *
import logging

from flask import Flask

try:
    from flask.ext.compress import Compress
except ImportError:
    log.error("[System] Please install the flask extension: Flask-Compress")
    sys.exit(2)

# setup flask app
app = Flask(__name__)

# logging to file
myPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
logPath = os.path.join(myPath, 'log/pyoverwatch.log')
logging.basicConfig(
    filename=logPath,
    format='%(asctime)s %(levelname)-7s %(message)s',
    datefmt='%Y-%d-%m %H:%M:%S',
    level=logging.INFO)

log = logging.getLogger(__name__)
log.info("[System] PyOverwatch system is starting up")

# compress plugin
Compress(app)

try:
    os.environ['PYOVERWATCH_CFG']
    log.info("[System] Loading config from: %s" % os.environ['PYOVERWATCH_CFG'])
except KeyError:
    log.warning("[System] Loading config from dist/pyoverwatch.cfg.example "
                "becuase PYOVERWATCH_CFG environment variable is not set.")
    os.environ['PYOVERWATCH_CFG'] = "../dist/pyoverwatch.cfg.example"


@app.route("/GetHeroes")
def getHeroes():
    resolver = HeroesResolver()
    return resolver.getHeroes()


@app.route("/CalculateHeroes", methods=['POST'])
def calculateHeroes(heroes):
    resolver = HeroesResolver()
    return resolver.oneShot(heroes)


if __name__ == "__main__":
    app.run()
