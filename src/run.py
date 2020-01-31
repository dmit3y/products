import asyncio
import click
import logging
import unittest
from products.server import run
from products.load_csv import load_csv
from products.db import init_db

logging.basicConfig(level=logging.INFO)

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    """Initialize database with needed collections and indexes"""
    asyncio.run(init_db())

@cli.command()
def runserver():
    """Run web server"""
    run()

@cli.command()
def ttt(*args, **kwargs):
    unittest.main()


@cli.command()
@click.argument("filename")
def loadcsv(filename):
    """Load CSV in db"""
    asyncio.run(load_csv(filename))

if __name__ == "__main__":
    cli()
