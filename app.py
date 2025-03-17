from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app=Flask(__name__)

import controllers.config 
import controllers.routes
import models.models
