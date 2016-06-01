#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import logging
import pprint
import yaml
import operator
import json

# logging.basicConfig(level=logging.DEBUG)


class Hero:
    """Class for single heroes"""
    def __str__(self):
        return self.name

    def __init__(self, dict=None):
        self.name = None
        self.role = None
        self.weak_against = []
        if dict:
            self.loadFromDict(dict)

    def loadFromDict(self, dict):
        self.name = dict['name']
        self.role = dict['role']
        self.weak_against = dict['weak_against']

    def isWeakness(self, opponent):
        """Check if the given opponent hero is a weaknes for this hero"""
        if opponent.name in self.weak_against:
            return True
        return False

    def isNemesis(self, opponent):
        """Check if the this hero is a weaknes for a given opponent hero"""
        if self.name in opponent.weak_against:
            return True
        return False


class HeroesResolver:
    """This is the hero resolver which calculates hero points"""
    def __init__(self):
        logging.debug("__init__ called")
        self.heroes = []
        self.enemies = []
        self.result = {}

        self.loadHeroes()

    def loadHeroes(self):
        """Loading heroes from YAML file to memory"""
        logging.debug("loadHeroes called")
        with open("heroes.yml", 'r') as stream:
            try:
                for heroData in yaml.load(stream)['heroes']:
                    self.heroes.append(Hero(heroData))

                logging.debug("Loaded %s heroes" % (len(self.heroes)))
            except yaml.YAMLError as e:
                logging.error("Error loading heroes: %s" % (e))

    def getHeroes(self):
        """Get all heroes as JSON"""
        logging.debug("getHeroes called")
        ret = []
        for hero in self.heroes:
            ret.append([hero.name])
        return json.dumps(sorted(ret))

    def addEnemies(self, enemies=[]):
        """Add one or more enemies to be taken into the calculation"""
        logging.debug("addEnemies called")

        def findHero(name):
            for hero in self.heroes:
                if hero.name == unicode(name, encoding='utf-8'):
                    return hero

        if isinstance(enemies, list):
            for enemie in enemies:
                hero = findHero(enemie)
                if hero:
                    logging.debug("Found enemie: %s" % (hero))
                    self.enemies.append(findHero(enemie))
        else:
            self.enemies.append(findHero(enemie))
        logging.debug("Enemy team has now %s heroes" % (len(self.enemies)))

    def calculate(self):
        """Calculate hero points by taking enemies into consideration.
           Returning JSON."""
        logging.debug("calculate called")

        # initialize scores
        for hero in self.heroes:
            self.result[hero.name] = 0

        # calculate score based on enemy weaknesses
        for friendHero in self.heroes:
            for enemyHero in self.enemies:
                # take waskness into consideration
                if friendHero.isWeakness(enemyHero):
                    self.result[friendHero.name] += 1

                # take strangths into consideration
                if friendHero.isNemesis(enemyHero):
                    self.result[friendHero.name] -= 1

        res = json.dumps(sorted(self.result.items(),
                                key=operator.itemgetter(1)))
        logging.debug("Resolver result: %s" % (res))
        return res

    def cleanEnemies(self):
        """Wipe enemies"""
        logging.debug("cleanEnemies called")
        self.enemies = []

    def oneShot(self, enemies):
        """Combine all steps into one method"""
        logging.debug("oneShot called")
        self.addEnemies(enemies)
        res = self.calculate()
        self.cleanEnemies()
        return res


if __name__ == "__main__":
    resolver = HeroesResolver()
    print resolver.getHeroes()
    print resolver.oneShot(["D.VA",
                            "Soldier: 76",
                            "Genji",
                            "Widowmaker",
                            "Mercy",
                            "Torbjörn"])
