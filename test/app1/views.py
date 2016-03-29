# 3C车间设计

from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *
import json, time, random
from itertools import chain
from django.core import serializers
from Agv import AgvCar
import sys, os
import threading
import datetime

















